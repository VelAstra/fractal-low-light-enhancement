"""
Fractal-Guided Low-Light Image Enhancement Engine.
Leverages local fractal dimension to amplify subtle structural textures
while preventing noise over-amplification in uniform dark regions.
"""

from typing import Tuple
import numpy as np
from scipy.ndimage import uniform_filter

from .decomposition import decompose_illumination_reflectance


def estimate_local_roughness(image: np.ndarray, window_size: int = 5) -> np.ndarray:
    """
    Computes local intensity variance as a fast proxy for fractal roughness:
    High roughness corresponds to complex textures, low roughness corresponds to flat noise.
    """
    mean = uniform_filter(image, size=window_size)
    sq_mean = uniform_filter(image ** 2, size=window_size)
    var = np.maximum(0.0, sq_mean - mean ** 2)
    return np.sqrt(var)


def fractal_low_light_enhance(
    image: np.ndarray,
    gamma: float = 0.45,
    texture_gain: float = 1.35,
    sigma: float = 12.0
) -> np.ndarray:
    """
    Enhances a low-light grayscale or RGB image using fractal-guided illumination adjustment.
    """
    is_rgb = image.ndim == 3
    if is_rgb:
        # Convert RGB to HSV-like luminance (V channel)
        v = np.max(image, axis=2).astype(np.float32)
        illum, ref = decompose_illumination_reflectance(v, sigma=sigma)
    else:
        v = image.astype(np.float32)
        illum, ref = decompose_illumination_reflectance(v, sigma=sigma)

    # 1. Non-linear adaptive illumination enhancement (Gamma correction on L)
    enhanced_illum = np.power(illum, gamma)

    # 2. Fractal roughness guided detail enhancement on Reflectance
    roughness = estimate_local_roughness(ref, window_size=5)
    # Normalized weight [0, 1]
    weight = np.clip(roughness / (np.percentile(roughness, 90) + 1e-5), 0.0, 1.0)

    # Apply texture boost only where fractal roughness is prominent (avoids blowing up dark noise)
    enhanced_ref = ref * (1.0 + (texture_gain - 1.0) * weight)

    # 3. Reconstruct luminance
    enhanced_v = np.clip(enhanced_illum * enhanced_ref * 255.0, 0.0, 255.0)

    if is_rgb:
        # Scale RGB channels proportionally by enhanced_v / (v + eps)
        scale = enhanced_v / np.maximum(1.0, v)
        enhanced_rgb = np.clip(image * scale[:, :, np.newaxis], 0.0, 255.0).astype(np.uint8)
        return enhanced_rgb
    else:
        return enhanced_v.astype(np.uint8)
