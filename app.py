import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

with open("normativa.txt", "r", encoding="utf-8") as f:
    NORMATIVA_ROLEPLAY = f.read()

generation_config = {"temperature": 0.3}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=f"Eres un asistente experto en la siguiente normativa de roleplay. Responde de forma clara, directa y cíñete estrictamente a las reglas provistas:\n\n{NORMATIVA_ROLEPLAY}",
    generation_config=generation_config
)

@app.route("/preguntar", methods=["POST"])
def preguntar():
    data = request.json
    pregunta_usuario = data.get("pregunta", "")
    
    try:
        response = model.generate_content(pregunta_usuario)
        return jsonify({"respuesta": response.text})
    except Exception as e:
        return jsonify({"respuesta": "Hubo un error procesando tu consulta."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
