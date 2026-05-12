from flask import Flask, request, render_template, send_file
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
import os

app = Flask(__name__)

# ======================
# FUNCION PARA GRAFICA
# ======================
def generar_grafica(x, y):
    plt.figure(figsize=(4,3))
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
    tipo = request.form["tipo"]

    if tipo == "pendiente":
        m = float(request.form["m"])
        b = float(request.form["b"])
        x = np.linspace(-10,10,100)
        y = m*x + b
        resultado = f"y = {m}x + {b}"

    elif tipo == "dos_puntos":
        x1 = float(request.form["x1"])
        y1 = float(request.form["y1"])
        x2 = float(request.form["x2"])
        y2 = float(request.form["y2"])
        m = (y2-y1)/(x2-x1)
        b = y1 - m*x1
        x = np.linspace(-10,10,100)
        y = m*x + b
        resultado = f"y = {round(m,2)}x + {round(b,2)}"

    grafica = generar_grafica(x,y)

    return render_template("index.html", resultado=resultado, grafica=grafica)


# ======================
# CUADRATICA
# ======================
@app.route("/cuadratica", methods=["POST"])
def cuadratica():
    a = float(request.form["a"])
    b = float(request.form["b"])
    c = float(request.form["c"])

    x = np.linspace(-10,10,100)
    y = a*x**2 + b*x + c

    discriminante = b**2 - 4*a*c

    if discriminante >= 0:
        x1 = (-b + np.sqrt(discriminante))/(2*a)
        x2 = (-b - np.sqrt(discriminante))/(2*a)
        resultado = f"Raíces: {round(x1,2)} , {round(x2,2)}"
    else:
        resultado = "No tiene raíces reales"

    grafica = generar_grafica(x,y)

    return render_template("index.html", resultado=resultado, grafica=grafica)


# ======================
# SISTEMA 2x2
# ======================
@app.route("/sistema2", methods=["POST"])
def sistema2():
    a1 = float(request.form["a1"])
    b1 = float(request.form["b1"])
    c1 = float(request.form["c1"])

    a2 = float(request.form["a2"])
    b2 = float(request.form["b2"])
    c2 = float(request.form["c2"])

    A = np.array([[a1,b1],[a2,b2]])
    B = np.array([c1,c2])

    sol = np.linalg.solve(A,B)

    resultado = f"x = {round(sol[0],2)}, y = {round(sol[1],2)}"

    return render_template("index.html", resultado=resultado)


# ======================
# SISTEMA 3x3
# ======================
@app.route("/sistema3", methods=["POST"])
def sistema3():
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

    sol = np.linalg.solve(A,B)

    resultado = f"x={round(sol[0],2)}, y={round(sol[1],2)}, z={round(sol[2],2)}"

    return render_template("index.html", resultado=resultado)


# ======================
# PDF
# ======================
@app.route("/pdf")
def pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    story = []
    story.append(Paragraph("Resultado generado", styles["Title"]))

    if os.path.exists("grafica.png"):
        story.append(Image("grafica.png", width=200, height=150))

    doc.build(story)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="resultado.pdf")


# ======================
# PUERTO
# ======================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
