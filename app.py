import streamlit as st
import random
import time

st.set_page_config(page_title="Kuis Bilangan Bulat", layout="centered")

st.title("📝 Kuis Interaktif Bilangan Bulat")

# ======================
# INIT SESSION
# ======================
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.index = 0
    st.session_state.total = 10
    st.session_state.soal = []

# ======================
# BANK SOAL (TP 1–7)
# ======================
def generate_question():
    tipe = random.choice(["garis", "invers", "banding", "operasi", "faktor", "konteks"])

    if tipe == "garis":
        x = random.randint(-10, 10)
        return f"Posisi bilangan {x} terhadap nol?", str(x)

    elif tipe == "invers":
        x = random.randint(-10, 10)
        return f"Invers dari {x} adalah?", str(-x)

    elif tipe == "banding":
        a, b = random.randint(-10,10), random.randint(-10,10)
        benar = str(max(a,b))
        return f"Mana lebih besar: {a} atau {b}?", benar

    elif tipe == "operasi":
        a, b = random.randint(-10,10), random.randint(-10,10)
        return f"{a} + {b} = ?", str(a+b)

    elif tipe == "faktor":
        x = random.choice([6,8,10])
        faktor = ",".join(map(str,[i for i in range(1,x+1) if x%i==0]))
        return f"Sebutkan faktor dari {x} (pisahkan koma)", faktor

    elif tipe == "konteks":
        return "Suhu -2°C naik 5°C, hasilnya?", "3"

# ======================
# GENERATE SOAL
# ======================
if not st.session_state.soal:
    st.session_state.soal = [generate_question() for _ in range(st.session_state.total)]

# ======================
# PROGRESS BAR
# ======================
progress = st.session_state.index / st.session_state.total
st.progress(progress)

# ======================
# TAMPILKAN SOAL
# ======================
if st.session_state.index < st.session_state.total:

    soal, benar = st.session_state.soal[st.session_state.index]

    st.subheader(f"Soal {st.session_state.index+1}")
    st.write(soal)

    jawaban = st.text_input("Jawaban kamu", key=st.session_state.index)

    if st.button("Submit"):

        with st.spinner("Memeriksa jawaban..."):
            time.sleep(1)

        if jawaban.strip().lower() == benar:
            st.success("✅ Benar!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Salah. Jawaban: {benar}")

        st.session_state.index += 1
        time.sleep(1)
        st.rerun()

# ======================
# HASIL AKHIR
# ======================
else:
    st.balloons()
    st.success(f"🎉 Skor kamu: {st.session_state.score}/{st.session_state.total}")

    if st.session_state.score >= 8:
        st.write("🔥 Sangat baik!")
    elif st.session_state.score >= 5:
        st.write("👍 Cukup baik, tingkatkan lagi!")
    else:
        st.write("💡 Perlu latihan lagi")

    if st.button("Ulangi Kuis"):
        st.session_state.score = 0
        st.session_state.index = 0
        st.session_state.soal = []
        st.rerun()
