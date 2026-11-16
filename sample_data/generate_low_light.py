"""
Low-Light Synthetic Benchmark Image Pair Generator.
Creates ground-truth well-lit image and degraded dark low-light counterpart.
"""

import os
from typing import Tuple
import numpy as np
from PIL import Image, ImageDraw


def generate_low_light_pair(
    size: int = 256,
    filepath_dark: str = "sample_data/dark.png",
    filepath_gt: str = "sample_data/gt_normal.png"
) -> Tuple[str, str]:
    os.makedirs(os.path.dirname(filepath_dark), exist_ok=True)

    # 1. Create well-lit ground truth scene with shapes, text, gradients
    img = Image.new("RGB", (size, size), color=(210, 220, 230))
    draw = ImageDraw.Draw(img)

    draw.rectangle([30, 40, 110, 160], fill=(180, 50, 50), outline=(30, 30, 30), width=2)
    draw.ellipse([140, 50, 220, 130], fill=(50, 130, 180), outline=(20, 20, 20), width=2)
    draw.rectangle([50, 180, 200, 220], fill=(60, 160, 80), outline=(20, 20, 20), width=2)

    gt_arr = np.array(img, dtype=np.float32)

    # 2. Simulate non-uniform low-light degradation (Gamma 2.8 + non-uniform illumination gradient)
    y, x = np.mgrid[0:size, 0:size]
    illum_vignette = 0.15 + 0.25 * (1.0 - np.sqrt((x - size/2)**2 + (y - size/2)**2) / (size * 0.707))
    illum_vignette = np.clip(illum_vignette, 0.08, 0.35)[:, :, np.newaxis]

    dark_arr = ((gt_arr / 255.0) ** 1.8) * illum_vignette * 255.0
    # Add slight Poisson/Gaussian sensor noise
    rng = np.random.default_rng(42)
    noise = rng.normal(0, 3.0, dark_arr.shape)
    dark_arr = np.clip(dark_arr + noise, 0, 255).astype(np.uint8)

    Image.fromarray(gt_arr.astype(np.uint8)).save(filepath_gt)
    Image.fromarray(dark_arr).save(filepath_dark)

    return filepath_dark, filepath_gt


if __name__ == "__main__":
    d, g = generate_low_light_pair()
    print(f"Generated low light pair: {d} and {g}")
