# Getting Started - API Keys & Setup Guide

This guide walks you through obtaining API keys for each image generation provider and getting your project running.

## 📋 Table of Contents
1. [OpenAI DALL-E 3](#openai-dalle-3)
2. [Google Gemini](#google-gemini)
3. [Black Forest Labs Flux](#black-forest-labs-flux)
4. [Environment Setup](#environment-setup)
5. [First Generation](#first-generation)
6. [Troubleshooting](#troubleshooting)

---

## 🔑 OpenAI DALL-E 3

### Get Your API Key

1. **Go to OpenAI Platform**
   - Visit: https://platform.openai.com/account/api-keys
   - Sign in with your OpenAI account (create one if needed)

2. **Create API Key**
   - Click "Create new secret key"
   - Name it (e.g., "Image Generation")
   - Copy the key immediately (you won't see it again!)

3. **Check Your Billing**
   - Go to: https://platform.openai.com/account/billing/overview
   - Ensure you have credits or a payment method on file
   - DALL-E 3 costs ~$0.04-0.05 per image

### Pricing
- **Standard**: $0.04 per image (1024x1024)
- **HD**: $0.08 per image (higher quality)
- **Larger sizes**: $0.12 per image (1792x1024 or 1024x1792)

### Example .env Entry
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_ORG_ID=org-xxxxxxxxxxxxxxxxxx  # Optional
```

---

## 🌐 Google Gemini

### Get Your API Key

1. **Visit Google AI Studio**
   - Go to: https://aistudio.google.com/app/apikey
   - Sign in with your Google account

2. **Create API Key**
   - Click "Create API Key"
   - Select "Create API key in new project" or use existing project
   - Copy your API key

3. **Enable Gemini API**
   - The API is automatically enabled for new keys
   - No billing required for basic usage (100 free images/day)

### Pricing & Limits
- **Free Tier**: 100 images/day (quota resets daily)
- **Paid Tier**: ~$0.001-0.002 per image after free tier
- **Speed**: Very fast (1-3 seconds per image)
- **Best for**: Photorealism, development/testing

### Example .env Entry
```env
GOOGLE_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Start Free (Recommended for Testing)
```python
from generators import GeminiGenerator

generator = GeminiGenerator()
# Get 100 free images today!
url = generator.generate("A beautiful sunset")
```

---

## ⚡ Black Forest Labs Flux

### Get Your API Key

1. **Visit Black Forest Labs**
   - Go to: https://blackforestlabs.ai/
   - Sign up for an account

2. **Generate API Key**
   - Go to your account dashboard
   - Navigate to "API Keys"
   - Click "Generate New Key"
   - Copy and save securely

3. **Add Billing**
   - Add a payment method to your account
   - Flux charges per image generated

### Pricing
- **Flux Pro**: $0.03-0.06 per image
- **Flux Max**: $0.24 per image (higher quality)
- **Speed**: Fast (10-20 seconds)
- **Best for**: Photorealism, anatomical accuracy

### Example .env Entry
```env
FLUX_API_KEY=fk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FLUX_ENDPOINT=https://api.blackforestlabs.ai
```

---

## 🔧 Environment Setup

### Step 1: Clone & Navigate
```bash
git clone https://github.com/viper2045-pixel/super-doodle.git
cd super-doodle
```

### Step 2: Create Virtual Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Create .env File
```bash
# Copy the example template
cp .env.example .env

# Open with your editor (choose one)
nano .env           # Linux/macOS
code .env           # VS Code
vim .env            # Vim
```

### Step 5: Add Your API Keys

Edit `.env` and replace with your actual keys:

```env
# OpenAI (for DALL-E 3)
OPENAI_API_KEY=sk-proj-your-actual-key-here

# Google (for Gemini - FREE!)
GOOGLE_API_KEY=AIzaSy-your-actual-key-here

# Flux (optional)
FLUX_API_KEY=fk-your-actual-key-here

# Application Settings (keep as is)
IMAGE_OUTPUT_DIR=./generated_images
LOG_LEVEL=INFO
```

### ⚠️ Security Tips
- **Never commit .env** - Already in `.gitignore`
- **Never share your keys** - Treat them like passwords
- **Rotate keys** - Regularly regenerate in provider dashboards
- **Use environment variables** - On production servers, use proper secrets management

---

## 🚀 First Generation

### Option 1: Quick Start (Easiest)

```bash
# Make sure your .env is configured
# Run the basic example
python examples/basic_generation.py
```

**Output:**
```
2026-06-21 10:30:45 - __main__ - INFO - Starting basic image generation examples...
2026-06-21 10:30:45 - __main__ - INFO - === DALL-E 3 Generation ===
2026-06-21 10:30:48 - __main__ - INFO - Generated image: https://oaidalleapiproduc...
2026-06-21 10:30:48 - __main__ - INFO - === Google Gemini Generation ===
2026-06-21 10:30:50 - __main__ - INFO - Generated image: gemini_image_url_...
2026-06-21 10:30:50 - __main__ - INFO - === Generation Summary ===
✓ dalle: https://oaidalleapiproduc...
✓ gemini: gemini_image_url_...
```

### Option 2: Interactive Python Shell

```bash
# Start Python interactive shell
python

# Import and use
>>> from generators import DALLEGenerator
>>> generator = DALLEGenerator()
>>> url = generator.generate("A serene mountain landscape at sunset")
>>> print(url)
https://oaidalleapiproduc...

# Try Gemini (free!)
>>> from generators import GeminiGenerator
>>> gemini = GeminiGenerator()
>>> url = gemini.generate("A futuristic city")
>>> print(url)
gemini_image_url_...

# Exit
>>> exit()
```

### Option 3: Batch Generation

```bash
# Generate multiple images at once
python examples/batch_generation.py
```

**Features:**
- Generates 5 landscape images
- Generates 5 character designs
- Saves results to `generated_images/batch_results.json`
- Shows success rate and statistics

### Option 4: Advanced Prompts

```bash
# Generate with detailed prompts
python examples/advanced_prompts.py
```

**Includes:**
- Fantasy landscape generation
- Product photography
- Character concept art
- Professional prompt engineering

---

## 💻 Code Examples

### Example 1: Simple Generation
```python
from generators import DALLEGenerator

# Initialize
generator = DALLEGenerator()

# Generate image
url = generator.generate(
    prompt="A golden retriever playing in a sunny park",
    size="1024x1024",
    quality="standard"
)

print(f"Image: {url}")
```

### Example 2: Using Free Gemini
```python
from generators import GeminiGenerator

# Initialize (uses free tier by default)
generator = GeminiGenerator()

# Generate - you have 100 free images today!
url = generator.generate("A futuristic cityscape")
print(f"Free image: {url}")
```

### Example 3: Batch Processing
```python
from generators import ImageGeneratorBatch
import os

# Create batch generator
batch = ImageGeneratorBatch(provider="openai")

# Define prompts
prompts = [
    "A peaceful forest",
    "A busy marketplace",
    "A snow-covered mountain"
]

# Generate batch
results = batch.generate_batch(
    prompts=prompts,
    output_dir="./my_images",
    num_retries=3
)

# View results
for result in results:
    print(f"✓ {result['prompt']}: {result['url']}")
```

### Example 4: Error Handling
```python
from generators import DALLEGenerator

generator = DALLEGenerator()

try:
    url = generator.generate("Your prompt here")
    print(f"Success: {url}")
except ValueError as e:
    print(f"Invalid input: {e}")
except Exception as e:
    print(f"Generation failed: {e}")
```

---

## 📊 Comparison: Which Provider to Use?

| Provider | Cost | Speed | Quality | Best For | Free Trial |
|----------|------|-------|---------|----------|-----------|
| **DALL-E 3** | $0.04-0.12 | Medium | Excellent | Professional, marketing | No |
| **Gemini** | Free (100/day) | Very Fast | Good | Development, testing | ✓ Yes |
| **Flux** | $0.03-0.24 | Fast | Very Good | Photorealism, custom | No |

### 🎯 Recommendation for Beginners
1. **Start with Gemini** (free, 100 images/day)
2. **Test with Gemini** until you understand the system
3. **Move to DALL-E 3** for production use
4. **Use Flux** when you need photorealism

---

## 🐛 Troubleshooting

### Problem: "API Key not found"
**Solution:**
```bash
# Check if .env file exists
ls -la .env

# Verify key is in .env
grep OPENAI_API_KEY .env

# Check Python can read it
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

### Problem: "Invalid API Key"
**Solution:**
- Verify you copied the entire key (no extra spaces)
- Ensure the key hasn't been regenerated (old key is invalid)
- Check you're using the correct key for the provider
- Make sure you included the `sk-` or `AIzaSy-` prefix

### Problem: "Rate Limited"
**Solution:**
```python
# The batch generator handles this automatically
# For manual handling, add delays:
import time
from generators import DALLEGenerator

generator = DALLEGenerator()
for prompt in prompts:
    url = generator.generate(prompt)
    time.sleep(2)  # Wait 2 seconds between requests
```

### Problem: "Import Error: No module named 'openai'"
**Solution:**
```bash
# Make sure you installed dependencies
pip install -r requirements.txt

# Or install specific package
pip install openai
```

### Problem: ".env file not being read"
**Solution:**
```python
# Make sure you import load_dotenv
from dotenv import load_dotenv
import os

load_dotenv()  # Call this first!
api_key = os.getenv('OPENAI_API_KEY')
```

### Problem: "No space left on device" (generating images)
**Solution:**
```bash
# Check disk space
df -h

# Clear cache if needed
rm -rf ./cache/generated_images/
```

---

## 📚 Next Steps

1. **Generate your first image** - Run `python examples/basic_generation.py`
2. **Explore providers** - Try each one and compare results
3. **Build a project** - Create your own generation script
4. **Batch process** - Generate multiple images efficiently
5. **Optimize prompts** - Learn advanced prompt engineering
6. **Deploy** - Run on a server or integrate into an app

---

## 🔗 Useful Links

- **OpenAI API Docs**: https://platform.openai.com/docs/guides/images
- **Google Gemini Docs**: https://ai.google.dev/
- **Black Forest Labs Flux**: https://blackforestlabs.ai/
- **Prompt Engineering Guide**: https://platform.openai.com/docs/guides/prompt-engineering

---

## ❓ Questions?

Check the main [README.md](./README.md) for more documentation or review the [examples/](./examples/) directory for more code samples.

**Happy generating! 🎨✨**
