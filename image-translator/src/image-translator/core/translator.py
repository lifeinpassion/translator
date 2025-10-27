"""
Translation engine supporting multiple backends.
"""

import logging
from typing import Dict, List, Optional
from deep_translator import GoogleTranslator, DeeplTranslator
from functools import lru_cache

logger = logging.getLogger(__name__)


class TranslationEngine:
    """Multi-backend translation engine with caching."""
    
    def __init__(self, config: Dict):
        """
        Initialize translation engine.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.engine_name = config.get('engine', 'google')
        self.source_lang = config.get('source_lang', 'auto')
        self.target_lang = config.get('target_lang', 'zh-CN')
        self.use_cache = config.get('cache_translations', True)
        
        self.translator = self._initialize_translator()
        
    def _initialize_translator(self):
        """Initialize the appropriate translation backend."""
        try:
            if self.engine_name == 'google':
                logger.info("Initializing Google Translator")
                return GoogleTranslator(source=self.source_lang, target=self.target_lang)
                
            elif self.engine_name == 'deepl':
                logger.info("Initializing DeepL Translator")
                api_key = self.config.get('deepl_api_key')
                if not api_key:
                    raise ValueError("DeepL API key required in config")
                return DeeplTranslator(
                    api_key=api_key,
                    source=self.source_lang,
                    target=self.target_lang
                )
                
            else:
                raise ValueError(f"Unsupported translation engine: {self.engine_name}")
                
        except Exception as e:
            logger.error(f"Failed to initialize translator: {e}")
            raise
    
    @lru_cache(maxsize=1000)
    def _cached_translate(self, text: str) -> str:
        """Cached translation for efficiency."""
        return self.translator.translate(text)
    
    def translate(self, text: str) -> str:
        """
        Translate text.
        
        Args:
            text: Source text to translate
            
        Returns:
            Translated text
        """
        if not text or not text.strip():
            return text
            
        try:
            if self.use_cache:
                translated = self._cached_translate(text)
            else:
                translated = self.translator.translate(text)
                
            logger.debug(f"Translated: '{text}' → '{translated}'")
            return translated
            
        except Exception as e:
            logger.error(f"Translation failed for '{text}': {e}")
            return text  # Return original on failure
    
    def translate_batch(self, texts: List[str]) -> List[str]:
        """
        Translate multiple texts efficiently.
        
        Args:
            texts: List of texts to translate
            
        Returns:
            List of translated texts
        """
        return [self.translate(text) for text in texts]
    
    def switch_direction(self):
        """Switch translation direction (e.g., EN→ZH to ZH→EN)."""
        self.source_lang, self.target_lang = self.target_lang, self.source_lang
        self.translator = self._initialize_translator()
        logger.info(f"Switched direction: {self.source_lang} → {self.target_lang}")