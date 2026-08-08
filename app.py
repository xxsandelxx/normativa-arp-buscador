import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configurar la API key de Google Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Intentar leer la normativa de roleplay de forma segura
try:
    with open("normativa.txt", "r", encoding="utf-8") as f:
        NORMATIVA_ROLEPLAY = f.read()
except Exception as e:
    NORMATIVA_ROLEPLAY = "Normativa no cargada correctamente."

# Inicializar el modelo con gemini-1.5-flash
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route("/", methods=["GET"])
def home():
    return "¡El buscador de normativa está activo! 🚀"

@app.route("/preguntar", methods=["POST"])
def preguntar():
    try:
        data = request.json or {}
        pregunta_usuario = data.get("pregunta", "")
        
        if not pregunta_usuario:
            return jsonify({"respuesta": "Por favor, escribe una pregunta válida."}), 400
            
        prompt_completo = f"""Eres un asistente experto en la siguiente normativa de roleplay. Responde a la pregunta del usuario de forma clara, directa y cíñete estrictamente a las reglas provistas:

NORMATIVA:
{NORMATIVA_ROLEPLAY}

PREGUNTA DEL USUARIO:
{pregunta_usuario}"""

        response = model.generate_content(prompt_completo)
        return jsonify({"respuesta": response.text})
    except Exception as e:
        return jsonify({"respuesta": f"Error interno: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
