import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class WebsiteAnalyzer:
    
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': config.USER_AGENT
        })
    
    def analyze_website(self, url: str) -> Dict[str, Any]:
        """Main analysis function that performs all checks"""
        try:
            # Make initial request
            response = self.session.get(
                url, 
                timeout=self.config.REQUEST_TIMEOUT,
                allow_redirects=True,
                verify=True
            )
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = {
                'cloudflare': self._detect_cloudflare(response),
                'captcha': self._detect_captcha(soup, response.text),
                'graphql': self._detect_graphql(url),
                'wordpress': self._detect_wordpress(soup, response.text),
                'woocommerce': self._detect_woocommerce(soup, response.text),
                'cms': self._detect_cms(soup, response.text),
                'response_code': response.status_code,
                'final_url': response.url
            }
            
            return results
            
        except requests.exceptions.Timeout:
            raise Exception("Request timeout - website took too long to respond")
        except requests.exceptions.ConnectionError:
            raise Exception("Connection error - unable to reach website")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Analysis failed: {str(e)}")
    
    def _detect_cloudflare(self, response: requests.Response) -> Dict[str, Any]:
        """Detect Cloudflare protection"""
        cloudflare_detected = False
        evidence = []
        
        # Check Cloudflare-specific headers (excluding generic 'server')
        cloudflare_specific_headers = ['cf-ray', 'cf-cache-status', 'cf-request-id']
        for header in cloudflare_specific_headers:
            if header.lower() in [h.lower() for h in response.headers.keys()]:
                cloudflare_detected = True
                evidence.append(f"Header: {header}")
        
        # Check server header specifically for Cloudflare
        server_header = response.headers.get('Server', '').lower()
        if 'cloudflare' in server_header:
            cloudflare_detected = True
            evidence.append(f"Server: {server_header}")
        
        # Check for Cloudflare-specific cookies
        for cookie in response.cookies:
            if cookie.name.startswith('__cf') or 'cloudflare' in cookie.name.lower():
                cloudflare_detected = True
                evidence.append(f"Cookie: {cookie.name}")
        
        # Check for Cloudflare challenge pages in content
        if hasattr(response, 'text'):
            content_lower = response.text.lower()
            if 'cloudflare' in content_lower and ('challenge' in content_lower or 'checking your browser' in content_lower):
                cloudflare_detected = True
                evidence.append("Challenge page detected")
        
        return {
            'detected': cloudflare_detected,
            'evidence': evidence
        }
    
    def _detect_captcha(self, soup: BeautifulSoup, html_content: str) -> Dict[str, Any]:
        """Detect CAPTCHA systems"""
        detected_captchas = set()
        evidence = []
        
        # Define CAPTCHA system priorities to avoid conflicts
        captcha_systems = {
            'recaptcha': ['recaptcha', 'g-recaptcha'],
            'hcaptcha': ['hcaptcha', 'h-captcha'],
            'turnstile': ['cf-turnstile', 'turnstile'],
            'geetest': ['geetest'],
            'arkose': ['arkose', 'arkose-labs', 'funcaptcha'],
            'datadome': ['datadome'],
            'perimeterx': ['perimeterx'],
            'captcha': ['captcha-id']  # Generic captcha as last resort
        }
        
        # Check script sources first (most reliable)
        scripts = soup.find_all('script', src=True)
        for script in scripts:
            src = script.get('src', '').lower()
            for system, indicators in captcha_systems.items():
                for indicator in indicators:
                    if indicator in src:
                        detected_captchas.add(system.title())
                        evidence.append(f"Script: {indicator} in {src[:50]}...")
                        break
        
        # Check for iframe sources (common for CAPTCHAs)
        iframes = soup.find_all('iframe', src=True)
        for iframe in iframes:
            src = iframe.get('src', '').lower()
            for system, indicators in captcha_systems.items():
                for indicator in indicators:
                    if indicator in src:
                        detected_captchas.add(system.title())
                        evidence.append(f"Iframe: {indicator}")
                        break
        
        # Check for div classes and IDs
        divs = soup.find_all('div', {'class': True}) + soup.find_all('div', {'id': True})
        for div in divs:
            classes = ' '.join(div.get('class', [])).lower() if div.get('class') else ''
            div_id = div.get('id', '').lower() if div.get('id') else ''
            for system, indicators in captcha_systems.items():
                for indicator in indicators:
                    if indicator in classes or indicator in div_id:
                        detected_captchas.add(system.title())
                        evidence.append(f"Element: {indicator}")
                        break
        
        # Only check content as last resort and be more specific
        if not detected_captchas:
            content_lower = html_content.lower()
            for system, indicators in captcha_systems.items():
                for indicator in indicators:
                    # Be more strict about content matches to avoid false positives
                    if f'"{indicator}"' in content_lower or f"'{indicator}'" in content_lower or f'/{indicator}/' in content_lower:
                        detected_captchas.add(system.title())
                        evidence.append(f"Content: {indicator}")
                        break
        
        return {
            'detected': len(detected_captchas) > 0,
            'types': list(detected_captchas),
            'evidence': list(set(evidence))
        }
    
    def _detect_graphql(self, base_url: str) -> Dict[str, Any]:
        """Detect GraphQL endpoints"""
        graphql_endpoints = []
        
        for path in self.config.GRAPHQL_PATHS:
            try:
                test_url = base_url.rstrip('/') + path
                
                # Try POST request with GraphQL introspection query first (more reliable)
                introspection_query = {
                    "query": "{ __schema { types { name } } }"
                }
                
                response = self.session.post(
                    test_url,
                    json=introspection_query,
                    timeout=self.config.REQUEST_TIMEOUT
                )
                
                if response.status_code == 200:
                    try:
                        json_response = response.json()
                        # Look for actual GraphQL response structure
                        if ('data' in json_response and '__schema' in str(json_response)) or \
                           ('errors' in json_response and any('graphql' in str(error).lower() for error in json_response.get('errors', []))):
                            graphql_endpoints.append(test_url)
                            continue
                    except:
                        pass
                
                # Try GET request for GraphQL endpoint detection
                response = self.session.get(
                    test_url,
                    timeout=self.config.REQUEST_TIMEOUT
                )
                
                # Only consider it GraphQL if we get specific GraphQL responses
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '').lower()
                    content = response.text.lower()
                    
                    # Look for specific GraphQL indicators, not just the word "query"
                    graphql_indicators = [
                        'graphql playground',
                        'graphql endpoint',
                        '"graphql"',
                        'query introspection',
                        '__schema',
                        'graphql-ws',
                        'application/graphql'
                    ]
                    
                    if any(indicator in content for indicator in graphql_indicators) or \
                       'application/graphql' in content_type:
                        graphql_endpoints.append(test_url)
                        
            except:
                continue
        
        return {
            'detected': len(graphql_endpoints) > 0,
            'endpoints': graphql_endpoints
        }
    
    def _detect_wordpress(self, soup: BeautifulSoup, html_content: str) -> Dict[str, Any]:
        """Detect WordPress"""
        wordpress_evidence = []
        
        # Check meta generator (most reliable)
        meta_generator = soup.find('meta', {'name': 'generator'})
        if meta_generator and 'wordpress' in meta_generator.get('content', '').lower():
            wordpress_evidence.append("Meta generator: WordPress")
        
        # Check for wp-json API endpoint (very reliable)
        links = soup.find_all('link', href=True)
        for link in links:
            href = link.get('href', '')
            if 'wp-json' in href or 'wp/v2' in href:
                wordpress_evidence.append("WP-JSON API detected")
                break
        
        # Check for WordPress-specific CSS/JS files (reliable)
        scripts_and_links = soup.find_all(['script', 'link'], src=True) + soup.find_all(['script', 'link'], href=True)
        for element in scripts_and_links:
            src = element.get('src', '') or element.get('href', '')
            if '/wp-content/' in src or '/wp-includes/' in src:
                wordpress_evidence.append("WordPress assets detected")
                break
        
        # Check for very specific WordPress indicators only if we don't have other evidence
        if not wordpress_evidence:
            specific_indicators = ['wp-admin', 'wp-login.php', 'xmlrpc.php']
            for indicator in specific_indicators:
                if f'/{indicator}' in html_content or f'"{indicator}"' in html_content:
                    wordpress_evidence.append(f"WordPress indicator: {indicator}")
                    break
        
        return {
            'detected': len(wordpress_evidence) > 0,
            'evidence': wordpress_evidence
        }
    
    def _detect_woocommerce(self, soup: BeautifulSoup, html_content: str) -> Dict[str, Any]:
        """Detect WooCommerce"""
        woocommerce_evidence = []
        
        # Check for WooCommerce scripts (most reliable)
        scripts = soup.find_all('script', src=True)
        for script in scripts:
            src = script.get('src', '') or ''
            if 'woocommerce' in src.lower() or '/wc-' in src.lower():
                woocommerce_evidence.append("WooCommerce scripts detected")
                break
        
        # Check for specific WooCommerce CSS classes (reliable)
        woo_classes = ['woocommerce-page', 'woocommerce-cart', 'woocommerce-checkout', 'wc-checkout']
        for element in soup.find_all(class_=True):
            classes = element.get('class', [])
            if isinstance(classes, list):
                classes_str = ' '.join(classes).lower()
                for woo_class in woo_classes:
                    if woo_class in classes_str:
                        woocommerce_evidence.append("WooCommerce CSS classes detected")
                        break
                if woocommerce_evidence:
                    break
        
        # Check for WooCommerce meta or very specific content only if no other evidence
        if not woocommerce_evidence:
            if 'woocommerce' in html_content.lower() and ('add-to-cart' in html_content.lower() or 'shop-' in html_content.lower()):
                woocommerce_evidence.append("WooCommerce shop detected")
        
        return {
            'detected': len(woocommerce_evidence) > 0,
            'evidence': woocommerce_evidence
        }
    
    def _detect_cms(self, soup: BeautifulSoup, html_content: str) -> Dict[str, str]:
        """Detect Content Management System"""
        # Check for various CMS indicators
        cms_indicators = {
            'wordpress': ['wp-content', 'wordpress'],
            'drupal': ['drupal', '/sites/default/', 'drupal.js'],
            'joomla': ['joomla', '/media/jui/', 'joomla.js'],
            'magento': ['magento', 'mage/', 'varien'],
            'shopify': ['shopify', 'shopify-analytics', 'shopifycdn'],
            'squarespace': ['squarespace', 'squarespace.com'],
            'wix': ['wix.com', 'wixstatic'],
            'webflow': ['webflow', 'webflow.com'],
            'gatsby': ['gatsby', '__gatsby'],
            'next.js': ['_next/', '__next'],
            'react': ['react', 'react-dom'],
            'vue': ['vue.js', 'vue.min.js'],
            'angular': ['angular', 'ng-'],
            'bootstrap': ['bootstrap', 'bs-']
        }
        
        detected_cms = []
        
        for cms, indicators in cms_indicators.items():
            for indicator in indicators:
                if indicator.lower() in html_content.lower():
                    detected_cms.append(cms.title())
                    break
        
        # Check meta generator
        meta_generator = soup.find('meta', {'name': 'generator'})
        if meta_generator:
            generator = meta_generator.get('content', '').lower()
            for cms in cms_indicators.keys():
                if cms in generator:
                    detected_cms.append(cms.title())
        
        return {
            'detected': ', '.join(set(detected_cms)) if detected_cms else 'Unknown',
            'types': list(set(detected_cms))
        }
