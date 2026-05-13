from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# ======================
# INICIO
# ======================
@app.route("/")
def index():
    return render_template("index.html")
    return render_template("resultado.html")
    return render_template("sistema2x2.html")
    return render_template("sistema3x3.html")
    return render_template("cuadratica.html")
    return render_template("lineal.html")
    

# ======================
# ECUACION LINEAL
# ax + b = 0
# ======================
@app.route("/lineal", methods=["GET", "POST"])
def lineal():
    if request.method == "POST":
        tipo = request.form["tipo"]

        if tipo == "coef":
            a = float(request.form["a"] or 0)
            b = float(request.form["b"] or 0)

        elif tipo == "puntos":
            x1 = float(request.form["x1"] or 0)
            y1 = float(request.form["y1"] or 0)
            x2 = float(request.form["x2"] or 0)
            y2 = float(request.form["y2"] or 0)

            a = (y2 - y1) / (x2 - x1)
            b = y1 - a*x1

        if a != 0:
            x = -b/a
            resultado = f"x = {round(x,2)}"

            xs = list(range(-10,10))
            ys = [a*i + b for i in xs]

            plt.plot(xs, ys)
            plt.axhline(0)
            plt.axvline(0)

            if not os.path.exists("static"):
                os.makedirs("static")

            ruta = "static/lineal.png"
            plt.savefig(ruta)
            plt.clf()

        else:
            resultado = "Sin solución"
            ruta = None

        return render_template("resultado.html", ecuacion=resultado, imagen=ruta)

    return render_template("lineal.html")

# ======================
# ECUACION CUADRATICA
# ax^2 + bx + c = 0
# ======================
@app.route("/cuadratica", methods=["GET", "POST"])
def cuadratica():
    if request.method == "POST":

        a = float(request.form["a"] or 0)
        b = float(request.form["b"] or 0)
        c = float(request.form["c"] or 0)

        d = b**2 - 4*a*c

        if d >= 0 and a != 0:
            x1 = (-b + d**0.5)/(2*a)
            x2 = (-b - d**0.5)/(2*a)
            resultado = f"x1={round(x1,2)}, x2={round(x2,2)}"
        else:
            resultado = "Sin solución real"

        xs = list(range(-10,10))
        ys = [a*i**2 + b*i + c for i in xs]

        plt.plot(xs, ys)
        plt.axhline(0)
        plt.axvline(0)

        if not os.path.exists("static"):
            os.makedirs("static")

        ruta = "static/cuadratica.png"
        plt.savefig(ruta)
        plt.clf()

        return render_template("resultado.html", ecuacion=resultado, imagen=ruta)

    return render_template("cuadratica.html")

# ======================
# SISTEMA 2x2
# ======================
@app.route("/sistema2x2", methods=["GET", "POST"])
def sistema2x2():
    if request.method == "POST":

        a1 = float(request.form["a1"] or 0)
        b1 = float(request.form["b1"] or 0)
        c1 = float(request.form["c1"] or 0)

        a2 = float(request.form["a2"] or 0)
        b2 = float(request.form["b2"] or 0)
        c2 = float(request.form["c2"] or 0)

        A = np.array([[a1,b1],[a2,b2]])
        B = np.array([c1,c2])

        try:
            sol = np.linalg.solve(A,B)
            resultado = f"x={round(sol[0],2)}, y={round(sol[1],2)}"
        except:
            resultado = "Sin solución"
            sol = None

        xs = list(range(-10,10))
        y1 = [(c1 - a1*x)/b1 if b1!=0 else 0 for x in xs]
        y2 = [(c2 - a2*x)/b2 if b2!=0 else 0 for x in xs]

        plt.plot(xs, y1, label="E1")
        plt.plot(xs, y2, label="E2")
        plt.legend()

        if not os.path.exists("static"):
            os.makedirs("static")

        ruta = "static/sistema.png"
        plt.savefig(ruta)
        plt.clf()

        return render_template("resultado.html", ecuacion=resultado, imagen=ruta)

    return render_template("sistema2x2.html")

# ======================
# SISTEMA 3x3
# ======================
@app.route("/sistema3x3", methods=["GET", "POST"])
def sistema3x3():
    if request.method == "POST":

        a1 = float(request.form["a1"] or 0)
        b1 = float(request.form["b1"] or 0)
        c1 = float(request.form["c1"] or 0)
        d1 = float(request.form["d1"] or 0)

        a2 = float(request.form["a2"] or 0)
        b2 = float(request.form["b2"] or 0)
        c2 = float(request.form["c2"] or 0)
        d2 = float(request.form["d2"] or 0)

        a3 = float(request.form["a3"] or 0)
        b3 = float(request.form["b3"] or 0)
        c3 = float(request.form["c3"] or 0)
        d3 = float(request.form["d3"] or 0)

        A = np.array([
            [a1, b1, c1],
            [a2, b2, c2],
            [a3, b3, c3]
        ])

        B = np.array([d1, d2, d3])

        try:
            sol = np.linalg.solve(A, B)
            resultado = f"x = {round(sol[0],2)}, y = {round(sol[1],2)}, z = {round(sol[2],2)}"
        except:
            resultado = "Sistema sin solución única"

        return render_template("resultado.html", ecuacion=resultado, imagen=None)

    return render_template("sistema3x3.html")


if __name__ == "__main__":
    app.run(debug=True)
