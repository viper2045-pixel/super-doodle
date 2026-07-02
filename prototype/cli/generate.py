#!/usr/bin/env python3
"""
Minimal CLI prototype: text -> image using Diffusers (Stable Diffusion 2.1 by default).

Usage example:
  python generate.py "a cute cartoon dog riding a skateboard" --outdir outputs --steps 30

Notes:
- Default model: stabilityai/stable-diffusion-2-1 (change with --model).
- GPU (CUDA) is used automatically if available. For GPUs we attempt fp16 for lower memory use.
- This is a minimal prototype and does NOT include a safety checker or advanced optimizations.
  Use for local experimentation only and obey model license terms.
"""

import argparse
import os
import json
import time
import uuid
from datetime import datetime

import torch
from diffusers import DiffusionPipeline


def parse_args():
    p = argparse.ArgumentParser(description="Minimal text->image CLI prototype")
    p.add_argument("prompt", type=str, help="Text prompt to generate an image from")
    p.add_argument("--model", type=str, default="stabilityai/stable-diffusion-2-1",
                   help="Pretrained model id or local path (default: stabilityai/stable-diffusion-2-1)")
    p.add_argument("--outdir", type=str, default="outputs", help="Directory to save images")
    p.add_argument("--steps", type=int, default=30, help="Number of inference steps")
    p.add_argument("--width", type=int, default=512, help="Image width")
    p.add_argument("--height", type=int, default=512, help="Image height")
    p.add_argument("--seed", type=int, default=None, help="RNG seed (optional)")
    p.add_argument("--num_images", type=int, default=1, help="How many images to generate")
    p.add_argument("--device", type=str, choices=["auto", "cpu", "cuda"], default="auto",
                   help="Device to run on (auto detects CUDA)")
    return p.parse_args()


def ensure_outdir(path):
    os.makedirs(path, exist_ok=True)


def load_pipeline(model_id: str, device: torch.device):
    # Choose dtype: use fp16 on CUDA to save memory
    torch_dtype = torch.float16 if (device.type == "cuda") else torch.float32
    print(f"Loading pipeline from {model_id} with dtype={torch_dtype} on {device}")
    pipeline = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch_dtype)
    pipeline = pipeline.to(device)

    # Try to enable some optional speedups if available
    try:
        pipeline.enable_xformers_memory_efficient_attention()
        print("Enabled xFormers memory efficient attention")
    except Exception:
        pass

    return pipeline


def save_image_with_metadata(image, outdir, meta):
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    uid = uuid.uuid4().hex[:8]
    filename = f"img_{ts}_{uid}.png"
    path = os.path.join(outdir, filename)
    image.save(path)

    # write metadata
    meta_path = path + ".json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    return path, meta_path


def main():
    args = parse_args()

    # Device selection
    if args.device == "auto":
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(args.device)

    ensure_outdir(args.outdir)

    pipeline = None
    try:
        pipeline = load_pipeline(args.model, device)
    except Exception as e:
        print("Failed to load model pipeline:", e)
        return

    # Generator
    generator = None
    if args.seed is not None:
        # Generator device must match pipeline device
        gen_device = "cpu" if device.type == "cpu" else device
        generator = torch.Generator(device=gen_device).manual_seed(args.seed)

    print("Generating...")
    start = time.time()
    try:
        output = pipeline(
            prompt=args.prompt,
            num_inference_steps=args.steps,
            guidance_scale=7.5,
            height=args.height,
            width=args.width,
            num_images_per_prompt=args.num_images,
            generator=generator,
        )
    except Exception as e:
        print("Generation failed:", e)
        return

    elapsed = time.time() - start
    images = output.images

    saved = []
    for i, img in enumerate(images):
        meta = {
            "prompt": args.prompt,
            "model": args.model,
            "steps": args.steps,
            "width": args.width,
            "height": args.height,
            "seed": args.seed,
            "index": i,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "elapsed_seconds": elapsed,
        }
        img_path, meta_path = save_image_with_metadata(img, args.outdir, meta)
        saved.append({"image": img_path, "meta": meta_path})
        print(f"Saved image: {img_path}")

    print("Done. Generated images:")
    for s in saved:
        print(" -", s["image"], "(meta:", s["meta"], ")")


if __name__ == "__main__":
    main()
