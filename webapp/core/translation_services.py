"""
Translation service implementations for different tiers
"""

import os
from typing import Optional
from functools import lru_cache

# Import translation libraries with error handling
try:
    from deep_translator import GoogleTranslator
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    print("Warning: deep-translator not installed. Free tier disabled.")

try:
    import deepl
    DEEPL_AVAILABLE = True
except ImportError:
    DEEPL_AVAILABLE = False
    print("Warning: deepl not installed. DeepL tier disabled.")

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: openai not installed. ChatGPT tier disabled.")

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("Warning: anthropic not installed. Claude tier disabled.")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not installed. Gemini tier disabled.")


class TranslationService:
    """Base class for translation services"""

    def __init__(self, source_lang='en', target_lang='zh-CN', api_key=None):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.api_key = api_key

    @lru_cache(maxsize=10000)
    def translate_cached(self, text: str) -> str:
        """Translate with caching"""
        if not text or not text.strip():
            return text
        return self.translate(text)

    def translate(self, text: str) -> str:
        """Override in subclasses"""
        raise NotImplementedError


class GoogleTranslateService(TranslationService):
    """Google Translate (Free tier)"""

    def __init__(self, source_lang='en', target_lang='zh-CN', **kwargs):
        super().__init__(source_lang, target_lang)
        if not GOOGLE_AVAILABLE:
            raise ImportError("deep-translator not installed")
        self.translator = GoogleTranslator(source=source_lang, target=target_lang)

    def translate(self, text: str) -> str:
        if not text or not text.strip():
            return text
        try:
            return self.translator.translate(text)
        except Exception as e:
            print(f"Translation error: {e}")
            return text


class DeepLTranslateService(TranslationService):
    """DeepL API (Pro tier)"""

    def __init__(self, source_lang='en', target_lang='zh-CN', api_key=None, **kwargs):
        super().__init__(source_lang, target_lang, api_key)
        if not DEEPL_AVAILABLE:
            raise ImportError("deepl not installed")
        if not api_key:
            raise ValueError("DeepL requires an API key")
        self.translator = deepl.Translator(api_key)

    def translate(self, text: str) -> str:
        if not text or not text.strip():
            return text
        try:
            result = self.translator.translate_text(
                text,
                target_lang=self.target_lang.split('-')[0].upper()
            )
            return result.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text


class ChatGPTTranslationService(TranslationService):
    """OpenAI ChatGPT (AI Premium tier)"""

    def __init__(self, source_lang='en', target_lang='zh-CN', api_key=None, model='gpt-4o-mini'):
        super().__init__(source_lang, target_lang, api_key)
        if not OPENAI_AVAILABLE:
            raise ImportError("openai not installed")
        if not api_key:
            raise ValueError("OpenAI API key required")
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.source_lang_name = self._format_language(source_lang)
        self.target_lang_name = self._format_language(target_lang)

    def _format_language(self, lang_code):
        """Convert language codes to names"""
        lang_map = {
            'en': 'English', 'zh-CN': 'Simplified Chinese', 'zh-TW': 'Traditional Chinese',
            'es': 'Spanish', 'fr': 'French', 'de': 'German', 'ja': 'Japanese',
            'ko': 'Korean', 'ru': 'Russian', 'ar': 'Arabic', 'pt': 'Portuguese',
            'it': 'Italian'
        }
        return lang_map.get(lang_code, lang_code)

    def translate(self, text: str) -> str:
        if not text or not text.strip():
            return text
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are a professional translator. Translate from {self.source_lang_name} to {self.target_lang_name}. Only return the translation without explanations."},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=len(text) * 3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Translation error: {e}")
            return text


class ClaudeTranslationService(TranslationService):
    """Anthropic Claude (AI Premium tier)"""

    def __init__(self, source_lang='en', target_lang='zh-CN', api_key=None, model='claude-3-5-haiku-20241022'):
        super().__init__(source_lang, target_lang, api_key)
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("anthropic not installed")
        if not api_key:
            raise ValueError("Anthropic API key required")
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.source_lang_name = self._format_language(source_lang)
        self.target_lang_name = self._format_language(target_lang)

    def _format_language(self, lang_code):
        """Convert language codes to names"""
        lang_map = {
            'en': 'English', 'zh-CN': 'Simplified Chinese', 'zh-TW': 'Traditional Chinese',
            'es': 'Spanish', 'fr': 'French', 'de': 'German', 'ja': 'Japanese',
            'ko': 'Korean', 'ru': 'Russian', 'ar': 'Arabic', 'pt': 'Portuguese',
            'it': 'Italian'
        }
        return lang_map.get(lang_code, lang_code)

    def translate(self, text: str) -> str:
        if not text or not text.strip():
            return text
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=len(text) * 3,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": f"Translate from {self.source_lang_name} to {self.target_lang_name}. Only return the translation:\n\n{text}"}
                ]
            )
            return message.content[0].text.strip()
        except Exception as e:
            print(f"Translation error: {e}")
            return text


class GeminiTranslationService(TranslationService):
    """Google Gemini (AI Premium tier)"""

    def __init__(self, source_lang='en', target_lang='zh-CN', api_key=None, model='gemini-1.5-flash'):
        super().__init__(source_lang, target_lang, api_key)
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai not installed")
        if not api_key:
            raise ValueError("Google API key required")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        self.source_lang_name = self._format_language(source_lang)
        self.target_lang_name = self._format_language(target_lang)

    def _format_language(self, lang_code):
        """Convert language codes to names"""
        lang_map = {
            'en': 'English', 'zh-CN': 'Simplified Chinese', 'zh-TW': 'Traditional Chinese',
            'es': 'Spanish', 'fr': 'French', 'de': 'German', 'ja': 'Japanese',
            'ko': 'Korean', 'ru': 'Russian', 'ar': 'Arabic', 'pt': 'Portuguese',
            'it': 'Italian'
        }
        return lang_map.get(lang_code, lang_code)

    def translate(self, text: str) -> str:
        if not text or not text.strip():
            return text
        try:
            response = self.model.generate_content(
                f"Translate from {self.source_lang_name} to {self.target_lang_name}. Only return the translation without explanations:\n\n{text}",
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=len(text) * 3,
                )
            )
            return response.text.strip()
        except Exception as e:
            print(f"Translation error: {e}")
            return text
