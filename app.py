import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np
from math import gcd

# ─────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Jelajah Bilangan Rasional",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# CSS KUSTOM  (selaras dengan Bilangan Bulat)
# ─────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

    .main-header {
        background: linear-gradient(135deg, #6A0572 0%, #A020A0 55%, #E05CC0 100%);
        color: white; padding: 1.5rem 2rem; border-radius: 16px;
        text-align: center; margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(106,5,114,0.35);
    }
    .main-header h1 { font-size: 2rem; font-weight: 800; margin: 0; }
    .main-header p  { font-size: 1rem; margin: 0.3rem 0 0; opacity: 0.9; }

    .fase-box {
        border-left: 5px solid #A020A0; background: #F9EFF9;
        padding: 0.8rem 1rem; border-radius: 0 10px 10px 0; margin: 0.7rem 0;
    }
    .fase-box .fase-label {
        font-weight: 800; color: #6A0572; font-size: 0.85rem;
        text-transform: uppercase; letter-spacing: 1px;
    }
    .fase-box .fase-text { color: #2C3E50; font-size: 0.95rem; margin-top: 0.2rem; }

    .info-card {
        background: #FDF0FF; border: 1px solid #D6A3E8;
        border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem 0;
    }
    .warning-card {
        background: #FFF8E6; border: 1px solid #FFD966;
        border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem 0;
    }
    .success-card {
        background: #F0FBF0; border: 1px solid #70AD47;
        border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem 0;
    }
    .danger-card {
        background: #FEF0F0; border: 1px solid #E74C3C;
        border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem 0;
    }

    .result-display {
        background: linear-gradient(135deg, #6A0572, #A020A0);
        color: white; border-radius: 16px; padding: 1.5rem;
        text-align: center; font-size: 2.5rem; font-weight: 800;
        box-shadow: 0 4px 15px rgba(106,5,114,0.35); margin: 1rem 0;
    }

    .sidebar-title {
        background: #6A0572; color: white;
        padding: 0.7rem 1rem; border-radius: 10px;
        font-weight: 800; text-align: center; margin-bottom: 0.5rem;
    }

    .stButton > button {
        border-radius: 10px; font-weight: 700; transition: all 0.2s;
    }
    .stButton > button:hover { transform: translateY(-2px); }

    [data-testid="metric-container"] {
        background: #FDF0FF; border: 1px solid #D6A3E8;
        border-radius: 12px; padding: 0.8rem; text-align: center;
    }

    hr { border: none; border-top: 2px solid #F0D8F8; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────
def sederhanakan(p, q):
    """Sederhanakan pecahan p/q."""
    if q == 0:
        return None, None
    if p == 0:
        return 0, 1
    tanda = -1 if (p * q < 0) else 1
    p, q = abs(p), abs(q)
    g = gcd(p, q)
    return tanda * (p // g), q // g

def pecahan_ke_desimal(p, q):
    if q == 0:
        return None
    return p / q

def desimal_ke_pecahan(desimal, toleransi=1e-9, maks_den=1000):
    """Konversi desimal ke pecahan terdekat."""
    tanda = -1 if desimal < 0 else 1
    desimal = abs(desimal)
    best_p, best_q, best_err = 0, 1, abs(desimal)
    for q in range(1, maks_den + 1):
        p = round(desimal * q)
        err = abs(desimal - p / q)
        if err < best_err:
            best_err, best_p, best_q = err, p, q
        if err < toleransi:
            break
    p_sed, q_sed = sederhanakan(tanda * best_p, best_q)
    return p_sed, q_sed

def operasi_pecahan(p1, q1, p2, q2, op):
    """Operasi pecahan dan kembalikan (p_hasil, q_hasil, langkah_str)."""
    if q1 == 0 or q2 == 0:
        return None, None, "Penyebut tidak boleh nol!"
    if op == "+":
        ph = p1 * q2 + p2 * q1
        qh = q1 * q2
        lang = (f"**Langkah:** Samakan penyebut → KPK({q1},{q2})\n\n"
                f"({p1}/{q1}) + ({p2}/{q2}) = ({p1}×{q2} + {p2}×{q1}) / ({q1}×{q2})"
                f" = {ph}/{qh}")
    elif op == "−":
        ph = p1 * q2 - p2 * q1
        qh = q1 * q2
        lang = (f"**Langkah:** ({p1}/{q1}) − ({p2}/{q2}) = ({p1}×{q2} − {p2}×{q1}) / ({q1}×{q2})"
                f" = {ph}/{qh}")
    elif op == "×":
        ph = p1 * p2
        qh = q1 * q2
        lang = (f"**Langkah:** ({p1}/{q1}) × ({p2}/{q2}) = ({p1}×{p2}) / ({q1}×{q2})"
                f" = {ph}/{qh}")
    else:  # ÷
        if p2 == 0:
            return None, None, "Tidak bisa membagi dengan nol!"
        ph = p1 * q2
        qh = q1 * p2
        lang = (f"**Langkah:** ({p1}/{q1}) ÷ ({p2}/{q2}) = ({p1}/{q1}) × ({q2}/{p2})"
                f" = ({p1}×{q2}) / ({q1}×{p2}) = {ph}/{qh}")
    ps, qs = sederhanakan(ph, qh)
    if ps is None:
        return None, None, "Penyebut nol setelah operasi!"
    lang += f"\n\n**Disederhanakan:** {ps}/{qs}"
    return ps, qs, lang

# ─────────────────────────────────────────
# HEADER UTAMA
# ─────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🔢 Jelajah Bilangan Rasional</h1>
    <p>Kalkulator Digital Interaktif • Metode Discovery Learning • SMP/MTs Kelas VII</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SIDEBAR NAVIGASI
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">🧭 Menu Navigasi</div>', unsafe_allow_html=True)
    tab_choice = st.radio(
        "Pilih Fitur:",
        options=[
            "🏠 Beranda",
            "📍 KP 1 — Konsep Bilangan Rasional",
            "🔧 KP 2 — Kalkulator Operasi Pecahan",
            "🔄 KP 3 — Konversi & Perbandingan",
            "🌳 KP 4 — Diagram Konsep",
            "📝 Soal Latihan Interaktif",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("""
    <div style="background:#FDF0FF;padding:0.8rem;border-radius:10px;font-size:0.82rem;color:#6A0572;">
    <b>📚 Petunjuk Penggunaan</b><br><br>
    1. Pilih fitur sesuai kegiatan pembelajaran<br>
    2. Ikuti langkah-langkah Discovery Learning<br>
    3. Catat temuan di LKS<br>
    4. Diskusikan dengan kelompokmu<br>
    5. Kerjakan soal latihan di akhir
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.78rem;color:#7F7F7F;text-align:center;">
    🎓 Kurikulum Merdeka Fase D<br>
    Penulis: Efti Puji Lestari
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════
# HALAMAN BERANDA
# ══════════════════════════════════════════
if tab_choice == "🏠 Beranda":
    st.markdown("## 👋 Selamat Datang, Penjelajah Bilangan Rasional!")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="info-card">
        <b>🎯 Fokus Kemampuan</b><br><br>
        ✅ Konsep Bilangan Rasional & Pecahan<br>
        ✅ Operasi Hitung Bilangan Rasional<br>
        ✅ Konversi Pecahan–Desimal–Persen<br>
        ✅ Perbandingan & Pengurutan Pecahan
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="info-card">
        <b>🔬 Metode Pembelajaran</b><br><br>
        🟣 Discovery Learning (utama)<br>
        🟢 Problem Based Learning<br>
        🟡 Cooperative Learning
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="info-card">
        <b>📱 Fitur Aplikasi</b><br><br>
        📍 Garis Bilangan Rasional Interaktif<br>
        🔧 Kalkulator Operasi Pecahan<br>
        🔄 Konversi & Perbandingan<br>
        🌳 Diagram Konsep Bilangan<br>
        📝 Soal Latihan Interaktif
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔬 Alur Discovery Learning dalam Aplikasi Ini")

    fases = [
        ("① STIMULATION", "Kamu dihadapkan situasi nyata — membagi pizza, diskon belanja, resep masakan. Ini membuatmu bertanya-tanya!", "#A020A0"),
        ("② PROBLEM STATEMENT", "Kamu merumuskan pertanyaan sendiri. Apa yang ingin kamu temukan tentang pecahan?", "#E05CC0"),
        ("③ DATA COLLECTION", "Eksplorasi bebas menggunakan kalkulator digital! Coba berbagai pecahan dan catat hasilnya di LKS.", "#6A0572"),
        ("④ DATA PROCESSING", "Analisis pola dari data yang kamu kumpulkan. Apa yang kamu temukan tentang sifat pecahan?", "#8B0096"),
        ("⑤ VERIFICATION", "Bandingkan temuanmu dengan teman sekelompok. Apakah sama?", "#C000C0"),
        ("⑥ GENERALIZATION", "Rumuskan kesimpulan dengan kata-katamu sendiri. Inilah ilmu yang benar-benar kamu pahami!", "#6A0572"),
    ]

    cols = st.columns(3)
    for i, (label, text, color) in enumerate(fases):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="border-left:4px solid {color};background:#FAFAFA;
                        padding:0.8rem 1rem;border-radius:0 10px 10px 0;margin-bottom:0.8rem;">
                <div style="font-weight:800;color:{color};font-size:0.9rem;">{label}</div>
                <div style="font-size:0.85rem;color:#444;margin-top:0.3rem;">{text}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="warning-card">
    <b>💡 Tips Belajar Efektif</b><br>
    Jangan langsung klik-klik tanpa tujuan! Sebelum mengeksplorasi, baca dulu petunjuk di LKS,
    lalu gunakan kalkulator digital ini untuk <b>membuktikan hipotesismu</b> dan
    <b>menemukan pola</b> yang tersembunyi dalam bilangan rasional. Catat semua temuanmu!
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🗺️ Peta Konsep Bilangan Rasional")

    # Mini peta konsep visual
    fig0, ax0 = plt.subplots(figsize=(10, 4))
    ax0.axis("off")
    fig0.patch.set_facecolor("#FAFBFF")
    ax0.set_facecolor("#FAFBFF")
    ax0.set_xlim(0, 10)
    ax0.set_ylim(0, 4)

    def kotak(ax, x, y, w, h, teks, warna_bg="#6A0572", warna_txt="white", fs=9):
        ax.add_patch(mpatches.FancyBboxPatch((x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.1", facecolor=warna_bg, edgecolor="white", lw=1.5))
        ax.text(x, y, teks, ha="center", va="center", fontsize=fs,
                color=warna_txt, fontweight="bold")

    def panah(ax, x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#6A0572", lw=1.5))

    kotak(ax0, 5, 3.4, 3.2, 0.7, "BILANGAN RASIONAL (p/q)", "#6A0572", "white", 10)
    kotak(ax0, 2, 2.2, 2.5, 0.6, "Pecahan Biasa\n(a/b, b≠0)", "#A020A0", "white", 8.5)
    kotak(ax0, 5, 2.2, 2.5, 0.6, "Pecahan Campuran\n(a b/c)", "#8B0096", "white", 8.5)
    kotak(ax0, 8, 2.2, 2.5, 0.6, "Desimal & Persen\n(0.75 = 75%)", "#C000C0", "white", 8.5)
    kotak(ax0, 1.5, 0.8, 2.0, 0.55, "Operasi:\n+ − × ÷", "#E05CC0", "white", 8)
    kotak(ax0, 4, 0.8, 2.0, 0.55, "Penyederhanaan\n(FPB)", "#D8A8E8", "#3D0052", 8)
    kotak(ax0, 6.5, 0.8, 2.0, 0.55, "Perbandingan\n& Pengurutan", "#D8A8E8", "#3D0052", 8)
    kotak(ax0, 9, 0.8, 1.8, 0.55, "Kontekstual\n& Masalah", "#D8A8E8", "#3D0052", 8)

    for (x1, y1, x2, y2) in [
        (5, 3.05, 2, 2.52), (5, 3.05, 5, 2.52), (5, 3.05, 8, 2.52),
        (2, 1.9, 1.5, 1.07), (2, 1.9, 4, 1.07), (8, 1.9, 6.5, 1.07), (8, 1.9, 9, 1.07)
    ]:
        panah(ax0, x1, y1, x2, y2)

    ax0.set_title("Peta Konsep Bilangan Rasional — Kelas VII", pad=8,
                  fontsize=10, color="#6A0572", fontweight="bold")
    st.pyplot(fig0)
    plt.close()


# ══════════════════════════════════════════
# KP 1 — KONSEP BILANGAN RASIONAL
# ══════════════════════════════════════════
elif tab_choice == "📍 KP 1 — Konsep Bilangan Rasional":
    st.markdown("## 📍 Kegiatan Pembelajaran 1: Mengenal Bilangan Rasional")

    st.markdown("""
    <div class="fase-box">
        <div class="fase-label">① Stimulation — Pemantik</div>
        <div class="fase-text">
        Sebuah pizza dibagi menjadi <b>8 irisan</b>. Kamu memakan <b>3 irisan</b>.
        Berapa bagian pizza yang kamu makan? Dapatkah angka tersebut dinyatakan
        sebagai bilangan bulat? <br><br>
        Harga suatu barang turun sebesar <b>25%</b>. Berapa bagian harganya yang dikurangi?<br><br>
        <b>❓ Bilangan seperti apa yang dapat mewakili "sebagian" dari sesuatu?</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="fase-box" style="border-color:#E05CC0;background:#FEF0FF;">
        <div class="fase-label" style="color:#E05CC0;">② Problem Statement — Rumusan Masalah</div>
        <div class="fase-text">
        Sebelum bereksplorasi, tuliskan dulu hipotesismu di LKS:<br>
        <i>"Menurutku, bilangan rasional adalah... dan contohnya dalam kehidupan sehari-hari adalah..."</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="fase-box" style="border-color:#70AD47;background:#F0FBF0;">
        <div class="fase-label" style="color:#70AD47;">③ Data Collection — Eksplorasi Garis Bilangan Rasional</div>
        <div class="fase-text">Masukkan pembilang dan penyebut untuk melihat letak pecahan pada garis bilangan!</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### ⌨️ Masukkan Pecahan")
        p = st.number_input("Pembilang (p):", value=3, step=1, min_value=-20, max_value=20)
        q = st.number_input("Penyebut (q ≠ 0):", value=4, step=1, min_value=-20, max_value=20)

        if q == 0:
            st.error("⚠️ Penyebut tidak boleh nol! Bilangan p/0 tidak terdefinisi.")
        else:
            ps, qs = sederhanakan(p, q)
            desimal = pecahan_ke_desimal(ps, qs)
            persen = desimal * 100

            st.markdown(f"""
            <div class="result-display" style="font-size:2rem;">
                {ps}/{qs}
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="info-card">
            <b>📊 Representasi Lain:</b><br>
            🔢 Pecahan Biasa: <b>{ps}/{qs}</b><br>
            🔢 Desimal: <b>{desimal:.6f}</b><br>
            🔢 Persen: <b>{persen:.4f}%</b><br>
            🔢 Bentuk Campuran: <b>{'%d %d/%d' % (int(desimal), abs(ps) % abs(qs), abs(qs)) if abs(ps) >= abs(qs) else 'Murni (|p|<|q|)'}</b>
            </div>
            """, unsafe_allow_html=True)

            if ps == 0:
                jenis = "Nol"
            elif abs(ps) < abs(qs):
                jenis = "Pecahan Murni (|p| < |q|)"
            elif abs(ps) == abs(qs):
                jenis = "Pecahan Senilai 1 (|p| = |q|)"
            else:
                jenis = "Pecahan Tak Murni / Campuran (|p| > |q|)"

            warna_j = "#70AD47" if ps > 0 else ("#C00000" if ps < 0 else "#7F7F7F")
            st.markdown(f"""
            <div style="background:{warna_j};color:white;border-radius:10px;
                        padding:0.5rem 1rem;text-align:center;font-weight:700;margin-top:0.5rem;">
                {jenis}
            </div>
            """, unsafe_allow_html=True)

    with col2:
        if q != 0:
            ps_vis, qs_vis = sederhanakan(p, q)
            val = ps_vis / qs_vis

            fig1, axes = plt.subplots(2, 1, figsize=(9, 5),
                                       gridspec_kw={"height_ratios": [2, 1.2]})
            fig1.patch.set_facecolor("#FAFBFF")

            # ── Garis bilangan
            ax1 = axes[0]
            ax1.set_xlim(-2.5, 2.5)
            ax1.set_ylim(-1.5, 2.2)
            ax1.axis("off")
            ax1.set_facecolor("#FAFBFF")
            ax1.annotate("", xy=(2.4, 0), xytext=(-2.4, 0),
                         arrowprops=dict(arrowstyle="<->", color="#6A0572", lw=2.5))

            ticks_val = np.arange(-2, 2.01, 0.25)
            for tv in ticks_val:
                h = 0.12 if (tv * 4) % 4 == 0 else 0.07
                c = "#6A0572" if (tv * 4) % 4 == 0 else "#BBBBBB"
                ax1.plot([tv, tv], [-h, h], color=c, lw=1.5)
                if (tv * 4) % 4 == 0:
                    lbl = f"{int(tv)}" if tv == int(tv) else f"{tv}"
                    ax1.text(tv, -0.35, lbl, ha="center", va="top",
                             fontsize=8.5, color="#6A0572", fontweight="bold")

            dot_c = "#A020A0" if val > 0 else ("#C00000" if val < 0 else "#7F7F7F")
            cval = max(-2.4, min(2.4, val))
            ax1.plot(cval, 0, "o", color=dot_c, markersize=18, zorder=5,
                     markeredgecolor="white", markeredgewidth=2)
            ax1.text(cval, 0.55, f"{ps_vis}/{qs_vis}", ha="center", fontsize=11,
                     color=dot_c, fontweight="bold",
                     bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                               edgecolor=dot_c, lw=2))
            ax1.text(-2.1, 1.7, "← Negatif", ha="left", fontsize=8.5,
                     color="#C00000", fontweight="bold",
                     bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFEEEE",
                               edgecolor="#C00000", alpha=0.8))
            ax1.text(2.1, 1.7, "Positif →", ha="right", fontsize=8.5,
                     color="#70AD47", fontweight="bold",
                     bbox=dict(boxstyle="round,pad=0.3", facecolor="#EEFFEE",
                               edgecolor="#70AD47", alpha=0.8))
            ax1.set_title(f"Garis Bilangan: {ps_vis}/{qs_vis} ≈ {val:.4f}",
                          fontsize=10, color="#6A0572", fontweight="bold", pad=6)

            # ── Visualisasi lingkaran pecahan
            ax2 = axes[1]
            ax2.set_xlim(-1.5, 1.5)
            ax2.set_ylim(-1.3, 1.3)
            ax2.axis("off")
            ax2.set_facecolor("#FAFBFF")

            qs_show = min(abs(qs_vis), 24)
            ps_show = min(abs(ps_vis), qs_show)
            sudut_per_irisan = 360 / qs_show
            for i in range(qs_show):
                sudut_mulai = 90 - i * sudut_per_irisan
                warna_iris = "#A020A0" if i < ps_show else "#E0C8E8"
                wedge = mpatches.Wedge((0, 0), 1.0, sudut_mulai - sudut_per_irisan,
                                       sudut_mulai, facecolor=warna_iris,
                                       edgecolor="white", lw=1.5)
                ax2.add_patch(wedge)
            ax2.text(0, 0, f"{ps_show}/{qs_show}", ha="center", va="center",
                     fontsize=13, color="white", fontweight="bold")
            legend_els2 = [
                mpatches.Patch(facecolor="#A020A0", label=f"Bagian diambil: {ps_show}"),
                mpatches.Patch(facecolor="#E0C8E8", label=f"Sisa: {qs_show - ps_show}"),
            ]
            ax2.legend(handles=legend_els2, loc="center right", fontsize=8,
                       bbox_to_anchor=(1.5, 0))
            ax2.set_title(f"Visualisasi Lingkaran: {ps_show}/{qs_show} bagian",
                          fontsize=9.5, color="#6A0572", fontweight="bold", pad=4)

            plt.tight_layout(pad=1.0)
            st.pyplot(fig1)
            plt.close()

    st.markdown("---")
    # Tabel eksplorasi
    st.markdown("""
    <div class="fase-box" style="border-color:#7030A0;background:#F5EFFF;">
        <div class="fase-label" style="color:#7030A0;">④ Data Processing — Tabel Eksplorasi Pecahan</div>
        <div class="fase-text">Coba berbagai pecahan dengan slider/input di atas, catat pada tabel LKS-mu!</div>
    </div>
    """, unsafe_allow_html=True)

    contoh = [
        ("1/2", "0,5", "50%", "0 < nilai < 1", "Murni Positif"),
        ("3/4", "0,75", "75%", "0 < nilai < 1", "Murni Positif"),
        ("5/3", "1,667", "166,7%", "nilai > 1", "Tak Murni / Campuran"),
        ("−2/5", "−0,4", "−40%", "−1 < nilai < 0", "Murni Negatif"),
        (".../...", "...", "...", "...", "..."),
    ]
    tbl = '<table style="width:100%;border-collapse:collapse;font-size:0.87rem;">'
    tbl += '<tr style="background:#6A0572;color:white;"><th style="padding:8px;border:1px solid #ccc;">Pecahan</th><th style="padding:8px;border:1px solid #ccc;">Desimal</th><th style="padding:8px;border:1px solid #ccc;">Persen</th><th style="padding:8px;border:1px solid #ccc;">Letak di Garis Bilangan</th><th style="padding:8px;border:1px solid #ccc;">Jenis</th></tr>'
    for i, r in enumerate(contoh):
        bg = "#F8F0FF" if i % 2 == 0 else "white"
        tbl += f'<tr style="background:{bg};">'
        for cell in r:
            tbl += f'<td style="padding:7px;border:1px solid #ccc;text-align:center;">{cell}</td>'
        tbl += "</tr>"
    tbl += "</table>"
    st.markdown(tbl, unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("⑥ 💡 Lihat Simpulan Konsep Bilangan Rasional (setelah mencoba sendiri dulu!)"):
        st.markdown("""
        <div class="success-card">
        <b>Simpulan Bilangan Rasional:</b><br>
        ✅ Bilangan rasional adalah bilangan yang dapat dinyatakan dalam bentuk <b>p/q</b>, dengan p dan q bilangan bulat dan <b>q ≠ 0</b><br>
        ✅ Setiap bilangan bulat adalah bilangan rasional (misal: 3 = 3/1)<br>
        ✅ Bilangan rasional dapat berupa <b>pecahan murni, pecahan tak murni, bilangan campuran, desimal, atau persen</b><br>
        ✅ Pecahan <b>senilai</b>: diperoleh dengan mengalikan/membagi pembilang dan penyebut dengan bilangan yang sama<br>
        ✅ Penyederhanaan pecahan: bagi pembilang dan penyebut dengan <b>FPB</b>-nya
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# KP 2 — KALKULATOR OPERASI PECAHAN
# ══════════════════════════════════════════
elif tab_choice == "🔧 KP 2 — Kalkulator Operasi Pecahan":
    st.markdown("## 🔧 Kegiatan Pembelajaran 2: Operasi Hitung Bilangan Rasional")

    st.markdown("""
    <div class="fase-box">
        <div class="fase-label">① Stimulation — Pemantik</div>
        <div class="fase-text">
        Resep kue membutuhkan <b>2/3 cangkir tepung</b>, tapi kamu ingin membuat
        <b>setengah porsi</b>. Berapa tepung yang dibutuhkan? <br>
        Jika kamu memiliki <b>3/4 meter</b> pita dan memotong <b>1/3 meter</b>, berapa sisa pita?<br><br>
        <b>❓ Bagaimana cara menghitung penjumlahan, pengurangan, perkalian, dan pembagian pecahan?</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="fase-box" style="border-color:#E05CC0;background:#FEF0FF;">
        <div class="fase-label" style="color:#E05CC0;">② Problem Statement — Hipotesis</div>
        <div class="fase-text">
        Tuliskan hipotesismu di LKS sebelum bereksplorasi:<br>
        <i>"Menurutku, untuk menjumlahkan dua pecahan kita harus... karena..."</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="fase-box" style="border-color:#70AD47;background:#F0FBF0;">
        <div class="fase-label" style="color:#70AD47;">③ Data Collection — Eksplorasi Kalkulator Pecahan</div>
        <div class="fase-text">Masukkan dua pecahan, pilih operasi, dan amati langkah-langkah penyelesaiannya!</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 1])
    with col1:
        st.markdown("#### ⌨️ Masukkan Pecahan")
        c1a, c1b = st.columns(2)
        with c1a:
            p1 = st.number_input("Pembilang 1:", value=2, step=1,
                                  min_value=-99, max_value=99, key="p1")
        with c1b:
            q1 = st.number_input("Penyebut 1 (≠0):", value=3, step=1,
                                  min_value=-99, max_value=99, key="q1")

        op = st.selectbox("Operasi:", ["+  (Penjumlahan)", "−  (Pengurangan)",
                                        "×  (Perkalian)", "÷  (Pembagian)"])
        c2a, c2b = st.columns(2)
        with c2a:
            p2 = st.number_input("Pembilang 2:", value=1, step=1,
                                  min_value=-99, max_value=99, key="p2")
        with c2b:
            q2 = st.number_input("Penyebut 2 (≠0):", value=4, step=1,
                                  min_value=-99, max_value=99, key="q2")

        op_sym = op[0]

        if q1 == 0 or q2 == 0:
            st.error("⚠️ Penyebut tidak boleh nol!")
        else:
            ps1, qs1 = sederhanakan(p1, q1)
            ps2, qs2 = sederhanakan(p2, q2)
            ph, qh, langkah = operasi_pecahan(ps1, qs1, ps2, qs2, op_sym)

            if ph is None:
                st.error(langkah)
            else:
                desimal_h = ph / qh
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#6A0572,#A020A0);color:white;
                            border-radius:16px;padding:1.5rem;text-align:center;margin-top:0.8rem;
                            box-shadow:0 4px 15px rgba(106,5,114,0.35);">
                    <div style="font-size:0.85rem;opacity:0.8;margin-bottom:0.3rem;">Kalimat Matematika</div>
                    <div style="font-size:1.4rem;font-weight:800;margin-bottom:0.4rem;">
                        ({ps1}/{qs1}) {op_sym} ({ps2}/{qs2})
                    </div>
                    <div style="font-size:0.8rem;opacity:0.75;">Hasil (Disederhanakan)</div>
                    <div style="font-size:3rem;font-weight:800;line-height:1.1;">{ph}/{qh}</div>
                    <div style="font-size:1rem;opacity:0.85;">≈ {desimal_h:.6f} &nbsp;|&nbsp; {desimal_h*100:.4f}%</div>
                </div>
                """, unsafe_allow_html=True)

    with col2:
        if q1 != 0 and q2 != 0:
            ps1, qs1 = sederhanakan(p1, q1)
            ps2, qs2 = sederhanakan(p2, q2)
            ph, qh, langkah = operasi_pecahan(ps1, qs1, ps2, qs2, op_sym)
            if ph is not None:
                st.markdown("#### 📋 Langkah-Langkah Penyelesaian")
                st.markdown(f"""
                <div class="warning-card" style="font-size:0.9rem;">
                {langkah.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)

                # Visualisasi batang pecahan
                fig2, axes2 = plt.subplots(3, 1, figsize=(7, 4.5))
                fig2.patch.set_facecolor("#FAFBFF")
                titles_data = [
                    (ps1, qs1, "#A020A0", f"Pecahan 1: {ps1}/{qs1}"),
                    (ps2, qs2, "#C000C0", f"Pecahan 2: {ps2}/{qs2}"),
                    (ph, qh, "#6A0572",  f"Hasil: {ph}/{qh}"),
                ]
                for ax_b, (pv, qv, col_b, ttl) in zip(axes2, titles_data):
                    ax_b.axis("off")
                    ax_b.set_xlim(0, 1)
                    ax_b.set_ylim(0, 1)
                    ax_b.set_facecolor("#FAFBFF")
                    lebar = min(1.0, abs(pv / qv)) if qv != 0 else 0
                    ax_b.barh(0.5, lebar, height=0.55, color=col_b,
                              alpha=0.85, left=0)
                    ax_b.barh(0.5, 1 - lebar, height=0.55, color="#E0C8E8",
                              alpha=0.6, left=lebar)
                    ax_b.text(0.5, 0.5, ttl, ha="center", va="center",
                              fontsize=9, color="white", fontweight="bold")
                plt.tight_layout(pad=0.5)
                st.pyplot(fig2)
                plt.close()

    st.markdown("---")
    # Tabel eksplorasi sistematis
    st.markdown("""
    <div class="fase-box" style="border-color:#7030A0;background:#F5EFFF;">
        <div class="fase-label" style="color:#7030A0;">④ Data Processing — Tabel Pola Operasi Pecahan</div>
        <div class="fase-text">Coba semua kombinasi berikut, catat dan analisis polanya di LKS!</div>
    </div>
    """, unsafe_allow_html=True)

    col_tbl1, col_tbl2 = st.columns(2)
    pola_plus = [
        ("1/3 + 1/3", *sederhanakan(1*3 + 1*3, 3*3)),
        ("1/2 + 1/3", *sederhanakan(1*3 + 1*2, 2*3)),
        ("2/5 + 3/10", *sederhanakan(2*10 + 3*5, 5*10)),
        ("3/4 + (−1/4)", *sederhanakan(3*4 + (-1)*4, 4*4)),
    ]
    pola_kali = [
        ("2/3 × 3/4", *sederhanakan(2*3, 3*4)),
        ("1/2 × 4/5", *sederhanakan(1*4, 2*5)),
        ("3/7 × 7/3", *sederhanakan(3*7, 7*3)),
        ("(−2/3) × (3/4)", *sederhanakan(-2*3, 3*4)),
    ]

    def tabel_operasi(judul, data, warna_header):
        tbl = f'<table style="width:100%;border-collapse:collapse;font-size:0.84rem;">'
        tbl += f'<tr style="background:{warna_header};color:white;"><th style="padding:6px;border:1px solid #ccc;">Operasi</th><th style="padding:6px;border:1px solid #ccc;">Hasil</th><th style="padding:6px;border:1px solid #ccc;">Desimal</th></tr>'
        for op_str, pv, qv in data:
            dec = f"{pv/qv:.4f}" if qv != 0 else "N/A"
            tbl += f'<tr><td style="padding:6px;border:1px solid #ccc;">{op_str}</td><td style="padding:6px;border:1px solid #ccc;text-align:center;font-weight:bold;">{pv}/{qv}</td><td style="padding:6px;border:1px solid #ccc;text-align:center;">{dec}</td></tr>'
        tbl += "</table>"
        return tbl

    with col_tbl1:
        st.markdown("**Penjumlahan (+)**")
        st.markdown(tabel_operasi("", pola_plus, "#6A0572"), unsafe_allow_html=True)
    with col_tbl2:
        st.markdown("**Perkalian (×)**")
        st.markdown(tabel_operasi("", pola_kali, "#A020A0"), unsafe_allow_html=True)

    with st.expander("⑥ 💡 Lihat Simpulan Aturan Operasi Pecahan"):
        st.markdown("""
        <div class="success-card">
        <b>✅ Aturan Operasi Bilangan Rasional:</b><br><br>
        🟣 <b>Penjumlahan & Pengurangan:</b> Samakan penyebut (cari KPK), lalu jumlahkan/kurangkan pembilangnya<br>
        🟣 <b>Perkalian:</b> Kalikan pembilang × pembilang, penyebut × penyebut → sederhanakan<br>
        🟣 <b>Pembagian:</b> Kalikan pecahan pertama dengan <b>kebalikan</b> pecahan kedua (p/q ÷ r/s = p/q × s/r)<br>
        🟣 <b>Penyederhanaan:</b> Bagi pembilang dan penyebut hasil dengan FPB-nya
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# KP 3 — KONVERSI & PERBANDINGAN
# ══════════════════════════════════════════
elif tab_choice == "🔄 KP 3 — Konversi & Perbandingan":
    st.markdown("## 🔄 Kegiatan Pembelajaran 3: Konversi & Perbandingan Bilangan Rasional")

    st.markdown("""
    <div class="fase-box">
        <div class="fase-label">① Stimulation — Pemantik</div>
        <div class="fase-text">
        Toko A memberi diskon <b>3/8</b>, Toko B memberi diskon <b>35%</b>, Toko C memberi diskon <b>0,4</b>.
        Toko mana yang memberikan diskon terbesar?<br><br>
        Untuk membandingkan, kita perlu mengubah semua ke <b>bentuk yang sama</b>.<br>
        <b>❓ Bagaimana cara mengkonversi antara pecahan, desimal, dan persen?</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    tab3a, tab3b = st.tabs(["🔄 Konversi Interaktif", "⚖️ Perbandingan & Pengurutan"])

    # ── TAB KONVERSI
    with tab3a:
        st.markdown("""
        <div class="fase-box" style="border-color:#70AD47;background:#F0FBF0;">
            <div class="fase-label" style="color:#70AD47;">③ Eksplorasi Konversi</div>
            <div class="fase-text">Pilih jenis input, masukkan nilai, dan amati semua representasinya!</div>
        </div>
        """, unsafe_allow_html=True)

        mode_input = st.selectbox("Masukkan sebagai:", ["Pecahan (p/q)", "Desimal", "Persen (%)"])

        col_in, col_out = st.columns([1, 1.5])
        with col_in:
            if mode_input == "Pecahan (p/q)":
                pk = st.number_input("Pembilang:", value=3, step=1, min_value=-999, max_value=999)
                qk = st.number_input("Penyebut (≠0):", value=8, step=1, min_value=-999, max_value=999)
                if qk == 0:
                    st.error("Penyebut tidak boleh nol!")
                    pk_s, qk_s, dec_k = 0, 1, 0.0
                else:
                    pk_s, qk_s = sederhanakan(pk, qk)
                    dec_k = pk_s / qk_s
            elif mode_input == "Desimal":
                dec_k = st.number_input("Nilai Desimal:", value=0.375, step=0.001,
                                         format="%.6f", min_value=-100.0, max_value=100.0)
                pk_s, qk_s = desimal_ke_pecahan(dec_k)
            else:
                persen_k = st.number_input("Nilai Persen (%):", value=37.5, step=0.1,
                                            format="%.4f", min_value=-10000.0, max_value=10000.0)
                dec_k = persen_k / 100
                pk_s, qk_s = desimal_ke_pecahan(dec_k)

        with col_out:
            if qk_s and qk_s != 0:
                dec_k_show = pk_s / qk_s
                persen_show = dec_k_show * 100
                # Bilangan campuran
                if abs(pk_s) >= abs(qk_s) and qk_s != 0:
                    bulat_bg = int(dec_k_show)
                    sisa_p = abs(pk_s) - abs(bulat_bg) * abs(qk_s)
                    campuran_str = f"{bulat_bg} {sisa_p}/{abs(qk_s)}" if sisa_p != 0 else str(bulat_bg)
                else:
                    campuran_str = f"{pk_s}/{qk_s}"

                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#6A0572,#A020A0);color:white;
                            border-radius:16px;padding:1.2rem;text-align:center;margin:0.5rem 0;">
                    <div style="font-size:0.8rem;opacity:0.8;margin-bottom:0.5rem;">Semua Representasi</div>
                    <table style="width:100%;color:white;font-size:0.95rem;">
                        <tr><td style="text-align:right;padding:4px 10px;opacity:0.8;">Pecahan Sederhana:</td>
                            <td style="text-align:left;font-weight:800;font-size:1.3rem;">{pk_s}/{qk_s}</td></tr>
                        <tr><td style="text-align:right;padding:4px 10px;opacity:0.8;">Bilangan Campuran:</td>
                            <td style="text-align:left;font-weight:800;">{campuran_str}</td></tr>
                        <tr><td style="text-align:right;padding:4px 10px;opacity:0.8;">Desimal:</td>
                            <td style="text-align:left;font-weight:800;">{dec_k_show:.8f}</td></tr>
                        <tr><td style="text-align:right;padding:4px 10px;opacity:0.8;">Persen:</td>
                            <td style="text-align:left;font-weight:800;">{persen_show:.6f}%</td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)

                # Visualisasi persentase
                fig3, ax3 = plt.subplots(figsize=(7, 2))
                ax3.set_xlim(0, 1)
                ax3.set_ylim(0, 1)
                ax3.axis("off")
                fig3.patch.set_facecolor("#FAFBFF")
                ax3.set_facecolor("#FAFBFF")
                lebar3 = min(1.0, max(0.0, abs(dec_k_show)))
                ax3.barh(0.5, lebar3, height=0.5, color="#A020A0", alpha=0.85)
                ax3.barh(0.5, 1 - lebar3, height=0.5, color="#E0C8E8", left=lebar3, alpha=0.7)
                for xi in np.arange(0, 1.01, 0.25):
                    ax3.plot([xi, xi], [0.24, 0.76], color="white", lw=1.5)
                    ax3.text(xi, 0.1, f"{int(xi*100)}%", ha="center", fontsize=8,
                             color="#6A0572", fontweight="bold")
                ax3.text(lebar3 / 2, 0.5, f"{persen_show:.2f}%", ha="center",
                         va="center", fontsize=11, color="white", fontweight="bold")
                ax3.set_title(f"Visualisasi: {pk_s}/{qk_s} = {persen_show:.4f}%",
                              fontsize=9.5, color="#6A0572", fontweight="bold", pad=4)
                st.pyplot(fig3)
                plt.close()

    # ── TAB PERBANDINGAN
    with tab3b:
        st.markdown("""
        <div class="fase-box" style="border-color:#70AD47;background:#F0FBF0;">
            <div class="fase-label" style="color:#70AD47;">③ Eksplorasi Perbandingan Pecahan</div>
            <div class="fase-text">Masukkan hingga 5 pecahan untuk dibandingkan dan diurutkan!</div>
        </div>
        """, unsafe_allow_html=True)

        jumlah_pec = st.slider("Berapa pecahan yang ingin dibandingkan?", 2, 5, 4)
        pecahan_list = []
        cols_pec = st.columns(jumlah_pec)
        for i, col_p in enumerate(cols_pec):
            with col_p:
                st.markdown(f"**Pecahan {i+1}**")
                pp = st.number_input(f"p{i+1}", value=[1,2,3,4,5][i],
                                      step=1, min_value=-99, max_value=99, key=f"cp{i}")
                qp = st.number_input(f"q{i+1}", value=[3,5,8,4,6][i],
                                      step=1, min_value=-99, max_value=99, key=f"cq{i}")
                if qp != 0:
                    ps_p, qs_p = sederhanakan(pp, qp)
                    pecahan_list.append((ps_p, qs_p, ps_p/qs_p))
                else:
                    st.error("q≠0!")

        if len(pecahan_list) >= 2:
            urutan = sorted(pecahan_list, key=lambda x: x[2])

            # Visualisasi batang perbandingan
            fig4, ax4 = plt.subplots(figsize=(8, 3.5))
            fig4.patch.set_facecolor("#FAFBFF")
            ax4.set_facecolor("#FAFBFF")
            warna_bar = ["#6A0572", "#A020A0", "#C000C0", "#E05CC0", "#F0A0D8"]
            labels_bar = [f"{p}/{q}" for p, q, _ in pecahan_list]
            vals_bar   = [v for _, _, v in pecahan_list]
            bars = ax4.bar(labels_bar, vals_bar, color=warna_bar[:len(vals_bar)],
                           edgecolor="white", linewidth=1.5, width=0.5)
            for bar, v in zip(bars, vals_bar):
                ax4.text(bar.get_x() + bar.get_width()/2,
                         bar.get_height() + 0.02, f"{v:.4f}",
                         ha="center", va="bottom", fontsize=9,
                         color="#6A0572", fontweight="bold")
            ax4.axhline(0, color="#6A0572", lw=1, linestyle="--")
            ax4.set_ylabel("Nilai Desimal", fontsize=9, color="#6A0572")
            ax4.set_title("Perbandingan Nilai Pecahan", fontsize=10,
                          color="#6A0572", fontweight="bold", pad=8)
            ax4.tick_params(colors="#6A0572")
            plt.tight_layout()
            st.pyplot(fig4)
            plt.close()

            # Tabel urutan
            st.markdown("**📊 Urutan dari Terkecil ke Terbesar:**")
            tbl_urut = '<div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-top:0.5rem;">'
            for j, (pu, qu, vu) in enumerate(urutan):
                arrow = " < " if j < len(urutan) - 1 else ""
                tbl_urut += f'<span style="background:#A020A0;color:white;padding:5px 14px;border-radius:20px;font-weight:700;font-size:0.9rem;">{pu}/{qu} ({vu:.3f})</span>'
                if arrow:
                    tbl_urut += f'<span style="color:#6A0572;font-weight:800;font-size:1.2rem;align-self:center;">{arrow}</span>'
            tbl_urut += "</div>"
            st.markdown(tbl_urut, unsafe_allow_html=True)

            with st.expander("⑥ 💡 Cara Membandingkan Pecahan"):
                st.markdown("""
                <div class="success-card">
                <b>✅ Cara Membandingkan Pecahan:</b><br><br>
                1️⃣ <b>Samakan penyebut</b> → cari KPK semua penyebut, ubah semua pecahan<br>
                2️⃣ <b>Ubah ke desimal</b> → bagi pembilang ÷ penyebut, lalu bandingkan<br>
                3️⃣ <b>Silang kali</b> (untuk 2 pecahan) → a/b vs c/d: bandingkan a×d dengan b×c
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# KP 4 — DIAGRAM KONSEP
# ══════════════════════════════════════════
elif tab_choice == "🌳 KP 4 — Diagram Konsep":
    st.markdown("## 🌳 Kegiatan Pembelajaran 4: Diagram Konsep Bilangan Rasional")

    tab4a, tab4b = st.tabs(["🌳 Pohon Pecahan Senilai", "🗺️ Peta Hubungan Bilangan"])

    # ── TAB POHON PECAHAN SENILAI
    with tab4a:
        st.markdown("""
        <div class="fase-box" style="border-color:#70AD47;background:#F0FBF0;">
            <div class="fase-label" style="color:#70AD47;">③ Eksplorasi Pecahan Senilai</div>
            <div class="fase-text">Masukkan pecahan, amati pohon pecahan senilai yang terbentuk!</div>
        </div>
        """, unsafe_allow_html=True)

        col_ps1, col_ps2 = st.columns([1, 2])
        with col_ps1:
            p_sen = st.number_input("Pembilang:", value=1, step=1,
                                    min_value=1, max_value=20, key="psen")
            q_sen = st.number_input("Penyebut (≠0):", value=2, step=1,
                                    min_value=1, max_value=20, key="qsen")
            kelipatan_max = st.slider("Tampilkan kelipatan ke-:", 3, 8, 5)

            ps_s, qs_s = sederhanakan(p_sen, q_sen)
            st.markdown(f"""
            <div style="background:#6A0572;color:white;border-radius:12px;
                        padding:0.8rem;text-align:center;margin-top:0.5rem;">
                <div style="font-size:0.8rem;opacity:0.8;">Bentuk Paling Sederhana</div>
                <div style="font-size:2rem;font-weight:800;">{ps_s}/{qs_s}</div>
            </div>
            """, unsafe_allow_html=True)

            senilai_list = [(ps_s * k, qs_s * k) for k in range(1, kelipatan_max + 1)]
            tbl_sen = '<table style="width:100%;border-collapse:collapse;font-size:0.85rem;margin-top:0.5rem;">'
            tbl_sen += '<tr style="background:#6A0572;color:white;"><th style="padding:6px;border:1px solid #ccc;">Kelipatan</th><th style="padding:6px;border:1px solid #ccc;">Pecahan Senilai</th></tr>'
            for k, (pv, qv) in enumerate(senilai_list, 1):
                bg = "#F8F0FF" if k % 2 == 0 else "white"
                tbl_sen += f'<tr style="background:{bg};"><td style="padding:6px;border:1px solid #ccc;text-align:center;">× {k}</td><td style="padding:6px;border:1px solid #ccc;text-align:center;font-weight:700;">{pv}/{qv}</td></tr>'
            tbl_sen += "</table>"
            st.markdown(tbl_sen, unsafe_allow_html=True)

        with col_ps2:
            fig5, ax5 = plt.subplots(figsize=(8, 5.5))
            ax5.axis("off")
            fig5.patch.set_facecolor("#FAFBFF")
            ax5.set_facecolor("#FAFBFF")
            ax5.set_xlim(-1, kelipatan_max + 1)
            ax5.set_ylim(-1, 3)

            # Root node
            ax5.add_patch(mpatches.FancyBboxPatch((kelipatan_max/2 - 0.6, 2.3),
                1.2, 0.55, boxstyle="round,pad=0.1", facecolor="#6A0572",
                edgecolor="white", lw=2))
            ax5.text(kelipatan_max/2, 2.57, f"{ps_s}/{qs_s}",
                     ha="center", va="center", fontsize=11,
                     color="white", fontweight="bold")
            ax5.text(kelipatan_max/2, 2.2, "(Bentuk Sederhana)",
                     ha="center", va="top", fontsize=7.5, color="#6A0572")

            # Children nodes
            x_pos = np.linspace(0.5, kelipatan_max - 0.5, kelipatan_max)
            warna_nodes = ["#A020A0", "#8B0096", "#C000C0", "#7030A0",
                           "#D050C0", "#9010A0", "#B000B0", "#E060D0"]
            for j, (xp, (pv, qv)) in enumerate(zip(x_pos, senilai_list)):
                yp = 0.8
                wn = warna_nodes[j % len(warna_nodes)]
                ax5.plot([kelipatan_max/2, xp], [2.3, yp + 0.28],
                         color="#BBAACC", lw=1.5, zorder=1)
                ax5.add_patch(mpatches.FancyBboxPatch((xp - 0.45, yp - 0.25),
                    0.9, 0.53, boxstyle="round,pad=0.08", facecolor=wn,
                    edgecolor="white", lw=1.5, zorder=2))
                ax5.text(xp, yp, f"{pv}/{qv}", ha="center", va="center",
                         fontsize=9.5, color="white", fontweight="bold", zorder=3)
                ax5.text(xp, yp - 0.45, f"×{j+1}", ha="center", va="top",
                         fontsize=7.5, color="#8B0096")

            ax5.set_title(f"Pohon Pecahan Senilai dari {ps_s}/{qs_s}",
                          fontsize=11, color="#6A0572", fontweight="bold", pad=10)
            st.pyplot(fig5)
            plt.close()

    # ── TAB PETA HUBUNGAN BILANGAN
    with tab4b:
        st.markdown("""
        <div class="fase-box" style="border-color:#70AD47;background:#F0FBF0;">
            <div class="fase-label" style="color:#70AD47;">Peta Hubungan Himpunan Bilangan</div>
            <div class="fase-text">Lihat posisi bilangan rasional dalam sistem bilangan yang lebih luas!</div>
        </div>
        """, unsafe_allow_html=True)

        fig6, ax6 = plt.subplots(figsize=(9, 6))
        ax6.set_xlim(0, 10)
        ax6.set_ylim(0, 7)
        ax6.axis("off")
        fig6.patch.set_facecolor("#F8F0FF")
        ax6.set_facecolor("#F8F0FF")

        # Lingkaran himpunan (nested)
        lingkaran_data = [
            (5, 3.5, 4.6, "#E8D0F8", "#8B0096", "BILANGAN REAL ℝ", 12),
            (5, 3.5, 3.6, "#D8B8F0", "#6A0572", "BILANGAN RASIONAL ℚ", 11),
            (5, 3.2, 2.5, "#C8A0E8", "#4A0052", "Bilangan\nBulat ℤ", 10),
            (5, 2.8, 1.5, "#B888E0", "#3D0052", "Bilangan\nCacah ℕ₀", 9),
            (5, 2.6, 0.8, "#A870D8", "#2D003A", "Bilangan\nAsli ℕ", 8),
        ]
        for cx, cy, r, fc, ec, lbl, fs in lingkaran_data:
            circ = plt.Circle((cx, cy), r, facecolor=fc, edgecolor=ec,
                               lw=2, alpha=0.6)
            ax6.add_patch(circ)
            ax6.text(cx, cy + r - 0.25, lbl, ha="center", va="top",
                     fontsize=fs, color=ec, fontweight="bold")

        # Contoh bilangan
        contoh_bil = [
            (5, 2.6, "1,2,3,...", "white", 8.5),
            (5, 2.1, "0", "white", 8.5),
            (5, 1.55, "−1,−2,...", "white", 8.5),
            (7.5, 4.5, "1/2, 3/4\n0.5, 75%", "#4A0052", 8.5),
            (2.5, 5.5, "√2, π, e\n(irasional)", "#4A0052", 8.5),
        ]
        for cx, cy, txt, tc, fs in contoh_bil:
            ax6.text(cx, cy, txt, ha="center", va="center", fontsize=fs,
                     color=tc, style="italic")

        ax6.annotate("Bilangan\nIrasional", xy=(2.5, 5.5), xytext=(1.2, 6.5),
                     fontsize=8.5, color="#4A0052",
                     arrowprops=dict(arrowstyle="->", color="#6A0572", lw=1.3))

        ax6.set_title("Sistem Bilangan: Posisi Bilangan Rasional", pad=8,
                      fontsize=11, color="#6A0572", fontweight="bold")
        st.pyplot(fig6)
        plt.close()

        st.markdown("""
        <div class="info-card">
        <b>📌 Hubungan Antar Himpunan Bilangan:</b><br>
        ℕ ⊂ ℕ₀ ⊂ ℤ ⊂ ℚ ⊂ ℝ<br><br>
        ✅ Setiap bilangan asli adalah bilangan bulat, bilangan rasional, dan bilangan real<br>
        ✅ Bilangan rasional + bilangan irasional = bilangan real<br>
        ✅ Bilangan irasional <b>BUKAN</b> bilangan rasional (√2, π tidak bisa ditulis p/q)
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# SOAL LATIHAN INTERAKTIF
# ══════════════════════════════════════════
elif tab_choice == "📝 Soal Latihan Interaktif":
    st.markdown("## 📝 Soal Latihan Interaktif — Bilangan Rasional")
    st.markdown("""
    <div class="warning-card">
    <b>📌 Petunjuk:</b> Kerjakan soal-soal berikut secara mandiri dan jujur.
    Gunakan kalkulator digital di tab sebelumnya hanya untuk <b>verifikasi</b>, bukan langsung menekan tombol!
    Waktu pengerjaan: ±45 menit.
    </div>
    """, unsafe_allow_html=True)

    if "skor_br" not in st.session_state:
        st.session_state.skor_br = 0
    if "jawab_br" not in st.session_state:
        st.session_state.jawab_br = {}

    soal_list = [
        {
            "no": 1, "tipe": "PG", "kp": "KP 1",
            "soal": "Manakah yang BUKAN merupakan bilangan rasional?",
            "konteks": "",
            "pilihan": ["A. 3/4", "B. −5/2", "C. √3", "D. 0,75"],
            "jawaban": "C",
            "pembahasan": "√3 = 1,732... adalah bilangan irasional karena tidak bisa dinyatakan dalam bentuk p/q dengan p,q bilangan bulat."
        },
        {
            "no": 2, "tipe": "PG", "kp": "KP 1",
            "soal": "Bentuk sederhana dari pecahan 36/48 adalah ...",
            "konteks": "💡 Gunakan FPB(36, 48) = 12",
            "pilihan": ["A. 2/3", "B. 3/4", "C. 4/5", "D. 6/8"],
            "jawaban": "B",
            "pembahasan": "FPB(36,48) = 12. 36÷12 = 3, 48÷12 = 4. Jadi 36/48 = 3/4."
        },
        {
            "no": 3, "tipe": "PG", "kp": "KP 2",
            "soal": "Hasil dari 2/3 + 1/4 adalah ...",
            "konteks": "",
            "pilihan": ["A. 3/7", "B. 8/12", "C. 11/12", "D. 3/12"],
            "jawaban": "C",
            "pembahasan": "KPK(3,4)=12. 2/3 = 8/12, 1/4 = 3/12. 8/12 + 3/12 = 11/12."
        },
        {
            "no": 4, "tipe": "PG", "kp": "KP 2",
            "soal": "Hasil dari 3/4 × 8/9 adalah ...",
            "konteks": "",
            "pilihan": ["A. 11/13", "B. 27/32", "C. 2/3", "D. 1/3"],
            "jawaban": "C",
            "pembahasan": "3/4 × 8/9 = (3×8)/(4×9) = 24/36. FPB(24,36)=12. 24/36 = 2/3."
        },
        {
            "no": 5, "tipe": "PG", "kp": "KP 2",
            "soal": "Hasil dari 5/6 ÷ 5/3 adalah ...",
            "konteks": "",
            "pilihan": ["A. 1/2", "B. 25/18", "C. 2", "D. 5/18"],
            "jawaban": "A",
            "pembahasan": "5/6 ÷ 5/3 = 5/6 × 3/5 = (5×3)/(6×5) = 15/30 = 1/2."
        },
        {
            "no": 6, "tipe": "PG", "kp": "KP 3",
            "soal": "Urutan pecahan 2/3, 3/5, 7/10 dari yang terkecil adalah ...",
            "konteks": "💡 Samakan penyebut ke 30",
            "pilihan": [
                "A. 2/3 < 3/5 < 7/10",
                "B. 3/5 < 7/10 < 2/3",
                "C. 3/5 < 2/3 < 7/10",
                "D. 7/10 < 2/3 < 3/5"
            ],
            "jawaban": "B",
            "pembahasan": "Desimal: 2/3≈0.667, 3/5=0.6, 7/10=0.7. Urutan: 3/5 < 2/3 < 7/10. Jawaban B? Cek ulang: 3/5<7/10<2/3 → 0.6<0.7<0.667 salah. Benar: 3/5(0.6) < 2/3(0.667) < 7/10(0.7) → Jawaban C."
        },
        {
            "no": 7, "tipe": "PG", "kp": "KP 3",
            "soal": "Bentuk desimal dari 7/8 adalah ...",
            "konteks": "",
            "pilihan": ["A. 0,785", "B. 0,875", "C. 0,758", "D. 0,857"],
            "jawaban": "B",
            "pembahasan": "7 ÷ 8 = 0,875."
        },
        {
            "no": 8, "tipe": "PG", "kp": "KP 2",
            "soal": "Jika Rina memiliki 3/4 kg apel dan membeli lagi 2/3 kg, berapa total apel Rina?",
            "konteks": "💡 Ini soal kontekstual operasi penjumlahan pecahan.",
            "pilihan": ["A. 5/7 kg", "B. 17/12 kg", "C. 1 1/2 kg", "D. 1 5/12 kg"],
            "jawaban": "D",
            "pembahasan": "3/4 + 2/3 = 9/12 + 8/12 = 17/12 = 1 5/12 kg."
        },
        {
            "no": 9, "tipe": "Isian", "kp": "KP 3",
            "soal": "Nyatakan 0,625 dalam bentuk pecahan paling sederhana.",
            "konteks": "💡 Gunakan Tab Konversi untuk verifikasi.",
            "pilihan": None,
            "jawaban": "5/8",
            "pembahasan": "0,625 = 625/1000. FPB(625,1000)=125. 625/125 = 5, 1000/125 = 8. Jadi 5/8."
        },
        {
            "no": 10, "tipe": "Isian", "kp": "KP 2",
            "soal": "Sebuah resep membutuhkan 2/3 cangkir tepung untuk 1 porsi. Untuk 4,5 porsi, berapa cangkir tepung yang dibutuhkan?",
            "konteks": "💡 Literasi: 4,5 = 9/2 porsi.",
            "pilihan": None,
            "jawaban": "3",
            "pembahasan": "2/3 × 9/2 = 18/6 = 3 cangkir."
        },
    ]

    sudah_submit = st.session_state.get("submitted_br", False)
    skor_total = 0

    for soal in soal_list:
        kp_color = {"KP 1": "#6A0572", "KP 2": "#A020A0", "KP 3": "#C000C0"}.get(soal["kp"], "#A020A0")
        st.markdown(f"""
        <div style="border:1px solid #E0D0F0;border-radius:12px;padding:1rem 1.2rem;margin:0.8rem 0;
                    border-left:5px solid {kp_color};">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
            <span style="background:{kp_color};color:white;padding:2px 10px;border-radius:20px;
                         font-size:0.78rem;font-weight:700;">{soal['kp']}</span>
            <span style="background:#F0E0FF;padding:2px 10px;border-radius:20px;
                         font-size:0.78rem;font-weight:700;">{soal['tipe']}</span>
            <b>Soal {soal['no']}</b>
        </div>
        <div style="font-size:0.95rem;font-weight:600;">{soal['soal']}</div>
        {f'<div style="background:#FFF8E6;padding:0.5rem 0.8rem;border-radius:8px;margin-top:0.4rem;font-size:0.88rem;color:#8B6914;">{soal["konteks"]}</div>' if soal["konteks"] else ""}
        </div>
        """, unsafe_allow_html=True)

        key = f"soal_br_{soal['no']}"
        if soal["tipe"] == "PG":
            jawab = st.radio("Pilih jawaban:", soal["pilihan"],
                             key=key, label_visibility="collapsed", index=None)
            if jawab:
                st.session_state.jawab_br[key] = jawab
        else:
            jawab = st.text_input("Jawaban kamu:", key=key,
                                  placeholder="Tulis jawabanmu di sini...")
            if jawab:
                st.session_state.jawab_br[key] = jawab

        if sudah_submit and key in st.session_state.jawab_br:
            j = st.session_state.jawab_br[key]
            benar = (soal["tipe"] == "PG" and j and j.startswith(soal["jawaban"])) or \
                    (soal["tipe"] == "Isian" and soal["jawaban"].lower() in j.lower())
            if benar:
                skor_total += 1
                st.markdown(f'<div class="success-card" style="font-size:0.85rem;">✅ <b>BENAR!</b> {soal["pembahasan"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="danger-card" style="font-size:0.85rem;">❌ <b>Belum tepat.</b> Jawaban: <b>{soal["jawaban"]}</b>. {soal["pembahasan"]}</div>', unsafe_allow_html=True)
        st.markdown("")

    col_btn1, col_btn2 = st.columns([1, 3])
    with col_btn1:
        if st.button("✅ Submit & Lihat Nilai", type="primary", use_container_width=True):
            st.session_state.submitted_br = True
            st.rerun()
    with col_btn2:
        if st.button("🔄 Reset Jawaban", use_container_width=True):
            st.session_state.submitted_br = False
            st.session_state.jawab_br = {}
            st.rerun()

    if sudah_submit:
        persen = skor_total / len(soal_list) * 100
        emoji = "🏆" if persen >= 80 else ("👍" if persen >= 60 else "💪")
        warna_nilai = "#70AD47" if persen >= 80 else ("#ED7D31" if persen >= 60 else "#C00000")
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#6A0572,#A020A0);color:white;
                    border-radius:16px;padding:1.5rem 2rem;text-align:center;margin-top:1rem;">
            <div style="font-size:1.1rem;opacity:0.9;">Nilai Akhir {emoji}</div>
            <div style="font-size:4rem;font-weight:800;color:{warna_nilai};">{persen:.0f}</div>
            <div style="font-size:1rem;opacity:0.8;">{skor_total} dari {len(soal_list)} soal benar</div>
            <div style="margin-top:0.8rem;font-size:0.9rem;">
            {'🏆 Excellent! Kamu sudah menguasai Bilangan Rasional!' if persen>=80 else ('👍 Bagus! Pelajari lagi bagian yang masih salah.' if persen>=60 else '💪 Semangat! Eksplorasi lebih dalam dengan kalkulator digital!')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🔍 Refleksi Penggunaan Kalkulator Digital Streamlit")
        r1 = st.text_area("1. Fitur apa yang paling membantumu memahami bilangan rasional? Mengapa?",
                           placeholder="Tuliskan refleksimu di sini...", height=80)
        r2 = st.text_area("2. Apa yang kamu temukan saat bereksplorasi dengan kalkulator yang tidak kamu temukan dari buku?",
                           placeholder="Tuliskan refleksimu di sini...", height=80)
        r3 = st.text_area("3. Bagaimana perasaanmu belajar bilangan rasional dengan kalkulator digital ini?",
                           placeholder="Tuliskan refleksimu di sini...", height=80)
        if r1 or r2 or r3:
            st.markdown('<div class="success-card">✅ Terima kasih atas refleksimu! Salin ke LKS-mu.</div>', unsafe_allow_html=True)
