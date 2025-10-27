"""
Text rendering with Chinese font support.
"""

import logging
from typing import Tuple, Optional
import numpy as np
import cv2
from PIL import Image, ImageDraw
from .font_manager import FontManager

logger = logging.getLogger(__name__)


class TextRenderer:
    """Render translated text onto images."""
    
    def __init__(self, config: Dict, font_manager: FontManager):
        """
        Initialize text renderer.
        
        Args:
            config: Configuration dictionary
            font_manager: FontManager instance
        """
        self.config = config
        self.font_manager = font_manager
        self.auto_scale = config.get('auto_scale', True)
        self.line_spacing = config.get('line_spacing', 1.3)
        
    def render_text(
        self,
        image: np.ndarray,
        text: str,
        bbox: Tuple[int, int, int, int],
        color: Tuple[int, int, int] = (0, 0, 0),
        style: str = 'modern'
    ) -> np.ndarray:
        """
        Render text onto image at specified location.
        
        Args:
            image: Source image (BGR)
            text: Text to render
            bbox: (x, y, w, h) bounding box
            color: Text color (R, G, B)
            style: Font style
            
        Returns:
            Image with rendered text
        """
        try:
            x, y, w, h = bbox
            
            # Convert BGR to RGB for PIL
            img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(img_pil)
            
            # Get appropriate font
            is_chinese = any('\u4e00' <= char <= '\u9fff' for char in text)
            font_path = self.font_manager.get_font_path(style, simplified=is_chinese)
            
            # Find optimal font size
            if self.auto_scale:
                font_size = self.font_manager.find_optimal_font_size(
                    text, font_path, w, h
                )
            else:
                font_size = min(h, 32)  # Default size
            
            font = self.font_manager.load_font(font_path, font_size)
            
            # Calculate position (center text)
            bbox_pil = font.getbbox(text)
            text_width = bbox_pil[2] - bbox_pil[0]
            text_height = bbox_pil[3] - bbox_pil[1]
            
            text_x = x + (w - text_width) // 2
            text_y = y + (h - text_height) // 2
            
            # Draw text
            draw.text((text_x, text_y), text, font=font, fill=color)
            
            # Convert back to BGR
            result = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
            
            logger.debug(f"Rendered text: '{text}' at ({x}, {y})")
            return result
            
        except Exception as e:
            logger.error(f"Text rendering failed: {e}")
            return image  # Return original on failure
    
    def estimate_text_expansion(self, source_lang: str, target_lang: str) -> float:
        """
        Estimate text expansion/contraction ratio.
        
        Args:
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Expansion ratio (1.0 = no change)
        """
        # English to Chinese typically contracts 60-90% in width
        if source_lang == 'en' and 'zh' in target_lang:
            return 0.75  # Chinese takes ~75% of English width
        elif 'zh' in source_lang and target_lang == 'en':
            return 1.3  # English takes ~130% of Chinese width
        else:
            return 1.0  # No change