"""
Font management for Chinese text rendering on macOS.
"""

import logging
from typing import Optional, Tuple
from pathlib import Path
from PIL import ImageFont

logger = logging.getLogger(__name__)


class FontManager:
    """Manages Chinese fonts for macOS."""
    
    # Default macOS fonts
    FONTS = {
        'pingfang_sc': '/System/Library/Fonts/PingFang.ttc',
        'pingfang_tc': '/System/Library/Fonts/PingFang.ttc',
        'heiti': '/System/Library/Fonts/STHeiti Medium.ttc',
        'songti': '/Library/Fonts/Songti.ttc',
        'kaiti': '/System/Library/Fonts/Kaiti.ttc',
    }
    
    def __init__(self, config: Dict):
        """
        Initialize font manager.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.font_cache = {}
        
    def get_font_path(self, style: str = 'modern', simplified: bool = True) -> str:
        """
        Get appropriate font path for Chinese text.
        
        Args:
            style: Font style (modern, serif, script)
            simplified: True for Simplified Chinese, False for Traditional
            
        Returns:
            Path to font file
        """
        if style == 'modern' or style == 'sans':
            font_key = 'pingfang_sc' if simplified else 'pingfang_tc'
        elif style == 'serif':
            font_key = 'songti'
        elif style == 'script':
            font_key = 'kaiti'
        else:
            font_key = 'pingfang_sc'
        
        font_path = self.FONTS.get(font_key, self.FONTS['heiti'])
        
        # Verify font exists
        if not Path(font_path).exists():
            logger.warning(f"Font not found: {font_path}, using fallback")
            font_path = self.FONTS['heiti']
        
        return font_path
    
    def load_font(self, font_path: str, size: int) -> ImageFont.FreeTypeFont:
        """
        Load font with caching.
        
        Args:
            font_path: Path to font file
            size: Font size in points
            
        Returns:
            PIL ImageFont object
        """
        cache_key = f"{font_path}_{size}"
        
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]
        
        try:
            font = ImageFont.truetype(font_path, size)
            self.font_cache[cache_key] = font
            return font
            
        except Exception as e:
            logger.error(f"Failed to load font {font_path}: {e}")
            raise
    
    def find_optimal_font_size(
        self,
        text: str,
        font_path: str,
        max_width: int,
        max_height: int,
        min_size: int = 8,
        max_size: int = 200
    ) -> int:
        """
        Find optimal font size to fit text in bounding box.
        
        Args:
            text: Text to render
            font_path: Path to font file
            max_width: Maximum width in pixels
            max_height: Maximum height in pixels
            min_size: Minimum font size
            max_size: Maximum font size
            
        Returns:
            Optimal font size
        """
        # Binary search for optimal size
        left, right = min_size, max_size
        optimal_size = min_size
        
        while left <= right:
            mid_size = (left + right) // 2
            font = self.load_font(font_path, mid_size)
            
            # Measure text
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Check if fits
            if text_width <= max_width and text_height <= max_height:
                optimal_size = mid_size
                left = mid_size + 1
            else:
                right = mid_size - 1
        
        return optimal_size