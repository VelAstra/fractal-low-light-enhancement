"""
Retinex Illumination-Reflectance Decomposition Module.
Decomposes observed low-light image S into Illumination component L and Reflectance component R:
S(x, y) = L(x, y) * R(x, y)
"""

from typing import Tuple
import numpy as np
from scipy.ndimage import gaussian_filter


def decompose_illumination_reflectance(
    image: np.ndarray,
    sigma: float = 15.0
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Decomposes normalized image [0.0, 1.0] into Illumination L and Reflectance R.
    """
    img_float = np.maximum(1e-4, image.astype(np.float32) / 255.0)

    # Estimate illumination using multi-scale Gaussian smoothing
    illumination = gaussian_filter(img_float, sigma=sigma)
    illumination = np.maximum(1e-4, illumination)

    # Reflectance component in log domain
    log_r = np.log(img_float) - np.log(illumination)
    reflectance = np.exp(log_r)

    return illumination, reflectance
