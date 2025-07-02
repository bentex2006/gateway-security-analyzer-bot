"""
Payment system detection module
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any
import re
import logging

logger = logging.getLogger(__name__)

class PaymentAnalyzer:
    """Analyzes websites for payment systems and gateways"""
    
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': config.USER_AGENT
        })
    
    def detect_payment_systems(self, url: str) -> Dict[str, Any]:
        """Detect payment systems and gateways"""
        try:
            response = self.session.get(
                url,
                timeout=self.config.REQUEST_TIMEOUT,
                allow_redirects=True
            )
            
            soup = BeautifulSoup(response.text, 'html.parser')
            html_content = response.text
            
            detected_payments = {}
            payment_evidence = []
            
            # Check for payment gateways using improved detection
            import re
            detected_gateways = set()
            
            # Check scripts first (most reliable)
            scripts = soup.find_all('script', src=True)
            for script in scripts:
                src = script.get('src', '') or ''
                for gateway, pattern in self.config.PAYMENT_GATEWAY_PATTERNS.items():
                    if re.search(pattern, src, re.IGNORECASE):
                        detected_gateways.add(gateway)
                        payment_evidence.append(f"Script: {gateway}")
                        break
            
            # Check inline scripts for payment initialization
            inline_scripts = soup.find_all('script', src=False)
            for script in inline_scripts:
                script_content = script.get_text() if script.get_text() else ''
                for gateway, pattern in self.config.PAYMENT_GATEWAY_PATTERNS.items():
                    # More specific matching for inline scripts
                    if re.search(pattern, script_content, re.IGNORECASE):
                        # Avoid CSS/FontAwesome false positives 
                        if not any(term in script_content.lower() for term in ['font-awesome', 'fas fa-', 'far fa-', 'fab fa-']):
                            detected_gateways.add(gateway)
                            payment_evidence.append(f"Inline script: {gateway}")
                            break
            
            # Check forms and form actions (reliable for payment processors)
            forms = soup.find_all('form', action=True)
            for form in forms:
                action = form.get('action', '') or ''
                for gateway, pattern in self.config.PAYMENT_GATEWAY_PATTERNS.items():
                    if re.search(pattern, action, re.IGNORECASE):
                        detected_gateways.add(gateway)
                        payment_evidence.append(f"Form action: {gateway}")
                        break
            
            # Create payment systems dict
            for gateway in detected_gateways:
                detected_payments[gateway.lower()] = {
                    'detected': True,
                    'evidence': [f"Gateway: {gateway}"]
                }
            
            # Look for general e-commerce indicators
            ecommerce_indicators = self._detect_ecommerce_features(soup, html_content)
            
            # Check for checkout processes
            checkout_detected = self._detect_checkout_process(soup, html_content)
            
            return {
                'payment_systems': detected_payments,
                'total_systems_detected': len(detected_payments),
                'ecommerce_features': ecommerce_indicators,
                'checkout_process': checkout_detected,
                'evidence': list(set(payment_evidence))
            }
            
        except Exception as e:
            logger.error(f"Payment system detection failed: {e}")
            raise Exception(f"Payment analysis failed: {str(e)}")
    
    def _detect_ecommerce_features(self, soup: BeautifulSoup, html_content: str) -> Dict[str, Any]:
        """Detect general e-commerce features"""
        ecommerce_features = {
            'shopping_cart': False,
            'product_pages': False,
            'price_display': False,
            'add_to_cart': False,
            'checkout_button': False
        }
        
        evidence = []
        
        # Shopping cart indicators
        cart_indicators = ['cart', 'basket', 'shopping-cart', 'add-to-cart', 'shopping-basket']
        for indicator in cart_indicators:
            if indicator in html_content:
                ecommerce_features['shopping_cart'] = True
                evidence.append(f"Cart indicator: {indicator}")
                break
        
        # Product page indicators
        product_indicators = ['product', 'item', 'sku', 'price', 'buy-now']
        for indicator in product_indicators:
            if indicator in html_content:
                ecommerce_features['product_pages'] = True
                evidence.append(f"Product indicator: {indicator}")
                break
        
        # Price display patterns
        price_patterns = [
            r'\$\d+\.?\d*',  # $100 or $100.00
            r'€\d+\.?\d*',   # €100 or €100.00
            r'£\d+\.?\d*',   # £100 or £100.00
            r'\d+\.?\d*\s*USD', # 100 USD
            r'price["\s]*[:=]["\s]*\d+' # price: 100
        ]
        
        for pattern in price_patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                ecommerce_features['price_display'] = True
                evidence.append(f"Price pattern found")
                break
        
        # Add to cart buttons
        buttons = soup.find_all(['button', 'input', 'a'])
        for button in buttons:
            button_text = button.get_text().lower()
            button_value = button.get('value', '').lower()
            button_class = ' '.join(button.get('class', [])).lower()
            
            add_to_cart_terms = ['add to cart', 'add-to-cart', 'addtocart', 'buy now', 'purchase']
            for term in add_to_cart_terms:
                if term in button_text or term in button_value or term in button_class:
                    ecommerce_features['add_to_cart'] = True
                    evidence.append(f"Add to cart button found")
                    break
        
        # Checkout buttons
        checkout_terms = ['checkout', 'proceed to checkout', 'go to checkout', 'checkout-btn']
        for button in buttons:
            button_text = button.get_text().lower()
            button_class = ' '.join(button.get('class', [])).lower()
            
            for term in checkout_terms:
                if term in button_text or term in button_class:
                    ecommerce_features['checkout_button'] = True
                    evidence.append(f"Checkout button found")
                    break
        
        return {
            'features': ecommerce_features,
            'evidence': evidence,
            'ecommerce_score': sum(ecommerce_features.values()) / len(ecommerce_features) * 100
        }
    
    def _detect_checkout_process(self, soup: BeautifulSoup, html_content: str) -> Dict[str, Any]:
        """Detect checkout process and payment forms"""
        checkout_indicators = {
            'payment_form': False,
            'billing_address': False,
            'shipping_address': False,
            'payment_method_selection': False,
            'order_summary': False
        }
        
        evidence = []
        
        # Look for payment-related forms
        forms = soup.find_all('form')
        for form in forms:
            form_html = str(form).lower()
            
            # Payment form indicators
            payment_form_terms = ['payment', 'billing', 'credit card', 'card number', 'cvv', 'expiry']
            for term in payment_form_terms:
                if term in form_html:
                    checkout_indicators['payment_form'] = True
                    evidence.append(f"Payment form detected")
                    break
        
        # Look for billing/shipping address fields
        address_fields = ['billing', 'shipping', 'address', 'zip', 'postal', 'country']
        inputs = soup.find_all(['input', 'select', 'textarea'])
        
        for input_field in inputs:
            field_name = input_field.get('name', '').lower()
            field_id = input_field.get('id', '').lower()
            field_class = ' '.join(input_field.get('class', [])).lower()
            
            for address_term in address_fields:
                if address_term in field_name or address_term in field_id or address_term in field_class:
                    if 'billing' in field_name or 'billing' in field_id or 'billing' in field_class:
                        checkout_indicators['billing_address'] = True
                        evidence.append("Billing address fields found")
                    elif 'shipping' in field_name or 'shipping' in field_id or 'shipping' in field_class:
                        checkout_indicators['shipping_address'] = True
                        evidence.append("Shipping address fields found")
                    break
        
        # Look for payment method selection
        payment_methods = ['visa', 'mastercard', 'amex', 'paypal', 'apple pay', 'google pay']
        for method in payment_methods:
            if method in html_content:
                checkout_indicators['payment_method_selection'] = True
                evidence.append(f"Payment method found: {method}")
                break
        
        # Look for order summary
        order_terms = ['order summary', 'cart total', 'subtotal', 'total amount', 'order total']
        for term in order_terms:
            if term in html_content:
                checkout_indicators['order_summary'] = True
                evidence.append("Order summary detected")
                break
        
        return {
            'checkout_features': checkout_indicators,
            'evidence': list(set(evidence)),
            'checkout_score': sum(checkout_indicators.values()) / len(checkout_indicators) * 100
        }
