import asyncio
import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

from config import Config
from database import Database
from handlers.admin_handlers import AdminHandlers
from handlers.url_handler import URLHandler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class GatewayBot:
    def __init__(self):
        self.config = Config()
        self.db = Database()
        self.admin_handlers = AdminHandlers(self.db, self.config)
        self.url_handler = URLHandler(self.db, self.config)
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        chat = update.effective_chat
        
        # Send start GIF
        await context.bot.send_animation(
            chat_id=chat.id,
            animation=self.config.START_GIF,
            caption=" **Gateway Analyzer Bot**\n\n"
                   "website security and technology detection bot!\n\n"
                   "**Commands:**\n"
                   "• `/url <website>` - Analyze a website\n"
                   "• `/approve <user_id>` - Approve user (Admin only)\n"
                   "• `/groupuse <on/off>` - Control group usage (Admin only)\n\n"
                   "**Note:** This bot requires admin approval to use.\n\n"
                   "Developed by **Skittle** | Credits to **SigmaX**",
            parse_mode=ParseMode.MARKDOWN
        )
        
        logger.info(f"User {user.id} started the bot")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
 **Gateway Analyzer Bot**

**Available Commands:**
• `/start` - Start the bot
• `/help` - Show this help message
• `/url <website>` - Analyze website security and technology
• `/approve <user_id>` - Approve user to use bot (Admin only)
• `/groupuse <on/off>` - Enable/disable group usage (Admin only)

**What I can detect:**
🔒 Cloudflare protection
🤖 CAPTCHA systems (reCAPTCHA, hCaptcha)
🔍 GraphQL endpoints
🛒 WordPress/WooCommerce
🛡️ Security headers
💳 Payment gateways
🔐 SSL certificate details

**Example Usage:**
`/url https://example.com`

Developed by **Skittle** | Credits to **SigmaX**
        """
        
        await update.message.reply_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN
        )

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Log errors and send error message to user"""
        logger.error(f"Exception while handling an update: {context.error}")
        
        if isinstance(update, Update) and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred while processing your request. Please try again later."
            )

    def setup_handlers(self, app: Application):
        """Setup all command and message handlers"""
        # Basic commands
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("help", self.help_command))
        
        # URL analysis handler
        app.add_handler(CommandHandler("url", self.url_handler.handle_url_command))
        
        # Admin handlers
        app.add_handler(CommandHandler("approve", self.admin_handlers.approve_user))
        app.add_handler(CommandHandler("groupuse", self.admin_handlers.group_use))
        app.add_handler(CommandHandler("stats", self.admin_handlers.admin_stats))
        
        # Error handler
        app.add_error_handler(self.error_handler)

    def run_bot(self):
        """Run the bot with polling"""
        app = Application.builder().token(self.config.BOT_TOKEN).build()
        
        self.setup_handlers(app)
        
        logger.info("Bot is starting...")
        logger.info("Bot token configured, ready to receive messages")
        
        # Run the bot
        app.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function to run the bot"""
    bot = GatewayBot()
    
    try:
        bot.run_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")

if __name__ == "__main__":
    main()
