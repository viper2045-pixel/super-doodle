# Gemini generator returns stub string instead of real API result

**Tool:** `mini_audit`
**Severity:** critical
**Category:** correctness
**Location:** `generators/gemini_generator.py:57`

## What's wrong

The `generate` method constructs and returns a fake placeholder string `gemini_image_url_<timestamp>` rather than calling the Gemini API. The `genai.GenerativeModel` is instantiated but never called. Any downstream code that treats this return value as a real image URL will silently fail (404s on download, invalid metadata saved to disk).

**Fix:** Replace the stub with an actual call to `self.model.generate_content(prompt)` and extract the real image URL/data from the response.
