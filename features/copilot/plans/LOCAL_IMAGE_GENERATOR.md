# LOCAL_IMAGE_GENERATOR — Design & Implementation Plan

Status: proposal

Short summary / goal
- Provide a local-first image generation capability (text-to-image, image-to-image, and simple inpainting) that runs on the user's hardware with privacy-first defaults. The feature is aimed at developers and power users who want an easy-to-run local inference pipeline (CLI + optional lightweight UI) with clear licensing and safety controls.

Principles
- Local-first: By default, all model inference, prompts, and outputs remain local and are never sent to external services.
- Modular: Clear separation between model/engine, API service, and UI so components can be swapped or optimized independently.
- License-aware: Model weights must be selected and documented with license and usage restrictions.
- Safe-by-default: Integrate local safety checks (NSFW/illegal content filters) and opt-in behavior for higher-risk capabilities.

Recommended architecture
- Inference engine: single local process (Python) that loads model weights and exposes a small HTTP REST API for the UI/CLI.
- CLI: Minimal command-line tool for prompt-based generation and common options (seed, steps, sampler, width/height, scheduler, number of images).
- Optional UI: Small React single-page app or minimal Electron wrapper that calls the local REST API.
- Model manager: local path for model weights, optional helper to download/verify weights (explicit opt-in, show license/sha256 before download).
- Persistence: save generated images to a configurable local output directory with metadata (prompt, seed, model, timestamp).

Model & inference choices (recommendations)
- Primary family: Stable Diffusion (SD) family — SD 2.1 or SDXL depending on target quality and hardware.
  - SD 2.1: good balance for mid-range GPUs and broad compatibility.
  - SDXL: higher quality, larger memory footprint — opt-in for users with >=24GB VRAM or optimized backends.
- Inference stacks:
  - Python + PyTorch + diffusers (high developer velocity)
  - Optional ONNX / ONNX Runtime for CPU or low-memory deployments
  - Optional TensorRT or Triton for NVIDIA acceleration in performance builds
- Optimization techniques:
  - FP16 mixed precision for GPUs
  - 8-bit quantization (bitsandbytes) for lower-memory GPUs
  - Use xformers / attention optimizations if available

Software stack & dependencies
- Language: Python 3.10+
- Core libs: diffusers, transformers, accelerate, safetensors, torch (CUDA where available)
- Optional: onnxruntime, bitsandbytes, xformers, transformers
- CLI: plain Python CLI (argparse / click)
- UI: simple React app (Vite) or static HTML + fetch for the first iteration
- Packaging: Dockerfile for local container runs (optional)

Security, privacy & safety
- Default local-only operation: no calls to external APIs unless explicitly enabled by the user.
- Model downloads: explicit opt-in with displayed license and checksum; no automatic downloads.
- Safety filter: integrate a local NSFW / content classifier (e.g., CLIP-based or dedicated safety model) that blocks or flags images by default.
- Sandbox: run inference worker with limited file-system access and document recommended folder permissions.
- Rate-limiting & resource caps: protect host from runaway jobs (max concurrent jobs, memory/VRAM checks).

Licensing & legal
- Include a model license checklist in docs (for each supported model: model name, source URL, license, redistribution restrictions).
- Prefer models whose license allows local use for the intended product. Do not auto-bundle or redistribute weights without complying with license terms.

Developer plan & phased deliverables
Phase 1 — Design doc & minimal CLI prototype (2–4 days)
- Create features/copilot/plans/LOCAL_IMAGE_GENERATOR.md (this file)
- Minimal CLI prototype (prototype/cli/generate.py) that:
  - Loads a specified local model path using diffusers
  - Runs a text prompt -> image and writes output + metadata
  - Provides CPU and GPU fallback notes
  - (Optional) sample prompts + environment setup

Phase 2 — Local service + basic web UI (3–7 days)
- Add a small REST API (FastAPI/Flask) that exposes endpoints:
  - POST /generate — body: prompt, model, options -> returns job id and status
  - GET /status/{job_id} and GET /result/{job_id}
- Simple React UI for prompt entry, preview, and download
- Model selection and seed control in the UI

Phase 3 — Optimization & packaging (3–7 days)
- Add quantized/ONNX/TensorRT execution paths
- Add GPU detection and configuration (auto-fp16 when CUDA available)
- Dockerfile and docs for containerized local runs

Phase 4 — Tests, docs & release (2–4 days)
- End-to-end tests for CLI and API
- Usage docs, example prompts, and license checklist
- User-facing safety documentation and opt-in flows for higher-risk features

Hardware & performance notes
- GPU recommended: NVIDIA with CUDA. For SD2.1: 8–12GB VRAM minimum for modest sizes; SDXL benefits from 24GB+.
- CPU-only: possible with ONNX/ORT for very small models or heavy quantization; expect long runtimes.
- Offer presets: high-quality (large model, more steps), balanced, and low-memory (smaller model, fewer steps, quantized).

Files recommended to add now
- features/copilot/plans/LOCAL_IMAGE_GENERATOR.md — design & phased plan (this file)

Suggested next steps (I can do these for you)
- I can add the prototype CLI and README (prototype/cli/) and a Dockerfile. Tell me if you want SD 2.1, SDXL, or a smaller CPU-friendly model as the default in the prototype.
- I can also add a small FastAPI service and a minimal React UI if you prefer a web interface.

Notes & warnings
- This project touches on potentially sensitive areas (NSFW generation, copyrighted content). Please ensure your usage and distribution of models comply with legal / license requirements and platform policies.

---

Author: GitHub Copilot (generated plan)
Date: 2026-07-02
