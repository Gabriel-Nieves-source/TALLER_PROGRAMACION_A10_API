import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.8-flash",  # <--- Asegúrate de cambiarlo aquí
    contents="Hola Gemini, saluda al sistema SITRAL de control de lotes.",
)

print("Respuesta de Gemini:")
print(response.text)