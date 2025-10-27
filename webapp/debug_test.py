#!/usr/bin/env python3
"""
Debug script to test all endpoints and show detailed errors
"""

import sys
import os

# Test imports
print("Testing imports...")
errors = []

try:
    from flask import Flask
    print("✅ Flask imported")
except ImportError as e:
    print(f"❌ Flask import failed: {e}")
    errors.append("Flask")

try:
    from flask_cors import CORS
    print("✅ flask-cors imported")
except ImportError as e:
    print(f"❌ flask-cors import failed: {e}")
    errors.append("flask-cors")

try:
    from deep_translator import GoogleTranslator
    print("✅ deep-translator imported")
except ImportError as e:
    print(f"❌ deep-translator import failed: {e}")
    errors.append("deep-translator")

try:
    from langdetect import detect
    print("✅ langdetect imported")
except ImportError as e:
    print(f"❌ langdetect import failed: {e}")
    errors.append("langdetect")

try:
    from core.translation_services import GoogleTranslateService
    print("✅ core.translation_services imported")
except ImportError as e:
    print(f"❌ core.translation_services import failed: {e}")
    errors.append("core.translation_services")

try:
    from services.translation_manager import TranslationManager
    print("✅ services.translation_manager imported")
except ImportError as e:
    print(f"❌ services.translation_manager import failed: {e}")
    errors.append("services.translation_manager")

try:
    from services.language_detector import LanguageDetector
    print("✅ services.language_detector imported")
except ImportError as e:
    print(f"❌ services.language_detector import failed: {e}")
    errors.append("services.language_detector")

try:
    from models.user import User, UserTier
    print("✅ models.user imported")
except ImportError as e:
    print(f"❌ models.user import failed: {e}")
    errors.append("models.user")

try:
    from models.database import Database
    print("✅ models.database imported")
except ImportError as e:
    print(f"❌ models.database import failed: {e}")
    errors.append("models.database")

print("\n" + "="*60)

if errors:
    print(f"❌ {len(errors)} import errors found!")
    print("\nInstall missing packages:")
    print("pip install Flask flask-cors deep-translator langdetect python-dotenv werkzeug")
    sys.exit(1)
else:
    print("✅ All imports successful!")

print("\nTesting services...")

# Test translation
try:
    translator = GoogleTranslator(source='en', target='zh-CN')
    result = translator.translate("Hello")
    print(f"✅ Translation works: 'Hello' -> '{result}'")
except Exception as e:
    print(f"❌ Translation failed: {e}")

# Test language detection
try:
    lang = detect("Hello world")
    print(f"✅ Language detection works: detected '{lang}'")
except Exception as e:
    print(f"❌ Language detection failed: {e}")

# Test database
try:
    db = Database()
    print("✅ Database initialized")
except Exception as e:
    print(f"❌ Database failed: {e}")

# Test TranslationManager
try:
    from models.user import UserTier
    tm = TranslationManager()
    result = tm.translate_text("Hello", "en", "zh-CN", UserTier.FREE)
    print(f"✅ TranslationManager works: 'Hello' -> '{result}'")
except Exception as e:
    print(f"❌ TranslationManager failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("\nIf all tests pass, the app should work.")
print("If any fail, check the error messages above.")
