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
