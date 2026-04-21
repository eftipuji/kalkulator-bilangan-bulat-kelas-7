import streamlit as st
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Bilangan Bulat Interaktif", layout="wide")

# ======================
# CUSTOM CSS (BACKGROUND)
# ======================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #4facfe, #00f2fe);
    color: white;
}
h1, h2, h3 {
    color: #ffffff;
}
.css-1d391kg {background-color: rgba(0,0,0,0.3);}
</style>
""", unsafe_allow_html=True)

# ======================
# FUNGSI GARIS BILANGAN
# ======================
def garis_bilangan(x):
    fig, ax = plt.subplots()
    ax.axhline(0)

    for i in range(-10, 11):
        ax.plot(i, 0, 'o', color='white')

    ax.plot(x, 0, 'ro')
    ax.text(x, 0.3, str(x), ha='center', color='white')

    ax.set_xlim(-10, 10)
    ax.set_yticks([])
    ax.set_facecolor('none')
    fig.patch.set_alpha(0)
    return fig

# ======================
# SIDEBAR
# ======================
menu = st.sidebar.radio(
    "📚 Menu",
    ["Panduan", "Materi Interaktif", "Kalkulator", "Kuis TP"]
)

# ======================
# 1. PANDUAN
# ======================
if menu == "Panduan":
    st.title("📘 Panduan")

    st.markdown("""
    ### Cara Belajar:
    1. Pelajari konsep di Materi Interaktif
    2. Gunakan Kalkulator untuk eksplorasi
    3. Kerjakan Kuis untuk evaluasi
    
    🎯 Target:
    Memahami bilangan bulat secara konsep & aplikasi
    """)

# ======================
# 2. MATERI INTERAKTIF
# ======================
elif menu == "Materi Interaktif":
    st.title("📖 Materi Interaktif")

    tab1, tab2, tab3 = st.tabs(["Garis Bilangan", "Invers", "Perbandingan"])

    with tab1:
        st.subheader("Garis Bilangan")
        x = st.slider("Pilih bilangan", -10, 10, 0)
        st.pyplot(garis_bilangan(x))
        st.write(f"Jarak dari nol: {abs(x)}")

    with tab2:
        st.subheader("Invers")
        inv = -x
        st.write(f"Invers dari {x} adalah {inv}")
        st.write(f"{x} + ({inv}) = 0")

    with tab3:
        st.subheader("Perbandingan")
        data = st.text_input("Masukkan bilangan", "-3,5,0,-1")
        try:
            angka = list(map(int, data.split(",")))
            st.write("Urutan:", sorted(angka))
        except:
            st.warning("Input salah")

# ======================
# 3. KALKULATOR
# ======================
elif menu == "Kalkulator":
    st.title("🧮 Kalkulator Interaktif")

    a = st.number_input("Bilangan pertama", step=1)
    b = st.number_input("Bilangan kedua", step=1)

    op = st.selectbox("Operasi", ["+", "-", "×", "÷"])

    if st.button("Hitung"):
        if op == "+":
            hasil = a + b
            st.success(f"{a} + {b} = {hasil}")
            st.pyplot(garis_bilangan(int(hasil)))

        elif op == "-":
            hasil = a - b
            st.success(f"{a} - {b} = {hasil}")

        elif op == "×":
            hasil = a * b
            st.success(f"{a} × {b} = {hasil}")

        elif op == "÷":
            if b != 0:
                hasil = a / b
                st.success(f"{a} ÷ {b} = {hasil}")
            else:
                st.error("Tidak bisa dibagi nol")

    st.subheader("Faktor")
    x = st.number_input("Cari faktor", min_value=1, value=6)
    faktor = [i for i in range(1, x+1) if x % i == 0]
    st.write(faktor)

# ======================
# 4. KUIS SESUAI TP
# ======================
elif menu == "Kuis TP":
    st.title("📝 Kuis Berdasarkan Tujuan Pembelajaran")

    if "score" not in st.session_state:
        st.session_state.score = 0
        st.session_state.q = 0

    soal_list = [
        ("TP1: Posisi -3 dari nol?", "-3"),
        ("TP2: Invers dari 5?", "-5"),
        ("TP3: Mana lebih besar: -2 atau 3?", "3"),
        ("TP4: 4 + (-4) = ?", "0"),
        ("TP5: -3 + 5 = ?", "2"),
        ("TP6: Faktor dari 6?", "1,2,3,6"),
        ("TP7: Suhu -2 naik 5 = ?", "3")
    ]

    if st.session_state.q < len(soal_list):
        soal, benar = soal_list[st.session_state.q]

        st.write(soal)
        jawab = st.text_input("Jawaban")

        if st.button("Submit"):
            if jawab.strip() == benar:
                st.success("Benar!")
                st.session_state.score += 1
            else:
                st.error(f"Salah. Jawaban: {benar}")

            st.session_state.q += 1
            st.rerun()

    else:
        st.success(f"Skor akhir: {st.session_state.score}/7")
        if st.button("Ulangi"):
            st.session_state.score = 0
            st.session_state.q = 0
            st.rerun()
