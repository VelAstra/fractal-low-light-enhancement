"""
Baseline Low-Light Image Enhancement Algorithms.
Provides Standard Histogram Equalization (HE) and Single-Scale Retinex (SSR) for benchmarking.
"""

import numpy as np
from scipy.ndimage import gaussian_filter


def histogram_equalization(image: np.ndarray) -> np.ndarray:
    """Standard global histogram equalization."""
    is_rgb = image.ndim == 3
    if is_rgb:
        gray = np.mean(image, axis=2).astype(np.uint8)
    else:
        gray = image.astype(np.uint8)

    hist, bins = np.histogram(gray.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_m = np.ma.masked_equal(cdf, 0)
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
    cdf_final = np.ma.filled(cdf_m, 0).astype("uint8")

    if is_rgb:
        out = np.zeros_like(image)
        for c in range(3):
            out[:, :, c] = cdf_final[image[:, :, c]]
        return out
    else:
        return cdf_final[gray]


def single_scale_retinex(image: np.ndarray, sigma: float = 15.0) -> np.ndarray:
    """Standard Single-Scale Retinex (SSR)."""
    img_f = np.maximum(1.0, image.astype(np.float32))
    blur = gaussian_filter(img_f, sigma=sigma)
    retinex = np.log10(img_f) - np.log10(np.maximum(1.0, blur))

    # Normalize to [0, 255]
    r_min = np.min(retinex)
    r_max = np.max(retinex)
    if r_max - r_min < 1e-5:
        return image
    norm = ((retinex - r_min) / (r_max - r_min) * 255.0)
    return np.clip(norm, 0, 255).astype(np.uint8)
