"""
URL analysis handler for the Telegram bot
"""

import asyncio
import time
import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from utils.validators import URLValidator
from utils.formatting import MessageFormatter
from analyzers.website_analyzer import WebsiteAnalyzer
from analyzers.security_analyzer import SecurityAnalyzer
from analyzers.ssl_analyzer import SSLAnalyzer
from analyzers.payment_analyzer import PaymentAnalyzer

logger = logging.getLogger(__name__)

class URLHandler:
    """Handles URL analysis commands"""
    
    def __init__(self, database, config):
        self.db = database
        self.config = config
        self.website_analyzer = WebsiteAnalyzer(config)
        self.security_analyzer = SecurityAnalyzer(config)
        self.ssl_analyzer = SSLAnalyzer(config)
        self.payment_analyzer = PaymentAnalyzer(config)
    
    def check_permissions(self, user_id: int, chat_type: str, chat_id: int) -> bool:
        """Check if user has permission to use the bot"""
        # Admin bypass
        if user_id in self.config.ADMIN_IDS:
            return True
        
        # Private chat - check if auth is required
        if chat_type == 'private':
            if not self.db.is_auth_required():
                return True  # Auth disabled, allow all users
            return self.db.is_user_approved(user_id)
        
        # Group chat - check group usage settings
        if chat_type in ['group', 'supergroup']:
            group_enabled = self.db.is_group_usage_enabled(chat_id)
            if group_enabled:
                return True  # Anyone can use in enabled groups
            else:
                return self.db.is_user_approved(user_id)  # Only approved users in disabled groups
        
        return False
    
    async def handle_url_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /url command"""
        user = update.effective_user
        chat = update.effective_chat
        
        # Check permissions
        if not self.check_permissions(user.id, chat.type, chat.id):
            await update.message.reply_text(
                MessageFormatter.format_permission_denied(),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Check if URL argument is provided
        if not context.args:
            await update.message.reply_text(
                "❌ **Usage**: `/url <website>`\n\n"
                "**Examples**:\n"
                "• `/url https://example.com`\n"
                "• `/url example.com`\n"
                "• `/url shop.example.com/checkout`\n\n"
                "The bot will analyze the website for security features, "
                "technology stack, and payment systems.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Extract and validate URL
        url_input = ' '.join(context.args)
        is_valid, normalized_url, error_message = URLValidator.validate_and_normalize_url(url_input)
        
        if not is_valid:
            await update.message.reply_text(
                f"❌ **Invalid URL**: {error_message}\n\n"
                "**Valid formats**:\n"
                "• `https://example.com`\n"
                "• `example.com`\n"
                "• `subdomain.example.com`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Send processing message with GIF
        processing_message = await context.bot.send_animation(
            chat_id=chat.id,
            animation=self.config.PROCESSING_GIF,
            caption="🔍 **Analyzing website...**\n\n"
                   "Please wait while I scan for:\n"
                   "• Security features\n"
                   "• Technology stack\n"
                   "• Payment systems\n"
                   "• SSL certificate\n"
                   "• And more...",
            parse_mode=ParseMode.MARKDOWN
        )
        
        start_time = time.time()
        
        try:
            # Perform analysis
            analysis_results = await self.analyze_website(normalized_url)
            
            # Format results
            result_message = MessageFormatter.format_main_result(
                analysis_results,
                URLValidator.sanitize_url_for_display(normalized_url),
                user.username,
                start_time
            )
            
            # Delete processing message
            await processing_message.delete()
            
            # Send result with GIF
            await context.bot.send_animation(
                chat_id=chat.id,
                animation=self.config.RESULT_GIF,
                caption=result_message,
                parse_mode=ParseMode.MARKDOWN
            )
            
            logger.info(f"User {user.id} analyzed URL: {normalized_url}")
            
        except Exception as e:
            logger.error(f"Analysis failed for {normalized_url}: {e}")
            
            # Delete processing message
            await processing_message.delete()
            
            # Send error message
            await update.message.reply_text(
                MessageFormatter.format_error_message(str(e)),
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def analyze_website(self, url: str) -> dict:
        """Perform comprehensive website analysis"""
        results = {}
        
        try:
            # Website analysis (Cloudflare, CAPTCHA, GraphQL, WordPress, etc.)
            results['website'] = self.website_analyzer.analyze_website(url)
        except Exception as e:
            logger.error(f"Website analysis failed: {e}")
            results['website'] = {'error': str(e)}
        
        try:
            # Security analysis (headers, HTTPS redirect, cookies)
            results['security'] = self.security_analyzer.analyze_security_headers(url)
        except Exception as e:
            logger.error(f"Security analysis failed: {e}")
            results['security'] = {'error': str(e)}
        
        try:
            # SSL analysis
            results['ssl'] = self.ssl_analyzer.analyze_ssl_certificate(url)
        except Exception as e:
            logger.error(f"SSL analysis failed: {e}")
            results['ssl'] = {'error': str(e)}
        
        try:
            # Payment analysis
            results['payment'] = self.payment_analyzer.detect_payment_systems(url)
        except Exception as e:
            logger.error(f"Payment analysis failed: {e}")
            results['payment'] = {'error': str(e)}
        
        return results
