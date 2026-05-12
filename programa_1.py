from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def crear_grafica(funcion_x, funcion_y):
    fig, ax = plt.subplots(figsize=(4,3))  # gráfica más pequeña
    ax.plot(funcion_x, funcion_y)
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

        if metodo == "lineal":
            m = float(request.form["m"])
            b = float(request.form["b"])

            x = np.linspace(-10, 10, 100)
            y = m*x + b

            grafica = crear_grafica(x, y)
            resultado = f"La recta tiene pendiente {m} y corta en {b}"

        elif metodo == "cuadratica":
            a = float(request.form["a"])
            b = float(request.form["b"])
            c = float(request.form["c"])

            discriminante = b**2 - 4*a*c

            if discriminante >= 0:
                x1 = (-b + np.sqrt(discriminante)) / (2*a)
                x2 = (-b - np.sqrt(discriminante)) / (2*a)
                resultado = f"Soluciones reales: x1={x1:.2f}, x2={x2:.2f}"
            else:
                resultado = "No tiene soluciones reales"

            x = np.linspace(-10, 10, 100)
            y = a*x**2 + b*x + c
            grafica = crear_grafica(x, y)

        elif metodo == "sistema2":
            a1 = float(request.form["a1"])
            b1 = float(request.form["b1"])
            c1 = float(request.form["c1"])

            a2 = float(request.form["a2"])
            b2 = float(request.form["b2"])
            c2 = float(request.form["c2"])

            A = np.array([[a1, b1], [a2, b2]])
            B = np.array([c1, c2])

            sol = np.linalg.solve(A, B)
            resultado = f"x={sol[0]:.2f}, y={sol[1]:.2f}"

        elif metodo == "sistema3":
            A = np.array([
                [float(request.form["a1"]), float(request.form["b1"]), float(request.form["c1"])],
                [float(request.form["a2"]), float(request.form["b2"]), float(request.form["c2"])],
                [float(request.form["a3"]), float(request.form["b3"]), float(request.form["c3"])]
            ])

            B = np.array([
                float(request.form["d1"]),
                float(request.form["d2"]),
                float(request.form["d3"])
            ])

            sol = np.linalg.solve(A, B)
            resultado = f"x={sol[0]:.2f}, y={sol[1]:.2f}, z={sol[2]:.2f}"

    return render_template("index.html", resultado=resultado, grafica=grafica, metodo=metodo)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
