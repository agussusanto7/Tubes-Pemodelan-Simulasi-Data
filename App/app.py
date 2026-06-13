"""
Simulasi Antrian Kantin Kampus
Agent-Based Modeling & Monte Carlo Analysis
"""

import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

from abm_core import analisis_multi_kasir, monte_carlo, ringkas_mc, run_abm

# =========================================================================
# KONSTANTA APLIKASI
# =========================================================================
APP_NAME = "Simulasi Antrian Kantin Kampus"
APP_VERSION = "1.0.0"
APP_YEAR = "2026"
APP_OWNER = "Pencipta"
APP_TAGLINE = "Agent-Based Modeling & Monte Carlo Analysis"

# Palet warna (modern minimalist)
WARNA_BIASA = "#10b981"   # emerald-500
WARNA_RUSH = "#ef4444"    # red-500
WARNA_AKSEN = "#6366f1"   # indigo-500
WARNA_TEKS = "#0f172a"    # slate-900
WARNA_MUTED = "#64748b"   # slate-500
WARNA_LATAR = "#f8fafc"   # slate-50
WARNA_KARTU = "#ffffff"
WARNA_BORDER = "#e2e8f0"  # slate-200

# Konfigurasi matplotlib (font & ukuran konsisten)
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.titlecolor": WARNA_TEKS,
    "axes.labelcolor": WARNA_TEKS,
    "axes.edgecolor": WARNA_BORDER,
    "axes.linewidth": 0.8,
    "xtick.color": WARNA_MUTED,
    "ytick.color": WARNA_MUTED,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "legend.frameon": False,
    "figure.facecolor": WARNA_KARTU,
    "axes.facecolor": WARNA_KARTU,
    "axes.grid": True,
    "grid.color": WARNA_BORDER,
    "grid.linestyle": ":",
    "grid.linewidth": 0.6,
    "grid.alpha": 0.7,
})

# =========================================================================
# KONFIGURASI STREAMLIT
# =========================================================================
st.set_page_config(
    page_title=f"{APP_NAME} v{APP_VERSION}",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================================
# CSS GLOBAL
# =========================================================================
st.markdown(
    f"""
<style>
    /* Tweak container utama */
    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 0.5rem;
        max-width: 1400px;
    }}

    /* Header banner */
    .app-header {{
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid {WARNA_BORDER};
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 18px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }}
    .app-header h1 {{
        margin: 0;
        font-size: 1.6rem;
        color: {WARNA_TEKS};
        font-weight: 700;
    }}
    .app-header .subtitle {{
        color: {WARNA_MUTED};
        font-size: 0.9rem;
        margin-top: 2px;
    }}
    .app-header .meta {{
        color: {WARNA_MUTED};
        font-size: 0.78rem;
        margin-top: 6px;
        letter-spacing: 0.3px;
    }}
    .app-header .meta strong {{
        color: {WARNA_AKSEN};
    }}

    /* Section header */
    .section-header {{
        font-size: 1.05rem;
        font-weight: 700;
        color: {WARNA_TEKS};
        margin: 18px 0 10px 0;
        padding-bottom: 6px;
        border-bottom: 1px solid {WARNA_BORDER};
    }}

    /* KPI Card */
    .kpi-row {{
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 12px;
        margin: 10px 0 18px 0;
    }}
    .kpi-card {{
        background: {WARNA_KARTU};
        border: 1px solid {WARNA_BORDER};
        border-radius: 10px;
        padding: 14px 16px;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    }}
    .kpi-card .kpi-icon {{
        font-size: 1.1rem;
        margin-bottom: 4px;
    }}
    .kpi-card .kpi-label {{
        color: {WARNA_MUTED};
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }}
    .kpi-card .kpi-value {{
        color: {WARNA_TEKS};
        font-size: 1.55rem;
        font-weight: 700;
        line-height: 1.2;
        margin-top: 4px;
    }}
    .kpi-card .kpi-sub {{
        color: {WARNA_MUTED};
        font-size: 0.75rem;
        margin-top: 2px;
    }}
    .kpi-card.biasa {{
        border-top: 3px solid {WARNA_BIASA};
    }}
    .kpi-card.rush {{
        border-top: 3px solid {WARNA_RUSH};
    }}
    .kpi-card.accent {{
        border-top: 3px solid {WARNA_AKSEN};
    }}

    /* Footer */
    .app-footer {{
        text-align: center;
        color: {WARNA_MUTED};
        font-size: 0.78rem;
        margin-top: 32px;
        padding: 16px 0;
        border-top: 1px solid {WARNA_BORDER};
        letter-spacing: 0.3px;
    }}
    .app-footer strong {{
        color: {WARNA_TEKS};
    }}

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
        border-bottom: 1px solid {WARNA_BORDER};
    }}
    .stTabs [data-baseweb="tab"] {{
        padding: 8px 18px;
        font-weight: 600;
        color: {WARNA_MUTED};
    }}
    .stTabs [aria-selected="true"] {{
        color: {WARNA_AKSEN} !important;
        border-bottom: 2px solid {WARNA_AKSEN};
    }}

    /* DataFrame */
    .stDataFrame {{
        border: 1px solid {WARNA_BORDER};
        border-radius: 8px;
        overflow: hidden;
    }}

    /* Hide Streamlit branding */
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================================
# HEADER
# =========================================================================
st.markdown(
    f"""
<div class="app-header">
    <h1>🍱 &nbsp;{APP_NAME}</h1>
    <div class="subtitle">{APP_TAGLINE}</div>
    <div class="meta">
        Versi <strong>v{APP_VERSION}</strong> &nbsp;·&nbsp;
        © {APP_YEAR} <strong>{APP_OWNER}</strong> &nbsp;·&nbsp;
        Powered by Streamlit
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================================================================
# HELPERS
# =========================================================================


def pick_value(df, row_idx, column, default, label, as_int=False, min_value=None):
    if column in (None, "(kosong)"):
        return default
    if df is None or df.empty:
        st.warning(f"Dataset kosong untuk parameter {label}.")
        return default

    value = df.iloc[row_idx][column]
    try:
        num = float(value)
    except (TypeError, ValueError):
        st.warning(f"Nilai kolom {column} tidak valid untuk {label}.")
        return default

    if np.isnan(num):
        st.warning(f"Nilai kolom {column} kosong untuk {label}.")
        return default

    if min_value is not None and num < min_value:
        st.warning(f"Nilai {label} dari dataset < {min_value}.")
        return default

    return int(round(num)) if as_int else num


def kpi_card(icon: str, label: str, value: str, sub: str, variant: str = "accent") -> str:
    """Kartu KPI kustom (HTML). variant: 'biasa' | 'rush' | 'accent'."""
    return (
        f'<div class="kpi-card {variant}">'
        f'<div class="kpi-icon">{icon}</div>'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-sub">{sub}</div>'
        "</div>"
    )


def style_axes(ax, title: str, xlabel: str = "", ylabel: str = ""):
    """Penerapan styling konsisten ke satu axes."""
    ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    # Sembunyikan top/right spine
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    # Grid halus (sudah dari rcParams, tapi set ulang per-axes utk safety)
    ax.grid(True, linestyle=":", linewidth=0.6, alpha=0.7)


# Setup seaborn
sns.set(style="whitegrid", palette="muted")

# Cache Monte Carlo
monte_carlo_cached = st.cache_data(show_spinner=False)(monte_carlo)


# =========================================================================
# SIDEBAR: SUMBER DATA + PARAMETER
# =========================================================================
dataset = None
use_dataset_params = False
dataset_row = 0
col_map = {}

with st.sidebar:
    st.markdown("### ⚙️ Panel Kontrol")
    st.caption("Atur parameter simulasi di sini.")

    st.divider()
    st.markdown("#### 📂 Sumber Data")
    uploaded_file = st.file_uploader("Upload dataset (CSV/XLSX)", type=["csv", "xlsx"])
    if uploaded_file is not None:
        if uploaded_file.name.lower().endswith(".xlsx"):
            xls = pd.ExcelFile(uploaded_file)
            sheet_name = st.selectbox("Sheet", xls.sheet_names)
            dataset = pd.read_excel(xls, sheet_name=sheet_name)
        else:
            dataset = pd.read_csv(uploaded_file)

        st.caption(f"Dataset: {len(dataset)} baris, {len(dataset.columns)} kolom")
        use_dataset_params = st.checkbox("Gunakan dataset untuk parameter")

        if use_dataset_params and not dataset.empty:
            dataset_row = st.number_input(
                "Pilih baris dataset",
                min_value=0,
                max_value=max(0, len(dataset) - 1),
                value=0,
                step=1,
            )
            cols = ["(kosong)"] + list(dataset.columns)
            col_map = {
                "sim_time": st.selectbox("Kolom SIM_TIME", cols, index=0),
                "jumlah_kasir": st.selectbox("Kolom JUMLAH_KASIR", cols, index=0),
                "avg_service": st.selectbox("Kolom AVG_SERVICE", cols, index=0),
                "std_service": st.selectbox("Kolom STD_SERVICE", cols, index=0),
                "interval_biasa": st.selectbox("Kolom INTERVAL_BIASA", cols, index=0),
                "interval_rush": st.selectbox("Kolom INTERVAL_RUSH", cols, index=0),
                "n_iter": st.selectbox("Kolom N_ITER", cols, index=0),
            }

    st.divider()
    st.markdown("#### 🎛️ Parameter Manual")
    sim_time = st.slider("Durasi simulasi (menit)", 60, 240, 120, step=10)
    jumlah_kasir = st.slider(
        "Jumlah kasir",
        1, 5, 2,
        help="Jumlah kasir yang beroperasi bersamaan. Lebih banyak kasir = antrian lebih pendek.",
    )
    avg_service = st.slider("Rata-rata waktu layanan (menit)", 1.0, 6.0, 3.0, 0.5)
    std_service = st.slider("Std dev waktu layanan", 0.1, 2.0, 0.5, 0.1)
    interval_biasa = st.slider("Interval Jam Biasa (menit)", 2, 10, 5)
    interval_rush = st.slider("Interval Rush Hour (menit)", 1, 5, 2)
    n_iter = st.slider(
        "Iterasi Monte Carlo / skenario",
        50, 1000, 200, 50,
        help="Jumlah pengulangan simulasi. Lebih banyak = hasil lebih stabil tapi lebih lambat.",
    )
    run_button = st.button("▶ Jalankan Simulasi", type="primary", use_container_width=True)

# =========================================================================
# RESOLUSI PARAMETER
# =========================================================================
params_current = {
    "sim_time": sim_time,
    "jumlah_kasir": jumlah_kasir,
    "avg_service": avg_service,
    "std_service": std_service,
    "interval_biasa": interval_biasa,
    "interval_rush": interval_rush,
    "n_iter": n_iter,
}

if use_dataset_params and dataset is not None and not dataset.empty:
    params_current = {
        "sim_time": pick_value(
            dataset, dataset_row, col_map.get("sim_time"),
            params_current["sim_time"], "SIM_TIME", as_int=True, min_value=1,
        ),
        "jumlah_kasir": pick_value(
            dataset, dataset_row, col_map.get("jumlah_kasir"),
            params_current["jumlah_kasir"], "JUMLAH_KASIR", as_int=True, min_value=1,
        ),
        "avg_service": pick_value(
            dataset, dataset_row, col_map.get("avg_service"),
            params_current["avg_service"], "AVG_SERVICE", min_value=0.1,
        ),
        "std_service": pick_value(
            dataset, dataset_row, col_map.get("std_service"),
            params_current["std_service"], "STD_SERVICE", min_value=0.0,
        ),
        "interval_biasa": pick_value(
            dataset, dataset_row, col_map.get("interval_biasa"),
            params_current["interval_biasa"], "INTERVAL_BIASA", min_value=0.1,
        ),
        "interval_rush": pick_value(
            dataset, dataset_row, col_map.get("interval_rush"),
            params_current["interval_rush"], "INTERVAL_RUSH", min_value=0.1,
        ),
        "n_iter": pick_value(
            dataset, dataset_row, col_map.get("n_iter"),
            params_current["n_iter"], "N_ITER", as_int=True, min_value=1,
        ),
    }

if run_button or "last_run" not in st.session_state:
    st.session_state["last_run"] = params_current

params = st.session_state.get("last_run")

# =========================================================================
# JALANKAN SIMULASI
# =========================================================================
df_biasa = run_abm(
    params["interval_biasa"],
    sim_time=params["sim_time"],
    jumlah_kasir=params["jumlah_kasir"],
    avg_service=params["avg_service"],
    std_service=params["std_service"],
    seed=42,
)
df_rush = run_abm(
    params["interval_rush"],
    sim_time=params["sim_time"],
    jumlah_kasir=params["jumlah_kasir"],
    avg_service=params["avg_service"],
    std_service=params["std_service"],
    seed=99,
)

hasil_biasa = monte_carlo_cached(
    params["interval_biasa"], params["n_iter"], "Jam Biasa",
    seed_offset=1000,
    sim_time=params["sim_time"], jumlah_kasir=params["jumlah_kasir"],
    avg_service=params["avg_service"], std_service=params["std_service"],
)
hasil_rush = monte_carlo_cached(
    params["interval_rush"], params["n_iter"], "Rush Hour",
    seed_offset=2000,
    sim_time=params["sim_time"], jumlah_kasir=params["jumlah_kasir"],
    avg_service=params["avg_service"], std_service=params["std_service"],
)
hasil_mc = pd.concat([hasil_biasa, hasil_rush], ignore_index=True)

stat_biasa = ringkas_mc(hasil_biasa)
stat_rush = ringkas_mc(hasil_rush)

# =========================================================================
# KARTU KPI
# =========================================================================
kpi_html = (
    '<div class="kpi-row">'
    + kpi_card(
        "🌤️", "Rata Tunggu (Biasa)",
        f"{stat_biasa['Rata_Tunggu']:.2f} mnt",
        "Waktu tunggu rata-rata", "biasa",
    )
    + kpi_card(
        "⛈️", "Rata Tunggu (Rush)",
        f"{stat_rush['Rata_Tunggu']:.2f} mnt",
        "Waktu tunggu rata-rata", "rush",
    )
    + kpi_card(
        "⏱️", "Max Tunggu (Rush)",
        f"{stat_rush['Max_Tunggu']:.2f} mnt",
        "Kasus terburuk", "rush",
    )
    + kpi_card(
        "👥", "Mhs/Iter (Biasa)",
        f"{stat_biasa['Total_Mahasiswa']:.0f}",
        "Rata-rata terlayani", "accent",
    )
    + kpi_card(
        "📊", "Mhs/Iter (Rush)",
        f"{stat_rush['Total_Mahasiswa']:.0f}",
        "Rata-rata terlayani", "accent",
    )
    + "</div>"
)
st.markdown(kpi_html, unsafe_allow_html=True)

# =========================================================================
# TABS
# =========================================================================
tab_labels = ["📊 Dashboard", "🎲 Monte Carlo", "📖 Tentang", "📋 Dokumentasi", "💾 Data"]
if dataset is not None:
    tab_labels.append("📁 Dataset")
tabs = st.tabs(tab_labels)
tab_dashboard, tab_monte, tab_tentang, tab_dok, tab_data = tabs[:5]
tab_dataset = tabs[5] if len(tabs) > 5 else None

# ----- TAB DASHBOARD -----
with tab_dashboard:
    st.markdown('<div class="section-header">Ringkasan Skenario</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            f"**🌤️ Jam Biasa**\n\n"
            f"- Interval kedatangan: `{params['interval_biasa']} menit`\n"
            f"- λ (lambda): `{1/params['interval_biasa']:.2f} org/menit`\n"
            f"- Kasir aktif: `{params['jumlah_kasir']}`"
        )
    with col_b:
        st.markdown(
            f"**⛈️ Rush Hour**\n\n"
            f"- Interval kedatangan: `{params['interval_rush']} menit`\n"
            f"- λ (lambda): `{1/params['interval_rush']:.2f} org/menit`\n"
            f"- Kasir aktif: `{params['jumlah_kasir']}`"
        )

    st.markdown('<div class="section-header">Alur ABM (Time-step)</div>', unsafe_allow_html=True)
    step_cols = st.columns(4)
    step_cols[0].markdown("**① Kedatangan**\n\nGenerate agen via Poisson per menit.")
    step_cols[1].markdown("**② Update Kasir**\n\nKurangi sisa waktu layanan yang sedang berjalan.")
    step_cols[2].markdown("**③ Assign Antrian**\n\nKasir kosong ambil agen berikutnya (FIFO).")
    step_cols[3].markdown("**④ Logging**\n\nCatat transaksi saat layanan selesai.")

    st.markdown('<div class="section-header">Dashboard Run Contoh ABM</div>', unsafe_allow_html=True)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        f"Visualisasi Run Contoh ABM · {params['jumlah_kasir']} Kasir · {params['sim_time']} Menit",
        fontsize=14, fontweight="bold", color=WARNA_TEKS, y=1.00,
    )

    # Boxplot
    ax1 = axes[0, 0]
    data_box = [df_biasa["Waktu_Tunggu"], df_rush["Waktu_Tunggu"]]
    bp = ax1.boxplot(
        data_box, patch_artist=True, notch=False,
        boxprops=dict(linewidth=1.5),
        medianprops=dict(color=WARNA_TEKS, linewidth=2),
        whiskerprops=dict(color=WARNA_MUTED),
        capprops=dict(color=WARNA_MUTED),
        flierprops=dict(marker="o", markerfacecolor=WARNA_MUTED, markersize=4, alpha=0.5),
    )
    bp["boxes"][0].set_facecolor(WARNA_BIASA)
    bp["boxes"][1].set_facecolor(WARNA_RUSH)
    for patch in bp["boxes"]:
        patch.set_alpha(0.85)
    ax1.set_xticks([1, 2])
    ax1.set_xticklabels(["Jam Biasa", "Rush Hour"], fontsize=10)
    style_axes(ax1, "Distribusi Waktu Tunggu", "", "Menit Menunggu")

    # Line chart
    ax2 = axes[0, 1]
    ax2.plot(range(len(df_biasa)), df_biasa["Waktu_Tunggu"],
             color=WARNA_BIASA, label="Jam Biasa", linewidth=1.5, alpha=0.85, marker="o", markersize=3)
    ax2.plot(range(len(df_rush)), df_rush["Waktu_Tunggu"],
             color=WARNA_RUSH, label="Rush Hour", linewidth=1.5, alpha=0.85, marker="o", markersize=3)
    ax2.axhline(y=df_biasa["Waktu_Tunggu"].mean(), color=WARNA_BIASA,
                linestyle="--", linewidth=1, alpha=0.7,
                label=f"Rata Biasa ({df_biasa['Waktu_Tunggu'].mean():.1f})")
    ax2.axhline(y=df_rush["Waktu_Tunggu"].mean(), color=WARNA_RUSH,
                linestyle="--", linewidth=1, alpha=0.7,
                label=f"Rata Rush ({df_rush['Waktu_Tunggu'].mean():.1f})")
    style_axes(ax2, "Tren Waktu Tunggu per Urutan Kedatangan",
               "Urutan Kedatangan", "Menit Menunggu")
    ax2.legend(loc="upper left", fontsize=8)

    # Histogram
    ax3 = axes[1, 0]
    ax3.hist(df_biasa["Waktu_Tunggu"], bins=15, color=WARNA_BIASA,
             alpha=0.85, label="Jam Biasa", edgecolor="white", linewidth=0.8)
    ax3.hist(df_rush["Waktu_Tunggu"], bins=15, color=WARNA_RUSH,
             alpha=0.85, label="Rush Hour", edgecolor="white", linewidth=0.8)
    style_axes(ax3, "Distribusi Frekuensi Waktu Tunggu",
               "Menit Menunggu", "Jumlah Mahasiswa")
    ax3.legend(fontsize=9)

    # Scatter
    ax4 = axes[1, 1]
    ax4.scatter(df_biasa["Waktu_Datang"], df_biasa["Waktu_Tunggu"],
                color=WARNA_BIASA, alpha=0.7, s=40, label="Jam Biasa",
                edgecolors="white", linewidth=0.5)
    ax4.scatter(df_rush["Waktu_Datang"], df_rush["Waktu_Tunggu"],
                color=WARNA_RUSH, alpha=0.7, s=40, label="Rush Hour",
                edgecolors="white", linewidth=0.5)
    style_axes(ax4, "Waktu Datang vs Waktu Tunggu",
               "Menit Kedatangan (dari t=0)", "Menit Menunggu")
    ax4.legend(fontsize=9)

    plt.tight_layout()
    st.pyplot(fig)

# ----- TAB MONTE CARLO -----
with tab_monte:
    st.markdown('<div class="section-header">Ringkasan Monte Carlo</div>', unsafe_allow_html=True)
    ringkasan = pd.DataFrame(
        {
            "Indikator": [
                "Rata-rata Waktu Tunggu (menit)",
                "Waktu Tunggu Maksimum (menit)",
                "Total Mahasiswa Terlayani (rata-rata)",
                "Standar Deviasi Tunggu (rata-rata)",
                "% Mahasiswa yang Harus Antri (rata-rata)",
            ],
            "🌤️ Jam Biasa": [
                f"{stat_biasa['Rata_Tunggu']:.2f}",
                f"{stat_biasa['Max_Tunggu']:.2f}",
                f"{stat_biasa['Total_Mahasiswa']:.0f}",
                f"{stat_biasa['Std_Tunggu']:.2f}",
                f"{stat_biasa['Pct_Tunggu']:.1f}%",
            ],
            "⛈️ Rush Hour": [
                f"{stat_rush['Rata_Tunggu']:.2f}",
                f"{stat_rush['Max_Tunggu']:.2f}",
                f"{stat_rush['Total_Mahasiswa']:.0f}",
                f"{stat_rush['Std_Tunggu']:.2f}",
                f"{stat_rush['Pct_Tunggu']:.1f}%",
            ],
        }
    )
    st.dataframe(ringkasan, width='stretch', hide_index=True)

    st.markdown('<div class="section-header">Distribusi Rata-rata Waktu Tunggu</div>', unsafe_allow_html=True)
    fig_mc, ax = plt.subplots(1, 2, figsize=(12, 4))
    fig_mc.suptitle(
        f"Distribusi Hasil Monte Carlo ({params['n_iter']} iterasi per skenario)",
        fontsize=12, fontweight="bold", color=WARNA_TEKS,
    )

    sns.histplot(hasil_biasa["Rata_Tunggu"], bins=20, color=WARNA_BIASA,
                 ax=ax[0], edgecolor="white", linewidth=0.8, alpha=0.85)
    style_axes(ax[0], "🌤️ Jam Biasa", "Rata-rata Waktu Tunggu (menit)", "Frekuensi")

    sns.histplot(hasil_rush["Rata_Tunggu"], bins=20, color=WARNA_RUSH,
                 ax=ax[1], edgecolor="white", linewidth=0.8, alpha=0.85)
    style_axes(ax[1], "⛈️ Rush Hour", "Rata-rata Waktu Tunggu (menit)", "Frekuensi")

    plt.tight_layout()
    st.pyplot(fig_mc)

# ----- TAB TENTANG -----
with tab_tentang:
    st.markdown('<div class="section-header">Tentang Aplikasi</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
**{APP_NAME}** adalah aplikasi simulasi sistem antrian makanan di kantin kampus
yang menggunakan metode **Agent-Based Modeling (ABM)** berbasis **time-step**
disertai analisis **Monte Carlo** untuk mengevaluasi performa pelayanan.

Aplikasi ini dirancang untuk menjawab tiga pertanyaan utama:

1. Berapa lama rata-rata mahasiswa menunggu di antrian?
2. Apakah jumlah kasir yang tersedia sudah cukup?
3. Apa perbedaan performa antara **Jam Biasa** dan **Jam Makan Siang (Rush Hour)**?
"""
    )

    st.markdown('<div class="section-header">Klaim Orisinalitas (HKI)</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
> Aplikasi **{APP_NAME}** v{APP_VERSION} merupakan ciptaan orisil yang
> dikembangkan oleh **{APP_OWNER}** pada tahun **{APP_YEAR}**.
>
> Seluruh kode sumber, logika simulasi Agent-Based Modeling, integrasi
> Monte Carlo, dan desain antarmuka dilindungi oleh Hak Kekayaan Intelektual.
> Dilarang memperbanyak atau mengubah tanpa izin pemegang hak.
"""
    )

    st.markdown('<div class="section-header">Metodologi Singkat</div>', unsafe_allow_html=True)
    method_col1, method_col2 = st.columns(2)
    with method_col1:
        st.markdown(
            """
**🧬 Agent-Based Modeling (ABM)**

Setiap mahasiswa dimodelkan sebagai agen independen dengan atribut:
- `id`, `arrival_time` (waktu datang)
- `start_time` (waktu mulai dilayani)
- `service_time` (durasi pelayanan)

Simulasi berjalan per menit (time-step). Pada setiap langkah, sistem:
1. Generate kedatangan baru (Poisson)
2. Update status kasir yang sedang melayani
3. Assign agen ke kasir kosong (FIFO)
4. Catat transaksi saat layanan selesai
"""
        )
    with method_col2:
        st.markdown(
            """
**🎲 Monte Carlo (N = 2000)**

Simulasi ABM diulang sebanyak **N** kali per skenario untuk mengukur
variabilitas dan mendapatkan estimasi robust:

| Skenario | Iterasi | Tujuan |
|---|---|---|
| 🌤️ Jam Biasa | 1000 | Baseline performa |
| ⛈️ Rush Hour | 1000 | Stress test sistem |

Distribusi yang digunakan:
- **Poisson** per menit untuk kedatangan
- **Normal** (μ=3, σ=0.5) untuk durasi pelayanan
"""
        )

    st.markdown('<div class="section-header">Informasi Versi</div>', unsafe_allow_html=True)
    info_df = pd.DataFrame(
        {
            "Komponen": ["Versi Aplikasi", "Tahun Ciptaan", "Pemegang Hak", "Bahasa", "Framework", "Lisensi"],
            "Detail": [
                f"v{APP_VERSION}",
                APP_YEAR,
                APP_OWNER,
                "Python 3.13",
                "Streamlit",
                "HKI – All Rights Reserved",
            ],
        }
    )
    st.dataframe(info_df, width='stretch', hide_index=True)

# ----- TAB DOKUMENTASI -----
with tab_dok:
    st.markdown('<div class="section-header">Parameter Simulasi</div>', unsafe_allow_html=True)
    param_df = pd.DataFrame(
        {
            "Parameter": [
                "sim_time", "jumlah_kasir", "avg_service", "std_service",
                "interval_biasa", "interval_rush", "n_iter",
            ],
            "Deskripsi": [
                "Durasi simulasi (time-step).",
                "Jumlah kasir yang beroperasi bersamaan.",
                "Rata-rata durasi pelayanan per mahasiswa.",
                "Standar deviasi durasi pelayanan (variasi).",
                "Rata-rata jeda kedatangan pada Jam Biasa.",
                "Rata-rata jeda kedatangan pada Rush Hour.",
                "Jumlah iterasi Monte Carlo per skenario.",
            ],
            "Satuan": ["menit", "kasir", "menit", "menit", "menit", "menit", "iterasi"],
            "Default": [120, 2, 3.0, 0.5, 5, 2, 200],
            "Rentang": ["60–240", "1–5", "1.0–6.0", "0.1–2.0", "2–10", "1–5", "50–1000"],
        }
    )
    st.dataframe(param_df, width='stretch', hide_index=True)

    st.markdown('<div class="section-header">Cara Pakai</div>', unsafe_allow_html=True)
    st.markdown(
        """
1. **Atur parameter** di sidebar kiri (atau unggah dataset CSV/XLSX).
2. Klik tombol **▶ Jalankan Simulasi**.
3. Lihat hasil di tab:
   - **Dashboard** → 4 visualisasi run contoh ABM.
   - **Monte Carlo** → tabel ringkasan & histogram distribusi.
   - **Data** → unduh hasil Monte Carlo dalam CSV.
4. (Opsional) Aktifkan **"Gunakan dataset untuk parameter"** untuk mengambil
   nilai parameter dari baris dataset yang dipilih.
"""
    )

    st.markdown('<div class="section-header">FAQ</div>', unsafe_allow_html=True)
    with st.expander("❓ Kenapa distribusi Poisson untuk kedatangan?"):
        st.markdown(
            """
Poisson per menit adalah standar pemodelan untuk proses kedatangan acak
yang independen. Cocok untuk skenario di mana jumlah kedatangan dalam
interval pendek (1 menit) bersifat acak dengan rata-rata konstan.
"""
        )
    with st.expander("❓ Kenapa distribusi Normal untuk durasi pelayanan?"):
        st.markdown(
            """
Distribusi Normal digunakan karena durasi pelayanan memiliki **variasi
kecil** di sekitar rata-rata (μ=3, σ=0.5). Mayoritas transaksi memakan
waktu ±1 menit dari rata-rata.
"""
        )
    with st.expander("❓ Apa beda Jam Biasa dan Rush Hour?"):
        st.markdown(
            """
- **Jam Biasa** → interval kedatangan rata-rata **5 menit** (jeda panjang).
- **Rush Hour** → interval kedatangan rata-rata **2 menit** (kepadatan tinggi).
Ini mensimulasikan jam makan siang (11.30–13.00) di mana mahasiswa berbondong-bondong ke kantin.
"""
        )
    with st.expander("❓ Berapa iterasi Monte Carlo yang ideal?"):
        st.markdown(
            """
- **200 iterasi** → cukup untuk eksplorasi awal (default aplikasi).
- **1000 iterasi** → standar industri, hasil lebih stabil.
- **1000+ iterasi** → untuk publikasi atau analisis presisi tinggi (memakan waktu lebih lama).
"""
        )

# ----- TAB DATA -----
with tab_data:
    st.markdown('<div class="section-header">Data Hasil Monte Carlo</div>', unsafe_allow_html=True)
    st.caption(f"Menampilkan 20 baris pertama dari total {len(hasil_mc)} baris.")
    st.dataframe(hasil_mc.head(20), width='stretch')

    csv_buffer = io.StringIO()
    hasil_mc.to_csv(csv_buffer, index=False)
    st.download_button(
        label="⬇ Unduh hasil Monte Carlo (CSV)",
        data=csv_buffer.getvalue(),
        file_name="hasil_monte_carlo.csv",
        mime="text/csv",
        type="primary",
    )

# ----- TAB DATASET (opsional) -----
if tab_dataset is not None:
    with tab_dataset:
        st.markdown('<div class="section-header">Dataset yang Diunggah</div>', unsafe_allow_html=True)
        if dataset is None or dataset.empty:
            st.info("Dataset kosong atau belum dipilih.")
        else:
            st.dataframe(dataset.head(50), width='stretch')

# =========================================================================
# FOOTER
# =========================================================================
st.markdown(
    f"""
<div class="app-footer">
    <strong>{APP_NAME}</strong> v{APP_VERSION} &nbsp;·&nbsp;
    © {APP_YEAR} {APP_OWNER} &nbsp;·&nbsp;
    Agent-Based Modeling &nbsp;·&nbsp; Monte Carlo &nbsp;·&nbsp; Streamlit
</div>
""",
    unsafe_allow_html=True,
)
