from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import os

app = Flask(__name__)

# ===== GRAFICA =====
def crear_grafica(x, y):
    fig, ax = plt.subplots(figsize=(4,3))
    ax.plot(x, y)
    ax.grid()

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close(fig)  # 🔥 IMPORTANTE para evitar errores en Railway

    return base64.b64encode(img.getvalue()).decode()

# ===== RUTA PRINCIPAL =====
@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    grafica = None

    if request.method == "POST":
        metodo = request.form.get("metodo")

        try:
            # ===== LINEAL =====
            if metodo == "lineal":
                m = float(request.form.get("m"))
                b = float(request.form.get("b"))

                x = np.linspace(-10, 10, 100)
                y = m*x + b

                grafica = crear_grafica(x, y)
                resultado = f"Recta: y = {m}x + {b}"

            # ===== CUADRATICA =====
            elif metodo == "cuadratica":
                a = float(request.form.get("a"))
                b = float(request.form.get("b"))
                c = float(request.form.get("c"))

                x = np.linspace(-10, 10, 100)
                y = a*x**2 + b*x + c

                grafica = crear_grafica(x, y)
                resultado = "Ecuación cuadrática procesada correctamente"

            # ===== SISTEMA 2x2 =====
            elif metodo == "sistema2":
                A = np.array([
                    [float(request.form.get("a1")), float(request.form.get("b1"))],
                    [float(request.form.get("a2")), float(request.form.get("b2"))]
                ])
                B = np.array([
                    float(request.form.get("c1")),
                    float(request.form.get("c2"))
                ])

                sol = np.linalg.solve(A, B)
                resultado = f"x = {sol[0]:.2f}, y = {sol[1]:.2f}"

            # ===== SISTEMA 3x3 =====
            elif metodo == "sistema3":
                A = np.array([
                    [float(request.form.get("a1")), float(request.form.get("b1")), float(request.form.get("c1"))],
                    [float(request.form.get("a2")), float(request.form.get("b2")), float(request.form.get("c2"))],
                    [float(request.form.get("a3")), float(request.form.get("b3")), float(request.form.get("c3"))]
                ])
                B = np.array([
                    float(request.form.get("d1")),
                    float(request.form.get("d2")),
                    float(request.form.get("d3"))
                ])

                sol = np.linalg.solve(A, B)
                resultado = f"x = {sol[0]:.2f}, y = {sol[1]:.2f}, z = {sol[2]:.2f}"

        except Exception as e:
            resultado = f"Error en los datos: {str(e)}"

    return render_template("index.html", resultado=resultado, grafica=grafica)


# ===== RUN (RAILWAY CORRECTO) =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
