"""
Image inpainting for text removal using OpenCV.
"""

import logging
from typing import Tuple, List
import numpy as np
import cv2

logger = logging.getLogger(__name__)


class Inpainter:
    """Text removal using OpenCV inpainting algorithms."""
    
    def __init__(self, config: Dict):
        """
        Initialize inpainter.
        
        Args:
            config: Configuration dictionary
        """
        self.method = config.get('method', 'telea')
        self.radius = config.get('radius', 5)
        self.expand_mask = config.get('expand_mask', 2)
        
        # Select inpainting algorithm
        if self.method == 'telea':
            self.algorithm = cv2.INPAINT_TELEA
        elif self.method == 'ns':
            self.algorithm = cv2.INPAINT_NS
        else:
            raise ValueError(f"Unknown inpainting method: {self.method}")
        
        logger.info(f"Initialized inpainter with method: {self.method}")
    
    def create_mask(self, image_shape: Tuple[int, int], 
                    bboxes: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """
        Create binary mask from bounding boxes.
        
        Args:
            image_shape: (height, width) of image
            bboxes: List of (x, y, w, h) bounding boxes
            
        Returns:
            Binary mask (uint8)
        """
        mask = np.zeros(image_shape[:2], dtype=np.uint8)
        
        for bbox in bboxes:
            x, y, w, h = bbox
            # Draw filled rectangle on mask
            cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
        
        # Expand mask slightly for better inpainting
        if self.expand_mask > 0:
            kernel = np.ones((self.expand_mask, self.expand_mask), np.uint8)
            mask = cv2.dilate(mask, kernel, iterations=1)
        
        return mask
    
    def inpaint(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """
        Remove text using inpainting.
        
        Args:
            image: Source image (BGR)
            mask: Binary mask (white pixels indicate text)
            
        Returns:
            Inpainted image
        """
        try:
            logger.debug(f"Inpainting with radius={self.radius}, method={self.method}")
            
            inpainted = cv2.inpaint(image, mask, self.radius, self.algorithm)
            
            return inpainted
            
        except Exception as e:
            logger.error(f"Inpainting failed: {e}")
            raise
    
    def remove_text(self, image: np.ndarray, 
                    bboxes: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """
        Complete text removal pipeline.
        
        Args:
            image: Source image
            bboxes: List of text bounding boxes
            
        Returns:
            Image with text removed
        """
        if not bboxes:
            logger.info("No text regions to remove")
            return image
        
        # Create mask
        mask = self.create_mask(image.shape, bboxes)
        
        # Inpaint
        result = self.inpaint(image, mask)
        
        logger.info(f"Removed {len(bboxes)} text regions")
        return result