"""
CLI for Fractal Low-Light Image Enhancement Suite.
"""

import argparse
import sys
import numpy as np
from PIL import Image

from core.fractal_enhancer import fractal_low_light_enhance
from core.baselines import histogram_equalization, single_scale_retinex
from core.evaluation import compute_psnr, compute_ssim, compute_entropy


def cmd_enhance(args):
    img = Image.open(args.input).convert("RGB")
    arr = np.array(img)
    print(f"[Enhancement] Memproses citra: {args.input} ({arr.shape[1]}x{arr.shape[0]})")

    out_enh = fractal_low_light_enhance(arr, gamma=args.gamma, texture_gain=args.gain)
    out_path = args.output or "sample_data/enhanced_output.png"
    Image.fromarray(out_enh).save(out_path)
    print(f"Hasil enhancement disimpan di: {out_path}")

    ent_orig = compute_entropy(arr)
    ent_enh = compute_entropy(out_enh)
    print(f"Entropi Informasi Citra Asli : {ent_orig:.3f} bits")
    print(f"Entropi Informasi Hasil      : {ent_enh:.3f} bits (Peningkatan: +{ent_enh - ent_orig:.3f})")

    if args.gt:
        gt = np.array(Image.open(args.gt).convert("RGB"))
        psnr_val = compute_psnr(gt, out_enh)
        ssim_val = compute_ssim(gt, out_enh)
        print(f"PSNR terhadap Ground Truth   : {psnr_val:.2f} dB")
        print(f"SSIM terhadap Ground Truth   : {ssim_val:.4f}")


def cmd_benchmark(args):
    from sample_data.generate_low_light import generate_low_light_pair
    dark_path, gt_path = generate_low_light_pair()

    dark = np.array(Image.open(dark_path).convert("RGB"))
    gt = np.array(Image.open(gt_path).convert("RGB"))

    he = histogram_equalization(dark)
    ssr = single_scale_retinex(dark)
    fractal = fractal_low_light_enhance(dark)

    methods = [
        ("Asli (Low-Light)", dark),
        ("Histogram Equalization (HE)", he),
        ("Single-Scale Retinex (SSR)", ssr),
        ("Fractal-Guided Retinex (Ours)", fractal),
    ]

    print("\n" + "=" * 65)
    print(f"{'Metode':<30}{'PSNR (dB)':<12}{'SSIM':<10}{'Entropy':<10}")
    print("=" * 65)
    for name, res in methods:
        p = compute_psnr(gt, res)
        s = compute_ssim(gt, res)
        e = compute_entropy(res)
        print(f"{name:<30}{p:<12.2f}{s:<10.4f}{e:<10.2f}")
    print("=" * 65 + "\n")


def cmd_gui(args):
    from gui.app import launch_gui
    launch_gui()


def main():
    p = argparse.ArgumentParser(description="Fractal Low-Light Image Enhancement")
    sub = p.add_subparsers(dest="command")

    p_enh = sub.add_parser("enhance", help="Enhance a low-light image")
    p_enh.add_argument("input", help="Input dark image")
    p_enh.add_argument("-o", "--output", help="Output enhanced path")
    p_enh.add_argument("--gt", help="Ground truth normal image for evaluation")
    p_enh.add_argument("--gamma", type=float, default=0.45, help="Gamma illumination lift (default: 0.45)")
    p_enh.add_argument("--gain", type=float, default=1.35, help="Fractal texture gain (default: 1.35)")

    sub.add_parser("benchmark", help="Run comparative benchmark on synthetic dataset")
    sub.add_parser("gui", help="Launch interactive Tkinter GUI")

    args = p.parse_args()
    if args.command == "enhance":
        cmd_enhance(args)
    elif args.command == "benchmark":
        cmd_benchmark(args)
    elif args.command == "gui":
        cmd_gui(args)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
