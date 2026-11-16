"""
Quality Evaluation Metrics for Low-Light Image Enhancement.
Computes PSNR, SSIM, Information Entropy, and Contrast Gain.
"""

import math
from typing import Dict, Any
import numpy as np
from scipy.ndimage import uniform_filter


def compute_psnr(orig: np.ndarray, enhanced: np.ndarray) -> float:
    mse = np.mean((orig.astype(np.float64) - enhanced.astype(np.float64)) ** 2)
    if mse < 1e-10:
        return float("inf")
    return float(10.0 * math.log10((255.0 ** 2) / mse))


def compute_ssim(x: np.ndarray, y: np.ndarray, window_size: int = 11) -> float:
    x_f = x.astype(np.float64)
    y_f = y.astype(np.float64)

    c1 = (0.01 * 255.0) ** 2
    c2 = (0.03 * 255.0) ** 2

    mu_x = uniform_filter(x_f, size=window_size)
    mu_y = uniform_filter(y_f, size=window_size)

    mu_x_sq = mu_x ** 2
    mu_y_sq = mu_y ** 2
    mu_xy = mu_x * mu_y

    sigma_x_sq = uniform_filter(x_f ** 2, size=window_size) - mu_x_sq
    sigma_y_sq = uniform_filter(y_f ** 2, size=window_size) - mu_y_sq
    sigma_xy = uniform_filter(x_f * y_f, size=window_size) - mu_xy

    numerator = (2.0 * mu_xy + c1) * (2.0 * sigma_xy + c2)
    denominator = (mu_x_sq + mu_y_sq + c1) * (sigma_x_sq + sigma_y_sq + c2)
    return float(np.mean(numerator / (denominator + 1e-12)))


def compute_entropy(image: np.ndarray) -> float:
    """Computes Shannon Information Entropy (higher indicates richer visual information)."""
    gray = image if image.ndim == 2 else np.mean(image, axis=2).astype(np.uint8)
    hist, _ = np.histogram(gray, bins=256, range=(0, 256), density=True)
    hist = hist[hist > 0]
    return float(-np.sum(hist * np.log2(hist)))
