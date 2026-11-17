# LAPORAN CAPSTONE PROJECT

## PENINGKATAN CITRA PENCAHAYAAN RENDAH MENGGUNAKAN TEORI RETINEX BERBASIS FRACTAL TEXTURE PRESERVATION
### (*Low-Light Image Enhancement via Fractal-Guided Retinex Decomposition*)

**Program Studi**: S1 Ilmu Komputer / Informatika  
**Fakultas**: Matematika dan Ilmu Pengetahuan Alam (FMIPA)  
**Kelompok**: Tim Pengembang Capstone DIKE FMIPA UGM  
**Anggota Tim**:  
1. Aji Kusuma Putra (NIM: 22/503701/PA/21657)  
2. Rayhan Haldi Hermawan (NIM: 24/545406/PA/23176)  
**Kontak**: Rayhanhaldi13@gmail.com | [GitHub Repositori](https://github.com/VelAstra)  
**Tahun Akademik**: 2026/2027  

---

## RINGKASAN EKSEKUTIF

Citra yang diambil dalam kondisi pencahayaan rendah sering kali mengalami kehilangan kontras drastis, detail tekstur mikro yang tersembunyi, dan rasio sinyal terhadap derau (*Signal-to-Noise Ratio* - SNR) yang sangat buruk. Metode pemerataan histogram (HE) konvensional cenderung mengekspos derau latar belakang secara berlebihan (*over-enhancement*).

Proyek capstone ini mengembangkan pendekatan **Fractal-Guided Retinex Enhancement**. Citra didekomposisi menjadi komponen iluminasi $L$ dan reflektansi $R$. Komponen iluminasi ditingkatkan secara adaptif menggunakan koreksi gamma non-linier, sementara komponen reflektansi diperkuat menggunakan bobot kekasaran fraktal lokal (*local fractal roughness*). Mekanisme ini memastikan penguatan tekstur hanya terjadi pada area tepi dan objek nyata, serta menekan amplifikasi derau pada area gelap seragam. Hasil pengujian menunjukkan peningkatan entropi informasi dari **5,69 bits menjadi 6,96 bits** dengan kualitas visual natural.

---

## BAB I: PENDAHULUAN

### 1.1 Latar Belakang
Kamera pengawas malam hari, fotografi gawai dalam ruangan, dan pencitraan medis radiologi sering menghasilkan citra underexposed. Model Retinex memodelkan citra $S$ sebagai perkalian antara iluminasi lingkungan $L$ dan reflektansi intrinsik objek $R$:
$$S(x, y) = L(x, y) \cdot R(x, y)$$
Tantangannya adalah meningkatkan komponen $L$ tanpa mendistorsi warna dan mengekspos derau sensor pada komponen $R$.

### 1.2 Rumusan Masalah
1. Bagaimana mendekomposisi citra rendah cahaya menjadi estimasi komponen iluminasi dan reflektansi yang akurat?
2. Bagaimana memanfaatkan estimasi kekasaran fraktal untuk mengontrol penguatan kontras lokal?
3. Bagaimana membandingkan performa metode yang dikembangkan terhadap metode acuan seperti Histogram Equalization dan Single-Scale Retinex (SSR)?

### 1.3 Pembagian Tugas Tim Capstone (2 Mahasiswa)
1. **Aji Kusuma Putra** (NIM: 22/503701/PA/21657): Preprocessing dataset low-light, sintesis citra pencahayaan rendah sintetis, modul dekomposisi Retinex, dan estimasi komponen iluminasi lingkungan adaptif. (`sample_data/generate_low_light.py`, `core/decomposition.py`).
2. **Rayhan Haldi Hermawan** (NIM: 24/545406/PA/23176): Mesin pembobotan tekstur fraktal reflektansi, baseline pembanding (HE dan SSR), rekonstruksi luminansi, Desktop GUI Tkinter, visualisasi sebelum/sesudah, dan evaluasi metrik (Entropi, PSNR, SSIM). (`core/fractal_enhancer.py`, `core/baselines.py`, `core/evaluation.py`, `gui/app.py`, `cli.py`).

---

## BAB II: LANDASAN TEORI & FORMULASI MATEMATIKA

### 2.1 Model Dekomposisi Retinex
Dalam domain logaritma:
$$\log S(x, y) = \log L(x, y) + \log R(x, y)$$
Iluminasi $L$ diestimasi menggunakan filter Gauss multi-skala:
$$L(x, y) = S(x, y) * G_\sigma(x, y)$$

### 2.2 Pembobotan Tekstur Fraktal
Kekasaran fraktal lokal dihitung dari variansi lokal reflektansi:
$$\omega(x, y) = \frac{\sigma_R(x, y)}{\text{Percentile}_{90}(\sigma_R) + \epsilon}$$
Reflektansi yang ditingkatkan dirumuskan sebagai:
$$R_{\text{enhanced}}(x, y) = R(x, y) \cdot [1 + (\gamma_T - 1) \cdot \omega(x, y)]$$

---

## BAB III: METODOLOGI & ARSITEKTUR SISTEM

Alur kerja peningkatan citra:
1. Konversi citra ke ruang warna pemisah luminansi.
2. Ekstraksi iluminasi latar belakang menggunakan Gaussian blur.
3. Koreksi gamma non-linier pada peta iluminasi $L^{\gamma}$.
4. Deteksi area tekstur berkarakter fraktal pada peta reflektansi.
5. Rekombinasi dan penskalaan kembali saluran warna RGB asli.

---

## BAB IV: PENGUJIAN DAN EVALUASI

Evaluasi komparatif pada benchmark sintetis:
* **Entropi Informasi**: 6,96 bits (meningkat signifikan dari 5,69 bits pada citra awal).
* **Fidelitas Struktural (SSIM)**: 0,7069.
* **Perbandingan Visual**: Metode yang diusulkan menghasilkan warna alami tanpa artefak *color blooming* yang biasa ditemui pada Histogram Equalization.

---

## BAB V: KESIMPULAN

Pendekatan Retinex berbasis panduan kekasaran fraktal terbukti mampu meningkatkan keterlihatan citra pencahayaan rendah secara selektif dengan mempertahankan detail tekstur alami.
