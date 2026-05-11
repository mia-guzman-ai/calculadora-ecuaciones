from flask import Flask, request, jsonify, send_file
import math

app = Flask(__name__)

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/lineal", methods=["POST"])
def lineal():
    data = request.json
    a = data["a"]
    b = data["b"]

    x_vals = list(range(-10, 11))
    y_vals = [a*x + b for x in x_vals]

    return jsonify({
        "x": x_vals,
        "y": y_vals,
        "resultado": f"x = {-b/a:.2f}"
    })

@app.route("/cuadratica", methods=["POST"])
def cuadratica():
    data = request.json
    a, b, c = data["a"], data["b"], data["c"]

    x_vals = list(range(-10, 11))
    y_vals = [a*x**2 + b*x + c for x in x_vals]

    d = b**2 - 4*a*c
    if d > 0:
        r = f"Raices: {(-b+math.sqrt(d))/(2*a):.2f}, {(-b-math.sqrt(d))/(2*a):.2f}"
    elif d == 0:
        r = f"Raiz: {-b/(2*a):.2f}"
    else:
        r = "No reales"

    return jsonify({"x": x_vals, "y": y_vals, "resultado": r})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
