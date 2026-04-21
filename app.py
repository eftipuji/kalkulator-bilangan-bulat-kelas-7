import streamlit as st

st.title("🧮 Kalkulator Bilangan Bulat")

a = st.number_input("Bilangan pertama", step=1)
b = st.number_input("Bilangan kedua", step=1)

operasi = st.selectbox("Operasi", ["+", "-", "×", "÷"])

if st.button("Hitung"):
    if operasi == "+":
        st.success(a + b)
    elif operasi == "-":
        st.success(a - b)
    elif operasi == "×":
        st.success(a * b)
    elif operasi == "÷":
        if b != 0:
            st.success(a / b)
        else:
            st.error("Tidak bisa dibagi nol")
