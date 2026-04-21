import streamlit as st
import matplotlib.pyplot as plt
import random
import time

st.set_page_config(page_title="Jelajah Bilangan Bulat", layout="wide")

# ======================
# HEADER
# ======================
st.title("🧭 JELAJAH BILANGAN BULAT")
st.markdown("Media interaktif untuk memahami bilangan bulat kelas 7")

# ======================
# GARIS BILANGAN
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
# SIDEBAR
# ======================
menu = st.sidebar.radio(
    "📚 Menu",
    ["Panduan", "Materi", "Kalkulator", "Kuis Game"]
)

# ======================
# 1. PANDUAN
# ======================
if menu == "Panduan":
    st.header("📘 Panduan")
    st.write("""
    1. Pelajari materi terlebih dahulu  
    2. Gunakan kalkulator untuk eksplorasi  
    3. Kerjakan kuis untuk evaluasi  
    """)

# ======================
# 2. MATERI
# ======================
elif menu == "Materi":
    st.header("📖 Materi Bilangan Bulat")

    st.subheader("Garis Bilangan")
    x = st.slider("Pilih bilangan", -10, 10, 0)
    st.pyplot(garis_bilangan(x))
    st.write(f"Jarak dari nol: {abs(x)}")

    st.subheader("Invers")
    st.write(f"Invers dari {x} adalah {-x}")
    st.write(f"{x} + ({-x}) = 0")

    st.subheader("Perbandingan")
    data = st.text_input("Masukkan bilangan (pisahkan koma)", "-3,5,0,-1")
    try:
        angka = list(map(int, data.split(",")))
        st.write("Urutan dari kecil ke besar:", sorted(angka))
    except:
        st.warning("Input tidak valid")

# ======================
# 3. KALKULATOR
# ======================
elif menu == "Kalkulator":
    st.header("🧮 Kalkulator Bilangan Bulat")

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

    st.subheader("Faktor Bilangan")
    x = st.number_input("Cari faktor dari", min_value=1, value=6)
    faktor = [i for i in range(1, x+1) if x % i == 0]
    st.write(f"Faktor dari {x}: {faktor}")

# ======================
# 4. KUIS GAME + REFLEKSI
# ======================
elif menu == "Kuis Game":
    st.header("🎮 Kuis Interaktif")

    if "score" not in st.session_state:
        st.session_state.score = 0
        st.session_state.index = 0
        st.session_state.total = 7
        st.session_state.soal = []
        st.session_state.salah = []

    # BANK SOAL
    def generate_question():
        tipe = random.choice(["operasi", "invers", "banding", "faktor", "konteks"])

        if tipe == "operasi":
            a, b = random.randint(-10,10), random.randint(-10,10)
            return (f"{a} + {b} = ?", str(a+b),
                    f"Gunakan aturan penjumlahan bilangan bulat: {a} + {b} = {a+b}")

        elif tipe == "invers":
            x = random.randint(-10,10)
            return (f"Invers dari {x}?", str(-x),
                    f"Invers adalah kebalikan: {x} menjadi {-x}")

        elif tipe == "banding":
            a, b = random.randint(-10,10), random.randint(-10,10)
            return (f"Mana lebih besar: {a} atau {b}?", str(max(a,b)),
                    "Bilangan yang lebih ke kanan pada garis bilangan lebih besar")

        elif tipe == "faktor":
            x = random.choice([6,8,10])
            faktor = ",".join(map(str,[i for i in range(1,x+1) if x%i==0]))
            return (f"Sebutkan faktor dari {x} (pisahkan koma)", faktor,
                    f"Faktor {x} adalah bilangan yang membagi habis {x}")

        elif tipe == "konteks":
            return ("Suhu -2 naik 5, hasilnya?", "3",
                    "Naik berarti bertambah: -2 + 5 = 3")

    # GENERATE SOAL
    if not st.session_state.soal:
        st.session_state.soal = [generate_question() for _ in range(st.session_state.total)]

    # PROGRESS
    st.progress(st.session_state.index / st.session_state.total)

    if st.session_state.index < st.session_state.total:

        soal, benar, penjelasan = st.session_state.soal[st.session_state.index]

        st.subheader(f"Soal {st.session_state.index+1}")
        st.write(soal)

        jawaban = st.text_input("Jawaban", key=st.session_state.index)

        if st.button("Submit"):
            with st.spinner("Memeriksa jawaban..."):
                time.sleep(1)

            if jawaban.strip() == benar:
                st.success("✅ Benar!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Salah. Jawaban benar: {benar}")
                st.session_state.salah.append((soal, benar, penjelasan))

            st.session_state.index += 1
            st.rerun()

    else:
        st.balloons()
        st.success(f"🎉 Skor akhir: {st.session_state.score}/{st.session_state.total}")

        st.subheader("📊 Refleksi Pembelajaran")

        if st.session_state.salah:
            for s in st.session_state.salah:
                st.warning(f"Soal: {s[0]}")
                st.write(f"Jawaban benar: {s[1]}")
                st.info(f"Penjelasan: {s[2]}")
        else:
            st.success("Semua jawaban benar! Pemahaman sangat baik!")

        if st.button("Ulangi Kuis"):
            st.session_state.score = 0
            st.session_state.index = 0
            st.session_state.soal = []
            st.session_state.salah = []
            st.rerun()
