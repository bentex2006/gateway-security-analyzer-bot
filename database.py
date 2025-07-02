import json
import os
from typing import Set, Dict

class Database:
    
    def __init__(self, db_file: str = "bot_data.json"):
        self.db_file = db_file
        self.approved_users: Set[int] = set()
        self.group_settings: Dict[int, bool] = {}  # chat_id -> group_usage_enabled
        self.auth_required: bool = True  # Whether user approval is required
        self.load_data()
    
    def load_data(self):
        """Load data from file"""
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r') as f:
                    data = json.load(f)
                    self.approved_users = set(data.get('approved_users', []))
                    self.group_settings = {int(k): v for k, v in data.get('group_settings', {}).items()}
                    self.auth_required = data.get('auth_required', True)
        except Exception as e:
            print(f"Error loading database: {e}")
    
    def save_data(self):
        """Save data to file"""
        try:
            data = {
                'approved_users': list(self.approved_users),
                'group_settings': {str(k): v for k, v in self.group_settings.items()},
                'auth_required': self.auth_required
            }
            with open(self.db_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving database: {e}")
    
    def approve_user(self, user_id: int):
        """Approve a user to use the bot"""
        self.approved_users.add(user_id)
        self.save_data()
    
    def is_user_approved(self, user_id: int) -> bool:
        """Check if a user is approved"""
        return user_id in self.approved_users
    
    def set_group_usage(self, chat_id: int, enabled: bool):
        """Set group usage permission"""
        self.group_settings[chat_id] = enabled
        self.save_data()
    
    def is_group_usage_enabled(self, chat_id: int) -> bool:
        """Check if group usage is enabled for a chat"""
        return self.group_settings.get(chat_id, True)  # Default to enabled
    
    def remove_user_approval(self, user_id: int):
        """Remove user approval"""
        self.approved_users.discard(user_id)
        self.save_data()
    
    def get_approved_users_count(self) -> int:
        """Get count of approved users"""
        return len(self.approved_users)
    
    def set_auth_required(self, required: bool):
        """Set whether user approval is required"""
        self.auth_required = required
        self.save_data()
    
    def is_auth_required(self) -> bool:
        """Check if user approval is required"""
        return self.auth_required
