import streamlit as st
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Bilangan Bulat Interaktif", layout="centered")

# ======================
# FUNGSI GARIS BILANGAN
# ======================
def garis_bilangan(x):
    fig, ax = plt.subplots()
    ax.axhline(0)

    for i in range(-10, 11):
        ax.plot(i, 0, 'o', color='gray')

    ax.plot(x, 0, 'ro')
    ax.text(x, 0.3, str(x), ha='center')

    ax.set_xlim(-10, 10)
    ax.set_yticks([])
    return fig

# ======================
# SIDEBAR MENU
# ======================
menu = st.sidebar.radio(
    "Menu",
    ["Panduan", "Pengantar Materi", "Kalkulator", "Kuis"]
)

# ======================
# 1. PANDUAN
# ======================
if menu == "Panduan":
    st.title("📘 Panduan Penggunaan")

    st.markdown("""
    ### Cara menggunakan:
    1. Baca pengantar materi terlebih dahulu
    2. Gunakan kalkulator untuk eksplorasi
    3. Kerjakan kuis untuk evaluasi
    
    ### Tujuan:
    Memahami bilangan bulat secara konsep dan penerapan
    """)

# ======================
# 2. PENGANTAR MATERI
# ======================
elif menu == "Pengantar Materi":
    st.title("📖 Pengantar Bilangan Bulat")

    st.subheader("1. Garis Bilangan")
    x = st.slider("Pilih bilangan", -10, 10, 0)
    st.pyplot(garis_bilangan(x))
    st.write(f"Jarak dari nol: {abs(x)}")

    st.subheader("2. Invers Bilangan")
    inv = -x
    st.write(f"Invers dari {x} adalah {inv}")
    st.write(f"{x} + ({inv}) = 0")

    st.subheader("3. Perbandingan")
    data = st.text_input("Masukkan bilangan (pisahkan koma)", "-3,5,0,-1")
    try:
        angka = list(map(int, data.split(",")))
        st.write("Urutan naik:", sorted(angka))
    except:
        st.warning("Input belum valid")

# ======================
# 3. KALKULATOR
# ======================
elif menu == "Kalkulator":
    st.title("🧮 Kalkulator Bilangan Bulat")

    a = st.number_input("Bilangan pertama", step=1)
    b = st.number_input("Bilangan kedua", step=1)

    operasi = st.selectbox("Operasi", ["+", "-", "×", "÷"])

    if st.button("Hitung"):
        if operasi == "+":
            hasil = a + b
            st.success(f"{a} + {b} = {hasil}")
            st.pyplot(garis_bilangan(int(a + b)))

        elif operasi == "-":
            hasil = a - b
            st.success(f"{a} - {b} = {hasil}")

        elif operasi == "×":
            hasil = a * b
            st.success(f"{a} × {b} = {hasil}")

        elif operasi == "÷":
            if b != 0:
                hasil = a / b
                st.success(f"{a} ÷ {b} = {hasil}")
            else:
                st.error("Tidak bisa dibagi nol")

    st.subheader("Faktor Bilangan")
    x = st.number_input("Cari faktor dari", min_value=1, value=6)
    faktor = [i for i in range(1, x+1) if x % i == 0]
    st.write(faktor)

# ======================
# 4. KUIS
# ======================
elif menu == "Kuis":
    st.title("📝 Kuis")

    if "soal" not in st.session_state:
        st.session_state.soal = (random.randint(-10,10), random.randint(-10,10))

    a, b = st.session_state.soal

    st.write(f"Berapakah {a} + {b}?")

    jawaban = st.number_input("Jawaban", step=1)

    if st.button("Cek Jawaban"):
        if jawaban == a + b:
            st.success("Benar!")
        else:
            st.error(f"Salah, jawabannya {a+b}")

    if st.button("Soal Baru"):
        st.session_state.soal = (random.randint(-10,10), random.randint(-10,10))
        st.rerun()

    st.subheader("Soal Kontekstual")
    st.write("Suhu -2°C naik 5°C, berapa sekarang?")

    jawab2 = st.number_input("Jawaban soal kontekstual", step=1)

    if st.button("Cek Kontekstual"):
        if jawab2 == 3:
            st.success("Benar!")
        else:
            st.error("Jawaban: 3°C")
