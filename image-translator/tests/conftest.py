# tests/conftest.py
"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
import yaml

@pytest.fixture
def sample_config():
    """Load sample configuration."""
    config_path = Path("config/default_config.yaml")
    with open(config_path) as f:
        return yaml.safe_load(f)

@pytest.fixture
def sample_image_path(tmp_path):
    """Create sample test image."""
    import cv2
    import numpy as np
    
    # Create simple test image
    img = np.ones((200, 400, 3), dtype=np.uint8) * 255
    cv2.putText(img, "Hello World", (50, 100), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    img_path = tmp_path / "test.jpg"
    cv2.imwrite(str(img_path), img)
    return img_path