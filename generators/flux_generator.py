"""Black Forest Labs Flux Image Generator"""

import os
from typing import List, Optional
import requests
from generators.base import BaseImageGenerator
from utils.logger import get_logger

logger = get_logger(__name__)


class FluxGenerator(BaseImageGenerator):
    """Generate images using Black Forest Labs Flux"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Flux generator.
        
        Args:
            api_key: Flux API key (defaults to FLUX_API_KEY env var)
        """
        if api_key is None:
            api_key = os.getenv("FLUX_API_KEY")
        if not api_key:
            raise ValueError("FLUX_API_KEY not provided")

        super().__init__(api_key)
        self.endpoint = os.getenv(
            "FLUX_ENDPOINT", "https://api.blackforestlabs.ai"
        )
        self.model = "flux-pro"

    def generate(
        self,
        prompt: str,
        height: int = 1024,
        width: int = 1024,
        num_inference_steps: int = 20,
    ) -> str:
        """Generate image using Flux.
        
        Args:
            prompt: Image description
            height: Image height in pixels
            width: Image width in pixels
            num_inference_steps: Number of inference steps
            
        Returns:
            URL of generated image
        """
        cache_key = f"flux_{prompt}_{height}_{width}"
        cached = self._get_cached(cache_key)
        if cached:
            logger.info(f"Cache hit: {prompt[:30]}...")
            return cached

        try:
            logger.info(f"Generating with Flux: {prompt[:50]}...")
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            payload = {
                "model": self.model,
                "prompt": prompt,
                "height": height,
                "width": width,
                "num_inference_steps": num_inference_steps,
            }

            response = requests.post(
                f"{self.endpoint}/v1/images/generations",
                json=payload,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()

            result = response.json()
            url = result["data"][0]["url"]
            self._set_cache(cache_key, url)
            self._log_generation(prompt, url)
            return url
        except Exception as e:
            logger.error(f"Flux generation failed: {str(e)}")
            raise

    def generate_batch(
        self,
        prompts: List[str],
        height: int = 1024,
        width: int = 1024,
    ) -> List[str]:
        """Generate multiple images.
        
        Args:
            prompts: List of image descriptions
            height: Image height
            width: Image width
            
        Returns:
            List of image URLs
        """
        urls = []
        for i, prompt in enumerate(prompts, 1):
            logger.info(f"Batch generation {i}/{len(prompts)}")
            try:
                url = self.generate(prompt, height=height, width=width)
                urls.append(url)
            except Exception as e:
                logger.warning(f"Failed to generate image {i}: {str(e)}")
                urls.append(None)
        return urls
