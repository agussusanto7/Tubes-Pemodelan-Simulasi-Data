import numpy as np
import pandas as pd

SIM_TIME = 120
JUMLAH_KASIR = 2
AVG_SERVICE = 3.0
STD_SERVICE = 0.5


def set_defaults(sim_time=None, jumlah_kasir=None, avg_service=None, std_service=None):
    global SIM_TIME, JUMLAH_KASIR, AVG_SERVICE, STD_SERVICE

    if sim_time is not None:
        SIM_TIME = int(sim_time)
    if jumlah_kasir is not None:
        JUMLAH_KASIR = int(jumlah_kasir)
    if avg_service is not None:
        AVG_SERVICE = float(avg_service)
    if std_service is not None:
        STD_SERVICE = float(std_service)


def run_abm(
    interval_kedatangan,
    sim_time=None,
    jumlah_kasir=None,
    avg_service=None,
    std_service=None,
    seed=None,
):
    sim_time = SIM_TIME if sim_time is None else sim_time
    jumlah_kasir = JUMLAH_KASIR if jumlah_kasir is None else jumlah_kasir
    avg_service = AVG_SERVICE if avg_service is None else avg_service
    std_service = STD_SERVICE if std_service is None else std_service

    rng = np.random.default_rng(seed)
    lam = 1 / interval_kedatangan
    queue = []
    kasir = [{"remaining": 0, "current": None} for _ in range(jumlah_kasir)]
    data_store = []
    nomor = 0

    for t in range(sim_time):
        n_datang = rng.poisson(lam)
        for _ in range(n_datang):
            nomor += 1
            queue.append({"id": f"MHS-{nomor:05d}", "arrival_time": t})

        for k in kasir:
            if k["remaining"] > 0:
                k["remaining"] -= 1
                if k["remaining"] == 0 and k["current"] is not None:
                    mhs = k["current"]
                    waktu_selesai = t + 1
                    data_store.append(
                        {
                            "ID_Mahasiswa": mhs["id"],
                            "Waktu_Datang": mhs["arrival_time"],
                            "Waktu_Tunggu": mhs["start_time"] - mhs["arrival_time"],
                            "Durasi_Layanan": mhs["service_time"],
                            "Waktu_Selesai": waktu_selesai,
                        }
                    )
                    k["current"] = None

        for k in kasir:
            if k["remaining"] == 0 and k["current"] is None and queue:
                mhs = queue.pop(0)
                durasi = max(1, int(round(rng.normal(avg_service, std_service))))
                mhs["start_time"] = t
                mhs["service_time"] = durasi
                k["current"] = mhs
                k["remaining"] = durasi

    t = sim_time
    while queue or any(k["remaining"] > 0 for k in kasir):
        for k in kasir:
            if k["remaining"] > 0:
                k["remaining"] -= 1
                if k["remaining"] == 0 and k["current"] is not None:
                    mhs = k["current"]
                    waktu_selesai = t + 1
                    data_store.append(
                        {
                            "ID_Mahasiswa": mhs["id"],
                            "Waktu_Datang": mhs["arrival_time"],
                            "Waktu_Tunggu": mhs["start_time"] - mhs["arrival_time"],
                            "Durasi_Layanan": mhs["service_time"],
                            "Waktu_Selesai": waktu_selesai,
                        }
                    )
                    k["current"] = None

        for k in kasir:
            if k["remaining"] == 0 and k["current"] is None and queue:
                mhs = queue.pop(0)
                durasi = max(1, int(round(rng.normal(avg_service, std_service))))
                mhs["start_time"] = t
                mhs["service_time"] = durasi
                k["current"] = mhs
                k["remaining"] = durasi

        t += 1

    return pd.DataFrame(data_store)


def monte_carlo(
    interval_kedatangan,
    n_iter,
    skenario,
    seed_offset=0,
    sim_time=None,
    jumlah_kasir=None,
    avg_service=None,
    std_service=None,
):
    rows = []
    for i in range(n_iter):
        df = run_abm(
            interval_kedatangan,
            sim_time=sim_time,
            jumlah_kasir=jumlah_kasir,
            avg_service=avg_service,
            std_service=std_service,
            seed=seed_offset + i,
        )
        if df.empty:
            mean_wait = 0.0
            max_wait = 0.0
            std_wait = 0.0
            total = 0
            pct_wait = 0.0
        else:
            mean_wait = df["Waktu_Tunggu"].mean()
            max_wait = df["Waktu_Tunggu"].max()
            std_wait = df["Waktu_Tunggu"].std()
            total = len(df)
            pct_wait = (df["Waktu_Tunggu"] > 0).mean() * 100

        rows.append(
            {
                "Skenario": skenario,
                "Iterasi": i + 1,
                "Rata_Tunggu": round(mean_wait, 2),
                "Max_Tunggu": round(max_wait, 2),
                "Std_Tunggu": round(0.0 if np.isnan(std_wait) else std_wait, 2),
                "Total_Mahasiswa": total,
                "Pct_Tunggu": round(pct_wait, 2),
            }
        )

    return pd.DataFrame(rows)


def ringkas_mc(df):
    return {
        "Rata_Tunggu": df["Rata_Tunggu"].mean(),
        "Max_Tunggu": df["Max_Tunggu"].max(),
        "Total_Mahasiswa": df["Total_Mahasiswa"].mean(),
        "Std_Tunggu": df["Std_Tunggu"].mean(),
        "Pct_Tunggu": df["Pct_Tunggu"].mean(),
    }


def analisis_multi_kasir(
    interval_kedatangan,
    n_iter,
    jumlah_kasir_range,
    sim_time,
    avg_service,
    std_service,
    seed_offset=5000,
):
    """
    Menjalankan simulasi berulang untuk setiap jumlah kasir (mis. 1-5) pada
    kondisi rush hour, lalu mengembalikan dataframe dengan metrik per skenario
    kasir.

    Parameters
    ----------
    interval_kedatangan : float
        Rata-rata interval kedatangan (menit), biasanya INTERVAL_RUSH = 2.
    n_iter : int
        Jumlah iterasi Monte Carlo per jumlah kasir.
    jumlah_kasir_range : range
        Rentang jumlah kasir yang dicoba, misalnya range(1, 6) untuk 1-5 kasir.
    sim_time, avg_service, std_service : float
        Parameter ABM yang sama dengan run_abm().
    seed_offset : int
        Basis seed agar hasil konsisten.

    Returns
    -------
    pd.DataFrame
        Kolom: Jumlah_Kasir, Rata_Tunggu, Max_Tunggu, Total_Mahasiswa,
        Utilisasi_Kasir_Pct
    """
    hasil = []
    for n_kasir in jumlah_kasir_range:
        rata_list = []
        max_list = []
        total_list = []
        util_list = []

        for i in range(n_iter):
            df_temp = run_abm(
                interval_kedatangan,
                sim_time=sim_time,
                jumlah_kasir=n_kasir,
                avg_service=avg_service,
                std_service=std_service,
                seed=seed_offset + n_kasir * 1000 + i,
            )
            if df_temp.empty:
                rata = 0.0
                max_t = 0.0
                total = 0
                utilisasi = 0.0
            else:
                rata = df_temp["Waktu_Tunggu"].mean()
                max_t = df_temp["Waktu_Tunggu"].max()
                total = len(df_temp)
                total_waktu_layanan = df_temp["Durasi_Layanan"].sum()
                utilisasi = (total_waktu_layanan / (n_kasir * sim_time)) * 100

            rata_list.append(rata)
            max_list.append(max_t)
            total_list.append(total)
            util_list.append(utilisasi)

        hasil.append(
            {
                "Jumlah_Kasir": n_kasir,
                "Rata_Tunggu": round(float(np.mean(rata_list)), 2),
                "Max_Tunggu": round(float(np.max(max_list)), 2),
                "Total_Mahasiswa": round(float(np.mean(total_list))),
                "Utilisasi_Kasir_Pct": round(float(np.mean(util_list)), 1),
            }
        )

    return pd.DataFrame(hasil)
