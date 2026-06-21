"""Unit tests for image generators"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from generators import DALLEGenerator, GeminiGenerator, FluxGenerator
from utils.config import Config


class TestDALLEGenerator:
    """Test DALL-E generator"""

    @pytest.fixture
    def generator(self):
        """Create test generator with mock API key"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            return DALLEGenerator(api_key="test-key")

    def test_initialization(self, generator):
        """Test generator initialization"""
        assert generator.api_key == "test-key"
        assert generator.model == "dall-e-3"

    def test_cache_hit(self, generator):
        """Test cache functionality"""
        prompt = "Test prompt"
        url = "https://example.com/image.png"
        
        cache_key = f"dalle_{prompt}_1024x1024_standard"
        generator._set_cache(cache_key, url)
        
        cached = generator._get_cached(cache_key)
        assert cached == url


class TestGeminiGenerator:
    """Test Gemini generator"""

    @pytest.fixture
    def generator(self):
        """Create test generator with mock API key"""
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"}):
            return GeminiGenerator(api_key="test-key")

    def test_initialization(self, generator):
        """Test generator initialization"""
        assert generator.api_key == "test-key"
        assert generator.model is not None


class TestFluxGenerator:
    """Test Flux generator"""

    @pytest.fixture
    def generator(self):
        """Create test generator with mock API key"""
        with patch.dict(os.environ, {"FLUX_API_KEY": "test-key"}):
            return FluxGenerator(api_key="test-key")

    def test_initialization(self, generator):
        """Test generator initialization"""
        assert generator.api_key == "test-key"
        assert generator.model == "flux-pro"


class TestConfig:
    """Test configuration"""

    def test_config_defaults(self):
        """Test default configuration values"""
        assert Config.LOG_LEVEL == "INFO"
        assert Config.BATCH_SIZE == 5
        assert Config.MAX_RETRIES == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
