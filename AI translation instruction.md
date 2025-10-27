AI translators like ChatGPT, Claude, and Gemini often provide better contextual translation than traditional services. Here's how to add them to your document translation system:## Installation and Setup

### 1. **Install AI Service Libraries**

```bash
# For ChatGPT (OpenAI)
pip install openai

# For Claude (Anthropic)
pip install anthropic

# For Gemini (Google)
pip install google-generativeai

# For local Ollama (optional)
# First install Ollama from https://ollama.ai
# Then pull a model: ollama pull llama3.2
pip install requests
```

### 2. **Set Up API Keys**

You can either set environment variables or pass API keys directly:

**Environment Variables (recommended):**
```bash
# Add to ~/.zshrc or ~/.bash_profile on macOS
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="..."
```

**Or pass directly in code:**
```python
translator = create_ai_document_translator(
    translation_service='chatgpt',
    api_key='your-api-key-here'
)
```

### 3. **Usage Examples**

**Using ChatGPT:**
```python
from ai_translator_addon import create_ai_document_translator

# Create translator with ChatGPT
translator = create_ai_document_translator(
    source_lang='en',
    target_lang='zh-CN',
    translation_service='chatgpt',
    model='gpt-4o-mini'  # or 'gpt-4o' for best quality
)

# Translate documents
translator.translate_document('document.pdf')
translator.translate_document('report.xlsx')
```

**Using Claude:**
```python
translator = create_ai_document_translator(
    source_lang='en',
    target_lang='fr',
    translation_service='claude',
    model='claude-3-5-haiku-20241022'  # Fastest & cheapest
    # or 'claude-3-5-sonnet-20241022' for best quality
)
```

**Using Gemini:**
```python
translator = create_ai_document_translator(
    source_lang='en',
    target_lang='es',
    translation_service='gemini',
    model='gemini-1.5-flash'  # Fast & cheap
    # or 'gemini-1.5-pro' for best quality
)
```

**Using Local Ollama (Free, Private):**
```python
# No API key needed! Runs locally on your Mac
translator = create_ai_document_translator(
    source_lang='en',
    target_lang='ja',
    translation_service='ollama',
    model='llama3.2'  # or any model you've pulled
)
```

**Using Hybrid Mode (Cost-Optimized):**
```python
# Uses Google Translate for short text, AI for complex paragraphs
translator = create_ai_document_translator(
    source_lang='en',
    target_lang='zh-CN',
    translation_service='hybrid',
    api_key='your-openai-api-key'  # For complex text
)
```

### 4. **Cost Comparison**

| Service | Model | Cost per 1M chars | Quality | Speed |
|---------|-------|-------------------|---------|-------|
| **Google Translate** | - | Free/$20 | Good | Fast |
| **ChatGPT** | GPT-4o-mini | ~$0.60 | Excellent | Fast |
| **ChatGPT** | GPT-4o | ~$10 | Best | Medium |
| **Claude** | Haiku | ~$0.80 | Excellent | Fast |
| **Claude** | Sonnet | ~$15 | Best | Medium |
| **Gemini** | Flash | ~$0.15 | Very Good | Fast |
| **Gemini** | Pro | ~$7 | Excellent | Medium |
| **Ollama** | Any | Free | Good | Slow |

### 5. **Advantages of AI Translators**

**Better Context Understanding:**
- AI models understand context better than traditional translators
- They preserve tone, style, and nuance
- Better with technical terms, idioms, and cultural references

**Example comparison:**
```python
# Traditional: "他在公司很吃香" → "He eats well at the company" ❌
# AI: "他在公司很吃香" → "He is very popular at the company" ✅
```

**Format-Aware Translation:**
- AI can be instructed to preserve formatting codes
- Better at maintaining document structure
- Can handle mixed content (code + text) intelligently

### 6. **Advanced Features**

**Batch Processing for Efficiency:**
```python
# AI services can translate multiple segments in one call
translator = create_ai_document_translator(
    translation_service='chatgpt',
    model='gpt-4o-mini'
)

# The system automatically batches small text segments
# This reduces API calls and costs
translator.translate_batch(['text1', 'text2', 'text3'])
```

**Custom Translation Instructions:**
```python
class CustomChatGPTService(ChatGPTTranslationService):
    def translate(self, text: str) -> str:
        # Add custom instructions
        system_prompt = f"""Translate from {self.source_lang} to {self.target_lang}.
        Special instructions:
        - Keep all numbers and dates in original format
        - Preserve any code snippets unchanged
        - Use formal tone for business documents
        - Keep company names in English
        """
        # ... rest of implementation
```

### 7. **Complete Working Example**

```python
import os
from ai_translator_addon import create_ai_document_translator

# Set your API key (or use environment variable)
os.environ['OPENAI_API_KEY'] = 'your-key-here'

# Create translator
translator = create_ai_document_translator(
    source_lang='en',
    target_lang='zh-CN',
    translation_service='chatgpt',
    model='gpt-4o-mini'
)

# Translate a single document
translator.translate_document('report.pdf', 'report_chinese.pdf')

# Batch translate a folder
translator.translate_batch('/path/to/documents', '/path/to/output')

# Compare different AI services
from ai_translator_addon import compare_translation_services
compare_translation_services(
    "The quarterly revenue exceeded expectations by 15%",
    source='en',
    target='zh-CN'
)
```

### 8. **Choosing the Right Service**

| Use Case | Recommended Service | Why |
|----------|-------------------|-----|
| **High volume, cost-sensitive** | Hybrid or Gemini Flash | Low cost with good quality |
| **Best quality, critical docs** | ChatGPT GPT-4o or Claude Sonnet | Highest accuracy |
| **Privacy-sensitive** | Ollama (local) | No data leaves your Mac |
| **Balanced quality/cost** | ChatGPT GPT-4o-mini | Good quality, reasonable cost |
| **Fast prototyping** | Google Translate | Free, instant |

### 9. **Tips for Best Results**

1. **Start with mini/flash models** - They're much cheaper and often good enough
2. **Use caching** - The system caches translations automatically
3. **Batch when possible** - Send multiple texts in one API call
4. **Monitor costs** - Set up usage alerts in your API dashboards
5. **Test quality** - Use the compare function to test different services on your content

The AI translation services provide significantly better contextual understanding than traditional services, especially for complex documents with technical terms, cultural references, or nuanced language. The modular design lets you easily switch between services or use different services for different document types.