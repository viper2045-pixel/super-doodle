#!/usr/bin/env python3
"""Advanced prompt engineering examples"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generators import DALLEGenerator, FluxGenerator
from utils.logger import get_logger
from utils.config import Config

logger = get_logger(__name__)


class PromptBuilder:
    """Build detailed prompts for better image generation"""

    def __init__(self):
        self.components = {}

    def set_subject(self, subject: str):
        """Set main subject"""
        self.components["subject"] = subject
        return self

    def set_style(self, style: str):
        """Set artistic style"""
        self.components["style"] = style
        return self

    def set_lighting(self, lighting: str):
        """Set lighting conditions"""
        self.components["lighting"] = lighting
        return self

    def set_mood(self, mood: str):
        """Set mood/atmosphere"""
        self.components["mood"] = mood
        return self

    def set_details(self, details: str):
        """Set additional details"""
        self.components["details"] = details
        return self

    def set_quality(self, quality: str):
        """Set quality descriptors"""
        self.components["quality"] = quality
        return self

    def build(self) -> str:
        """Build final prompt"""
        parts = []
        
        if "subject" in self.components:
            parts.append(self.components["subject"])
        
        if "style" in self.components:
            parts.append(f", {self.components['style']}")
        
        if "mood" in self.components:
            parts.append(f", {self.components['mood']}")
        
        if "lighting" in self.components:
            parts.append(f", {self.components['lighting']}")
        
        if "details" in self.components:
            parts.append(f", {self.components['details']}")
        
        if "quality" in self.components:
            parts.append(f", {self.components['quality']}")
        
        return "".join(parts)


def example_fantasy_landscape():
    """Generate fantasy landscape with advanced prompt"""
    logger.info("=== Fantasy Landscape Example ===")
    
    prompt = (PromptBuilder()
        .set_subject("A majestic fantasy kingdom built on floating islands in the clouds")
        .set_style("oil painting by John Howe")
        .set_mood("mystical and wondrous, ethereal mist")
        .set_lighting("golden sunlight breaking through clouds, dramatic shadows")
        .set_details("ornate towers, ancient architecture, waterfalls flowing between islands")
        .set_quality("4K, ultra-detailed, high resolution")
        .build())
    
    logger.info(f"Prompt: {prompt}")
    
    try:
        generator = DALLEGenerator()
        url = generator.generate(prompt, quality="hd")
        logger.info(f"Generated: {url}")
        return url
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        return None


def example_product_photography():
    """Generate product photography with advanced prompt"""
    logger.info("=== Product Photography Example ===")
    
    prompt = (PromptBuilder()
        .set_subject("A sleek stainless steel smartwatch on a minimalist white surface")
        .set_style("professional product photography")
        .set_mood("clean, modern, luxurious")
        .set_lighting("studio lighting with soft shadows, warm accent lights")
        .set_details("reflection on surface, minimalist composition, branded watch face")
        .set_quality("sharp focus, high-end commercial photography, 4K")
        .build())
    
    logger.info(f"Prompt: {prompt}")
    
    try:
        generator = DALLEGenerator()
        url = generator.generate(prompt, size="1024x1024")
        logger.info(f"Generated: {url}")
        return url
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        return None


def example_character_concept_art():
    """Generate character concept art with advanced prompt"""
    logger.info("=== Character Concept Art Example ===")
    
    prompt = (PromptBuilder()
        .set_subject("A confident female warrior in advanced futuristic battle armor")
        .set_style("concept art by Artstation, anime aesthetic")
        .set_mood("determined and powerful, ready for action")
        .set_lighting("neon blue and purple accent lighting, volumetric light rays")
        .set_details("holographic HUD elements, high-tech gauntlets, cape with digital patterns")
        .set_quality("character design sheet, intricate details, 8K")
        .build())
    
    logger.info(f"Prompt: {prompt}")
    
    try:
        generator = FluxGenerator()
        url = generator.generate(prompt)
        logger.info(f"Generated: {url}")
        return url
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        return None


def main():
    """Run advanced prompt examples"""
    logger.info("Starting advanced prompt engineering examples...")
    Config.validate()

    # Run examples
    fantasy = example_fantasy_landscape()
    logger.info("")
    product = example_product_photography()
    logger.info("")
    character = example_character_concept_art()

    # Summary
    logger.info("\n=== Generation Summary ===")
    logger.info(f"Fantasy Landscape: {'✓' if fantasy else '✗'}")
    logger.info(f"Product Photography: {'✓' if product else '✗'}")
    logger.info(f"Character Concept Art: {'✓' if character else '✗'}")


if __name__ == "__main__":
    main()
