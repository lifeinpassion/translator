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