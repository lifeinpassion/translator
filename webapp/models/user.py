"""
User model for authentication and subscription management
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class UserTier(Enum):
    """User subscription tiers"""
    FREE = "free"
    DEEPL = "deepl"
    AI = "ai"


@dataclass
class User:
    """User model"""
    email: str
    password_hash: str
    tier: UserTier = UserTier.FREE
    name: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    subscription_expires: Optional[datetime] = None
    api_key: Optional[str] = None

    # Usage tracking
    texts_translated_month: int = 0
    documents_translated_month: int = 0
    images_translated_month: int = 0
    characters_translated_month: int = 0

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'tier': self.tier.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'subscription_expires': self.subscription_expires.isoformat() if self.subscription_expires else None,
            'usage': {
                'texts': self.texts_translated_month,
                'documents': self.documents_translated_month,
                'images': self.images_translated_month,
                'characters': self.characters_translated_month
            }
        }

    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        tier = UserTier(data.get('tier', 'free'))

        user = cls(
            id=data.get('id'),
            email=data['email'],
            password_hash=data['password_hash'],
            name=data.get('name', ''),
            tier=tier,
            created_at=datetime.fromisoformat(data['created_at']) if isinstance(data.get('created_at'), str) else data.get('created_at', datetime.now()),
            updated_at=datetime.fromisoformat(data['updated_at']) if isinstance(data.get('updated_at'), str) else data.get('updated_at', datetime.now()),
            subscription_expires=datetime.fromisoformat(data['subscription_expires']) if data.get('subscription_expires') else None,
            api_key=data.get('api_key'),
            texts_translated_month=data.get('texts_translated_month', 0),
            documents_translated_month=data.get('documents_translated_month', 0),
            images_translated_month=data.get('images_translated_month', 0),
            characters_translated_month=data.get('characters_translated_month', 0)
        )

        return user

    def is_within_limits(self, operation: str = 'text') -> bool:
        """
        Check if user is within usage limits

        Args:
            operation: Type of operation ('text', 'document', 'image')

        Returns:
            True if within limits, False otherwise
        """
        limits = self._get_tier_limits()

        if operation == 'text':
            if limits['text_chars_per_month'] == -1:
                return True
            return self.characters_translated_month < limits['text_chars_per_month']

        elif operation == 'document':
            if limits['documents_per_month'] == -1:
                return True
            return self.documents_translated_month < limits['documents_per_month']

        elif operation == 'image':
            if limits['images_per_month'] == -1:
                return True
            return self.images_translated_month < limits['images_per_month']

        return False

    def _get_tier_limits(self):
        """Get limits for current tier"""
        limits = {
            UserTier.FREE: {
                'text_chars_per_month': 500000,
                'documents_per_month': 3,
                'images_per_month': 10,
                'max_file_size_mb': 10
            },
            UserTier.DEEPL: {
                'text_chars_per_month': 5000000,
                'documents_per_month': 50,
                'images_per_month': 100,
                'max_file_size_mb': 50
            },
            UserTier.AI: {
                'text_chars_per_month': -1,  # Unlimited
                'documents_per_month': -1,
                'images_per_month': -1,
                'max_file_size_mb': 100
            }
        }

        return limits.get(self.tier, limits[UserTier.FREE])

    def increment_usage(self, operation: str, characters: int = 0):
        """
        Increment usage counters

        Args:
            operation: Type of operation
            characters: Number of characters (for text translation)
        """
        if operation == 'text':
            self.texts_translated_month += 1
            self.characters_translated_month += characters
        elif operation == 'document':
            self.documents_translated_month += 1
        elif operation == 'image':
            self.images_translated_month += 1

        self.updated_at = datetime.now()

    def reset_monthly_usage(self):
        """Reset monthly usage counters"""
        self.texts_translated_month = 0
        self.documents_translated_month = 0
        self.images_translated_month = 0
        self.characters_translated_month = 0
        self.updated_at = datetime.now()
