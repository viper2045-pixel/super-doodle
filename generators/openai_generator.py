"""OpenAI DALL-E 3 Image Generator"""

import os
from typing import List, Optional
import openai
from generators.base import BaseImageGenerator
from utils.logger import get_logger

logger = get_logger(__name__)


class DALLEGenerator(BaseImageGenerator):
    """Generate images using OpenAI's DALL-E 3"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize DALL-E generator.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not provided")

        super().__init__(api_key)
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "dall-e-3"

    def generate(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "standard",
        n: int = 1,
    ) -> str:
        """Generate image using DALL-E 3.
        
        Args:
            prompt: Image description
            size: Image size (1024x1024, 1792x1024, 1024x1792)
            quality: Quality level (standard or hd)
            n: Number of images (DALL-E 3 only supports n=1)
            
        Returns:
            URL of generated image
        """
        # Check cache
        cache_key = f"dalle_{prompt}_{size}_{quality}"
        cached = self._get_cached(cache_key)
        if cached:
            logger.info(f"Cache hit: {prompt[:30]}...")
            return cached

        try:
            logger.info(f"Generating with DALL-E 3: {prompt[:50]}...")
            response = self.client.images.generate(
                model=self.model,
                prompt=prompt,
                size=size,
                quality=quality,
                n=n,
            )
            url = response.data[0].url
            self._set_cache(cache_key, url)
            self._log_generation(prompt, url)
            return url
        except Exception as e:
            logger.error(f"DALL-E generation failed: {str(e)}")
            raise

    def generate_batch(
        self,
        prompts: List[str],
        size: str = "1024x1024",
        quality: str = "standard",
    ) -> List[str]:
        """Generate multiple images.
        
        Args:
            prompts: List of image descriptions
            size: Image size
            quality: Quality level
            
        Returns:
            List of image URLs
        """
        urls = []
        for i, prompt in enumerate(prompts, 1):
            logger.info(f"Batch generation {i}/{len(prompts)}")
            try:
                url = self.generate(prompt, size=size, quality=quality)
                urls.append(url)
            except Exception as e:
                logger.warning(f"Failed to generate image {i}: {str(e)}")
                urls.append(None)
        return urls

    def generate_variations(
        self,
        prompt: str,
        num_variations: int = 4,
        size: str = "1024x1024",
    ) -> List[str]:
        """Generate variations of a prompt.
        
        Args:
            prompt: Base image description
            num_variations: Number of variations to create
            size: Image size
            
        Returns:
            List of variation URLs
        """
        # Generate multiple variations by appending variation hints
        variations = []
        variation_hints = [
            ", style A",
            ", style B",
            ", style C",
            ", different composition",
        ]

        for i, hint in enumerate(variation_hints[: num_variations]):
            varied_prompt = prompt + hint
            try:
                url = self.generate(varied_prompt, size=size)
                variations.append(url)
            except Exception as e:
                logger.warning(f"Failed to generate variation {i + 1}: {str(e)}")

        return variations
