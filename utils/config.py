"""Configuration management"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


class Config:
    """Application configuration"""

    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    FLUX_API_KEY = os.getenv("FLUX_API_KEY")
    MIDJOURNEY_API_KEY = os.getenv("MIDJOURNEY_API_KEY")

    # Endpoints
    FLUX_ENDPOINT = os.getenv("FLUX_ENDPOINT", "https://api.blackforestlabs.ai")

    # Application
    IMAGE_OUTPUT_DIR = os.getenv("IMAGE_OUTPUT_DIR", "./generated_images")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "app.log")

    # Batch Processing
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "5"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "2"))

    # Cache
    ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    CACHE_DIR = os.getenv("CACHE_DIR", "./cache")
    CACHE_EXPIRY_HOURS = int(os.getenv("CACHE_EXPIRY_HOURS", "24"))

    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.OPENAI_API_KEY:
            print("Warning: OPENAI_API_KEY not set")
        if not cls.GOOGLE_API_KEY:
            print("Warning: GOOGLE_API_KEY not set")
