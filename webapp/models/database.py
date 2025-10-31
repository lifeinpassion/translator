"""
Database management for users
Uses JSON file storage (can be upgraded to SQL later)
"""

import json
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime
import threading

from .user import User, UserTier


class Database:
    """Simple JSON-based database for users"""

    def __init__(self, db_path: str = None):
        """
        Initialize database

        Args:
            db_path: Path to database file
        """
        if db_path is None:
            db_path = Path(__file__).parent.parent / 'data' / 'users.json'
        else:
            db_path = Path(db_path)

        self.db_path = db_path
        self.lock = threading.Lock()

        # Ensure data directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize database if doesn't exist
        if not self.db_path.exists():
            self._save_data({'users': {}, 'usage_logs': []})

    def _load_data(self) -> Dict:
        """Load data from database file"""
        with self.lock:
            try:
                with open(self.db_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading database: {e}")
                return {'users': {}, 'usage_logs': []}

    def _save_data(self, data: Dict):
        """Save data to database file"""
        with self.lock:
            try:
                with open(self.db_path, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
            except Exception as e:
                print(f"Error saving database: {e}")

    def create_user(self, user: User) -> User:
        """
        Create new user

        Args:
            user: User object

        Returns:
            Created user
        """
        data = self._load_data()

        # Check if email already exists
        for existing_user in data['users'].values():
            if existing_user['email'] == user.email:
                raise ValueError(f"User with email {user.email} already exists")

        # Add user
        data['users'][user.id] = user.to_dict()
        self._save_data(data)

        return user

    def get_user(self, user_id: str) -> Optional[User]:
        """
        Get user by ID

        Args:
            user_id: User ID

        Returns:
            User object or None
        """
        data = self._load_data()
        user_data = data['users'].get(user_id)

        if user_data:
            return User.from_dict(user_data)

        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email

        Args:
            email: User email

        Returns:
            User object or None
        """
        data = self._load_data()

        for user_data in data['users'].values():
            if user_data['email'] == email:
                return User.from_dict(user_data)

        return None

    def update_user(self, user: User) -> User:
        """
        Update user

        Args:
            user: User object

        Returns:
            Updated user
        """
        data = self._load_data()

        if user.id not in data['users']:
            raise ValueError(f"User {user.id} not found")

        user.updated_at = datetime.now()
        data['users'][user.id] = user.to_dict()
        self._save_data(data)

        return user

    def delete_user(self, user_id: str):
        """
        Delete user

        Args:
            user_id: User ID
        """
        data = self._load_data()

        if user_id in data['users']:
            del data['users'][user_id]
            self._save_data(data)

    def get_all_users(self) -> List[User]:
        """
        Get all users

        Returns:
            List of users
        """
        data = self._load_data()
        return [User.from_dict(user_data) for user_data in data['users'].values()]

    def log_usage(self, user_id: str, operation: str, details: Dict):
        """
        Log usage event

        Args:
            user_id: User ID
            operation: Operation type
            details: Additional details
        """
        data = self._load_data()

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'operation': operation,
            'details': details
        }

        data['usage_logs'].append(log_entry)

        # Keep only last 10000 logs
        if len(data['usage_logs']) > 10000:
            data['usage_logs'] = data['usage_logs'][-10000:]

        self._save_data(data)

    def get_user_stats(self, user_id: str) -> Dict:
        """
        Get usage statistics for user

        Args:
            user_id: User ID

        Returns:
            Statistics dictionary
        """
        user = self.get_user(user_id)
        if not user:
            return {}

        data = self._load_data()

        # Count operations this month
        user_logs = [
            log for log in data['usage_logs']
            if log['user_id'] == user_id
        ]

        return {
            'tier': user.tier.value,
            'usage': {
                'texts': user.texts_translated_month,
                'documents': user.documents_translated_month,
                'images': user.images_translated_month,
                'characters': user.characters_translated_month
            },
            'limits': user._get_tier_limits(),
            'history': user_logs[-100:]  # Last 100 operations
        }

    def reset_monthly_usage_all(self):
        """Reset monthly usage for all users"""
        data = self._load_data()

        for user_id in data['users']:
            user = User.from_dict(data['users'][user_id])
            user.reset_monthly_usage()
            data['users'][user_id] = user.to_dict()

        self._save_data(data)
