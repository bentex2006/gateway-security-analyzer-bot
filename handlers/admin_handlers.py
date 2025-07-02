import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from utils.formatting import MessageFormatter

logger = logging.getLogger(__name__)

class AdminHandlers:
    
    def __init__(self, database, config):
        self.db = database
        self.config = config
    
    def is_admin(self, user_id: int) -> bool:
        return user_id in self.config.ADMIN_IDS
    
    async def approve_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        
        # Check if user is admin
        if not self.is_admin(user.id):
            await update.message.reply_text(
                "❌ You don't have permission to use this command.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Check if user_id argument is provided
        if not context.args:
            await update.message.reply_text(
                "❌ **Usage**: `/approve <user_id>`\n\n"
                "**Example**: `/approve 123456789`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        try:
            user_id_to_approve = int(context.args[0])
        except ValueError:
            await update.message.reply_text(
                "❌ Invalid user ID. Please provide a valid numeric user ID.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Check if user is already approved
        if self.db.is_user_approved(user_id_to_approve):
            await update.message.reply_text(
                f"ℹ️ User `{user_id_to_approve}` is already approved.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Approve the user
        self.db.approve_user(user_id_to_approve)
        
        # Send confirmation
        await update.message.reply_text(
            MessageFormatter.format_approval_success(user_id_to_approve),
            parse_mode=ParseMode.MARKDOWN
        )
        
        logger.info(f"Admin {user.id} approved user {user_id_to_approve}")
    
    async def group_use(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /groupuse command"""
        user = update.effective_user
        chat = update.effective_chat
        
        # Check if user is admin
        if not self.is_admin(user.id):
            await update.message.reply_text(
                "❌ You don't have permission to use this command.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Check if this is a group chat
        if chat.type not in ['group', 'supergroup']:
            await update.message.reply_text(
                "❌ This command can only be used in groups.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Check if argument is provided
        if not context.args:
            current_status = self.db.is_group_usage_enabled(chat.id)
            status_text = "enabled" if current_status else "disabled"
            
            await update.message.reply_text(
                f"ℹ️ **Current group usage status**: {status_text}\n\n"
                f"**Usage**: `/groupuse <on/off>`\n\n"
                f"**Examples**:\n"
                f"• `/groupuse on` - Enable group usage\n"
                f"• `/groupuse off` - Disable group usage",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Parse argument
        arg = context.args[0].lower()
        
        if arg in ['on', 'yes', 'enable', 'enabled', '1', 'true']:
            enabled = True
        elif arg in ['off', 'no', 'disable', 'disabled', '0', 'false']:
            enabled = False
        else:
            await update.message.reply_text(
                "❌ Invalid argument. Use `on` or `off`.\n\n"
                "**Examples**:\n"
                "• `/groupuse on`\n"
                "• `/groupuse off`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Update group usage setting
        self.db.set_group_usage(chat.id, enabled)
        
        # Send confirmation
        await update.message.reply_text(
            MessageFormatter.format_group_usage_update(enabled),
            parse_mode=ParseMode.MARKDOWN
        )
        
        logger.info(f"Admin {user.id} set group usage to {enabled} for chat {chat.id}")
    
    async def auth_toggle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /auth command to toggle approval requirement"""
        user = update.effective_user
        
        # Check if user is admin
        if not self.is_admin(user.id):
            await update.message.reply_text(
                "❌ Access denied. This command is only available to admins.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Check if argument provided
        if not context.args:
            current_status = "enabled" if self.db.is_auth_required() else "disabled"
            await update.message.reply_text(
                f"**🔐 Current Auth Status**: {current_status}\n\n"
                "**Usage**: `/auth on|off`\n\n"
                "**Examples**:\n"
                "• `/auth on` - Require user approval\n"
                "• `/auth off` - Allow all users",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Parse argument
        arg = context.args[0].lower()
        
        if arg in ['on', 'yes', 'enable', 'enabled', '1', 'true']:
            required = True
        elif arg in ['off', 'no', 'disable', 'disabled', '0', 'false']:
            required = False
        else:
            await update.message.reply_text(
                "❌ Invalid argument. Use `on` or `off`.\n\n"
                "**Examples**:\n"
                "• `/auth on`\n"
                "• `/auth off`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Update auth requirement
        self.db.set_auth_required(required)
        
        # Send confirmation
        status = "**enabled**" if required else "**disabled**"
        await update.message.reply_text(
            f"✅ **Auth System Updated**\n\n"
            f"🔐 **User approval is now {status}**\n\n"
            f"{'Users must be approved to use the bot.' if required else 'All users can use the bot without approval.'}",
            parse_mode=ParseMode.MARKDOWN
        )
        
        logger.info(f"Admin {user.id} set auth requirement to {required}")
    
    async def admin_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command (admin only)"""
        user = update.effective_user
        
        # Check if user is admin
        if not self.is_admin(user.id):
            await update.message.reply_text(
                "❌ You don't have permission to use this command.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Get statistics
        approved_users_count = self.db.get_approved_users_count()
        total_groups = len(self.db.group_settings)
        enabled_groups = sum(1 for enabled in self.db.group_settings.values() if enabled)
        disabled_groups = total_groups - enabled_groups
        
        stats_message = f"""📊 **Bot Statistics**

👥 **Users**:
├─ Approved: {approved_users_count}
└─ Admins: {len(self.config.ADMIN_IDS)}

💬 **Groups**:
├─ Total: {total_groups}
├─ Enabled: {enabled_groups}
└─ Disabled: {disabled_groups}

🔧 **Admin Commands**:
• `/approve <user_id>` - Approve user
• `/groupuse <on/off>` - Control group usage
• `/stats` - Show statistics

Developed by **Skittle** | Credits to **SigmaX**"""
        
        await update.message.reply_text(
            stats_message,
            parse_mode=ParseMode.MARKDOWN
        )
