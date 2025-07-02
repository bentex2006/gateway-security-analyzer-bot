import requests
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class SecurityAnalyzer:
    
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': config.USER_AGENT
        })
    
    def analyze_security_headers(self, url: str) -> Dict[str, Any]:
        """Analyze security headers"""
        try:
            response = self.session.get(
                url,
                timeout=self.config.REQUEST_TIMEOUT,
                allow_redirects=True
            )
            
            headers_analysis = {}
            missing_headers = []
            present_headers = []
            
            for header in self.config.SECURITY_HEADERS:
                if header in response.headers:
                    present_headers.append({
                        'name': header,
                        'value': response.headers[header]
                    })
                    headers_analysis[header] = {
                        'present': True,
                        'value': response.headers[header]
                    }
                else:
                    missing_headers.append(header)
                    headers_analysis[header] = {
                        'present': False,
                        'value': None
                    }
            
            # Calculate security score
            security_score = (len(present_headers) / len(self.config.SECURITY_HEADERS)) * 100
            
            return {
                'score': round(security_score, 1),
                'present_headers': present_headers,
                'missing_headers': missing_headers,
                'headers_analysis': headers_analysis,
                'total_headers_checked': len(self.config.SECURITY_HEADERS)
            }
            
        except Exception as e:
            logger.error(f"Security analysis failed: {e}")
            raise Exception(f"Security analysis failed: {str(e)}")
    
    def check_https_redirect(self, url: str) -> Dict[str, Any]:
        """Check if HTTP redirects to HTTPS"""
        try:
            if url.startswith('https://'):
                http_url = url.replace('https://', 'http://', 1)
            else:
                http_url = url
                
            response = self.session.get(
                http_url,
                timeout=self.config.REQUEST_TIMEOUT,
                allow_redirects=True
            )
            
            redirected_to_https = response.url.startswith('https://')
            
            return {
                'redirects_to_https': redirected_to_https,
                'final_url': response.url,
                'original_url': http_url
            }
            
        except Exception as e:
            logger.error(f"HTTPS redirect check failed: {e}")
            return {
                'redirects_to_https': False,
                'error': str(e)
            }
    
    def analyze_cookies(self, url: str) -> Dict[str, Any]:
        """Analyze cookie security settings"""
        try:
            response = self.session.get(
                url,
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            cookies_analysis = []
            secure_cookies = 0
            httponly_cookies = 0
            samesite_cookies = 0
            
            for cookie in response.cookies:
                cookie_info = {
                    'name': cookie.name,
                    'secure': cookie.secure,
                    'httponly': getattr(cookie, 'httponly', False),
                    'samesite': getattr(cookie, 'samesite', None),
                    'domain': cookie.domain,
                    'path': cookie.path
                }
                
                cookies_analysis.append(cookie_info)
                
                if cookie.secure:
                    secure_cookies += 1
                if getattr(cookie, 'httponly', False):
                    httponly_cookies += 1
                if getattr(cookie, 'samesite', None):
                    samesite_cookies += 1
            
            total_cookies = len(cookies_analysis)
            
            return {
                'total_cookies': total_cookies,
                'secure_cookies': secure_cookies,
                'httponly_cookies': httponly_cookies,
                'samesite_cookies': samesite_cookies,
                'cookies_details': cookies_analysis,
                'security_percentage': {
                    'secure': (secure_cookies / total_cookies * 100) if total_cookies > 0 else 0,
                    'httponly': (httponly_cookies / total_cookies * 100) if total_cookies > 0 else 0,
                    'samesite': (samesite_cookies / total_cookies * 100) if total_cookies > 0 else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Cookie analysis failed: {e}")
            return {
                'total_cookies': 0,
                'error': str(e)
            }
