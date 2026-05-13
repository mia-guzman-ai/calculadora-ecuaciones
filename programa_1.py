from flask import Flask, render_template_string, request
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# ================= FUNCION GRAFICA =================

def convertir_imagen(fig):

    img = io.BytesIO()

    fig.savefig(
        img,
        format='png',
        bbox_inches='tight',
        facecolor=fig.get_facecolor()
    )

    img.seek(0)

    return base64.b64encode(img.getvalue()).decode()

# ================= ESTILO PREMIUM =================

ESTILO = """

<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:'Poppins',sans-serif;
}

body{
    background:
    radial-gradient(circle at top left,#1e3a8a,#020617 70%);
    color:white;
    overflow-x:hidden;
}

/* ===== SIDEBAR ===== */

.sidebar{
    position:fixed;
    width:270px;
    height:100vh;
    background:rgba(15,23,42,0.95);
    backdrop-filter:blur(15px);
    padding:25px;
    border-right:1px solid rgba(255,255,255,0.1);
    box-shadow:0 0 30px rgba(0,0,0,0.5);
}

.logo{
    text-align:center;
    margin-bottom:40px;
}

.logo h1{
    color:#60a5fa;
    font-size:32px;
    font-weight:700;
}

.logo p{
    color:#94a3b8;
    margin-top:5px;
    font-size:14px;
}

.sidebar a{
    display:block;
    padding:16px;
    margin-bottom:12px;
    border-radius:14px;
    text-decoration:none;
    color:white;
    font-weight:500;
    transition:0.3s;
    background:rgba(255,255,255,0.03);
}

.sidebar a:hover{
    transform:translateX(6px);
    background:linear-gradient(135deg,#2563eb,#3b82f6);
    box-shadow:0 0 20px rgba(59,130,246,0.4);
}

/* ===== MAIN ===== */

.main{
    margin-left:290px;
    padding:40px;
}

.card{
    background:rgba(255,255,255,0.06);
    backdrop-filter:blur(20px);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:25px;
    padding:35px;
    margin-bottom:35px;
    box-shadow:0 8px 30px rgba(0,0,0,0.35);
}

h1{
    font-size:42px;
    margin-bottom:15px;
    color:#dbeafe;
}

h2{
    color:#93c5fd;
    margin-bottom:18px;
}

h3{
    color:#bfdbfe;
    margin-bottom:15px;
}

p{
    color:#dbeafe;
    line-height:1.8;
    font-size:16px;
}

/* ===== INPUTS ===== */

input{
    width:100%;
    padding:16px;
    margin-top:14px;
    border:none;
    border-radius:14px;
    background:#e0f2fe;
    color:#0f172a;
    font-size:15px;
    outline:none;
    transition:0.3s;
}

input:focus{
    transform:scale(1.02);
    box-shadow:0 0 15px rgba(59,130,246,0.5);
}

/* ===== BOTONES ===== */

.botones{
    display:flex;
    gap:15px;
    margin-top:25px;
}

button{
    flex:1;
    padding:15px;
    border:none;
    border-radius:16px;
    background:linear-gradient(135deg,#2563eb,#60a5fa);
    color:white;
    font-size:15px;
    font-weight:600;
    cursor:pointer;
    transition:0.3s;
}

button:hover{
    transform:translateY(-3px) scale(1.02);
    box-shadow:0 10px 25px rgba(59,130,246,0.4);
}

.btn-volver{
    display:inline-block;
    margin-top:25px;
    text-decoration:none;
    background:#1e40af;
    color:white;
    padding:14px 22px;
    border-radius:15px;
    transition:0.3s;
}

.btn-volver:hover{
    background:#2563eb;
    transform:scale(1.03);
}

/* ===== GRAFICAS ===== */

.grafica{
    background:white;
    border-radius:25px;
    padding:15px;
    margin-top:20px;
    box-shadow:0 10px 25px rgba(0,0,0,0.4);
}

.grafica img{
    width:100%;
    border-radius:15px;
}

/* ===== TEXTO RESULTADO ===== */

.resultado{
    font-size:30px;
    color:#7dd3fc;
    margin-top:15px;
    font-weight:700;
}

/* ===== LISTA ===== */

ul{
    margin-left:20px;
    margin-top:15px;
}

li{
    margin-bottom:12px;
    color:#dbeafe;
}

</style>

"""

# ================= MENU =================

MENU = """

<div class="sidebar">

    <div class="logo">
        <h1>Math App</h1>
        <p>Matemática Interactiva</p>
    </div>

    <a href="/">🏠 Inicio</a>
    <a href="/lineal">📈 Ecuación Lineal</a>
    <a href="/cuadratica">📉 Ecuación Cuadrática</a>
    <a href="/sistema2x2">🔢 Sistema 2x2</a>
    <a href="/sistema3x3">📊 Sistema 3x3</a>

</div>

"""

# ================= GRAFICA ESTILO GEOGEBRA =================

def estilo_grafica():

    fig, ax = plt.subplots(figsize=(9,5))

    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')

    ax.spines['bottom'].set_color('#111827')
    ax.spines['left'].set_color('#111827')

    ax.grid(True, color='#d1d5db', linestyle='--', linewidth=0.7)

    ax.set_xlim(-10,10)
    ax.set_ylim(-10,10)

    return fig, ax

# ================= HOME =================

@app.route("/")
def inicio():

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
                    Plataforma matemática profesional diseñada para resolver
                    ecuaciones y sistemas matemáticos con gráficas dinámicas.
                </p>

                <br>

                <p>
                    El sistema genera automáticamente soluciones,
                    interpretación matemática y visualizaciones avanzadas.
                </p>

                <br>

                <h2>Desarrollado por:</h2>

                <div class="resultado">
                    MIA GUZMAN MOSQUEDA
                </div>

            </div>

            <div class="card">

                <h2>Funciones Disponibles</h2>

                <ul>
                    <li>Resolución de ecuaciones lineales</li>
                    <li>Resolución de ecuaciones cuadráticas</li>
                    <li>Sistemas de ecuaciones 2x2</li>
                    <li>Sistemas de ecuaciones 3x3</li>
                    <li>Gráficas estilo GeoGebra</li>
                    <li>Interpretación matemática automática</li>
                </ul>

            </div>

        </div>

    </body>

    </html>

    """

    return render_template_string(html)

# ================= LINEAL =================

@app.route("/lineal", methods=["GET","POST"])
def lineal():

    if request.method == "POST":

        a = float(request.form["a"])
        b = float(request.form["b"])

        x = -b/a

        fig, ax = estilo_grafica()

        xs = np.linspace(-10,10,400)
        ys = a*xs + b

        ax.plot(
            xs,
            ys,
            color='#2563eb',
            linewidth=3,
            label='y = ax + b'
        )

        ax.scatter(
            [x],
            [0],
            color='red',
            s=80,
            zorder=5
        )

        ax.legend()

        ax.set_title(
            "Gráfica de la Ecuación Lineal",
            fontsize=16,
            fontweight='bold'
        )

        img = convertir_imagen(fig)

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

                    <div class="resultado">
                        x = {x:.2f}
                    </div>

                    <br>

                    <p>
                        La solución representa el punto donde la recta
                        intersecta el eje X.
                    </p>

                </div>

                <div class="card">

                    <h2>Visualización Matemática</h2>

                    <div class="grafica">

                        <img src="data:image/png;base64,{img}">

                    </div>

                </div>

            </div>

        </body>

        </html>

        """

        return render_template_string(html)

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

                <p>
                    Forma general:
                </p>

                <br>

                <div class="resultado">
                    ax + b = 0
                </div>

                <form method="POST">

                    <input
                    type="number"
                    step="any"
                    name="a"
                    placeholder="Coeficiente a | Ejemplo: 2"
                    required>

                    <input
                    type="number"
                    step="any"
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

# ================= MAIN =================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
