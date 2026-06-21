"""Base Image Generator Abstract Class"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from utils.logger import get_logger

logger = get_logger(__name__)


class BaseImageGenerator(ABC):
    """Abstract base class for image generators"""

    def __init__(self, api_key: str, timeout: int = 30):
        """Initialize base generator.
        
        Args:
            api_key: API key for the service
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.cache: Dict[str, str] = {}

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate an image from a prompt.
        
        Args:
            prompt: Text description of desired image
            **kwargs: Provider-specific parameters
            
        Returns:
            URL of generated image
        """
        pass

    @abstractmethod
    def generate_batch(self, prompts: List[str], **kwargs) -> List[str]:
        """Generate multiple images from prompts.
        
        Args:
            prompts: List of text descriptions
            **kwargs: Provider-specific parameters
            
        Returns:
            List of image URLs
        """
        pass

    def _get_cached(self, key: str) -> Optional[str]:
        """Retrieve cached result."""
        return self.cache.get(key)

    def _set_cache(self, key: str, value: str) -> None:
        """Cache a result."""
        self.cache[key] = value

    def _log_generation(self, prompt: str, url: str) -> None:
        """Log successful generation."""
        logger.info(f"Generated image: {prompt[:50]}... -> {url}")
