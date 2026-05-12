from flask import Flask, request, jsonify, send_from_directory
import numpy as np
import matplotlib.pyplot as plt
import io, base64

app = Flask(__name__)

# HOME
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# LINEAL
@app.route("/lineal", methods=["POST"])
def lineal():
    data = request.json
    m = data["m"]
    b = data["b"]

    x = np.linspace(-10, 10, 100)
    y = m*x + b

    plt.figure()
    plt.plot(x, y)
    plt.title("Ecuación Lineal")

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    grafica = base64.b64encode(img.getvalue()).decode()

    return jsonify({"grafica": grafica})

# CUADRATICA
@app.route("/cuadratica", methods=["POST"])
def cuadratica():
    data = request.json
    a = data["a"]
    b = data["b"]
    c = data["c"]

    x = np.linspace(-10, 10, 100)
    y = a*x**2 + b*x + c

    plt.figure()
    plt.plot(x, y)
    plt.title("Ecuación Cuadrática")

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    grafica = base64.b64encode(img.getvalue()).decode()

    return jsonify({"grafica": grafica})

# SISTEMA 2x2
@app.route("/sistema2", methods=["POST"])
def sistema2():
    data = request.json

    A = np.array([
        [float(data["a1"]), float(data["b1"])],
        [float(data["a2"]), float(data["b2"])]
    ])

    B = np.array([
        float(data["c1"]),
        float(data["c2"])
    ])

    sol = np.linalg.solve(A, B)

    return jsonify({
        "x": round(sol[0],2),
        "y": round(sol[1],2)
    })

# SISTEMA 3x3
@app.route("/sistema3", methods=["POST"])
def sistema3():
    # puedes completar esto luego
    return jsonify({"msg": "pendiente 3x3"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
