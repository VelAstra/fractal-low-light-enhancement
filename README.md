# Fractal-Based Low-Light Image Enhancement Suite

> **Proyek Capstone 4**: Peningkatan Citra Pencahayaan Rendah Menggunakan Teori Retinex Berbasis Fractal Texture Preservation  
> **Program Studi**: S1 Ilmu Komputer / Informatika, FMIPA, Universitas Gadjah Mada  
> **Anggota Tim Pengembang**:  
> - Aji Kusuma Putra (NIM: 22/503701/PA/21657)  
> - Rayhan Haldi Hermawan (NIM: 24/545406/PA/23176)  

---

## Ringkasan Proyek
Mengembangkan algoritma peningkatan citra pencahayaan rendah (*low-light image enhancement*) yang mendekomposisi citra menjadi iluminasi dan reflektansi, lalu menggunakan estimasi kekasaran fraktal lokal untuk menaikkan kontras tekstur asli tanpa mengamplifikasi derau latar belakang.

### Pembagian Tugas Tim (2 Mahasiswa)
1. **Aji Kusuma Putra** (`22/503701/PA/21657`): Preprocessing dataset low-light, sintesis citra pencahayaan rendah sintetis, modul dekomposisi Retinex, dan estimasi komponen iluminasi lingkungan adaptif. (Modul: `sample_data/generate_low_light.py`, `core/decomposition.py`).
2. **Rayhan Haldi Hermawan** (`24/545406/PA/23176`): Mesin pembobotan tekstur fraktal reflektansi, baseline pembanding (HE dan SSR), rekonstruksi luminansi, Desktop GUI Tkinter, visualisasi sebelum/sesudah, dan evaluasi metrik (Entropi, PSNR, SSIM). (Modul: `core/fractal_enhancer.py`, `core/baselines.py`, `core/evaluation.py`, `gui/app.py`, `cli.py`).

---

## Cara Menjalankan

```bash
# Menjalankan peningkatan citra
python cli.py enhance sample_data/dark.png --gt sample_data/gt_normal.png

# Menjalankan perbandingan benchmark dengan metode baseline (HE dan Retinex)
python cli.py benchmark

# Menjalankan antarmuka grafis
python cli.py gui

# Menjalankan uji otomatis
python -m unittest discover tests
```
