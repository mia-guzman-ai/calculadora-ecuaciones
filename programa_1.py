from flask import Flask, request, jsonify, send_file
import math
import os

@app.route("/")
def home():
    return send_file("index.html")
    
app = Flask(__name__)

# ======================
# ECUACION LINEAL
# ======================
@app.route("/lineal", methods=["POST"])
def lineal():
    data = request.json
    tipo = data["tipo"]

    x_vals = list(range(-10, 11))

    if tipo == "pendiente":
        a = data["a"]
        b = data["b"]
        y_vals = [a*x + b for x in x_vals]
        resultado = f"x = {-b/a:.2f}"

    elif tipo == "dos_puntos":
        x1, y1 = data["x1"], data["y1"]
        x2, y2 = data["x2"], data["y2"]

        m = (y2 - y1) / (x2 - x1)
        b = y1 - m*x1

        y_vals = [m*x + b for x in x_vals]
        resultado = f"y = {m:.2f}x + {b:.2f}"

    return jsonify({"x": x_vals, "y": y_vals, "resultado": resultado})


# ======================
# CUADRATICA
# ======================
@app.route("/cuadratica", methods=["POST"])
def cuadratica():
    data = request.json
    a, b, c = data["a"], data["b"], data["c"]

    x_vals = list(range(-10, 11))
    y_vals = [a*x**2 + b*x + c for x in x_vals]

    d = b**2 - 4*a*c

    if d > 0:
        r1 = (-b + math.sqrt(d)) / (2*a)
        r2 = (-b - math.sqrt(d)) / (2*a)
        resultado = f"Raíces: {r1:.2f}, {r2:.2f}"
    elif d == 0:
        r = -b / (2*a)
        resultado = f"Raíz: {r:.2f}"
    else:
        resultado = "No reales"

    return jsonify({"x": x_vals, "y": y_vals, "resultado": resultado})


# ======================
# SISTEMA 2x2
# ======================
@app.route("/sistema", methods=["POST"])
def sistema():
    data = request.json
    tipo = data["tipo"]

    if tipo == "directo":
        a, b, c = data["a"], data["b"], data["c"]
        d, e, f = data["d"], data["e"], data["f"]

    elif tipo == "puntos":
        x1, y1 = data["x1"], data["y1"]
        x2, y2 = data["x2"], data["y2"]

        m = (y2 - y1) / (x2 - x1)
        b_val = y1 - m*x1

        a, b, c = -m, 1, b_val
        d, e, f = 1, 0, 0

    det = a*e - b*d

    if det == 0:
        return jsonify({"resultado": "Sin solución"})

    x = (c*e - b*f) / det
    y = (a*f - c*d) / det

    return jsonify({"resultado": f"x = {x:.2f}, y = {y:.2f}"})


# ======================
# RUN
# ======================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
   app.run(host="0.0.0.0", port=port)
