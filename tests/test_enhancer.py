"""
Unit and Integration Tests for Fractal Low-Light Enhancement Suite.
"""

import unittest
import numpy as np

from core.decomposition import decompose_illumination_reflectance
from core.fractal_enhancer import fractal_low_light_enhance, estimate_local_roughness
from core.baselines import histogram_equalization, single_scale_retinex
from core.evaluation import compute_psnr, compute_ssim, compute_entropy


class TestLowLightEnhancement(unittest.TestCase):

    def setUp(self):
        self.dark_img = np.full((64, 64, 3), 30, dtype=np.uint8)
        self.dark_img[20:44, 20:44] = 70

    def test_decomposition(self):
        gray = self.dark_img[:, :, 0]
        illum, ref = decompose_illumination_reflectance(gray)
        self.assertEqual(illum.shape, (64, 64))
        self.assertEqual(ref.shape, (64, 64))
        self.assertTrue(np.all(illum > 0))

    def test_fractal_enhancement(self):
        enhanced = fractal_low_light_enhance(self.dark_img)
        self.assertEqual(enhanced.shape, self.dark_img.shape)
        # Enhanced image should be brighter on average
        self.assertGreater(float(np.mean(enhanced)), float(np.mean(self.dark_img)))

    def test_baselines(self):
        he = histogram_equalization(self.dark_img)
        ssr = single_scale_retinex(self.dark_img)
        self.assertEqual(he.shape, self.dark_img.shape)
        self.assertEqual(ssr.shape, self.dark_img.shape)

    def test_evaluation(self):
        ent_dark = compute_entropy(self.dark_img)
        enhanced = fractal_low_light_enhance(self.dark_img)
        ent_enh = compute_entropy(enhanced)
        # Enhanced should possess higher information entropy
        self.assertGreater(ent_enh, ent_dark)


if __name__ == "__main__":
    unittest.main()
