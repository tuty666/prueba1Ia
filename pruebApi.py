import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar la clave API desde .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
#Hacer una llamada a la API
model = genai.GenerativeModel("gemini-2.0-flash")
response = model.generate_content("Cuentame un chiste sobre un perro")

print(response.text)