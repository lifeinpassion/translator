
Here's how to set up and use this complete document translation system on your MacBook:

### 1. **Install Required Libraries**

Open Terminal and install all dependencies:

```bash
# Install all required libraries
pip install pymupdf openpyxl python-docx python-pptx deep-translator tenacity

# Optional: Install DeepL for better translation quality (requires API key)
pip install deepl
```

### 2. **Save the Code**

Save the code above as `document_translator.py` in your preferred directory.

### 3. **Basic Usage Examples**

**Translate a single document:**
```bash
# Translate a PDF to Chinese (default)
python document_translator.py document.pdf

# Translate to a specific language
python document_translator.py document.xlsx -t fr  # French
python document_translator.py presentation.pptx -t ja  # Japanese
python document_translator.py report.docx -t es  # Spanish

# Specify custom output path
python document_translator.py input.pdf -o translated_output.pdf
```

**Batch translate multiple files:**
```bash
# Translate all documents in a folder
python document_translator.py /path/to/documents --batch

# Translate with specific settings
python document_translator.py ~/Documents --batch -s en -t zh-CN
```

### 4. **Python Script Usage**

You can also use it directly in Python:

```python
from document_translator import DocumentTranslator

# Create translator instance
translator = DocumentTranslator(
    source_lang='en',
    target_lang='zh-CN',  # or 'fr', 'es', 'ja', etc.
    translation_service='google'  # free, no API key needed
)

# Translate a single file
translator.translate_document('my_document.pdf')

# Translate multiple files
translator.translate_batch('/path/to/documents')
```

### 5. **Supported Features by Format**

| Format | Features Preserved | Limitations |
|--------|-------------------|-------------|
| **PDF** | Text, formatting, images, layout | Creates bilingual layers (togglable) |
| **Excel** | Formulas, charts, formatting, styles | .xls not supported (use .xlsx) |
| **Word** | Paragraphs, tables, headers/footers | No tracked changes/comments |
| **PowerPoint** | Slides, layouts, notes, shapes | .ppt limited (convert to .pptx) |

### 6. **Language Codes**

Common language codes for translation:
- `en` - English
- `zh-CN` - Chinese (Simplified)
- `zh-TW` - Chinese (Traditional)
- `es` - Spanish
- `fr` - French
- `de` - German
- `ja` - Japanese
- `ko` - Korean
- `ru` - Russian
- `ar` - Arabic
- `pt` - Portuguese
- `it` - Italian

### 7. **Advanced Options**

**Using DeepL for better quality** (requires API key):
```python
translator = DocumentTranslator(
    source_lang='en',
    target_lang='zh-CN',
    translation_service='deepl',
    api_key='your-deepl-api-key'
)
```

**Processing specific file types only:**
```python
# In batch mode, you can specify patterns
from pathlib import Path
files = Path('/documents').glob('*.pdf')  # PDFs only
for file in files:
    translator.translate_document(str(file))
```

### 8. **Tips for Best Results**

1. **File Preparation:**
   - Convert old formats (.doc, .xls, .ppt) to modern formats (.docx, .xlsx, .pptx)
   - For Word docs with tracked changes, accept all changes first
   - Close files in Office apps before translating

2. **Performance:**
   - The first translation may be slower as it builds the translation cache
   - Repeated phrases are cached automatically for faster processing
   - Large files (>50MB) may take several minutes

3. **Quality:**
   - Google Translate is free but quality varies by language pair
   - For professional use, consider DeepL API (better quality, costs ~$20/million characters)
   - Always review critical translations

### 9. **Troubleshooting**

**If you get import errors:**
```bash
# Reinstall with upgrade flag
pip install --upgrade pymupdf openpyxl python-docx python-pptx deep-translator

# For M1/M2 Macs, if you have issues with PyMuPDF:
pip install --upgrade pymupdf --no-cache-dir
```

**For memory issues with large files:**
- The script automatically uses streaming for large Excel files
- PDFs are processed page by page to minimize memory usage

**Font issues in translated PDFs:**
- The system automatically selects appropriate fonts for Chinese/Japanese/Korean
- macOS fonts like PingFang SC are used by default

This complete system integrates all the research from our previous discussions and provides a production-ready solution for translating documents while preserving their formatting. It's optimized for macOS but works cross-platform, handles all major Office formats plus PDF, and includes intelligent caching and error handling for reliable operation.