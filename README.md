# Fractal-Based Low-Light Image Enhancement Suite

> **Proyek Capstone 4**: Peningkatan Citra Pencahayaan Rendah Menggunakan Teori Retinex Berbasis Fractal Texture Preservation  
> **Program Studi**: S1 Ilmu Komputer / Informatika, FMIPA, Universitas Gadjah Mada  

---

## Ringkasan Proyek
Mengembangkan algoritma peningkatan citra pencahayaan rendah (*low-light image enhancement*) yang mendekomposisi citra menjadi iluminasi dan reflektansi, lalu menggunakan estimasi kekasaran fraktal lokal untuk menaikkan kontras tekstur asli tanpa mengamplifikasi derau latar belakang.

### Pembagian Tugas Tim 4 Mahasiswa
1. **Mahasiswa 1**: Dataset Preprocessing & Simulasi Low-Light Sintetis.
2. **Mahasiswa 2**: Modul Dekomposisi Retinex & Estimasi Komponen Iluminasi.
3. **Mahasiswa 3**: Mesin Fractal Texture Preservation & Rekonstruksi Luminansi.
4. **Mahasiswa 4**: Antarmuka Grafis (Tkinter GUI), Visualisasi Komparatif, & Pengujian Metrik (PSNR, SSIM, Entropi).

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
