# Image Translator for macOS

**Production-ready image translation between English and Chinese**

Optimized for CPU-only processing on MacBook (both Intel and Apple Silicon).

## Features

✨ **Accurate OCR** - PaddleOCR with PP-OCRv5 (best-in-class for Chinese/English)  
🎨 **Smart Inpainting** - OpenCV-based text removal with minimal artifacts  
🔤 **Native Fonts** - PingFang SC/TC for beautiful Chinese rendering  
📄 **Document Support** - PDF and Word document translation  
⚡ **Batch Processing** - Parallel processing with progress tracking  
🛠️ **Production-Ready** - Comprehensive error handling and logging

## Installation

### Prerequisites
```bash
brew install poppler  # For PDF processing
```

### Install Package
```bash
pip install image-translator-macos
```

## Quick Start

### Command Line
```bash
# Translate single image
imgtrans translate input.jpg

# Batch translate directory
imgtrans batch ./images/ ./output/

# Specify output
imgtrans translate input.jpg --output result.jpg

# Visualize detection
imgtrans translate input.jpg --viz
```

### Python API
```python
from image_translator import TranslationPipeline
from image_translator.utils import load_config

config = load_config("config.yaml")
pipeline = TranslationPipeline(config)

# Translate image
result = pipeline.translate_image("input.jpg", "output.jpg")
```

## Configuration

Create `config.yaml`:
```yaml
ocr:
  languages: ["en", "ch"]
  use_gpu: false

translation:
  engine: "google"  # or "deepl", "argos"
  target_lang: "zh-CN"  # or "zh-TW" for Traditional

inpainting:
  method: "telea"  # or "ns"
  radius: 5

fonts:
  chinese_simplified: "/System/Library/Fonts/PingFang.ttc"
```

## Performance

**MacBook Pro M1:**
- Single image (1920x1080): ~3-5 seconds
- Batch (100 images): ~4-6 minutes (4 workers)

**Intel MacBook:**
- Single image: ~5-8 seconds
- Batch: ~8-12 minutes

## Supported Content

- ✅ Technical documents and diagrams
- ✅ Manga and comics
- ✅ Natural photos with text
- ✅ Screenshots and UI elements
- ✅ Mixed English/Chinese content
- ✅ Horizontal and vertical text

## Language Support

- **English ↔ Simplified Chinese**
- **English ↔ Traditional Chinese**
- **Auto-detection** of source language

## Development
```bash
# Clone repository
git clone https://github.com/yourusername/image-translator-macos.git
cd image-translator-macos

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src tests
```

## License

MIT License - see LICENSE file

## Credits

Built with:
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [OpenCV](https://opencv.org/)
- [deep-translator](https://github.com/nidhaloff/deep-translator)