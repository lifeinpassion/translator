"""
OCR Engine for text detection and recognition using PaddleOCR.
"""

import logging
from typing import List, Dict, Tuple, Optional
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image
import cv2

logger = logging.getLogger(__name__)


class OCRResult:
    """Container for OCR detection results."""
    
    def __init__(self, bbox: List[List[int]], text: str, confidence: float):
        self.bbox = bbox  # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
        self.text = text
        self.confidence = confidence
        
    def get_rect_bbox(self) -> Tuple[int, int, int, int]:
        """Convert polygon bbox to rectangular (x, y, w, h)."""
        points = np.array(self.bbox)
        x = int(points[:, 0].min())
        y = int(points[:, 1].min())
        w = int(points[:, 0].max() - x)
        h = int(points[:, 1].max() - y)
        return (x, y, w, h)


class OCREngine:
    """High-performance OCR engine using PaddleOCR."""
    
    def __init__(self, config: Dict):
        """
        Initialize OCR engine.
        
        Args:
            config: Configuration dictionary with OCR settings
        """
        self.config = config
        self.ocr = None
        self._initialize_ocr()
        
    def _initialize_ocr(self):
        """Initialize PaddleOCR with optimized settings for macOS."""
        try:
            logger.info("Initializing PaddleOCR...")
            
            # Determine language codes
            langs = self.config.get('languages', ['en', 'ch'])
            lang_code = 'en' if 'en' in langs and 'ch' in langs else langs[0]
            
            self.ocr = PaddleOCR(
                use_angle_cls=self.config.get('use_angle_cls', True),
                lang=lang_code,
                use_gpu=self.config.get('use_gpu', False),
                det_db_thresh=self.config.get('det_db_thresh', 0.3),
                det_db_box_thresh=self.config.get('det_db_box_thresh', 0.6),
                rec_batch_num=self.config.get('rec_batch_num', 6),
                drop_score=self.config.get('drop_score', 0.5),
                enable_mkldnn=self.config.get('enable_mkldnn', True),  # Intel CPU optimization
                show_log=False,
            )
            
            logger.info("PaddleOCR initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize PaddleOCR: {e}")
            raise
    
    def detect_text(self, image_path: str) -> List[OCRResult]:
        """
        Detect and recognize text in an image.
        
        Args:
            image_path: Path to input image
            
        Returns:
            List of OCRResult objects
        """
        try:
            logger.info(f"Processing image: {image_path}")
            
            # Run OCR
            results = self.ocr.ocr(image_path, cls=True)
            
            if not results or not results[0]:
                logger.warning(f"No text detected in {image_path}")
                return []
            
            # Parse results
            ocr_results = []
            for line in results[0]:
                bbox = line[0]  # Bounding box coordinates
                text_info = line[1]  # (text, confidence)
                text = text_info[0]
                confidence = text_info[1]
                
                ocr_results.append(OCRResult(bbox, text, confidence))
                logger.debug(f"Detected: '{text}' (confidence: {confidence:.2f})")
            
            logger.info(f"Detected {len(ocr_results)} text regions")
            return ocr_results
            
        except Exception as e:
            logger.error(f"OCR failed for {image_path}: {e}")
            raise
    
    def detect_text_from_array(self, image_array: np.ndarray) -> List[OCRResult]:
        """
        Detect text from numpy array (for in-memory processing).
        
        Args:
            image_array: Image as numpy array (BGR format)
            
        Returns:
            List of OCRResult objects
        """
        try:
            results = self.ocr.ocr(image_array, cls=True)
            
            if not results or not results[0]:
                return []
            
            ocr_results = []
            for line in results[0]:
                bbox = line[0]
                text_info = line[1]
                ocr_results.append(OCRResult(bbox, text_info[0], text_info[1]))
            
            return ocr_results
            
        except Exception as e:
            logger.error(f"OCR failed for array: {e}")
            raise