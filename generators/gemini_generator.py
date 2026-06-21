"""Google Gemini Image Generator"""

import os
import time
from typing import List, Optional
import google.generativeai as genai
from generators.base import BaseImageGenerator
from utils.logger import get_logger

logger = get_logger(__name__)


class GeminiGenerator(BaseImageGenerator):
    """Generate images using Google Gemini Vision API"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini generator.
        
        Args:
            api_key: Google API key (defaults to GOOGLE_API_KEY env var)
        """
        if api_key is None:
            api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not provided")

        super().__init__(api_key)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro-vision")

    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        """Generate image using Google Gemini.
        
        Args:
            prompt: Image description
            temperature: Sampling temperature (0-1)
            max_tokens: Max response tokens
            
        Returns:
            Generated image data or URL
        """
        cache_key = f"gemini_{prompt}_{temperature}"
        cached = self._get_cached(cache_key)
        if cached:
            logger.info(f"Cache hit: {prompt[:30]}...")
            return cached

        try:
            logger.info(f"Generating with Gemini: {prompt[:50]}...")
            # Gemini API returns generation data
            # In real implementation, you'd handle the response appropriately
            result = f"gemini_image_url_{int(time.time())}"
            self._set_cache(cache_key, result)
            self._log_generation(prompt, result)
            return result
        except Exception as e:
            logger.error(f"Gemini generation failed: {str(e)}")
            raise

    def generate_batch(
        self,
        prompts: List[str],
        max_retries: int = 3,
    ) -> List[str]:
        """Generate multiple images with retry logic.
        
        Args:
            prompts: List of image descriptions
            max_retries: Maximum retry attempts per prompt
            
        Returns:
            List of generated image URLs/data
        """
        urls = []
        for i, prompt in enumerate(prompts, 1):
            logger.info(f"Batch generation {i}/{len(prompts)}")
            retry_count = 0
            while retry_count < max_retries:
                try:
                    url = self.generate(prompt)
                    urls.append(url)
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count < max_retries:
                        wait_time = 2 ** retry_count
                        logger.warning(
                            f"Retry {retry_count}/{max_retries} after {wait_time}s"
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Failed after {max_retries} retries: {str(e)}")
                        urls.append(None)

        return urls
