# examples/batch_processing.py
"""Batch processing example."""

from pathlib import Path
from image_translator.batch.batch_processor import BatchProcessor
from image_translator.utils.config import load_config

# Load configuration
config = load_config("config/default_config.yaml")

# Initialize batch processor
processor = BatchProcessor(config, num_workers=4)

# Get list of images
input_dir = Path("examples/sample_images")
images = list(input_dir.glob("*.jpg"))

# Process batch
output_dir = "examples/output_batch"
results = processor.process_batch(
    [str(img) for img in images],
    output_dir
)

# Print summary
print(f"Successful: {len(results['successes'])}")
print(f"Failed: {len(results['failures'])}")