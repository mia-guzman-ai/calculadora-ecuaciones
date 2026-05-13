from flask import Flask, render_template_string, request
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# ================= FUNCION GRAFICA =================

def grafica(fig):
    img = io.BytesIO()

    fig.savefig(
        img,
        format='png',
        bbox_inches='tight',
        facecolor=fig.get_facecolor()
    )

    img.seek(0)

    return base64.b64encode(img.getvalue()).decode()

# ================= ESTILO GLOBAL =================

ESTILO = """

<style>

body{
    margin:0;
    font-family:Arial,sans-serif;
    background:linear-gradient(135deg,#081b33,#0f3460);
    color:white;
}

/* SIDEBAR */

.sidebar{
    width:260px;
    height:100vh;
    position:fixed;
    background:#06111f;
    padding-top:20px;
    box-shadow:2px 0 15px rgba(0,0,0,0.5);
}

.sidebar h2{
    text-align:center;
    color:#8ec5ff;
    margin-bottom:30px;
}

.sidebar a{
    display:block;
    color:white;
    text-decoration:none;
    padding:15px;
    transition:0.3s;
    border-left:4px solid transparent;
}

.sidebar a:hover{
    background:#12345c;
    border-left:4px solid #5aa9ff;
}

/* MAIN */

.main{
    margin-left:280px;
    padding:40px;
}

.card{
    background:rgba(255,255,255,0.08);
    backdrop-filter:blur(10px);
    border-radius:20px;
    padding:30px;
    margin-bottom:30px;
    box-shadow:0 0 20px rgba(0,0,0,0.4);
}

/* INPUTS */

input{
    width:95%;
    padding:14px;
    margin-top:12px;
    border:none;
    border-radius:10px;
    background:#dcecff;
    font-size:15px;
}

/* BOTONES */

.botones{
    display:flex;
    gap:10px;
    margin-top:20px;
}

button{
    flex:1;
    padding:14px;
    border:none;
    border-radius:12px;
    background:linear-gradient(135deg,#1d4e89,#2563b8);
    color:white;
    font-size:15px;
    cursor:pointer;
    transition:0.3s;
    font-weight:bold;
}

button:hover{
    transform:scale(1.03);
    background:linear-gradient(135deg,#2563b8,#3b82f6);
}

.btn-volver{
    display:inline-block;
    margin-top:20px;
    text-decoration:none;
    color:white;
    background:#16355c;
    padding:12px 20px;
    border-radius:12px;
}

.btn-volver:hover{
    background:#21558f;
}

img{
    width:100%;
    border-radius:15px;
    margin-top:15px;
    background:white;
    padding:10px;
}

h1,h2,h3{
    color:#b8dfff;
}

</style>

"""

# ================= MENU =================

MENU = """

<div class="sidebar">

    <h2>Math App</h2>

    <a href="/">🏠 Inicio</a>
    <a href="/lineal">📈 Ecuación Lineal</a>
    <a href="/cuadratica">📉 Ecuación Cuadrática</a>
    <a href="/sistema2x2">🔢 Sistema 2x2</a>
    <a href="/sistema3x3">📊 Sistema 3x3</a>

</div>

"""

# ================= HOME =================

@app.route("/")
def index():

    html = f"""

    <html>

    <head>
        <title>Math App</title>
        {ESTILO}
    </head>

    <body>

        {MENU}

        <div class="main">

            <div class="card">

                <h1>Bienvenido 👋</h1>

                <p>
                    Plataforma matemática interactiva diseñada para resolver
                    ecuaciones lineales, cuadráticas y sistemas de ecuaciones.
                </p>

                <p>
                    El sistema calcula automáticamente soluciones,
                    genera gráficas e interpreta resultados.
                </p>

                <h3>Desarrollado por:</h3>

                <h2>MIA GUZMAN MOSQUEDA</h2>

            </div>

            <div class="card">

                <h2>¿Qué puedes hacer?</h2>

                <ul>
                    <li>Resolver ecuaciones lineales</li>
                    <li>Resolver ecuaciones cuadráticas</li>
                    <li>Resolver sistemas 2x2</li>
                    <li>Resolver sistemas 3x3</li>
                    <li>Visualizar gráficas automáticas</li>
                </ul>

            </div>

        </div>

    </body>

    </html>

    """

    return render_template_string(html)

# ================= LINEAL =================

@app.route("/lineal", methods=["GET", "POST"])
def lineal():

    if request.method == "POST":

        try:

            a = float(request.form["a"])
            b = float(request.form["b"])

            x = -b / a

            fig, ax = plt.subplots(figsize=(8,5))

            fig.patch.set_facecolor('#0f172a')
            ax.set_facecolor('#eaf4ff')

            xs = np.linspace(-10,10,200)
            ys = a*xs + b

            ax.plot(
                xs,
                ys,
                color='#2563eb',
                linewidth=3,
                label='Recta'
            )

            ax.axhline(0,color='black')
            ax.axvline(0,color='black')

            ax.grid(True, linestyle='--', alpha=0.5)

            ax.set_title(
                "Gráfica de la Ecuación Lineal",
                fontsize=16,
                color='white'
            )

            ax.legend()

            img = grafica(fig)

            html = f"""

            <html>

            <head>
                <title>Resultado</title>
                {ESTILO}
            </head>

            <body>

                {MENU}

                <div class="main">

                    <div class="card">

                        <h1>Resultado</h1>

                        <h2>x = {x:.2f}</h2>

                        <p>
                            La solución representa el punto donde la recta
                            intersecta el eje X.
                        </p>

                    </div>

                    <div class="card">

                        <h2>Gráfica</h2>

                        <img src="data:image/png;base64,{img}">

                    </div>

                    <a class="btn-volver" href="/lineal">
                        Volver
                    </a>

                </div>

            </body>

            </html>

            """

            return render_template_string(html)

        except:
            return "Error en los datos"

    html = f"""

    <html>

    <head>
        <title>Lineal</title>
        {ESTILO}
    </head>

    <body>

        {MENU}

        <div class="main">

            <div class="card">

                <h1>Ecuación Lineal</h1>

                <form method="POST">

                    <input type="number" step="any"
                    name="a"
                    placeholder="Coeficiente a | Ejemplo: 2"
                    required>

                    <input type="number" step="any"
                    name="b"
                    placeholder="Coeficiente b | Ejemplo: -8"
                    required>

                    <div class="botones">

                        <button type="submit">
                            Calcular
                        </button>

                        <button type="reset">
                            Limpiar
                        </button>

                    </div>

                </form>

            </div>

        </div>

    </body>

    </html>

    """

    return render_template_string(html)

# ================= CUADRATICA =================

@app.route("/cuadratica", methods=["GET", "POST"])
def cuadratica():

    if request.method == "POST":

        try:

            a = float(request.form["a"])
            b = float(request.form["b"])
            c = float(request.form["c"])

            d = b**2 - 4*a*c

            if d < 0:
                return "No tiene raíces reales"

            x1 = (-b + np.sqrt(d))/(2*a)
            x2 = (-b - np.sqrt(d))/(2*a)

            fig, ax = plt.subplots(figsize=(8,5))

            fig.patch.set_facecolor('#0f172a')
            ax.set_facecolor('#eaf4ff')

            xs = np.linspace(-10,10,400)
            ys = a*xs**2 + b*xs + c

            ax.plot(
                xs,
                ys,
                color='#00d4ff',
                linewidth=3,
                label='Parábola'
            )

            ax.axhline(0,color='black')
            ax.axvline(0,color='black')

            ax.grid(True, linestyle='--', alpha=0.5)

            ax.set_title(
                "Gráfica de la Parábola",
                fontsize=16,
                color='white'
            )

            ax.legend()

            img = grafica(fig)

            html = f"""

            <html>

            <head>
                <title>Resultado</title>
                {ESTILO}
            </head>

            <body>

                {MENU}

                <div class="main">

                    <div class="card">

                        <h1>Resultado</h1>

                        <h2>x1 = {x1:.2f}</h2>
                        <h2>x2 = {x2:.2f}</h2>

                        <p>
                            Las raíces representan donde la parábola
                            corta el eje X.
                        </p>

                    </div>

                    <div class="card">

                        <h2>Gráfica</h2>

                        <img src="data:image/png;base64,{img}">

                    </div>

                    <a class="btn-volver" href="/cuadratica">
                        Volver
                    </a>

                </div>

            </body>

            </html>

            """

            return render_template_string(html)

        except:
            return "Error en los datos"

    html = f"""

    <html>

    <head>
        <title>Cuadrática</title>
        {ESTILO}
    </head>

    <body>

        {MENU}

        <div class="main">

            <div class="card">

                <h1>Ecuación Cuadrática</h1>

                <form method="POST">

                    <input type="number" step="any"
                    name="a"
                    placeholder="Coeficiente a"
                    required>

                    <input type="number" step="any"
                    name="b"
                    placeholder="Coeficiente b"
                    required>

                    <input type="number" step="any"
                    name="c"
                    placeholder="Coeficiente c"
                    required>

                    <div class="botones">

                        <button type="submit">
                            Calcular
                        </button>

                        <button type="reset">
                            Limpiar
                        </button>

                    </div>

                </form>

            </div>

        </div>

    </body>

    </html>

    """

    return render_template_string(html)

# ================= SISTEMA 2X2 =================

@app.route("/sistema2x2", methods=["GET", "POST"])
def sistema2x2():

    if request.method == "POST":

        try:

            A = np.array([
                [float(request.form["a1"]), float(request.form["b1"])],
                [float(request.form["a2"]), float(request.form["b2"])]
            ])

            B = np.array([
                float(request.form["c1"]),
                float(request.form["c2"])
            ])

            sol = np.linalg.solve(A,B)

            fig, ax = plt.subplots(figsize=(8,5))

            fig.patch.set_facecolor('#0f172a')
            ax.set_facecolor('#eaf4ff')

            x = np.linspace(-10,10,200)

            y1 = (B[0]-A[0][0]*x)/A[0][1]
            y2 = (B[1]-A[1][0]*x)/A[1][1]

            ax.plot(x,y1,linewidth=3,label='Ecuación 1')
            ax.plot(x,y2,linewidth=3,label='Ecuación 2')

            ax.grid(True, linestyle='--', alpha=0.5)

            ax.legend()

            ax.set_title(
                "Sistema de Ecuaciones 2x2",
                fontsize=16,
                color='white'
            )

            img = grafica(fig)

            html = f"""

            <html>

            <head>
                <title>Resultado</title>
                {ESTILO}
            </head>

            <body>

                {MENU}

                <div class="main">

                    <div class="card">

                        <h1>Resultado</h1>

                        <h2>x = {sol[0]:.2f}</h2>
                        <h2>y = {sol[1]:.2f}</h2>

                    </div>

                    <div class="card">

                        <h2>Gráfica</h2>

                        <img src="data:image/png;base64,{img}">

                    </div>

                </div>

            </body>

            </html>

            """

            return render_template_string(html)

        except:
            return "Error en los datos"

    html = f"""

    <html>

    <head>
        <title>Sistema 2x2</title>
        {ESTILO}
    </head>

    <body>

        {MENU}

        <div class="main">

            <div class="card">

                <h1>Sistema 2x2</h1>

                <form method="POST">

                    <input name="a1" placeholder="a1" required>
                    <input name="b1" placeholder="b1" required>
                    <input name="c1" placeholder="c1" required>

                    <input name="a2" placeholder="a2" required>
                    <input name="b2" placeholder="b2" required>
                    <input name="c2" placeholder="c2" required>

                    <div class="botones">

                        <button type="submit">
                            Calcular
                        </button>

                        <button type="reset">
                            Limpiar
                        </button>

                    </div>

                </form>

            </div>

        </div>

    </body>

    </html>

    """

    return render_template_string(html)

# ================= SISTEMA 3X3 =================

@app.route("/sistema3x3", methods=["GET", "POST"])
def sistema3x3():

    if request.method == "POST":

        try:

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

            html = f"""

            <html>

            <head>
                <title>Resultado</title>
                {ESTILO}
            </head>

            <body>

                {MENU}

                <div class="main">

                    <div class="card">

                        <h1>Resultado</h1>

                        <h2>x = {sol[0]:.2f}</h2>
                        <h2>y = {sol[1]:.2f}</h2>
                        <h2>z = {sol[2]:.2f}</h2>

                    </div>

                </div>

            </body>

            </html>

            """

            return render_template_string(html)

        except:
            return "Error en los datos"

    html = f"""

    <html>

    <head>
        <title>Sistema 3x3</title>
        {ESTILO}
    </head>

    <body>

        {MENU}

        <div class="main">

            <div class="card">

                <h1>Sistema 3x3</h1>

                <form method="POST">

                    <input name="a11" placeholder="a11" required>
                    <input name="a12" placeholder="a12" required>
                    <input name="a13" placeholder="a13" required>

                    <input name="a21" placeholder="a21" required>
                    <input name="a22" placeholder="a22" required>
                    <input name="a23" placeholder="a23" required>

                    <input name="a31" placeholder="a31" required>
                    <input name="a32" placeholder="a32" required>
                    <input name="a33" placeholder="a33" required>

                    <input name="b1" placeholder="b1" required>
                    <input name="b2" placeholder="b2" required>
                    <input name="b3" placeholder="b3" required>

                    <div class="botones">

                        <button type="submit">
                            Calcular
                        </button>

                        <button type="reset">
                            Limpiar
                        </button>

                    </div>

                </form>

            </div>

        </div>

    </body>

    </html>

    """

    return render_template_string(html)

# ================= MAIN =================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
