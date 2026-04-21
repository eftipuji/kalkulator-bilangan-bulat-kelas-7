import streamlit as st
import matplotlib.pyplot as plt
import random
import time

st.set_page_config(page_title="Bilangan Bulat Interaktif", layout="wide")

# ======================
# STYLE RINGAN (TIDAK MONOTON)
# ======================
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
.card {
    background-color: #f0f2f6;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

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
    st.title("📘 Panduan")

    st.markdown("""
    <div class="card">
    Gunakan aplikasi ini dengan urutan:
    <br>1. Pelajari materi
    <br>2. Gunakan kalkulator
    <br>3. Kerjakan kuis
    </div>
    """, unsafe_allow_html=True)

# ======================
# 2. MATERI
# ======================
elif menu == "Materi":
    st.title("📖 Materi Bilangan Bulat")

    tab1, tab2, tab3 = st.tabs(["Garis Bilangan", "Invers", "Perbandingan"])

    with tab1:
        x = st.slider("Pilih bilangan", -10, 10, 0)
        st.pyplot(garis_bilangan(x))
        st.write(f"Jarak dari nol: {abs(x)}")

    with tab2:
        st.write("Invers adalah kebalikan bilangan")
        x = st.number_input("Masukkan bilangan", value=5)
        st.write(f"Invers: {-x}")

    with tab3:
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
    st.title("🧮 Kalkulator")

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
# 4. KUIS GAME (UPGRADE)
# ======================
elif menu == "Kuis Game":
    st.title("🎮 Kuis Interaktif")

    # SESSION
    if "score" not in st.session_state:
        st.session_state.score = 0
        st.session_state.index = 0
        st.session_state.total = 10
        st.session_state.soal = []

    # BANK SOAL
    def generate_question():
        tipe = random.choice(["garis", "invers", "banding", "operasi", "faktor", "konteks"])

        if tipe == "garis":
            x = random.randint(-10, 10)
            return f"Bilangan {x} berada di posisi mana terhadap nol?", str(x)

        elif tipe == "invers":
            x = random.randint(-10, 10)
            return f"Invers dari {x}?", str(-x)

        elif tipe == "banding":
            a, b = random.randint(-10,10), random.randint(-10,10)
            return f"Mana lebih besar: {a} atau {b}?", str(max(a,b))

        elif tipe == "operasi":
            a, b = random.randint(-10,10), random.randint(-10,10)
            return f"{a} + {b} = ?", str(a+b)

        elif tipe == "faktor":
            x = random.choice([6,8,10])
            faktor = ",".join(map(str,[i for i in range(1,x+1) if x%i==0]))
            return f"Faktor dari {x}?", faktor

        elif tipe == "konteks":
            return "Suhu -2 naik 5, hasilnya?", "3"

    # GENERATE
    if not st.session_state.soal:
        st.session_state.soal = [generate_question() for _ in range(st.session_state.total)]

    # PROGRESS
    progress = st.session_state.index / st.session_state.total
    st.progress(progress)

    # TAMPILKAN
    if st.session_state.index < st.session_state.total:

        soal, benar = st.session_state.soal[st.session_state.index]

        st.subheader(f"Soal {st.session_state.index+1}")
        st.write(soal)

        jawaban = st.text_input("Jawaban", key=st.session_state.index)

        if st.button("Submit"):

            with st.spinner("Memeriksa..."):
                time.sleep(1)

            if jawaban.strip().lower() == benar:
                st.success("✅ Benar!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Salah. Jawaban: {benar}")

            st.session_state.index += 1
            time.sleep(1)
            st.rerun()

    else:
        st.balloons()
        st.success(f"🎉 Skor: {st.session_state.score}/{st.session_state.total}")

        if st.button("Main Lagi"):
            st.session_state.score = 0
            st.session_state.index = 0
            st.session_state.soal = []
            st.rerun()
