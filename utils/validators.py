import re
from urllib.parse import urlparse
from typing import Tuple, Optional

class URLValidator:
    
    
    @staticmethod
    def validate_and_normalize_url(url: str) -> Tuple[bool, Optional[str], Optional[str]]:

        
        if not url or not isinstance(url, str):
            return False, None, "URL is required"
        
        # Remove whitespace
        url = url.strip()
        
        if not url:
            return False, None, "URL cannot be empty"
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Basic URL pattern validation
        url_pattern = re.compile(
            r'^https?://'  # Protocol
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # Domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # Optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if not url_pattern.match(url):
            return False, None, "Invalid URL format"
        
        # Parse URL to validate components
        try:
            parsed = urlparse(url)
            
            if not parsed.netloc:
                return False, None, "Invalid domain"
            
            # Check for valid domain format
            domain_pattern = re.compile(
                r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
            )
            
            if not domain_pattern.match(parsed.netloc.split(':')[0]):
                return False, None, "Invalid domain format"
            
            return True, url, None
            
        except Exception as e:
            return False, None, f"URL parsing error: {str(e)}"
    
    @staticmethod
    def extract_domain(url: str) -> Optional[str]:
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc.split(':')[0]  # Remove port if present
        except (ValueError, AttributeError, IndexError):
            return None
    
    @staticmethod
    def is_valid_domain(domain: str) -> bool:
        
        if not domain:
            return False
        
        domain_pattern = re.compile(
            r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
        )
        
        return bool(domain_pattern.match(domain))
    
    @staticmethod
    def sanitize_url_for_display(url: str, max_length: int = 50) -> str:
        """Sanitize URL for safe display in messages"""
        if len(url) <= max_length:
            return url
        
        # Truncate long URLs
        return url[:max_length-3] + "..."
