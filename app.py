import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Obtener la API key
API_KEY = os.environ.get("GEMINI_API_KEY")

# Leer la normativa de roleplay
try:
    with open("normativa.txt", "r", encoding="utf-8") as f:
        NORMATIVA_ROLEPLAY = f.read()
except Exception as e:
    NORMATIVA_ROLEPLAY = "Normativa no cargada correctamente."

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
            
        if not API_KEY:
            return jsonify({"respuesta": "Error: GEMINI_API_KEY no está configurada en el servidor."}), 500

        # Usar la API REST oficial de Google con gemini-1.5-flash
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={API_KEY}"
        
        prompt_completo = f"""Eres un asistente experto en la siguiente normativa de roleplay. Responde a la pregunta del usuario de forma clara, directa y cíñete estrictamente a las reglas provistas:

NORMATIVA:
{NORMATIVA_ROLEPLAY}

PREGUNTA DEL USUARIO:
{pregunta_usuario}"""

        payload = {
            "contents": [{
                "parts": [{"text": prompt_completo}]
            }]
        }
        
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers)
        resultado_json = response.json()
        
        # Extraer la respuesta de la estructura de la API REST
        if response.status_code == 200:
            texto_respuesta = resultado_json["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"respuesta": texto_respuesta})
        else:
            error_msg = resultado_json.get("error", {}).get("message", "Error desconocido de la API")
            return jsonify({"respuesta": f"Error de la API de Google: {error_msg}"}), 500

    except Exception as e:
        return jsonify({"respuesta": f"Error interno del servidor: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
