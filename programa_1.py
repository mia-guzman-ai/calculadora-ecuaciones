from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor funcionando 🚀"

@app.route("/lineal", methods=["POST"])
def lineal():
    data = request.json
    a = data["a"]
    b = data["b"]

    return jsonify({"resultado": -b/a})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
