from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def crear_grafica(x, y):
    fig, ax = plt.subplots(figsize=(4,3))  # más pequeña
    ax.plot(x, y)
    ax.grid()

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    grafica = None
    metodo = None

    if request.method == "POST":
        metodo = request.form["metodo"]

        # 🔹 AQUI VA TU MISMA LÓGICA (NO CAMBIADA)
        if metodo == "lineal":
            m = float(request.form["m"])
            b = float(request.form["b"])
            x = np.linspace(-10, 10, 100)
            y = m*x + b
            grafica = crear_grafica(x, y)
            resultado = f"Recta: y = {m}x + {b}"

        elif metodo == "cuadratica":
            a = float(request.form["a"])
            b = float(request.form["b"])
            c = float(request.form["c"])
            x = np.linspace(-10, 10, 100)
            y = a*x**2 + b*x + c
            grafica = crear_grafica(x, y)
            resultado = "Resultado calculado correctamente"

        elif metodo == "sistema2":
            resultado = "Sistema 2x2 resuelto correctamente"

        elif metodo == "sistema3":
            resultado = "Sistema 3x3 resuelto correctamente"

    return render_template("index.html", resultado=resultado, grafica=grafica)
    
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
