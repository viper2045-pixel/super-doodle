"""Batch Image Generation Handler"""

from typing import List, Optional, Dict
from generators.openai_generator import DALLEGenerator
from generators.gemini_generator import GeminiGenerator
from generators.flux_generator import FluxGenerator
from utils.logger import get_logger
import json
import os

logger = get_logger(__name__)


class ImageGeneratorBatch:
    """Handle batch image generation across providers"""

    PROVIDERS = {
        "openai": DALLEGenerator,
        "gemini": GeminiGenerator,
        "flux": FluxGenerator,
    }

    def __init__(self, provider: str = "openai"):
        """Initialize batch generator.
        
        Args:
            provider: Image generation provider (openai, gemini, flux)
        """
        if provider not in self.PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}")
        
        self.provider_name = provider
        self.generator = self.PROVIDERS[provider]()
        logger.info(f"Initialized batch generator with {provider}")

    def generate_batch(
        self,
        prompts: List[str],
        output_dir: Optional[str] = None,
        num_retries: int = 3,
        save_metadata: bool = True,
    ) -> List[Dict]:
        """Generate batch of images with metadata.
        
        Args:
            prompts: List of image descriptions
            output_dir: Directory to save metadata
            num_retries: Number of retries per prompt
            save_metadata: Whether to save results to JSON
            
        Returns:
            List of result dictionaries with prompt and URL
        """
        if output_dir is None:
            output_dir = os.getenv("IMAGE_OUTPUT_DIR", "./generated_images")
        
        os.makedirs(output_dir, exist_ok=True)
        results = []

        logger.info(f"Starting batch generation: {len(prompts)} prompts")

        for i, prompt in enumerate(prompts, 1):
            logger.info(f"Processing {i}/{len(prompts)}: {prompt[:50]}...")
            
            url = None
            for attempt in range(num_retries):
                try:
                    url = self.generator.generate(prompt)
                    break
                except Exception as e:
                    logger.warning(
                        f"Attempt {attempt + 1}/{num_retries} failed: {str(e)}"
                    )
                    if attempt < num_retries - 1:
                        import time
                        wait_time = 2 ** (attempt + 1)
                        logger.info(f"Waiting {wait_time}s before retry...")
                        time.sleep(wait_time)

            result = {
                "index": i,
                "prompt": prompt,
                "url": url,
                "status": "success" if url else "failed",
                "provider": self.provider_name,
            }
            results.append(result)

        # Save metadata
        if save_metadata:
            metadata_file = os.path.join(output_dir, "batch_results.json")
            with open(metadata_file, "w") as f:
                json.dump(results, f, indent=2)
            logger.info(f"Saved metadata to {metadata_file}")

        # Summary
        successful = sum(1 for r in results if r["status"] == "success")
        logger.info(
            f"Batch complete: {successful}/{len(prompts)} images generated"
        )

        return results
