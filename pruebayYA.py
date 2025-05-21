import streamlit as st

st.set_page_config(page_title="Generador de Flujos de Apps", layout="centered")
st.title("Generador de Flujos de Apps con IA")

idea = st.text_input("Describe tu idea de app:")

if st.button("Generar flujo"):
    st.write("Aquí mostraremos el flujo generado.")