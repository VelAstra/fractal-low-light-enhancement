"""
Interactive GUI for Fractal Low-Light Image Enhancement.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from PIL import Image, ImageTk

from core.fractal_enhancer import fractal_low_light_enhance
from core.baselines import histogram_equalization, single_scale_retinex
from core.evaluation import compute_entropy


class LowLightApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fractal-Guided Low-Light Image Enhancement")
        self.geometry("1000x650")
        self.configure(bg="#0B0F19")

        self.dark_arr = None

        self._build_ui()
        sample = os.path.join(os.path.dirname(__file__), "..", "sample_data", "dark.png")
        if os.path.exists(sample):
            self.load_image(os.path.abspath(sample))

    def _build_ui(self):
        header = tk.Frame(self, bg="#1E293B", height=60, padx=20)
        header.pack(fill=tk.X)
        tk.Label(header, text="FRACTAL-GUIDED LOW-LIGHT ENHANCEMENT", font=("Segoe UI", 14, "bold"), fg="#38BDF8", bg="#1E293B").pack(anchor="w", pady=(10, 0))
        tk.Label(header, text="Peningkatan Citra Pencahayaan Rendah dengan Pelestarian Tekstur Fraktal", font=("Segoe UI", 9), fg="#94A3B8", bg="#1E293B").pack(anchor="w")

        tools = tk.Frame(self, bg="#0B0F19", padx=15, pady=8)
        tools.pack(fill=tk.X)
        ttk.Button(tools, text="Pilih Citra Gelap...", command=self.on_browse).pack(side=tk.LEFT, padx=5)
        ttk.Button(tools, text="Jalankan Enhancement Fraktal", command=self.on_enhance).pack(side=tk.LEFT, padx=5)

        views = tk.Frame(self, bg="#0B0F19")
        views.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        self.lbl_orig = self._create_panel(views, "Citra Asli (Low-Light)")
        self.lbl_enh = self._create_panel(views, "Hasil Fractal-Guided Retinex")

        self.status = tk.Label(self, text="Siap.", bg="#1E293B", fg="#F8FAFC", anchor="w", padx=10, font=("Segoe UI", 9))
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    def _create_panel(self, parent, title):
        f = tk.Frame(parent, bg="#1E293B", relief="groove", bd=1)
        f.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(f, text=title, font=("Segoe UI", 10, "bold"), bg="#1E293B", fg="#38BDF8").pack(pady=4)
        lbl = tk.Label(f, bg="#020617")
        lbl.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        return lbl

    def load_image(self, path):
        img = Image.open(path).convert("RGB")
        self.dark_arr = np.array(img)
        self._display(self.lbl_orig, img)
        self.status.config(text=f"Citra dimuat: {os.path.basename(path)}")

    def _display(self, target_lbl, pil_img):
        resized = pil_img.resize((380, 380), Image.Resampling.BILINEAR)
        tk_img = ImageTk.PhotoImage(resized)
        target_lbl.image = tk_img
        target_lbl.config(image=tk_img)

    def on_browse(self):
        f = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if f:
            self.load_image(f)

    def on_enhance(self):
        if self.dark_arr is None:
            return
        enh = fractal_low_light_enhance(self.dark_arr)
        pil_enh = Image.fromarray(enh)
        self._display(self.lbl_enh, pil_enh)
        ent = compute_entropy(enh)
        self.status.config(text=f"Enhancement selesai (Entropi informasi: {ent:.2f} bits)")


def launch_gui():
    app = LowLightApp()
    app.mainloop()


if __name__ == "__main__":
    launch_gui()
