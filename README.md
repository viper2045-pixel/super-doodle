# AI Image Generation Integration

A comprehensive Python project integrating multiple AI image generation APIs including OpenAI DALL-E 3, Google Gemini, Midjourney, and Flux.

## Features

- 🎨 Multi-provider API integration (DALL-E 3, Gemini, Flux, Midjourney)
- 🔧 Easy-to-use wrapper functions
- 📝 Configuration management via environment variables
- 🚀 Batch image generation support
- 📊 Logging and error handling
- 🧪 Example scripts for each provider

## Supported Providers

| Provider | Model | Speed | Cost | Text Rendering | Best For |
|----------|-------|-------|------|-----------------|----------|
| OpenAI | DALL-E 3 | Medium | $0.04-0.05/img | Excellent | Professional, marketing |
| Google | Nano Banana 2 | Very Fast | Free (100/day) | Good | Photorealism, batches |
| Black Forest Labs | Flux 2 | Fast | $0.02-0.06/img | Good | Realism, custom workflows |
| Midjourney | V8 | Medium | Subscription | Good | Artistic, concept art |

## Installation

### Prerequisites

- Python 3.9+
- pip or poetry

### Setup

1. Clone the repository:
```bash
git clone https://github.com/viper2045-pixel/super-doodle.git
cd super-doodle
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Environment Variables

```bash
# OpenAI
OPENAI_API_KEY=your_openai_key

# Google Gemini
GOOGLE_API_KEY=your_google_key

# Flux (Black Forest Labs)
FLUX_API_KEY=your_flux_key

# Midjourney (Discord webhook or API)
MIDJOURNEY_API_KEY=your_midjourney_key

# Output settings
IMAGE_OUTPUT_DIR=./generated_images
LOG_LEVEL=INFO
```

## Quick Start

### 1. Generate Image with DALL-E 3

```python
from generators import DALLEGenerator

generator = DALLEGenerator()
image_url = generator.generate("A serene mountain landscape at sunset, oil painting style")
print(f"Generated image: {image_url}")
```

### 2. Generate Image with Google Gemini

```python
from generators import GeminiGenerator

generator = GeminiGenerator()
image_url = generator.generate("A futuristic city with flying cars and neon lights")
print(f"Generated image: {image_url}")
```

### 3. Generate Image with Flux

```python
from generators import FluxGenerator

generator = FluxGenerator()
image_url = generator.generate("A hyperrealistic portrait of a woman in cyberpunk armor")
print(f"Generated image: {image_url}")
```

### 4. Batch Generation

```python
from generators import ImageGeneratorBatch

prompts = [
    "A peaceful forest with sunlight through trees",
    "A bustling marketplace in ancient Rome",
    "A cozy cabin in winter with smoke from chimney"
]

batch = ImageGeneratorBatch(provider="openai")
results = batch.generate_batch(prompts)

for prompt, image_url in zip(prompts, results):
    print(f"Prompt: {prompt}")
    print(f"URL: {image_url}\n")
```

## Project Structure

```
super-doodle/
├── README.md
├── requirements.txt
├── .env.example
├── generators/
│   ├── __init__.py
│   ├── base.py              # Base generator class
│   ├── openai_generator.py  # DALL-E 3 implementation
│   ├── gemini_generator.py  # Google Gemini implementation
│   ├── flux_generator.py    # Flux implementation
│   └── batch_generator.py   # Batch processing
├── utils/
│   ├── __init__.py
│   ├── config.py            # Configuration management
│   ├── logger.py            # Logging setup
│   └── image_utils.py       # Helper functions
├── examples/
│   ├── basic_generation.py
│   ├── batch_generation.py
│   ├── advanced_prompts.py
│   └── comparison.py
└── tests/
    ├── __init__.py
    └── test_generators.py
```

## Usage Examples

### Example 1: Basic Image Generation

```python
# examples/basic_generation.py
from generators import DALLEGenerator

def main():
    generator = DALLEGenerator()
    
    # Simple generation
    url = generator.generate(
        prompt="A golden retriever playing in a sunny park",
        size="1024x1024",
        quality="hd"
    )
    print(f"Image generated: {url}")

if __name__ == "__main__":
    main()
```

### Example 2: Batch Processing

```python
# examples/batch_generation.py
from generators import ImageGeneratorBatch
import json

def main():
    prompts = [
        "A modern office with panoramic city views",
        "A traditional Japanese garden with koi pond",
        "A futuristic space station interior"
    ]
    
    batch = ImageGeneratorBatch(provider="gemini")
    results = batch.generate_batch(
        prompts=prompts,
        num_retries=3,
        output_dir="./generated_images"
    )
    
    # Save results metadata
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
```

### Example 3: Advanced Prompting

```python
# examples/advanced_prompts.py
from generators import FluxGenerator
from utils.logger import get_logger

logger = get_logger(__name__)

ADVANCED_PROMPTS = [
    {
        "base": "A cyberpunk street scene",
        "style": "neon lights, rain-wet streets, high contrast",
        "quality": "hyperrealistic, 4K, cinematic lighting"
    },
    {
        "base": "A fantasy dragon",
        "style": "oil painting, Renaissance style",
        "quality": "intricate scales, dramatic lighting"
    }
]

def craft_prompt(prompt_config):
    """Craft detailed prompt from components"""
    return f"{prompt_config['base']}, {prompt_config['style']}, {prompt_config['quality']}"

def main():
    generator = FluxGenerator()
    
    for prompt_config in ADVANCED_PROMPTS:
        full_prompt = craft_prompt(prompt_config)
        logger.info(f"Generating: {full_prompt}")
        
        url = generator.generate(full_prompt)
        logger.info(f"Result: {url}")

if __name__ == "__main__":
    main()
```

## API Reference

### DALLEGenerator

```python
generator = DALLEGenerator()

# Generate single image
url = generator.generate(
    prompt="Your prompt here",
    size="1024x1024",  # or "1792x1024", "1024x1792"
    quality="standard"  # or "hd"
)

# Generate multiple variations
urls = generator.generate_variations(prompt, num_variations=4)
```

### GeminiGenerator

```python
generator = GeminiGenerator()

# Generate image
url = generator.generate(
    prompt="Your prompt here",
    model="gemini-pro-vision"
)

# Batch with retries
urls = generator.generate_batch(prompts, max_retries=3)
```

### FluxGenerator

```python
generator = FluxGenerator()

# Generate with custom parameters
url = generator.generate(
    prompt="Your prompt here",
    height=1024,
    width=1024,
    num_inference_steps=20
)
```

## Error Handling

```python
from generators import DALLEGenerator
from generators.exceptions import GenerationError, RateLimitError

generator = DALLEGenerator()

try:
    url = generator.generate("A beautiful sunset")
except RateLimitError:
    print("Rate limited! Please wait before retrying.")
except GenerationError as e:
    print(f"Generation failed: {e}")
```

## Performance Tips

1. **Batch Processing**: Use batch generation for multiple images
2. **Caching**: Results are cached to avoid duplicate API calls
3. **Provider Selection**: Choose based on speed/cost/quality needs
4. **Prompt Engineering**: More detailed prompts yield better results

## Pricing Comparison

| Provider | Cost | Notes |
|----------|------|-------|
| OpenAI DALL-E 3 | $0.04-0.05/image | High quality, excellent prompt adherence |
| Google Gemini | Free (100/day limit) | Fast, great for development |
| Flux 2 | $0.02-0.06/image | Good balance of speed and quality |
| Midjourney | $10-120/month | Subscription-based, artistic focus |

## Troubleshooting

### Issue: "API Key not found"
- Ensure `.env` file exists with `API_KEY=your_key`
- Check that environment variables are loaded: `python -c "import os; print(os.getenv('OPENAI_API_KEY'))"`

### Issue: Rate limiting
- Implement exponential backoff (handled automatically in batch generator)
- Reduce batch size or add delays between requests

### Issue: Poor image quality
- Refine your prompt with more descriptive details
- Specify art style, lighting, and composition
- Test with different providers

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Resources

- [OpenAI DALL-E Documentation](https://platform.openai.com/docs/guides/images)
- [Google Gemini API](https://ai.google.dev/)
- [Black Forest Labs Flux](https://blackforestlabs.ai/)
- [Midjourney Documentation](https://docs.midjourney.com/)

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Last Updated**: June 21, 2026
