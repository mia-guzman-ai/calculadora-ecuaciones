from flask import Flask, request, render_template
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import os

app = Flask(__name__)

# ======================
# GRAFICA
# ======================
def generar_grafica(x, y):
    plt.figure()
    plt.plot(x, y)
    plt.grid()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    grafica = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return grafica


# ======================
# INICIO
# ======================
@app.route("/")
def inicio():
    return render_template("index.html")


# ======================
# LINEAL
# ======================
@app.route("/lineal", methods=["POST"])
def lineal():
    try:
        tipo = request.form.get("tipo")

        if tipo == "pendiente":
            m = float(request.form.get("m", 0))
            b = float(request.form.get("b", 0))
        else:
            x1 = float(request.form.get("x1", 0))
            y1 = float(request.form.get("y1", 0))
            x2 = float(request.form.get("x2", 0))
            y2 = float(request.form.get("y2", 0))

            if x1 == x2:
                return render_template("index.html", resultado="Error: x1 no puede ser igual a x2")

            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1

        x = np.linspace(-10, 10, 100)
        y = m * x + b

        grafica = generar_grafica(x, y)
        resultado = f"y = {round(m,2)}x + {round(b,2)}"

        return render_template("index.html", resultado=resultado, grafica=grafica)

    except:
        return render_template("index.html", resultado="Error en datos")


# ======================
# CUADRATICA
# ======================
@app.route("/cuadratica", methods=["POST"])
def cuadratica():
    try:
        a = float(request.form.get("a", 0))
        b = float(request.form.get("b", 0))
        c = float(request.form.get("c", 0))

        x = np.linspace(-10, 10, 100)
        y = a * x**2 + b * x + c

        d = b**2 - 4*a*c

        if d >= 0:
            x1 = (-b + np.sqrt(d)) / (2*a)
            x2 = (-b - np.sqrt(d)) / (2*a)
            resultado = f"Raíces: {round(x1,2)} , {round(x2,2)}"
        else:
            resultado = "No tiene raíces reales"

        grafica = generar_grafica(x, y)

        return render_template("index.html", resultado=resultado, grafica=grafica)

    except:
        return render_template("index.html", resultado="Error en datos")


# ======================
# SISTEMA 2x2
# ======================
@app.route("/sistema2", methods=["POST"])
def sistema2():
    try:
        A = np.array([
            [float(request.form.get("a1", 0)), float(request.form.get("b1", 0))],
            [float(request.form.get("a2", 0)), float(request.form.get("b2", 0))]
        ])

        B = np.array([
            float(request.form.get("c1", 0)),
            float(request.form.get("c2", 0))
        ])

        sol = np.linalg.solve(A, B)

        resultado = f"x = {round(sol[0],2)}, y = {round(sol[1],2)}"

    except:
        resultado = "Sistema sin solución o error"

    return render_template("index.html", resultado=resultado)


# ======================
# SISTEMA 3x3
# ======================
@app.route("/sistema3", methods=["POST"])
def sistema3():
    try:
        A = np.array([
            [float(request.form.get("a1", 0)), float(request.form.get("b1", 0)), float(request.form.get("c1", 0))],
            [float(request.form.get("a2", 0)), float(request.form.get("b2", 0)), float(request.form.get("c2", 0))],
            [float(request.form.get("a3", 0)), float(request.form.get("b3", 0)), float(request.form.get("c3", 0))]
        ])

        B = np.array([
            float(request.form.get("d1", 0)),
            float(request.form.get("d2", 0)),
            float(request.form.get("d3", 0))
        ])

        sol = np.linalg.solve(A, B)

        resultado = f"x={round(sol[0],2)}, y={round(sol[1],2)}, z={round(sol[2],2)}"

    except:
        resultado = "Sistema sin solución o error"

    return render_template("index.html", resultado=resultado)


# ======================
# MAIN
# ======================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
