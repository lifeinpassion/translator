"""
Complete image translation pipeline.
"""

import logging
from typing import Dict, Optional
from pathlib import Path
import cv2
import numpy as np

from .ocr_engine import OCREngine
from .translator import TranslationEngine
from .inpainter import Inpainter
from .font_manager import FontManager
from .text_renderer import TextRenderer

logger = logging.getLogger(__name__)


class TranslationPipeline:
    """End-to-end image translation pipeline."""
    
    def __init__(self, config: Dict):
        """
        Initialize translation pipeline.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        
        # Initialize components
        logger.info("Initializing translation pipeline...")
        self.ocr = OCREngine(config['ocr'])
        self.translator = TranslationEngine(config['translation'])
        self.inpainter = Inpainter(config['inpainting'])
        self.font_manager = FontManager(config['fonts'])
        self.text_renderer = TextRenderer(config['rendering'], self.font_manager)
        
        logger.info("Pipeline initialized successfully")
    
    def translate_image(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        visualize: bool = False
    ) -> np.ndarray:
        """
        Translate text in an image.
        
        Args:
            input_path: Path to input image
            output_path: Path to save output (optional)
            visualize: Draw bounding boxes for debugging
            
        Returns:
            Translated image as numpy array
        """
        try:
            logger.info(f"Starting translation: {input_path}")
            
            # Step 1: Load image
            image = cv2.imread(input_path)
            if image is None:
                raise ValueError(f"Failed to load image: {input_path}")
            
            # Step 2: Detect text
            logger.info("Step 1/4: Detecting text...")
            ocr_results = self.ocr.detect_text(input_path)
            
            if not ocr_results:
                logger.warning("No text detected, returning original image")
                return image
            
            # Step 3: Extract bounding boxes and texts
            bboxes = [result.get_rect_bbox() for result in ocr_results]
            texts = [result.text for result in ocr_results]
            
            # Step 4: Remove original text
            logger.info("Step 2/4: Removing original text...")
            inpainted = self.inpainter.remove_text(image, bboxes)
            
            # Step 5: Translate texts
            logger.info("Step 3/4: Translating text...")
            translated_texts = self.translator.translate_batch(texts)
            
            # Step 6: Render translated text
            logger.info("Step 4/4: Rendering translated text...")
            result = inpainted.copy()
            
            for bbox, translated_text in zip(bboxes, translated_texts):
                result = self.text_renderer.render_text(
                    result,
                    translated_text,
                    bbox,
                    color=(0, 0, 0)  # Black text
                )
            
            # Visualize bounding boxes if requested
            if visualize:
                for bbox in bboxes:
                    x, y, w, h = bbox
                    cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Save output
            if output_path:
                cv2.imwrite(output_path, result)
                logger.info(f"Saved translated image: {output_path}")
            
            logger.info("Translation completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Translation failed: {e}", exc_info=True)
            raise