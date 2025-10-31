# Universal Translator Web App

A comprehensive web application that combines document and image translation with a 3-tier subscription model.

## Features

### Translation Capabilities
- **Text Translation**: Real-time text translation with auto-detection (similar to DeepL.com)
- **Document Translation**: PDF, Word (.docx), Excel (.xlsx), PowerPoint (.pptx) with format preservation
- **Image Translation**: OCR-based translation for images (screenshots, photos, manga, etc.)

### Subscription Tiers

#### 1. Free Tier
- **Translation Engine**: Google Translate (via deep-translator)
- **Limits**:
  - 500,000 characters/month
  - 3 documents/month
  - 10 images/month
  - 10MB max file size
- **Price**: $0/month

#### 2. DeepL Pro Tier
- **Translation Engine**: DeepL API
- **Limits**:
  - 5,000,000 characters/month
  - 50 documents/month
  - 100 images/month
  - 50MB max file size
- **Price**: $9.99/month
- **Benefits**: Higher quality translations, priority processing

#### 3. AI Premium Tier
- **Translation Engine**: AI-powered (ChatGPT, Claude, or Gemini)
- **Limits**: Unlimited everything
- **Features**:
  - Context-aware translation
  - Best translation quality
  - 100MB max file size
  - Batch processing
  - API access
  - Priority support
- **Price**: $29.99/month

## Installation

### Prerequisites

1. **Python 3.9+** installed
2. **System dependencies** (for image translation):
   ```bash
   # macOS
   brew install poppler

   # Ubuntu/Debian
   sudo apt-get install poppler-utils

   # Windows
   # Download poppler from: https://github.com/oschwartz10612/poppler-windows/releases/
   ```

### Setup Steps

1. **Clone the repository**:
   ```bash
   cd /home/user/translator/webapp
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the webapp directory:
   ```bash
   # Flask Configuration
   SECRET_KEY=your-secret-key-here

   # DeepL API (for DeepL Pro tier)
   DEEPL_API_KEY=your-deepl-api-key

   # AI Services (for AI Premium tier)
   OPENAI_API_KEY=your-openai-api-key
   ANTHROPIC_API_KEY=your-anthropic-api-key
   GOOGLE_API_KEY=your-google-api-key

   # AI Service Selection (chatgpt, claude, or gemini)
   AI_SERVICE=chatgpt
   AI_DEFAULT_MODEL=gpt-4o-mini
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Access the web app**:
   Open your browser and navigate to: `http://localhost:5000`

## API Keys Setup

### DeepL API
1. Sign up at [DeepL API](https://www.deepl.com/pro-api)
2. Get your API key from the account settings
3. Add to `.env` file: `DEEPL_API_KEY=your-key`

### OpenAI (ChatGPT)
1. Sign up at [OpenAI Platform](https://platform.openai.com/)
2. Create an API key in the API keys section
3. Add to `.env` file: `OPENAI_API_KEY=your-key`

### Anthropic (Claude)
1. Sign up at [Anthropic Console](https://console.anthropic.com/)
2. Generate an API key
3. Add to `.env` file: `ANTHROPIC_API_KEY=your-key`

### Google (Gemini)
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env` file: `GOOGLE_API_KEY=your-key`

## Usage

### Text Translation
1. Select source and target languages
2. Type or paste text in the left panel
3. Click "Translate" button
4. Copy translated text from the right panel

### Document Translation
1. Click "Document Translation" tab
2. Select source and target languages
3. Drag & drop or click to upload document
4. Click "Translate Document"
5. Download translated document when ready

### Image Translation
1. Click "Image Translation" tab
2. Select source and target languages
3. Upload image with text
4. Click "Translate Image"
5. View comparison and download result

## User Management

### Registration
- Navigate to `/register`
- Create an account (starts with Free tier)

### Login
- Navigate to `/login`
- Sign in with email and password

### Subscription Management
- Navigate to `/subscription`
- View usage statistics
- Upgrade or downgrade tier

## Project Structure

```
webapp/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .env                        # Environment variables (create this)
├── models/                     # Data models
│   ├── user.py                # User model and tiers
│   └── database.py            # Database management
├── services/                   # Business logic
│   ├── translation_manager.py # Translation service manager
│   └── language_detector.py   # Language detection
├── templates/                  # HTML templates
│   ├── index.html             # Main page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   └── subscription.html      # Subscription management
├── static/                     # Static files
│   ├── css/
│   │   └── style.css          # Styles
│   ├── js/
│   │   └── app.js             # Frontend JavaScript
│   └── uploads/               # Uploaded files (auto-created)
└── data/                       # Database files (auto-created)
    └── users.json             # User database
```

## API Endpoints

### Translation APIs
- `POST /api/translate-text` - Translate text
- `POST /api/translate-document` - Translate document
- `POST /api/translate-image` - Translate image
- `POST /api/detect-language` - Detect language
- `GET /api/languages` - Get supported languages

### User Management APIs
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout
- `POST /api/upgrade-subscription` - Upgrade subscription
- `GET /api/usage-stats` - Get user usage statistics

### File Management
- `GET /download/<filename>` - Download translated file

## Development

### Run in Development Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

### Testing
```bash
pytest tests/
```

### Code Formatting
```bash
black .
flake8 .
```

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Environment Variables for Production
```bash
SECRET_KEY=<strong-random-key>
FLASK_ENV=production
DEEPL_API_KEY=<your-key>
OPENAI_API_KEY=<your-key>
```

## Supported Languages

### Text Translation
- English, Chinese (Simplified/Traditional), Spanish, French, German
- Japanese, Korean, Russian, Arabic, Portuguese, Italian
- Dutch, Polish, Turkish, Vietnamese, Thai, Indonesian, Hindi
- And 20+ more languages

### Document Translation
- All text translation languages
- Preserves formatting for PDF, Word, Excel, PowerPoint

### Image Translation
- English, Chinese (Simplified/Traditional)
- Japanese, Korean
- More languages coming soon

## Troubleshooting

### Issue: Import errors
**Solution**: Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Image translation not working
**Solution**: Install system dependencies (poppler) and check if PaddleOCR is installed correctly.

### Issue: API key errors
**Solution**: Check that API keys are correctly set in `.env` file and that they are valid.

### Issue: File upload fails
**Solution**: Check file size limits and ensure the `static/uploads` directory exists and is writable.

## License

MIT License - see LICENSE file for details

## Credits

Built with:
- Flask - Web framework
- PaddleOCR - OCR engine
- OpenCV - Image processing
- DeepL/OpenAI/Anthropic - Translation APIs
- deep-translator - Free translation
- PyMuPDF, python-docx, openpyxl, python-pptx - Document processing

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API documentation
3. Contact support@universaltranslator.com

## Roadmap

- [ ] Add batch document translation
- [ ] Support for more document formats
- [ ] Real-time collaborative translation
- [ ] Mobile app (iOS/Android)
- [ ] Translation memory
- [ ] Glossary management
- [ ] API access for developers
- [ ] Webhook integrations
