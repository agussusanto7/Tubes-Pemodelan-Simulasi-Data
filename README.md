# Simulasi ABM Antrian Kantin Kampus

Proyek ini membangun **Agent‑Based Modeling (ABM)** untuk simulasi antrian kantin kampus dengan dua skenario: **Jam Biasa** dan **Rush Hour**. Simulasi dijalankan secara **time‑step per menit** dan dievaluasi dengan **Monte Carlo** untuk menghasilkan ringkasan statistik yang stabil. Tersedia **notebook Jupyter** dan **dashboard web Streamlit** untuk eksplorasi interaktif.

## Tujuan
Memberikan gambaran kuantitatif tentang:
- Perbedaan performa sistem antrian pada Jam Biasa vs Rush Hour
- Dampak parameter (jumlah kasir, interval kedatangan, durasi pelayanan)
- Distribusi waktu tunggu dan metrik kinerja lainnya

## Fitur Utama
- **ABM time‑step**: setiap mahasiswa sebagai agen (datang → antre → dilayani → selesai)
- **Monte Carlo 2000 iterasi**: 1000 iterasi per skenario
- **Dashboard interaktif** dengan slider parameter dan visualisasi
- **Import dataset** (CSV/XLSX) untuk mengisi parameter simulasi secara otomatis
- **Ekspor hasil** Monte Carlo ke CSV

## Struktur File
- `simulasi_antrian_kantin_kampus.ipynb` — notebook utama simulasi & analisis
- `app.py` — dashboard Streamlit
- `hasil_monte_carlo.csv` — output hasil iterasi (tersimpan setelah run)
- `requirements.txt` — dependensi Python
- `dashboard_kantin.png`, `verifikasi_distribusi.png`, `analisis_kasir.png` — output visual
- `Pemodelan dan Simulasi.pdf` — panduan tugas

## Cara Menjalankan (Notebook)
1. Buka `simulasi_antrian_kantin_kampus.ipynb` di Jupyter/VS Code.
2. Jalankan cell dari atas ke bawah.
3. Hasil Monte Carlo otomatis tersimpan ke `hasil_monte_carlo.csv`.

## Cara Menjalankan (Dashboard Streamlit)
```bash
pip install -r requirements.txt
streamlit run app.py
```
Dashboard akan terbuka di `http://localhost:8501`.

## Input Parameter
Parameter utama yang digunakan:
- `SIM_TIME` — durasi simulasi (menit)
- `JUMLAH_KASIR` — jumlah kasir aktif
- `AVG_SERVICE` — rata‑rata durasi pelayanan
- `STD_SERVICE` — variasi durasi pelayanan
- `INTERVAL_BIASA` — rata‑rata jeda kedatangan jam biasa
- `INTERVAL_RUSH` — rata‑rata jeda kedatangan rush hour
- `N_ITER` — jumlah iterasi Monte Carlo per skenario

### Import Dataset (CSV/XLSX)
Di dashboard, unggah dataset lalu:
1. Centang **“Gunakan dataset untuk parameter”**
2. Pilih baris data yang ingin dipakai
3. Mapping kolom dataset ke parameter simulasi
4. Klik **Jalankan Simulasi**

Jika nilai kolom tidak valid, dashboard akan memakai nilai default dari slider.

## Metodologi Singkat
- **Kedatangan**: Poisson per menit (λ = 1 / interval)
- **Pelayanan**: Normal (μ = AVG_SERVICE, σ = STD_SERVICE)
- **Antrian**: FIFO (first‑in, first‑out)
  
Output utama:
- Rata‑rata waktu tunggu
- Waktu tunggu maksimum
- Standar deviasi waktu tunggu
- Total mahasiswa terlayani
  
## Ekspor Hasil
Hasil Monte Carlo dapat diunduh dari dashboard (CSV) atau otomatis tersimpan saat menjalankan notebook:
```
hasil_monte_carlo.csv
```

## Lisensi
Digunakan untuk kebutuhan akademik dan tugas kuliah.
