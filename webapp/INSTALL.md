# Installation Guide

## Quick Start (Text Translation Only)

For basic text translation functionality, you only need the core dependencies:

```bash
cd webapp
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install Flask flask-cors deep-translator langdetect python-dotenv
```

Then run:
```bash
python app.py
```

This gives you:
- ✅ Text translation with Google Translate (Free tier)
- ✅ Language auto-detection
- ✅ User authentication
- ✅ DeepL/AI tiers (with API keys)

Document and image translation will show an error message prompting users to install additional dependencies.

## Full Installation (All Features)

For complete functionality including document and image translation:

```bash
pip install -r requirements.txt
```

This adds:
- PDF, Word, Excel, PowerPoint translation
- Image translation with OCR

### System Dependencies

**For PDF support (macOS):**
```bash
brew install poppler
```

**For PDF support (Ubuntu/Debian):**
```bash
sudo apt-get install poppler-utils
```

**For PDF support (Windows):**
Download poppler from: https://github.com/oschwartz10612/poppler-windows/releases/

## Configuration

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys (optional):

```
# For DeepL Pro tier
DEEPL_API_KEY=your-key-here

# For AI Premium tier (choose one)
OPENAI_API_KEY=your-key-here       # ChatGPT
ANTHROPIC_API_KEY=your-key-here    # Claude
GOOGLE_API_KEY=your-key-here       # Gemini

# AI service selection
AI_SERVICE=chatgpt
AI_DEFAULT_MODEL=gpt-4o-mini
```

## Troubleshooting

### Import Errors

If you see warnings about missing packages:
- For text-only: These warnings are OK - document/image features won't work
- For full features: Run `pip install -r requirements.txt`

### Port Already in Use

Edit `app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### SSL Warnings

The urllib3 warning about OpenSSL is safe to ignore - it doesn't affect functionality.

## Running the App

```bash
# Activate virtual environment
source venv/bin/activate

# Run the app
python app.py
```

Access at: http://localhost:5000

## What Works Without Extra Dependencies

| Feature | Status | Requirements |
|---------|--------|--------------|
| Text Translation | ✅ Works | Core only |
| Language Detection | ✅ Works | Core only |
| User Auth | ✅ Works | Core only |
| Google Translate (Free) | ✅ Works | Core only |
| DeepL API (Pro) | ✅ Works | Core + API key |
| AI Translation (Premium) | ✅ Works | Core + API key |
| PDF Translation | ⚠️ Optional | Full install |
| Word Translation | ⚠️ Optional | Full install |
| Excel Translation | ⚠️ Optional | Full install |
| PowerPoint Translation | ⚠️ Optional | Full install |
| Image Translation | ⚠️ Optional | Full install |

The app will show helpful error messages if users try to use features that require additional dependencies.
