"""
Universal Translator Web Application
Combines document and image translation with 3-tier subscription model
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session, send_file, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime, timedelta
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.translation_manager import TranslationManager
from services.language_detector import LanguageDetector
from models.user import User, UserTier
from models.database import Database

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['UPLOAD_FOLDER'] = Path(__file__).parent / 'static' / 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['ALLOWED_EXTENSIONS'] = {
    'documents': {'pdf', 'docx', 'xlsx', 'pptx', 'doc', 'xls', 'ppt'},
    'images': {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
}

CORS(app)

# Initialize services
translation_manager = TranslationManager()
language_detector = LanguageDetector()
db = Database()

# Ensure upload folder exists
app.config['UPLOAD_FOLDER'].mkdir(parents=True, exist_ok=True)


def allowed_file(filename, file_type='documents'):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS'][file_type]


def get_current_user():
    """Get current user from session"""
    user_id = session.get('user_id')
    if user_id:
        return db.get_user(user_id)
    return None


def get_user_tier():
    """Get current user's subscription tier"""
    user = get_current_user()
    if user:
        return user.tier
    return UserTier.FREE


@app.route('/')
def index():
    """Main page"""
    user = get_current_user()
    return render_template('index.html', user=user)


@app.route('/api/detect-language', methods=['POST'])
def detect_language():
    """Detect language of input text"""
    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text.strip():
            return jsonify({'error': 'No text provided'}), 400

        detected_lang = language_detector.detect(text)
        confidence = language_detector.get_confidence()

        return jsonify({
            'language': detected_lang,
            'confidence': confidence,
            'language_name': language_detector.get_language_name(detected_lang)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/translate-text', methods=['POST'])
def translate_text():
    """Translate text (like DeepL.com)"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        source_lang = data.get('source_lang', 'auto')
        target_lang = data.get('target_lang', 'en')

        if not text.strip():
            return jsonify({'error': 'No text provided'}), 400

        # Get user tier
        user_tier = get_user_tier()

        # Auto-detect language if needed
        if source_lang == 'auto':
            source_lang = language_detector.detect(text)

        # Translate using appropriate tier
        translated_text = translation_manager.translate_text(
            text=text,
            source_lang=source_lang,
            target_lang=target_lang,
            tier=user_tier
        )

        return jsonify({
            'translated_text': translated_text,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'tier_used': user_tier.value
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/translate-document', methods=['POST'])
def translate_document():
    """Translate document (PDF, Word, Excel, PowerPoint)"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename, 'documents'):
            return jsonify({'error': 'Invalid file type'}), 400

        # Get parameters
        source_lang = request.form.get('source_lang', 'auto')
        target_lang = request.form.get('target_lang', 'en')

        # Get user tier
        user_tier = get_user_tier()

        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        input_path = app.config['UPLOAD_FOLDER'] / unique_filename
        file.save(input_path)

        # Translate document
        output_path = translation_manager.translate_document(
            input_path=str(input_path),
            source_lang=source_lang,
            target_lang=target_lang,
            tier=user_tier
        )

        # Return download link
        return jsonify({
            'success': True,
            'download_url': url_for('download_file', filename=Path(output_path).name),
            'original_filename': filename,
            'tier_used': user_tier.value
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/translate-image', methods=['POST'])
def translate_image():
    """Translate image with OCR"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename, 'images'):
            return jsonify({'error': 'Invalid file type'}), 400

        # Get parameters
        source_lang = request.form.get('source_lang', 'auto')
        target_lang = request.form.get('target_lang', 'en')

        # Get user tier
        user_tier = get_user_tier()

        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        input_path = app.config['UPLOAD_FOLDER'] / unique_filename
        file.save(input_path)

        # Translate image
        output_path = translation_manager.translate_image(
            input_path=str(input_path),
            source_lang=source_lang,
            target_lang=target_lang,
            tier=user_tier
        )

        # Return download link
        return jsonify({
            'success': True,
            'download_url': url_for('download_file', filename=Path(output_path).name),
            'preview_url': url_for('static', filename=f'uploads/{Path(output_path).name}'),
            'original_filename': filename,
            'tier_used': user_tier.value
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download_file(filename):
    """Download translated file"""
    try:
        file_path = app.config['UPLOAD_FOLDER'] / secure_filename(filename)
        if file_path.exists():
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/languages')
def get_languages():
    """Get supported languages"""
    return jsonify({
        'languages': language_detector.get_supported_languages(),
        'popular': ['en', 'zh-CN', 'es', 'fr', 'de', 'ja', 'ko', 'pt', 'ru', 'ar']
    })


# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'GET':
        return render_template('login.html')

    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = db.get_user_by_email(email)

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return jsonify({'success': True, 'tier': user.tier.value})
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'GET':
        return render_template('register.html')

    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name', '')

        # Check if user exists
        if db.get_user_by_email(email):
            return jsonify({'error': 'Email already registered'}), 400

        # Create new user
        user = User(
            email=email,
            name=name,
            password_hash=generate_password_hash(password),
            tier=UserTier.FREE
        )

        db.create_user(user)
        session['user_id'] = user.id

        return jsonify({'success': True, 'tier': user.tier.value})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('index'))


@app.route('/subscription')
def subscription():
    """Subscription management page"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    return render_template('subscription.html', user=user)


@app.route('/api/upgrade-subscription', methods=['POST'])
def upgrade_subscription():
    """Upgrade user subscription"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Not authenticated'}), 401

        data = request.get_json()
        new_tier = data.get('tier')

        if new_tier not in ['free', 'deepl', 'ai']:
            return jsonify({'error': 'Invalid tier'}), 400

        # Update user tier
        tier_map = {
            'free': UserTier.FREE,
            'deepl': UserTier.DEEPL,
            'ai': UserTier.AI
        }

        user.tier = tier_map[new_tier]
        db.update_user(user)

        return jsonify({'success': True, 'tier': user.tier.value})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/usage-stats')
def usage_stats():
    """Get user usage statistics"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Not authenticated'}), 401

        stats = db.get_user_stats(user.id)

        return jsonify(stats)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500


if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=5000)
