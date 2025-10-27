# examples/basic_translation.py
"""Basic image translation example."""

from pathlib import Path
from image_translator.core.pipeline import TranslationPipeline
from image_translator.utils.config import load_config

# Load configuration
config_path = Path("config/default_config.yaml")
config = load_config(config_path)

# Initialize pipeline
pipeline = TranslationPipeline(config)

# Translate single image
input_image = "examples/sample_images/chinese_text.jpg"
output_image = "examples/output/translated.jpg"

result = pipeline.translate_image(input_image, output_image, visualize=True)
print(f"Translation complete! Saved to {output_image}")