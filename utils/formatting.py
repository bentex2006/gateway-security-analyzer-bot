"""
Message formatting utilities for the Telegram bot
"""

import time
from typing import Dict, Any

class MessageFormatter:
    """Formats analysis results into readable Telegram messages"""
    
    @staticmethod
    def format_main_result(analysis_results: Dict[str, Any], url: str, username: str, start_time: float) -> str:
        """Format the main analysis result message"""
        
        # Calculate processing time
        processing_time = round(time.time() - start_time, 2)
        
        # Extract results
        website_data = analysis_results.get('website', {})
        security_data = analysis_results.get('security', {})
        ssl_data = analysis_results.get('ssl', {})
        payment_data = analysis_results.get('payment', {})
        
        # Format components
        gateway_text = MessageFormatter._format_gateways(payment_data)
        captcha_text = MessageFormatter._format_captcha(website_data.get('captcha', {}))
        cloudflare_text = MessageFormatter._format_cloudflare(website_data.get('cloudflare', {}))
        checkout_text = MessageFormatter._format_checkout(payment_data)
        
        # Security details
        security_captcha = "✅ Detected" if website_data.get('captcha', {}).get('detected') else "❌ Not Found"
        security_cloudflare = "✅ Protected" if website_data.get('cloudflare', {}).get('detected') else "❌ Unprotected"
        graphql_detected = "✅ Available" if website_data.get('graphql', {}).get('detected') else "❌ Not Found"
        
        # SSL details (escape special characters for Telegram)
        ssl_issuer = MessageFormatter._escape_markdown(ssl_data.get('issuer', 'Unknown'))
        ssl_subject = MessageFormatter._escape_markdown(ssl_data.get('subject', 'Unknown'))
        ssl_valid = "✅ Valid" if ssl_data.get('valid') else "❌ Invalid"
        
        # Platform details
        cms_text = website_data.get('cms', {}).get('detected', 'Unknown')
        cards_text = MessageFormatter._format_cards(payment_data)
        
        # Checked by
        checked_by = f"@{username}" if username else "Anonymous"
        
        message = f"""┏━━━━『 𝓖𝓪𝓽𝓮𝔀𝓪𝔂 𝓡𝓮𝓼𝓾𝓵𝓽𝓼 』━━━━

🔍 𝗗𝗼𝗺𝗮𝗶𝗻: {url}
💳 𝗚𝗮𝘁𝗲𝘄𝗮𝘆𝘀: {gateway_text}
🔒 𝗖𝗔𝗣𝗧𝗖𝗛𝗔: {captcha_text}
🔒 𝗖𝗟𝗢𝗨𝗗𝗙𝗟𝗔𝗥𝗘: {cloudflare_text}
🛒 𝗖𝗛𝗘𝗖𝗞𝗢𝗨𝗧: {checkout_text}

🛡️ 𝗦𝗲𝗰𝘂𝗿𝗶𝘁𝘆:
├─ 𝗖𝗮𝗽𝘁𝗰𝗵𝗮: {security_captcha}
├─ 𝗖𝗹𝗼𝘂𝗱𝗳𝗹𝗮𝗿𝗲: {security_cloudflare}
└─ 𝗚𝗿𝗮𝗽𝗵𝗤𝗟: {graphql_detected}

🔐 𝗦𝗦𝗟 𝗗𝗲𝘁𝗮𝗶𝗹𝘀:
├─ 𝗜𝘀𝘀𝘂𝗲𝗿: {ssl_issuer}
├─ 𝗦𝘂𝗯𝗷𝗲𝗰𝘁: {ssl_subject}
└─ 𝗩𝗮𝗹𝗶𝗱: {ssl_valid}

🛍️ 𝗣𝗹𝗮𝘁𝗳𝗼𝗿𝗺:
├─ 𝗖𝗠𝗦: {cms_text}
└─ 𝗖𝗮𝗿𝗱𝘀: {cards_text}

⏱️ 𝗧𝗶𝗺𝗲: {processing_time}s
👤 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗯𝘆: {checked_by}

┗━━━━『 @skittlehideout 』━━━"""
        
        return message
    
    @staticmethod
    def _format_gateways(payment_data: Dict[str, Any]) -> str:
        """Format detected payment gateways"""
        if not payment_data or not payment_data.get('payment_systems'):
            return "❌ None Detected"
        
        gateways = list(payment_data['payment_systems'].keys())
        if not gateways:
            return "❌ None Detected"
        
        # Format gateway names
        formatted_gateways = []
        for gateway in gateways:
            formatted_gateways.append(gateway.title())
        
        return "✅ " + ", ".join(formatted_gateways)
    
    @staticmethod
    def _format_captcha(captcha_data: Dict[str, Any]) -> str:
        """Format CAPTCHA detection results"""
        if not captcha_data or not captcha_data.get('detected'):
            return "❌ Not Protected"
        
        captcha_types = captcha_data.get('types', [])
        if not captcha_types:
            return "✅ Protected"
        
        return "✅ " + ", ".join([t.title() for t in captcha_types])
    
    @staticmethod
    def _format_cloudflare(cloudflare_data: Dict[str, Any]) -> str:
        """Format Cloudflare detection results"""
        if not cloudflare_data or not cloudflare_data.get('detected'):
            return "❌ Not Protected"
        
        return "✅ Protected"
    
    @staticmethod
    def _format_checkout(payment_data: Dict[str, Any]) -> str:
        """Format checkout process detection"""
        if not payment_data:
            return "❌ Not Available"
        
        checkout_data = payment_data.get('checkout_process', {})
        if not checkout_data:
            return "❌ Not Available"
        
        checkout_score = checkout_data.get('checkout_score', 0)
        if checkout_score > 60:
            return "✅ Available"
        elif checkout_score > 30:
            return "⚠️ Partial"
        else:
            return "❌ Not Available"
    
    @staticmethod
    def _format_cards(payment_data: Dict[str, Any]) -> str:
        """Format card detection results"""
        if not payment_data:
            return "❌ None Detected"
        
        # Check if any major card processors are detected
        payment_systems = payment_data.get('payment_systems', {})
        card_systems = []
        
        card_indicators = ['stripe', 'square', 'braintree', 'authorize.net']
        
        for system in card_indicators:
            if system in payment_systems:
                card_systems.append(system.title())
        
        # Also check ecommerce features for general card acceptance
        ecommerce_data = payment_data.get('ecommerce_features', {})
        if ecommerce_data and ecommerce_data.get('ecommerce_score', 0) > 50:
            if not card_systems:
                card_systems.append("Generic")
        
        if card_systems:
            return "✅ " + ", ".join(card_systems)
        else:
            return "❌ None Detected"
    
    @staticmethod
    def format_error_message(error: str) -> str:
        """Format error message"""
        return f"""❌ **Analysis Failed**

🚫 **Error**: {error}

**Common causes:**
• Invalid URL format
• Website is unreachable
• Connection timeout
• SSL/TLS errors

Please check the URL and try again.

Developed by **Skittle** | Credits to **SigmaX**"""
    
    @staticmethod
    def format_permission_denied() -> str:
        """Format permission denied message"""
        return """🔒 **Access Denied**

You don't have permission to use this bot.

Please contact an administrator to get approved.

Developed by **Skittle** | Credits to **SigmaX**"""
    
    @staticmethod
    def format_approval_success(user_id: int) -> str:
        """Format user approval success message"""
        return f"✅ User `{user_id}` has been approved to use the bot."
    
    @staticmethod
    def format_group_usage_update(enabled: bool) -> str:
        """Format group usage update message"""
        status = "enabled" if enabled else "disabled"
        emoji = "✅" if enabled else "❌"
        return f"{emoji} Group usage has been {status}."
    
    @staticmethod
    def _escape_markdown(text: str) -> str:
        """Escape special characters that might break Telegram message parsing"""
        if not text or text == "Unknown":
            return text
        
        # Remove or replace characters that commonly cause Telegram parsing issues
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        
        for char in special_chars:
            text = text.replace(char, '')
        
        # Limit length to avoid overly long SSL certificate names
        if len(text) > 50:
            text = text[:47] + "..."
            
        return text
