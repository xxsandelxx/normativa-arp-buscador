import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app) 

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

with open("normativa.txt", "r", encoding="utf-8") as f:
    NORMATIVA_ROLEPLAY = f.read()

@app.route("/preguntar", methods=["POST"])
def preguntar():
    data = request.json
    pregunta_usuario = data.get("pregunta", "")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {
                    "role": "system", 
                    "content": f"Eres un asistente experto en la siguiente normativa de roleplay. Responde de forma clara, directa y cíñete estrictamente a las reglas provistas:\n\n{NORMATIVA_ROLEPLAY}"
                },
                {"role": "user", "content": pregunta_usuario}
            ],
            temperature=0.3
        )
        
        respuesta = response.choices[0].message.content
        return jsonify({"respuesta": respuesta})
    
    except Exception as e:
        return jsonify({"respuesta": "Hubo un error procesando tu consulta."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
