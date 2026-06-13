# Copilot instructions

## Running the notebook
- Primary entry point: simulasi_antrian_kantin_kampus.ipynb. Run cells top-to-bottom.
- Cell 1 installs SimPy via `!pip install simpy -q` and imports numpy/pandas/matplotlib/seaborn.

## High-level architecture
- Discrete-event simulation built in SimPy with two core processes:
  - `proses_mahasiswa(...)` models a single student's arrival, queue wait, service time, and logs a record into `data_store`.
  - `generator_mahasiswa(...)` is the arrival process (exponential inter-arrival) that spawns student processes.
- Two scenarios run in separate SimPy environments (jam biasa and rush hour) and produce `df_biasa` and `df_rush`, which drive the statistical tables and plots.
- Follow-up analyses include dashboard visualizations (saved as PNGs), input distribution verification via synthetic sampling, a multi-cashier sweep (1-5) producing `df_multi`, and automated textual conclusions.

## Key conventions
- Time unit is minutes; `SIM_TIME` is total simulated minutes.
- Global parameters live together in CELL 2: `SIM_TIME`, `JUMLAH_KASIR`, `AVG_SERVICE`, `STD_SERVICE`.
- Data records use fixed column names: `ID_Mahasiswa`, `Waktu_Datang`, `Waktu_Tunggu`, `Durasi_Layanan`, `Waktu_Selesai`.
- Randomness is controlled with `np.random.seed(...)` before each major analysis; keep seeds for reproducible outputs.
- Output artifacts are written to PNGs: `dashboard_kantin.png`, `verifikasi_distribusi.png`, `analisis_kasir.png`.
