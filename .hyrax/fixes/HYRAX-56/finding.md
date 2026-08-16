# Undeclared, heavyweight runtime dependencies (torch, diffusers) used in prototype/cli/generate.py but absent from requirements.txt

**Tool:** `deps`
**Severity:** high
**Category:** operations
**Location:** `prototype/cli/generate.py:22`

## What's wrong

`prototype/cli/generate.py` imports and directly depends on `torch` and `diffusers` (`from diffusers import DiffusionPipeline`, `import torch`, calls to `torch.cuda.is_available()`, `torch.Generator`, `pipeline.enable_xformers_memory_efficient_attention()`) but neither `torch`, `diffusers`, nor `xformers` appear anywhere in `requirements.txt`. This is the CLI entry point documented in the project conventions as the canonical three-stage pipeline (`parse_args` → `load_pipeline` → `save_image_with_metadata`).

Anyone following `requirements.txt` to set up the project will have a working `generators/` package (DALL-E, Gemini, Flux API clients) but the local CLI prototype will fail immediately with `ModuleNotFoundError: No module named 'torch'`. This is a functional break, not just a style nit — the documented entry point is unusable from a clean install.

Conversely, since `torch`/`diffusers` were never added to the manifest, there's no version constraint governing them at all — whatever happens to be present in a dev's environment is used, with no reproducibility guarantee once they are eventually added.

## What changed

Add `torch` and `diffusers` (and `xformers` as an optional extra, since it's wrapped in a try/except) to `requirements.txt` with appropriate version pins, e.g. as a separate `requirements-local.txt` or an `[project.optional-dependencies]` extra (`local-gen = ["torch>=2.1.0", "diffusers>=0.24.0"]`) since these are large ML dependencies not needed by the primary API-based generators.
