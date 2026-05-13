from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# =========================
# FUNCION PARA GRAFICA
# =========================
def grafica(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

# =========================
# LINEAL: ax + b = 0
# =========================
@app.route("/lineal", methods=["GET", "POST"])
def lineal():
    if request.method == "POST":
        try:
            a = float(request.form["a"])
            b = float(request.form["b"])

            if a == 0:
                return "Error: a no puede ser 0"

            x = -b / a

            fig, ax = plt.subplots()
            xs = np.linspace(-10, 10, 100)
            ys = a * xs + b
            ax.plot(xs, ys)
            ax.axhline(0, color="black")
            ax.axvline(x, color="red")

            img = grafica(fig)

            return render_template("resultado.html",
                titulo="Ecuación Lineal",
                resultado=f"x = {x:.2f}",
                imagen=img,
                explicacion="Intersección con el eje X"
            )

        except Exception as e:
            return f"Error lineal: {str(e)}"

    return render_template("lineal.html")

# =========================
# CUADRÁTICA
# =========================
@app.route("/cuadratica", methods=["GET", "POST"])
def cuadratica():
    if request.method == "POST":
        try:
            a = float(request.form["a"])
            b = float(request.form["b"])
            c = float(request.form["c"])

            disc = b**2 - 4*a*c

            if disc < 0:
                return "No hay raíces reales"

            x1 = (-b + np.sqrt(disc)) / (2*a)
            x2 = (-b - np.sqrt(disc)) / (2*a)

            fig, ax = plt.subplots()
            xs = np.linspace(-10, 10, 100)
            ys = a*xs**2 + b*xs + c
            ax.plot(xs, ys)
            ax.axhline(0)

            img = grafica(fig)

            return render_template("resultado.html",
                titulo="Cuadrática",
                resultado=f"x1={x1:.2f}, x2={x2:.2f}",
                imagen=img,
                explicacion="Raíces de la parábola"
            )

        except Exception as e:
            return f"Error cuadrática: {str(e)}"

    return render_template("cuadratica.html")

# =========================
# SISTEMA 2X2
# =========================
@app.route("/sistema2x2", methods=["GET", "POST"])
def sistema2x2():
    if request.method == "POST":
        try:
            A = np.array([
                [float(request.form["a1"]), float(request.form["b1"])],
                [float(request.form["a2"]), float(request.form["b2"])]
            ])

            B = np.array([float(request.form["c1"]), float(request.form["c2"])])

            if np.linalg.det(A) == 0:
                return "Sistema sin solución única (det = 0)"

            sol = np.linalg.solve(A, B)

            fig, ax = plt.subplots()
            x = np.linspace(-10, 10, 100)

            y1 = (B[0] - A[0][0]*x) / A[0][1]
            y2 = (B[1] - A[1][0]*x) / A[1][1]

            ax.plot(x, y1)
            ax.plot(x, y2)

            img = grafica(fig)

            return render_template("resultado.html",
                titulo="Sistema 2x2",
                resultado=f"x={sol[0]:.2f}, y={sol[1]:.2f}",
                imagen=img,
                explicacion="Intersección de dos rectas"
            )

        except Exception as e:
            return f"Error sistema 2x2: {str(e)}"

    return render_template("sistema2x2.html")

# =========================
# SISTEMA 3X3
# =========================
@app.route("/sistema3x3", methods=["GET", "POST"])
def sistema3x3():
    if request.method == "POST":
        A = np.array([
            [float(request.form["a11"]), float(request.form["a12"]), float(request.form["a13"])],
            [float(request.form["a21"]), float(request.form["a22"]), float(request.form["a23"])],
            [float(request.form["a31"]), float(request.form["a32"]), float(request.form["a33"])]
        ])
        B = np.array([
            float(request.form["b1"]),
            float(request.form["b2"]),
            float(request.form["b3"])
        ])

        sol = np.linalg.solve(A,B)

        return render_template("resultado.html",
            titulo="Sistema 3x3",
            resultado=f"x={sol[0]:.2f}, y={sol[1]:.2f}, z={sol[2]:.2f}",
            imagen=None,
            explicacion="Intersección de 3 planos en el espacio"
        )

    return render_template("sistema3x3.html")

# =========================
# INDEX
# =========================
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
