# Troubleshooting Guide

## 🔴 500 Internal Server Errors

You're seeing multiple 500 errors. Here's how to fix them:

### Step 1: Run the Debug Test

```bash
cd webapp
python debug_test.py
```

This will show you exactly what's failing.

### Step 2: Install Core Dependencies

If you see import errors, install the minimal requirements:

```bash
pip install -r requirements-minimal.txt
```

Or manually:

```bash
pip install Flask flask-cors deep-translator langdetect python-dotenv Werkzeug
```

### Step 3: Check Python Version

```bash
python --version
```

You need **Python 3.9 or higher**.

If you have Python 3.8 or lower, some packages might fail.

---

## 🐛 Common Errors and Fixes

### Error: "No module named 'core'"

**Problem:** Python can't find the `core` module.

**Fix:**
```bash
# Make sure you're in the webapp directory
cd webapp

# Check if core/__init__.py exists
ls core/__init__.py

# If not, create it
mkdir -p core
touch core/__init__.py
```

### Error: "No module named 'deep_translator'"

**Fix:**
```bash
pip install deep-translator
```

### Error: "No module named 'langdetect'"

**Fix:**
```bash
pip install langdetect
```

### Error: Translation returns empty or fails

**Problem:** Network issue or API rate limiting.

**Fix:** Google Translate (free) sometimes rate limits. Wait a few seconds and try again.

---

## 🔍 Getting Detailed Error Messages

### Method 1: Run with Debug Output

Edit `app.py` and make sure debug is on:

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

Then run:
```bash
python app.py
```

Now when you get a 500 error, you'll see the full traceback in the terminal.

### Method 2: Check Flask Logs

Look at your terminal where you ran `python app.py`. The errors will be printed there.

### Method 3: Add Print Debugging

Temporarily add print statements in `app.py`:

```python
@app.route('/api/translate-text', methods=['POST'])
def translate_text():
    try:
        print("=== TRANSLATE TEXT CALLED ===")
        data = request.get_json()
        print(f"Data received: {data}")

        text = data.get('text', '')
        print(f"Text to translate: {text}")

        # ... rest of code
```

---

## 🔐 Registration/Login Errors (500)

### Common Issues:

#### 1. Database Directory Doesn't Exist

**Fix:**
```bash
cd webapp
mkdir -p data
```

#### 2. Permission Issues

**Fix:**
```bash
chmod 755 data
```

#### 3. JSON Database Corruption

**Fix:**
```bash
# Backup existing database
cp data/users.json data/users.json.backup

# Reset database
echo '{"users": {}, "usage_logs": []}' > data/users.json
```

---

## 🧪 Test Individual Components

### Test Translation Service:

```bash
cd webapp
python -c "
from core.translation_services import GoogleTranslateService
service = GoogleTranslateService('en', 'zh-CN')
result = service.translate('Hello')
print(f'Result: {result}')
"
```

Expected output: `Result: 你好` (or similar Chinese translation)

### Test Language Detection:

```bash
python -c "
from services.language_detector import LanguageDetector
detector = LanguageDetector()
lang = detector.detect('Hello world')
print(f'Detected language: {lang}')
"
```

Expected output: `Detected language: en`

### Test Database:

```bash
python -c "
from models.database import Database
db = Database()
print('Database initialized successfully')
"
```

---

## 📋 Detailed Error Checklist

Run through this checklist:

- [ ] Python version is 3.9 or higher
- [ ] You're in the `webapp` directory
- [ ] Virtual environment is activated
- [ ] All minimal requirements installed (`pip install -r requirements-minimal.txt`)
- [ ] `data/` directory exists
- [ ] `core/__init__.py` exists
- [ ] `.env` file exists (or environment variables set)
- [ ] No firewall blocking localhost:5000

---

## 🚀 Complete Fresh Install

If nothing works, start fresh:

```bash
# 1. Go to webapp directory
cd webapp

# 2. Remove old virtual environment
rm -rf venv

# 3. Create new virtual environment
python3 -m venv venv

# 4. Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 5. Upgrade pip
pip install --upgrade pip

# 6. Install minimal requirements
pip install -r requirements-minimal.txt

# 7. Create necessary directories
mkdir -p data static/uploads

# 8. Create .env file
cp .env.example .env

# 9. Run debug test
python debug_test.py

# 10. If all passes, run the app
python app.py
```

---

## 🔧 Still Not Working?

### Get the Actual Error Message:

1. Run the app:
   ```bash
   python app.py
   ```

2. In another terminal, test an endpoint:
   ```bash
   curl -X POST http://localhost:5000/api/translate-text \
     -H "Content-Type: application/json" \
     -d '{"text":"Hello","source_lang":"en","target_lang":"zh-CN"}'
   ```

3. Look at the first terminal for the full error traceback.

4. Share that error message for specific help.

---

## 📞 Getting Help

When asking for help, provide:

1. **Python version:**
   ```bash
   python --version
   ```

2. **Installed packages:**
   ```bash
   pip list
   ```

3. **Full error traceback** from the terminal

4. **What endpoint failed** (e.g., `/api/translate-text`)

5. **Output of debug test:**
   ```bash
   python debug_test.py
   ```

---

## ✅ Expected Behavior

When everything works:

```bash
$ python app.py
✅ All imports successful!
✅ Translation works: 'Hello' -> '你好'
✅ Language detection works: detected 'en'
✅ Database initialized
✅ TranslationManager works: 'Hello' -> '你好'

 * Running on http://0.0.0.0:5000
```

Then in your browser at `http://localhost:5000`:
- Home page loads ✅
- Type "Hello" and click Translate ✅
- See Chinese translation ✅
- Register an account ✅
- Login works ✅

---

## 🎯 Quick Fixes Summary

| Error | Quick Fix |
|-------|-----------|
| 500 on all endpoints | `pip install -r requirements-minimal.txt` |
| Import errors | Check you're in `webapp/` directory |
| Database errors | `mkdir -p data` |
| Translation fails | Check internet connection |
| Registration fails | `mkdir -p data && chmod 755 data` |
| No module 'core' | Create `core/__init__.py` |

---

**Most Common Issue:** Missing dependencies.

**Most Common Fix:**
```bash
cd webapp
pip install Flask flask-cors deep-translator langdetect python-dotenv
python debug_test.py
```
