# SSRF: Unvalidated URL passed to requests.get

**Tool:** `mini_audit`
**Severity:** high
**Category:** security
**Location:** `utils/image_utils.py:24`

## What's wrong

The `url` parameter in `download_image` is passed directly to `requests.get` with no validation of the scheme, host, or destination. Any caller that forwards an API-returned or user-supplied URL here can trigger requests to internal network addresses (e.g. `http://169.254.169.254/latest/meta-data/`, `http://localhost:…`). In a CLI/script context where the URL comes from an external API response or is user-controlled, this is an exploitable SSRF primitive.

**Fix:** Validate the URL before fetching: reject non-`https` schemes and resolve/blocklist private IP ranges before issuing the request.
