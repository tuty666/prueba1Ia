import re
import json
import streamlit as st
from utils.mcp_prompt import construir_prompt_mcp
from dotenv import load_dotenv
import google.generativeai as genai
from graphviz import Digraph
import os

# Configuración inicial
load_dotenv()
#IMPORTANT
#API_KEY = os.getenv("GEMINI_API_KEY") # (Habilítalo únicamente para pruebas locales)
API_KEY = st.secrets["GEMINI_API_KEY"] # (Habilítalo para deploy en Streamlit Cloud)
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

st.set_page_config(page_title="Generador de Flujos de Apps con IA", layout="centered")
st.title("Generador de Flujos de Apps con IA")

# Entrada del usuario
idea = st.text_input("Describe tu idea de app:")

if st.button("Generar flujo"): 
    if not idea.strip():
        st.warning("Por favor, escribe una descripción.")
    else:
        prompt = construir_prompt_mcp(idea)
        response = model.generate_content(prompt)
        raw = response.text

        st.subheader("Respuesta recibida:")
        st.code(raw)

        try:
            # Remover markdown y buscar primer bloque JSON
            json_match = re.search(r"\{[\s\S]*\}", raw)
            if not json_match:
                raise ValueError("No se encontró un objeto JSON en la respuesta.")

            json_clean = json_match.group(0)
            data = json.loads(json_clean)

            flujo = data.get("flujo", [])
            if not isinstance(flujo, list) or not flujo:
                raise ValueError("La clave 'flujo' no es una lista válida.")

            # Mostrar cada pantalla con detalles
            st.subheader("Flujo de pantallas:")
            for idx, pantalla in enumerate(flujo, start=1):
                nombre = pantalla.get("pantalla", "Sin nombre")
                descripcion = pantalla.get("descripcion", "Sin descripción")
                elementos = pantalla.get("elementos", [])

                st.markdown(f"**{idx}. {nombre}**")
                st.markdown(f"_Descripción_: {descripcion}")
                if elementos:
                    st.markdown("- Elementos UI:")
                    for el in elementos:
                        st.markdown(f"  - {el}")
                st.markdown("---")

            # Visualización con Graphviz
            st.subheader("Visualización gráfica:")
            dot = Digraph("FlujoApp", format="png")
            # Estilo general
            dot.attr(rankdir="TB", splines="ortho", nodesep="0.6", ranksep="0.6")
            dot.attr("node", shape="box", style="filled", color="lightblue", fontname="Helvetica", fontsize="10", margin="0.3")

            # Nodos con nombre + resumen de elementos
            for pantalla in flujo:
                nombre = pantalla.get("pantalla", "Sin nombre")
                descripcion = pantalla.get("descripcion", "")
                elementos = pantalla.get("elementos", [])
                resumen = ", ".join(elementos[:2]) + ("..." if len(elementos) > 2 else "")
                label = f"{nombre}\\n{resumen}"
                dot.node(nombre, label=label)

            # Conexiones
            for i in range(len(flujo) - 1):
                dot.edge(flujo[i]["pantalla"], flujo[i + 1]["pantalla"])

            # Mostrar en Streamlit
            st.graphviz_chart(dot)


        except json.JSONDecodeError:
            st.error("Error al interpretar el JSON. ¿La respuesta contiene solo un objeto JSON?")
        except Exception as e:
            st.error(f"Error procesando el flujo: {e}")
