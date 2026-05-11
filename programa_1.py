from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

# LINEAL
@app.route("/lineal", methods=["POST"])
def lineal():
    data = request.json
    a = data["a"]
    b = data["b"]

    x = list(range(-10, 11))
    y = [a*i + b for i in x]

    resultado = -b/a if a != 0 else "Sin solución"

    return jsonify({
        "resultado": resultado,
        "x": x,
        "y": y
    })


# CUADRATICA
@app.route("/cuadratica", methods=["POST"])
def cuadratica():
    data = request.json
    a = data["a"]
    b = data["b"]
    c = data["c"]

    d = b*b - 4*a*c

    if d >= 0:
        x1 = (-b + d**0.5)/(2*a)
        x2 = (-b - d**0.5)/(2*a)
        resultado = f"x1={x1:.2f}, x2={x2:.2f}"
    else:
        resultado = "Sin soluciones reales"

    x = list(range(-10, 11))
    y = [a*i*i + b*i + c for i in x]

    return jsonify({
        "resultado": resultado,
        "x": x,
        "y": y
    })


# SISTEMA 2x2
@app.route("/sistema", methods=["POST"])
def sistema():
    data = request.json

    a = data["a1"]
    b = data["b1"]
    c = data["c1"]
    d = data["a2"]
    e = data["b2"]
    f = data["c2"]

    det = a*e - b*d

    if det == 0:
        return jsonify({"resultado": "Sin solución única"})

    x = (c*e - b*f)/det
    y = (a*f - c*d)/det

    X = list(range(-10, 11))
    Y1 = [(c - a*i)/b for i in X]
    Y2 = [(f - d*i)/e for i in X]

    return jsonify({
        "resultado": f"x={x:.2f}, y={y:.2f}",
        "x_vals": X,
        "y1": Y1,
        "y2": Y2
    })


if __name__ == "__main__":
    app.run(debug=True)
