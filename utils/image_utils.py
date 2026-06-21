"""Image utility functions"""

import os
from pathlib import Path
import requests
from PIL import Image
from io import BytesIO
from utils.logger import get_logger

logger = get_logger(__name__)


def download_image(url: str, output_path: str) -> bool:
    """Download image from URL and save locally.
    
    Args:
        url: Image URL
        output_path: Path to save image
        
    Returns:
        True if successful, False otherwise
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Create directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save image
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        logger.info(f"Downloaded image: {output_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to download image: {str(e)}")
        return False


def optimize_image(input_path: str, output_path: str, max_width: int = 1024) -> bool:
    """Optimize image size and quality.
    
    Args:
        input_path: Path to input image
        output_path: Path to save optimized image
        max_width: Maximum width in pixels
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with Image.open(input_path) as img:
            # Resize if needed
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # Save optimized
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            img.save(output_path, quality=85, optimize=True)
            logger.info(f"Optimized image: {output_path}")
            return True
    except Exception as e:
        logger.error(f"Failed to optimize image: {str(e)}")
        return False


def get_image_info(image_path: str) -> dict:
    """Get image information.
    
    Args:
        image_path: Path to image file
        
    Returns:
        Dictionary with image info
    """
    try:
        with Image.open(image_path) as img:
            return {
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "mode": img.mode,
                "size_kb": os.path.getsize(image_path) / 1024,
            }
    except Exception as e:
        logger.error(f"Failed to get image info: {str(e)}")
        return {}
