# Quick Start Guide - Universal Translator

This guide will get you up and running in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- pip package manager

## Installation

### 1. Run the setup script

```bash
cd /home/user/translator/webapp
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Create necessary directories
- Copy .env.example to .env

### 2. Configure API Keys (Optional)

Edit the `.env` file and add your API keys:

```bash
nano .env
```

**For Free Tier**: No API keys needed! Google Translate works out of the box.

**For DeepL Tier** (optional):
```
DEEPL_API_KEY=your-deepl-api-key
```
Get it at: https://www.deepl.com/pro-api

**For AI Premium Tier** (optional):
```
OPENAI_API_KEY=your-openai-key
# OR
ANTHROPIC_API_KEY=your-anthropic-key
# OR
GOOGLE_API_KEY=your-google-key
```

### 3. Run the application

```bash
./run.sh
```

Or manually:
```bash
source venv/bin/activate
python app.py
```

### 4. Access the web app

Open your browser and go to:
```
http://localhost:5000
```

## Quick Test

1. **Text Translation**:
   - Leave the default tab (Text Translation)
   - Type "Hello world" in the left panel
   - Click "Translate"
   - See the translation in the right panel

2. **Document Translation**:
   - Click "Document Translation" tab
   - Upload a PDF, Word, Excel, or PowerPoint file
   - Click "Translate Document"
   - Download the translated file

3. **Image Translation**:
   - Click "Image Translation" tab
   - Upload an image with text
   - Click "Translate Image"
   - Compare original and translated images

## User Accounts

### Register a New Account

1. Click "Sign Up" in the header
2. Fill in your details
3. You'll start with a **Free** tier account

### Available Tiers

| Tier | Price | Translation Engine | Limits |
|------|-------|-------------------|---------|
| **Free** | $0/month | Google Translate | 500K chars, 3 docs, 10 images/month |
| **DeepL Pro** | $9.99/month | DeepL API | 5M chars, 50 docs, 100 images/month |
| **AI Premium** | $29.99/month | ChatGPT/Claude | Unlimited |

### Upgrade Subscription

1. Log in to your account
2. Click "Upgrade" or go to `/subscription`
3. Select your desired tier
4. Confirm the change

## Supported Formats

### Documents
- PDF (.pdf)
- Microsoft Word (.docx)
- Microsoft Excel (.xlsx)
- Microsoft PowerPoint (.pptx)

### Images
- PNG, JPG, JPEG, GIF, BMP, WEBP
- Any image containing text

### Languages
Over 40 languages including:
- English, Chinese (Simplified/Traditional)
- Spanish, French, German
- Japanese, Korean, Russian
- Arabic, Portuguese, Italian
- And many more!

## Troubleshooting

### Port already in use
If port 5000 is already in use, edit `app.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Import errors
Make sure you activated the virtual environment:
```bash
source venv/bin/activate
```

Then reinstall dependencies:
```bash
pip install -r requirements.txt
```

### Image translation not working
Install system dependencies:

**macOS**:
```bash
brew install poppler
```

**Ubuntu/Debian**:
```bash
sudo apt-get install poppler-utils
```

### Translation quality issues
- **Free tier**: Uses Google Translate (basic quality)
- **DeepL tier**: Much better quality, especially for European languages
- **AI Premium tier**: Best quality with context awareness

## Features Demo

### Auto Language Detection
Just select "Detect Language" as source and start typing. The app will automatically detect the source language.

### Language Swap
Click the swap button (⇄) to quickly switch source and target languages.

### Copy Translation
Click the "Copy" button to copy the translated text to clipboard.

### Format Preservation
Documents are translated while preserving:
- Original formatting and styles
- Tables and charts
- Headers and footers
- Images and graphics

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [API documentation](README.md#api-endpoints) for programmatic access
- Explore batch translation features
- Set up production deployment

## Support

For issues or questions:
- Check the [Troubleshooting section](README.md#troubleshooting) in README
- Review the full documentation
- Check GitHub issues (if applicable)

## Development Mode

To run in development mode with auto-reload:

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

Changes to Python files will automatically reload the server.

---

**Enjoy translating! 🌍**
