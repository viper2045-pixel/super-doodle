#!/usr/bin/env python3
"""Batch image generation example"""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generators import ImageGeneratorBatch
from utils.logger import get_logger
from utils.config import Config

logger = get_logger(__name__)


def batch_generate_landscapes():
    """Generate batch of landscape images"""
    logger.info("=== Batch Landscape Generation ===")
    
    prompts = [
        "A peaceful mountain lake surrounded by pine trees during golden hour",
        "A dramatic desert canyon with layered rock formations",
        "A misty tropical rainforest with ancient waterfalls",
        "A snowy alpine peak with aurora borealis in the sky",
        "A sandy beach with turquoise ocean and palm trees",
    ]

    batch = ImageGeneratorBatch(provider="openai")
    results = batch.generate_batch(
        prompts=prompts,
        output_dir=os.path.join(Config.IMAGE_OUTPUT_DIR, "landscapes"),
        num_retries=3,
        save_metadata=True
    )

    return results


def batch_generate_character_designs():
    """Generate batch of character design images"""
    logger.info("=== Batch Character Design Generation ===")
    
    prompts = [
        "A steampunk engineer with goggles and brass mechanical armor",
        "An elegant elven archer in flowing green and silver robes",
        "A grizzled cyberpunk hacker with neon implants and leather jacket",
        "A mystical wizard with stars and moons in her robes",
        "A futuristic android warrior with glowing blue circuits",
    ]

    batch = ImageGeneratorBatch(provider="gemini")
    results = batch.generate_batch(
        prompts=prompts,
        output_dir=os.path.join(Config.IMAGE_OUTPUT_DIR, "characters"),
        num_retries=3,
        save_metadata=True
    )

    return results


def analyze_results(results):
    """Analyze and report batch results"""
    total = len(results)
    successful = sum(1 for r in results if r["status"] == "success")
    failed = total - successful
    success_rate = (successful / total * 100) if total > 0 else 0

    logger.info("\n=== Batch Analysis ===")
    logger.info(f"Total prompts: {total}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Success rate: {success_rate:.1f}%")

    return {
        "total": total,
        "successful": successful,
        "failed": failed,
        "success_rate": success_rate,
    }


def main():
    """Run batch generation examples"""
    logger.info("Starting batch image generation examples...")
    Config.validate()

    # Create output directory
    os.makedirs(Config.IMAGE_OUTPUT_DIR, exist_ok=True)

    # Run batch generations
    logger.info("\n" + "="*50)
    landscape_results = batch_generate_landscapes()
    landscape_analysis = analyze_results(landscape_results)

    logger.info("\n" + "="*50)
    character_results = batch_generate_character_designs()
    character_analysis = analyze_results(character_results)

    # Save combined analysis
    analysis = {
        "landscapes": {
            "results": landscape_results,
            "analysis": landscape_analysis,
        },
        "characters": {
            "results": character_results,
            "analysis": character_analysis,
        },
    }

    analysis_file = os.path.join(Config.IMAGE_OUTPUT_DIR, "batch_analysis.json")
    with open(analysis_file, "w") as f:
        json.dump(analysis, f, indent=2)
    
    logger.info(f"\nAnalysis saved to: {analysis_file}")


if __name__ == "__main__":
    main()
