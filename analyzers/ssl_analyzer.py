import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SSLAnalyzer:
    
    def __init__(self, config):
        self.config = config
    
    def analyze_ssl_certificate(self, url: str) -> dict:
        """Analyze SSL certificate details"""
        try:
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname or parsed_url.netloc
            port = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
            
            if parsed_url.scheme != 'https':
                return {
                    'valid': False,
                    'error': 'Not an HTTPS URL',
                    'issuer': 'N/A',
                    'subject': 'N/A',
                    'expires': 'N/A',
                    'days_until_expiry': 0
                }
            
            # Create SSL context
            context = ssl.create_default_context()
            
            # Get certificate
            with socket.create_connection((hostname, port), timeout=self.config.REQUEST_TIMEOUT) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
            
            # Parse certificate information
            issuer_info = dict(x[0] for x in cert['issuer'])
            subject_info = dict(x[0] for x in cert['subject'])
            
            # Get expiry date
            not_after = cert['notAfter']
            expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
            days_until_expiry = (expiry_date - datetime.now()).days
            
            # Determine certificate validity
            is_valid = days_until_expiry > 0
            
            return {
                'valid': is_valid,
                'issuer': issuer_info.get('organizationName', 'Unknown'),
                'subject': subject_info.get('commonName', hostname),
                'expires': expiry_date.strftime('%Y-%m-%d'),
                'days_until_expiry': days_until_expiry,
                'serial_number': cert.get('serialNumber', 'Unknown'),
                'version': cert.get('version', 'Unknown'),
                'signature_algorithm': cert.get('signatureAlgorithm', 'Unknown'),
                'subject_alt_names': [name[1] for name in cert.get('subjectAltName', [])]
            }
            
        except ssl.SSLError as e:
            logger.error(f"SSL error for {hostname}: {e}")
            return {
                'valid': False,
                'error': f'SSL Error: {str(e)}',
                'issuer': 'N/A',
                'subject': 'N/A',
                'expires': 'N/A',
                'days_until_expiry': 0
            }
        except socket.timeout:
            return {
                'valid': False,
                'error': 'Connection timeout',
                'issuer': 'N/A',
                'subject': 'N/A',
                'expires': 'N/A',
                'days_until_expiry': 0
            }
        except Exception as e:
            logger.error(f"Certificate analysis failed for {hostname}: {e}")
            return {
                'valid': False,
                'error': f'Analysis failed: {str(e)}',
                'issuer': 'N/A',
                'subject': 'N/A',
                'expires': 'N/A',
                'days_until_expiry': 0
            }
    
    def check_ssl_configuration(self, url: str) -> dict:
        """Check SSL configuration and supported protocols"""
        try:
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname or parsed_url.netloc
            port = parsed_url.port or 443
            
            if parsed_url.scheme != 'https':
                return {
                    'supported_protocols': [],
                    'cipher_suite': 'N/A',
                    'error': 'Not an HTTPS URL'
                }
            
            # Check supported SSL/TLS protocols
            supported_protocols = []
            
            protocols_to_test = [
                ('TLSv1.3', ssl.PROTOCOL_TLS),
                ('TLSv1.2', ssl.PROTOCOL_TLS),
                ('TLSv1.1', ssl.PROTOCOL_TLS),
                ('TLSv1', ssl.PROTOCOL_TLS),
            ]
            
            for protocol_name, protocol in protocols_to_test:
                try:
                    context = ssl.SSLContext(protocol)
                    with socket.create_connection((hostname, port), timeout=5) as sock:
                        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                            supported_protocols.append(protocol_name)
                            cipher_info = ssock.cipher()
                            break
                except:
                    continue
            
            return {
                'supported_protocols': supported_protocols,
                'cipher_suite': cipher_info[0] if 'cipher_info' in locals() else 'Unknown',
                'protocol_version': cipher_info[1] if 'cipher_info' in locals() else 'Unknown',
                'key_length': cipher_info[2] if 'cipher_info' in locals() else 0
            }
            
        except Exception as e:
            logger.error(f"SSL configuration check failed: {e}")
            return {
                'supported_protocols': [],
                'cipher_suite': 'Unknown',
                'error': str(e)
            }
