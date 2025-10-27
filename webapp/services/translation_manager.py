"""
Translation Manager - Unified service for all translation types
Manages 3-tier subscription system:
- FREE: Google Translate (via deep-translator)
- DEEPL: DeepL API
- AI: AI-powered translation (ChatGPT, Claude, etc.)
"""

import os
from pathlib import Path
from typing import Optional, Dict
from enum import Enum

# Import our translation services
from core.translation_services import (
    GoogleTranslateService,
    DeepLTranslateService,
    ChatGPTTranslationService,
    ClaudeTranslationService,
    GeminiTranslationService
)


class UserTier(Enum):
    """User subscription tiers"""
    FREE = "free"
    DEEPL = "deepl"
    AI = "ai"


class TranslationManager:
    """
    Unified translation manager for text, documents, and images
    """

    def __init__(self):
        """Initialize translation manager"""
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load configuration from environment or defaults"""
        return {
            'deepl_api_key': os.environ.get('DEEPL_API_KEY'),
            'openai_api_key': os.environ.get('OPENAI_API_KEY'),
            'anthropic_api_key': os.environ.get('ANTHROPIC_API_KEY'),
            'google_api_key': os.environ.get('GOOGLE_API_KEY'),
            'ai_default_model': os.environ.get('AI_DEFAULT_MODEL', 'gpt-4o-mini'),
            'ai_service': os.environ.get('AI_SERVICE', 'chatgpt')  # chatgpt, claude, gemini
        }

    def _get_translation_service(self, tier: UserTier, source_lang: str, target_lang: str):
        """
        Get appropriate translation service based on user tier

        Args:
            tier: User subscription tier
            source_lang: Source language code
            target_lang: Target language code

        Returns:
            Translation service instance
        """
        if tier == UserTier.FREE:
            # Free tier: Google Translate
            return GoogleTranslateService(
                source_lang=source_lang,
                target_lang=target_lang
            )

        elif tier == UserTier.DEEPL:
            # DeepL tier: DeepL API
            api_key = self.config.get('deepl_api_key')
            if not api_key:
                print("Warning: DeepL API key not configured, falling back to Google Translate")
                return GoogleTranslateService(source_lang=source_lang, target_lang=target_lang)

            return DeepLTranslateService(
                source_lang=source_lang,
                target_lang=target_lang,
                api_key=api_key
            )

        elif tier == UserTier.AI:
            # AI tier: ChatGPT, Claude, or Gemini
            ai_service = self.config.get('ai_service', 'chatgpt')

            if ai_service == 'chatgpt':
                api_key = self.config.get('openai_api_key')
                if not api_key:
                    print("Warning: OpenAI API key not configured, falling back to Google Translate")
                    return GoogleTranslateService(source_lang=source_lang, target_lang=target_lang)

                return ChatGPTTranslationService(
                    source_lang=source_lang,
                    target_lang=target_lang,
                    api_key=api_key,
                    model=self.config.get('ai_default_model', 'gpt-4o-mini')
                )

            elif ai_service == 'claude':
                api_key = self.config.get('anthropic_api_key')
                if not api_key:
                    print("Warning: Anthropic API key not configured, falling back to Google Translate")
                    return GoogleTranslateService(source_lang=source_lang, target_lang=target_lang)

                return ClaudeTranslationService(
                    source_lang=source_lang,
                    target_lang=target_lang,
                    api_key=api_key,
                    model='claude-3-5-haiku-20241022'
                )

            elif ai_service == 'gemini':
                api_key = self.config.get('google_api_key')
                if not api_key:
                    print("Warning: Google API key not configured, falling back to Google Translate")
                    return GoogleTranslateService(source_lang=source_lang, target_lang=target_lang)

                return GeminiTranslationService(
                    source_lang=source_lang,
                    target_lang=target_lang,
                    api_key=api_key,
                    model='gemini-1.5-flash'
                )

            else:
                print(f"Warning: Unknown AI service '{ai_service}', falling back to Google Translate")
                return GoogleTranslateService(source_lang=source_lang, target_lang=target_lang)

        else:
            raise ValueError(f"Unknown tier: {tier}")

    def translate_text(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        tier: UserTier
    ) -> str:
        """
        Translate plain text

        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            tier: User subscription tier

        Returns:
            Translated text
        """
        service = self._get_translation_service(tier, source_lang, target_lang)
        return service.translate_cached(text)

    def translate_document(
        self,
        input_path: str,
        source_lang: str,
        target_lang: str,
        tier: UserTier,
        preserve_original: bool = True
    ) -> str:
        """
        Translate document (PDF, Word, Excel, PowerPoint)

        Note: Document translation requires additional dependencies.
        For now, this is a placeholder that returns an error message.

        Args:
            input_path: Path to input document
            source_lang: Source language code
            target_lang: Target language code
            tier: User subscription tier
            preserve_original: For PDFs, whether to preserve original text

        Returns:
            Path to translated document
        """
        raise NotImplementedError(
            "Document translation requires additional dependencies. "
            "Please install: pip install pymupdf python-docx openpyxl python-pptx"
        )

    def translate_image(
        self,
        input_path: str,
        source_lang: str,
        target_lang: str,
        tier: UserTier
    ) -> str:
        """
        Translate image using OCR + translation + rendering

        Note: Image translation requires additional dependencies.
        For now, this is a placeholder that returns an error message.

        Args:
            input_path: Path to input image
            source_lang: Source language code
            target_lang: Target language code
            tier: User subscription tier

        Returns:
            Path to translated image
        """
        raise NotImplementedError(
            "Image translation requires additional dependencies. "
            "Please install: pip install paddlepaddle paddleocr opencv-python"
        )

    def get_tier_limits(self, tier: UserTier) -> Dict:
        """
        Get usage limits for a tier

        Returns:
            Dictionary with tier information and limits
        """
        limits = {
            UserTier.FREE: {
                'name': 'Free',
                'price': 0,
                'text_chars_per_month': 500000,  # 500K characters
                'documents_per_month': 3,
                'images_per_month': 10,
                'max_file_size_mb': 10,
                'features': [
                    'Google Translate',
                    'Basic text translation',
                    'Limited document translation',
                    'Limited image translation'
                ]
            },
            UserTier.DEEPL: {
                'name': 'DeepL Pro',
                'price': 9.99,
                'text_chars_per_month': 5000000,  # 5M characters
                'documents_per_month': 50,
                'images_per_month': 100,
                'max_file_size_mb': 50,
                'features': [
                    'DeepL API translation',
                    'Higher quality translations',
                    'Unlimited text translation',
                    'More document formats',
                    'Priority processing'
                ]
            },
            UserTier.AI: {
                'name': 'AI Premium',
                'price': 29.99,
                'text_chars_per_month': -1,  # Unlimited
                'documents_per_month': -1,  # Unlimited
                'images_per_month': -1,  # Unlimited
                'max_file_size_mb': 100,
                'features': [
                    'AI-powered translation (ChatGPT/Claude)',
                    'Best translation quality',
                    'Context-aware translation',
                    'Unlimited everything',
                    'Batch processing',
                    'API access',
                    'Priority support'
                ]
            }
        }

        return limits.get(tier, limits[UserTier.FREE])

    def get_tier_info(self) -> Dict:
        """Get information about all tiers"""
        return {
            'free': self.get_tier_limits(UserTier.FREE),
            'deepl': self.get_tier_limits(UserTier.DEEPL),
            'ai': self.get_tier_limits(UserTier.AI)
        }
