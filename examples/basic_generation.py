#!/usr/bin/env python3
"""Basic image generation example"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generators import DALLEGenerator, GeminiGenerator, FluxGenerator
from utils.logger import get_logger
from utils.config import Config

logger = get_logger(__name__)


def generate_with_dalle():
    """Generate image with DALL-E 3"""
    logger.info("=== DALL-E 3 Generation ===")
    try:
        generator = DALLEGenerator()
        prompt = "A serene mountain landscape at sunset, oil painting style"
        url = generator.generate(
            prompt=prompt,
            size="1024x1024",
            quality="standard"
        )
        logger.info(f"Image URL: {url}")
        return url
    except Exception as e:
        logger.error(f"DALL-E generation failed: {str(e)}")
        return None


def generate_with_gemini():
    """Generate image with Google Gemini"""
    logger.info("=== Google Gemini Generation ===")
    try:
        generator = GeminiGenerator()
        prompt = "A futuristic city with flying cars and neon lights"
        url = generator.generate(prompt=prompt)
        logger.info(f"Image URL: {url}")
        return url
    except Exception as e:
        logger.error(f"Gemini generation failed: {str(e)}")
        return None


def generate_with_flux():
    """Generate image with Flux"""
    logger.info("=== Flux Generation ===")
    try:
        generator = FluxGenerator()
        prompt = "A hyperrealistic portrait of a woman in cyberpunk armor"
        url = generator.generate(
            prompt=prompt,
            height=1024,
            width=1024
        )
        logger.info(f"Image URL: {url}")
        return url
    except Exception as e:
        logger.error(f"Flux generation failed: {str(e)}")
        return None


def main():
    """Run basic generation examples"""
    logger.info("Starting basic image generation examples...")
    Config.validate()

    # Create output directory
    os.makedirs(Config.IMAGE_OUTPUT_DIR, exist_ok=True)

    # Generate examples
    results = {
        "dalle": generate_with_dalle(),
        "gemini": generate_with_gemini(),
        "flux": generate_with_flux(),
    }

    # Summary
    logger.info("=== Generation Summary ===")
    for provider, url in results.items():
        status = "✓" if url else "✗"
        logger.info(f"{status} {provider}: {url if url else 'Failed'}")


if __name__ == "__main__":
    main()
