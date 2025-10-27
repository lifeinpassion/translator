"""
AI Translation Services Extension
Adds support for ChatGPT, Claude, Gemini, and other AI translators
to the document translation system
"""

import os
import json
from typing import Optional, List
from functools import lru_cache
import time

# OpenAI (ChatGPT)
try:
    import openai
    from openai import OpenAI
except ImportError:
    openai = None
    print("Warning: openai not installed. ChatGPT support disabled.")

# Anthropic (Claude)
try:
    import anthropic
    from anthropic import Anthropic
except ImportError:
    anthropic = None
    print("Warning: anthropic not installed. Claude support disabled.")

# Google Gemini
try:
    import google.generativeai as genai
except ImportError:
    genai = None
    print("Warning: google-generativeai not installed. Gemini support disabled.")

# For retry logic
try:
    from tenacity import retry, stop_after_attempt, wait_exponential
except ImportError:
    retry = lambda *args, **kwargs: lambda func: func


class AITranslationService:
    """Base class for AI-powered translation services"""
    
    def __init__(self, source_lang='en', target_lang='zh-CN', api_key=None, model=None):
        self.source_lang = self._format_language(source_lang)
        self.target_lang = self._format_language(target_lang)
        self.api_key = api_key
        self.model = model
        self.cache = {}
        
    def _format_language(self, lang_code):
        """Convert language codes to human-readable format for AI prompts"""
        lang_map = {
            'en': 'English',
            'zh-CN': 'Simplified Chinese',
            'zh-TW': 'Traditional Chinese',
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
            'hi': 'Hindi'
        }
        return lang_map.get(lang_code, lang_code)
    
    @lru_cache(maxsize=10000)
    def translate_cached(self, text: str) -> str:
        """Translate with caching to reduce API calls and costs"""
        if not text or not text.strip():
            return text
        return self.translate(text)
    
    def translate(self, text: str) -> str:
        """Override in subclasses"""
        raise NotImplementedError
    
    def translate_batch(self, texts: List[str]) -> List[str]:
        """Translate multiple texts in one API call for efficiency"""
        # Default implementation - override for better efficiency
        return [self.translate_cached(text) for text in texts]


class ChatGPTTranslationService(AITranslationService):
    """OpenAI ChatGPT translation service"""
    
    def __init__(self, source_lang='en', target_lang='zh-CN', api_key=None, model='gpt-4o-mini'):
        super().__init__(source_lang, target_lang, api_key, model)
        
        if not openai:
            raise ImportError("Please install openai: pip install openai")
        
        if not api_key:
            # Try to get from environment
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable or pass api_key parameter")
        
        self.client = OpenAI(api_key=api_key)
        self.model = model or 'gpt-4o-mini'  # Default to mini for cost efficiency
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def translate(self, text: str) -> str:
        if not text or not text.strip():
            return text
        
        try:
            # Create translation prompt
            system_prompt = f"""You are a professional translator. Translate the following text from {self.source_lang} to {self.target_lang}.
Maintain the original formatting, tone, and style. Only return the translated text without any explanations or additions."""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,  # Lower temperature for more consistent translations
                max_tokens=len(text) * 3  # Allow for text expansion
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"ChatGPT translation error: {e}")
            return text
    
    def translate_batch(self, texts: List[str]) -> List[str]:
        """Batch translation for efficiency"""
        if not texts:
            return []
        
        # Create batch prompt
        batch_text = "\n---SEPARATOR---\n".join(texts)
        system_prompt = f"""You are a professional translator. Translate each text segment from {self.source_lang} to {self.target_lang}.
The segments are separated by ---SEPARATOR---.
Maintain the original formatting and return translations in the same order, separated by ---SEPARATOR---."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": batch_text}
                ],
                temperature=0.3
            )
            
            translated = response.choices[0].message.content.strip()
            return translated.split("---SEPARATOR---")
            
        except Exception as e:
            print(f"Batch translation error: {e}")
            # Fall back to individual translations
            return [self.translate(text) for text in texts]


class ClaudeTranslationService(AITranslationService):
    """Anthropic Claude translation service"""
    
    def __init__(self, source_lang='en', target_lang='zh-CN', api_key=None, model='claude-3-5-haiku-20241022'):
        super().__init__(source_lang, target_lang, api_key, model)
        
        if not anthropic:
            raise ImportError("Please install anthropic: pip install anthropic")
        
        if not api_key:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                raise ValueError("Anthropic API key required. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter")
        
        self.client = Anthropic(api_key=api_key)
        self.model = model or 'claude-3-5-haiku-20241022'  # Haiku is most cost-effective
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def translate(self, text: str) -> str:
        if not text or not text.strip():
            return text
        
        try:
            prompt = f"""Translate the following text from {self.source_lang} to {self.target_lang}.
Maintain the original formatting, tone, and style. Only return the translated text.

Text to translate:
{text}"""
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=len(text) * 3,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text.strip()
            
        except Exception as e:
            print(f"Claude translation error: {e}")
            return text


class GeminiTranslationService(AITranslationService):
    """Google Gemini translation service"""
    
    def __init__(self, source_lang='en', target_lang='zh-CN', api_key=None, model='gemini-1.5-flash'):
        super().__init__(source_lang, target_lang, api_key, model)
        
        if not genai:
            raise ImportError("Please install google-generativeai: pip install google-generativeai")
        
        if not api_key:
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError("Google API key required. Set GOOGLE_API_KEY environment variable or pass api_key parameter")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model or 'gemini-1.5-flash')  # Flash is cost-effective
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def translate(self, text: str) -> str:
        if not text or not text.strip():
            return text
        
        try:
            prompt = f"""Translate the following text from {self.source_lang} to {self.target_lang}.
Maintain the original formatting, tone, and style. Only return the translated text without any explanations.

Text: {text}"""
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=len(text) * 3,
                )
            )
            
            return response.text.strip()
            
        except Exception as e:
            print(f"Gemini translation error: {e}")
            return text


class OllamaTranslationService(AITranslationService):
    """Local Ollama translation service (for privacy-conscious users)"""
    
    def __init__(self, source_lang='en', target_lang='zh-CN', model='llama3.2', base_url='http://localhost:11434'):
        super().__init__(source_lang, target_lang, None, model)
        self.base_url = base_url
        self.model = model
        
        try:
            import requests
            self.requests = requests
        except ImportError:
            raise ImportError("Please install requests: pip install requests")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def translate(self, text: str) -> str:
        if not text or not text.strip():
            return text
        
        try:
            prompt = f"""Translate from {self.source_lang} to {self.target_lang}. Only return the translation:

{text}"""
            
            response = self.requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3
                }
            )
            
            if response.status_code == 200:
                return response.json()['response'].strip()
            else:
                print(f"Ollama error: {response.status_code}")
                return text
                
        except Exception as e:
            print(f"Ollama translation error: {e}")
            return text


class HybridTranslationService(AITranslationService):
    """
    Hybrid service that uses traditional translation for simple text
    and AI for complex/contextual translation
    """
    
    def __init__(self, 
                 source_lang='en', 
                 target_lang='zh-CN',
                 simple_service=None,  # GoogleTranslator instance
                 complex_service=None,  # AI service instance
                 complexity_threshold=50):  # Character count threshold
        super().__init__(source_lang, target_lang)
        self.simple_service = simple_service
        self.complex_service = complex_service
        self.complexity_threshold = complexity_threshold
    
    def translate(self, text: str) -> str:
        if not text or not text.strip():
            return text
        
        # Use simple service for short text, AI for longer/complex text
        if len(text) < self.complexity_threshold:
            return self.simple_service.translate_cached(text)
        else:
            return self.complex_service.translate_cached(text)


# Updated DocumentTranslator class to support AI services
def create_ai_document_translator(
    source_lang: str = 'en',
    target_lang: str = 'zh-CN',
    translation_service: str = 'chatgpt',
    api_key: Optional[str] = None,
    model: Optional[str] = None
):
    """
    Factory function to create DocumentTranslator with AI translation services
    
    Args:
        source_lang: Source language code
        target_lang: Target language code
        translation_service: 'chatgpt', 'claude', 'gemini', 'ollama', or 'hybrid'
        api_key: API key for the service
        model: Specific model to use (optional)
    
    Returns:
        DocumentTranslator instance configured with AI translation
    """
    
    # Import the original DocumentTranslator
    from document_translator import DocumentTranslator
    
    # Create the appropriate AI translation service
    if translation_service == 'chatgpt':
        service = ChatGPTTranslationService(source_lang, target_lang, api_key, model)
    elif translation_service == 'claude':
        service = ClaudeTranslationService(source_lang, target_lang, api_key, model)
    elif translation_service == 'gemini':
        service = GeminiTranslationService(source_lang, target_lang, api_key, model)
    elif translation_service == 'ollama':
        service = OllamaTranslationService(source_lang, target_lang, model=model or 'llama3.2')
    elif translation_service == 'hybrid':
        # Use Google Translate for simple text, ChatGPT for complex
        from deep_translator import GoogleTranslator
        simple = GoogleTranslator(source=source_lang, target=target_lang)
        complex = ChatGPTTranslationService(source_lang, target_lang, api_key, model)
        service = HybridTranslationService(source_lang, target_lang, simple, complex)
    else:
        raise ValueError(f"Unknown translation service: {translation_service}")
    
    # Create a custom DocumentTranslator that uses our AI service
    translator = DocumentTranslator.__new__(DocumentTranslator)
    translator.translation_service = service
    
    # Initialize the format-specific translators
    import pymupdf
    from openpyxl import load_workbook
    from docx import Document
    from pptx import Presentation
    
    from document_translator import PDFTranslator, ExcelTranslator, WordTranslator, PowerPointTranslator
    
    translator.pdf_translator = PDFTranslator(service) if pymupdf else None
    translator.excel_translator = ExcelTranslator(service) if load_workbook else None
    translator.word_translator = WordTranslator(service) if Document else None
    translator.ppt_translator = PowerPointTranslator(service) if Presentation else None
    
    # Copy the methods we need
    translator.translate_document = DocumentTranslator.translate_document.__get__(translator, DocumentTranslator)
    translator.translate_batch = DocumentTranslator.translate_batch.__get__(translator, DocumentTranslator)
    translator._print_summary = DocumentTranslator._print_summary.__get__(translator, DocumentTranslator)
    
    return translator


# Example usage functions
def example_chatgpt():
    """Example using ChatGPT for translation"""
    translator = create_ai_document_translator(
        source_lang='en',
        target_lang='zh-CN',
        translation_service='chatgpt',
        api_key='your-openai-api-key',  # or set OPENAI_API_KEY env var
        model='gpt-4o-mini'  # or 'gpt-4o' for best quality
    )
    
    # Translate a document
    translator.translate_document('document.pdf', 'document_translated.pdf')
    
    return translator


def example_claude():
    """Example using Claude for translation"""
    translator = create_ai_document_translator(
        source_lang='en',
        target_lang='fr',
        translation_service='claude',
        api_key='your-anthropic-api-key',  # or set ANTHROPIC_API_KEY env var
        model='claude-3-5-haiku-20241022'  # or 'claude-3-5-sonnet-20241022' for best
    )
    
    translator.translate_document('report.docx', 'report_fr.docx')
    
    return translator


def example_gemini():
    """Example using Gemini for translation"""
    translator = create_ai_document_translator(
        source_lang='en',
        target_lang='es',
        translation_service='gemini',
        api_key='your-google-api-key',  # or set GOOGLE_API_KEY env var
        model='gemini-1.5-flash'  # or 'gemini-1.5-pro' for best quality
    )
    
    translator.translate_document('data.xlsx', 'data_es.xlsx')
    
    return translator


def example_ollama_local():
    """Example using local Ollama (no API key needed)"""
    translator = create_ai_document_translator(
        source_lang='en',
        target_lang='de',
        translation_service='ollama',
        model='llama3.2'  # Make sure this model is pulled in Ollama
    )
    
    translator.translate_document('presentation.pptx', 'presentation_de.pptx')
    
    return translator


def example_hybrid():
    """Example using hybrid approach for cost optimization"""
    translator = create_ai_document_translator(
        source_lang='en',
        target_lang='ja',
        translation_service='hybrid',
        api_key='your-openai-api-key',  # For complex translations
        model='gpt-4o-mini'
    )
    
    # This will use Google Translate for short text and ChatGPT for longer paragraphs
    translator.translate_document('mixed_document.pdf')
    
    return translator


# Comparison function for testing different services
def compare_translation_services(text: str, source='en', target='zh-CN'):
    """Compare translation quality across different AI services"""
    
    services = []
    
    # Add available services
    if os.getenv('OPENAI_API_KEY'):
        services.append(('ChatGPT', ChatGPTTranslationService(source, target)))
    
    if os.getenv('ANTHROPIC_API_KEY'):
        services.append(('Claude', ClaudeTranslationService(source, target)))
    
    if os.getenv('GOOGLE_API_KEY'):
        services.append(('Gemini', GeminiTranslationService(source, target)))
    
    # Always add Google Translate for comparison
    from deep_translator import GoogleTranslator
    google = type('GoogleService', (), {
        'translate_cached': lambda self, t: GoogleTranslator(source=source, target=target).translate(t)
    })()
    services.append(('Google Translate', google))
    
    print(f"Original text ({source}):\n{text}\n")
    print("=" * 60)
    
    for name, service in services:
        try:
            start_time = time.time()
            translated = service.translate_cached(text)
            elapsed = time.time() - start_time
            
            print(f"\n{name} (took {elapsed:.2f}s):")
            print(translated)
            print("-" * 40)
        except Exception as e:
            print(f"\n{name}: Error - {e}")
            print("-" * 40)


if __name__ == "__main__":
    # Quick test
    print("AI Translation Services Extension loaded successfully!")
    print("\nAvailable services:")
    print("- ChatGPT (OpenAI)")
    print("- Claude (Anthropic)")  
    print("- Gemini (Google)")
    print("- Ollama (Local)")
    print("- Hybrid (Google + AI)")
    
    # Test translation if API keys are available
    test_text = "The quick brown fox jumps over the lazy dog."
    print(f"\nTesting with: '{test_text}'")
    
    compare_translation_services(test_text)