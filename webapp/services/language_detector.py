"""
Language Detection Service
Detects source language automatically
"""

from typing import Optional, Dict, List
from functools import lru_cache

try:
    from langdetect import detect, detect_langs, DetectorFactory
    DetectorFactory.seed = 0  # For consistent results
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False
    print("Warning: langdetect not installed. Language detection disabled.")


class LanguageDetector:
    """Language detection with confidence scores"""

    def __init__(self):
        """Initialize language detector"""
        self.last_confidence = 0.0
        self.language_names = {
            'en': 'English',
            'zh-cn': 'Chinese (Simplified)',
            'zh-tw': 'Chinese (Traditional)',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'ja': 'Japanese',
            'ko': 'Korean',
            'ru': 'Russian',
            'ar': 'Arabic',
            'pt': 'Portuguese',
            'it': 'Italian',
            'nl': 'Dutch',
            'pl': 'Polish',
            'tr': 'Turkish',
            'vi': 'Vietnamese',
            'th': 'Thai',
            'id': 'Indonesian',
            'hi': 'Hindi',
            'sv': 'Swedish',
            'da': 'Danish',
            'fi': 'Finnish',
            'no': 'Norwegian',
            'cs': 'Czech',
            'sk': 'Slovak',
            'ro': 'Romanian',
            'hu': 'Hungarian',
            'el': 'Greek',
            'he': 'Hebrew',
            'uk': 'Ukrainian',
            'bg': 'Bulgarian',
            'hr': 'Croatian',
            'sr': 'Serbian',
            'lt': 'Lithuanian',
            'lv': 'Latvian',
            'et': 'Estonian',
            'sl': 'Slovenian',
            'ca': 'Catalan',
            'ms': 'Malay',
            'tl': 'Tagalog'
        }

    @lru_cache(maxsize=1000)
    def detect(self, text: str) -> str:
        """
        Detect language of text

        Args:
            text: Text to detect language

        Returns:
            Language code (e.g., 'en', 'zh-cn')
        """
        if not text or not text.strip():
            return 'en'

        if not LANGDETECT_AVAILABLE:
            # Fallback: simple heuristic
            return self._simple_detect(text)

        try:
            # Use langdetect
            detected = detect(text)

            # Get confidence
            langs = detect_langs(text)
            if langs:
                self.last_confidence = langs[0].prob
            else:
                self.last_confidence = 0.5

            # Normalize language code
            return self._normalize_lang_code(detected)

        except Exception as e:
            print(f"Language detection error: {e}")
            return self._simple_detect(text)

    def _simple_detect(self, text: str) -> str:
        """
        Simple language detection fallback using Unicode ranges

        Args:
            text: Text to detect

        Returns:
            Language code
        """
        # Count characters in different Unicode ranges
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        japanese_chars = sum(1 for c in text if '\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff')
        korean_chars = sum(1 for c in text if '\uac00' <= c <= '\ud7af')
        arabic_chars = sum(1 for c in text if '\u0600' <= c <= '\u06ff')
        cyrillic_chars = sum(1 for c in text if '\u0400' <= c <= '\u04ff')

        total_chars = len(text)

        # Determine language based on character ranges
        if chinese_chars / total_chars > 0.3:
            return 'zh-cn'
        elif japanese_chars / total_chars > 0.2:
            return 'ja'
        elif korean_chars / total_chars > 0.3:
            return 'ko'
        elif arabic_chars / total_chars > 0.3:
            return 'ar'
        elif cyrillic_chars / total_chars > 0.3:
            return 'ru'
        else:
            return 'en'

    def _normalize_lang_code(self, code: str) -> str:
        """
        Normalize language code to standard format

        Args:
            code: Language code from detector

        Returns:
            Normalized code
        """
        # langdetect returns 'zh-cn', we want 'zh-CN' for consistency
        code = code.lower()

        mapping = {
            'zh': 'zh-CN',
            'zh-cn': 'zh-CN',
            'zh-tw': 'zh-TW',
            'ja': 'ja',
            'ko': 'ko',
            'en': 'en',
            'es': 'es',
            'fr': 'fr',
            'de': 'de',
            'ru': 'ru',
            'ar': 'ar',
            'pt': 'pt',
            'it': 'it'
        }

        return mapping.get(code, code)

    def get_confidence(self) -> float:
        """
        Get confidence score of last detection

        Returns:
            Confidence score (0-1)
        """
        return self.last_confidence

    def get_language_name(self, code: str) -> str:
        """
        Get full language name from code

        Args:
            code: Language code

        Returns:
            Full language name
        """
        return self.language_names.get(code.lower(), code.upper())

    def get_supported_languages(self) -> List[Dict[str, str]]:
        """
        Get list of supported languages

        Returns:
            List of {code, name} dictionaries
        """
        # Most commonly used languages for translation
        common_languages = [
            'en', 'zh-cn', 'zh-tw', 'es', 'fr', 'de', 'ja', 'ko',
            'ru', 'ar', 'pt', 'it', 'nl', 'pl', 'tr', 'vi', 'th',
            'id', 'hi', 'sv', 'da', 'fi', 'no', 'cs', 'sk', 'ro',
            'hu', 'el', 'he', 'uk', 'bg', 'hr', 'sr', 'lt', 'lv',
            'et', 'sl', 'ca', 'ms', 'tl'
        ]

        return [
            {
                'code': code,
                'name': self.get_language_name(code)
            }
            for code in common_languages
        ]

    def detect_with_alternatives(self, text: str, n: int = 3) -> List[Dict]:
        """
        Detect language with alternative suggestions

        Args:
            text: Text to detect
            n: Number of alternatives

        Returns:
            List of {language, confidence} dictionaries
        """
        if not LANGDETECT_AVAILABLE:
            return [{'language': self.detect(text), 'confidence': 0.5}]

        try:
            langs = detect_langs(text)
            results = []

            for i, lang in enumerate(langs[:n]):
                results.append({
                    'language': self._normalize_lang_code(lang.lang),
                    'confidence': lang.prob,
                    'name': self.get_language_name(self._normalize_lang_code(lang.lang))
                })

            return results

        except Exception:
            return [{'language': self.detect(text), 'confidence': 0.5}]
