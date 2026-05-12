from flask import Flask, render_template, request, send_file
import numpy as np
import matplotlib.pyplot as plt
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

# ======================
# PAGINA PRINCIPAL
# ======================
@app.route("/")
def home():
    return render_template("index.html")

# ======================
# ECUACION LINEAL
# ======================
@app.route("/lineal", methods=["GET", "POST"])
def lineal():
    if request.method == "POST":
        m = float(request.form["m"])
        b = float(request.form["b"])

        x = np.linspace(-10, 10, 100)
        y = m*x + b

        # gráfica
        plt.figure()
        plt.plot(x, y)
        plt.title("Ecuación Lineal")
        plt.grid()

        img_path = "static/lineal.png"
        os.makedirs("static", exist_ok=True)
        plt.savefig(img_path)
        plt.close()

        # PDF
        pdf_path = "resultado_lineal.pdf"
        doc = SimpleDocTemplate(pdf_path)
        styles = getSampleStyleSheet()

        content = []
        content.append(Paragraph(f"Ecuación: y = {m}x + {b}", styles["Normal"]))
        content.append(Image(img_path))

        doc.build(content)

        return render_template("resultado.html",
                               ecuacion=f"y = {m}x + {b}",
                               imagen=img_path,
                               pdf=pdf_path)

    return render_template("lineal.html")

# ======================
# ECUACION CUADRATICA
# ======================
@app.route("/cuadratica", methods=["GET", "POST"])
def cuadratica():
    if request.method == "POST":
        a = float(request.form["a"])
        b = float(request.form["b"])
        c = float(request.form["c"])

        x = np.linspace(-10, 10, 100)
        y = a*x**2 + b*x + c

        plt.figure()
        plt.plot(x, y)
        plt.title("Ecuación Cuadrática")
        plt.grid()

        img_path = "static/cuadratica.png"
        os.makedirs("static", exist_ok=True)
        plt.savefig(img_path)
        plt.close()

        pdf_path = "resultado_cuadratica.pdf"
        doc = SimpleDocTemplate(pdf_path)
        styles = getSampleStyleSheet()

        content = []
        content.append(Paragraph(f"Ecuación: {a}x² + {b}x + {c}", styles["Normal"]))
        content.append(Image(img_path))

        doc.build(content)

        return render_template("resultado.html",
                               ecuacion=f"{a}x² + {b}x + {c}",
                               imagen=img_path,
                               pdf=pdf_path)

    return render_template("cuadratica.html")
# ======================
# SISTEMA 2 x 2
# ======================
    
    @app.route("/sistema2x2", methods=["GET", "POST"])
def sistema2x2():
    if request.method == "POST":
        tipo = request.form["tipo"]

        if tipo == "coef":
            a1 = float(request.form["a1"])
            b1 = float(request.form["b1"])
            c1 = float(request.form["c1"])

            a2 = float(request.form["a2"])
            b2 = float(request.form["b2"])
            c2 = float(request.form["c2"])

        else:
            # ecuaciones tipo: 2x + 3y = 5
            a1 = float(request.form["a1"])
            b1 = float(request.form["b1"])
            c1 = float(request.form["c1"])

            a2 = float(request.form["a2"])
            b2 = float(request.form["b2"])
            c2 = float(request.form["c2"])

        A = np.array([[a1, b1], [a2, b2]])
        B = np.array([c1, c2])

        try:
            sol = np.linalg.solve(A, B)
            resultado = f"x = {round(sol[0],2)}, y = {round(sol[1],2)}"
        except:
            resultado = "Sistema sin solución única"

        return render_template("resultado.html",
                               ecuacion=resultado,
                               imagen=None,
                               pdf=None)

    return render_template("sistema2x2.html")

# ======================
# SISTEMA 3 X 3
# ======================
@app.route("/sistema3x3", methods=["GET", "POST"])
def sistema3x3():
    if request.method == "POST":

        a1 = float(request.form["a1"])
        b1 = float(request.form["b1"])
        c1 = float(request.form["c1"])
        d1 = float(request.form["d1"])

        a2 = float(request.form["a2"])
        b2 = float(request.form["b2"])
        c2 = float(request.form["c2"])
        d2 = float(request.form["d2"])

        a3 = float(request.form["a3"])
        b3 = float(request.form["b3"])
        c3 = float(request.form["c3"])
        d3 = float(request.form["d3"])

        A = np.array([
            [a1, b1, c1],
            [a2, b2, c2],
            [a3, b3, c3]
        ])

        B = np.array([d1, d2, d3])

        try:
            sol = np.linalg.solve(A, B)
            resultado = f"x={round(sol[0],2)}, y={round(sol[1],2)}, z={round(sol[2],2)}"
        except:
            resultado = "Sistema sin solución única"

        return render_template("resultado.html",
                               ecuacion=resultado,
                               imagen=None,
                               pdf=None)

    return render_template("sistema3x3.html")
# ======================
# DESCARGA PDF
# ======================
@app.route("/descargar/<archivo>")
def descargar(archivo):
    return send_file(archivo, as_attachment=True)

# ======================
# MAIN
# ======================
if __name__ == "__main__":
    app.run(debug=True)
