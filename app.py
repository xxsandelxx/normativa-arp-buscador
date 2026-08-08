import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

try:
    with open("normativa.txt", "r", encoding="utf-8") as f:
        NORMATIVA_ROLEPLAY = f.read()
except Exception as e:
    NORMATIVA_ROLEPLAY = "Normativa no cargada correctamente."

generation_config = {"temperature": 0.3}
model = genai.GenerativeModel(
    model_name="gemini-pro",
    system_instruction=f"Eres un asistente experto en la siguiente normativa de roleplay. Responde de forma clara, directa y cíñete estrictamente a las reglas provistas:\n\n{NORMATIVA_ROLEPLAY}",
    generation_config=generation_config
)

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
            
        response = model.generate_content(pregunta_usuario)
        return jsonify({"respuesta": response.text})
    except Exception as e:
        return jsonify({"respuesta": f"Error interno: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
