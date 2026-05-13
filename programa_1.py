from flask import Flask, render_template_string, request
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# ================= FUNCION IMAGEN =================

def convertir_imagen(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight', facecolor=fig.get_facecolor())
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

# ================= SEGURIDAD INPUTS =================

def fget(key, default="0"):
    val = request.form.get(key)
    if val is None or val == "":
        return default
    return val

# ================= ESTILO (NO TOCADO) =================

ESTILO = """<style>
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

p{
    color:#dbeafe;
    line-height:1.8;
}

input, select{
    width:100%;
    padding:16px;
    margin-top:14px;
    border:none;
    border-radius:14px;
    background:#e0f2fe;
    color:#0f172a;
}

button{
    padding:15px;
    border:none;
    border-radius:16px;
    background:linear-gradient(135deg,#2563eb,#60a5fa);
    color:white;
    font-weight:600;
    cursor:pointer;
    margin-top:15px;
}

.grafica img{
    width:100%;
    border-radius:15px;
}

.resultado{
    font-size:28px;
    color:#7dd3fc;
    font-weight:700;
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

# ================= GRAFICA =================

def grafica_base():
    fig, ax = plt.subplots(figsize=(8,5))

    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.axhline(0,color="black")
    ax.axvline(0,color="black")

    ax.grid(True)

    ax.set_xlim(-10,10)
    ax.set_ylim(-10,10)

    return fig, ax

# ================= HOME =================

@app.route("/")
def inicio():
    return render_template_string(f"""
<html>
<head>{ESTILO}</head>
<body>{MENU}

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
<h2>MÍA GUZMÁN MOSQUEDA</h2>

</div>

<div class="card">

<h2>¿Qué puedes hacer?</h2>

<ul>
<li>Resolver ecuaciones lineales</li>
<li>Resolver ecuaciones cuadráticas</li>
<li>Resolver sistemas 2 x 2</li>
<li>Resolver sistemas 3 x 3</li>
<li>Visualizar gráficas automáticas</li>
</ul>

</div>

</div>

</body>
</html>
""")

# ================= LINEAL =================

@app.route("/lineal", methods=["GET","POST"])
def lineal():


    tipo = request.form.get("tipo","pendiente")

    resultado = ""
    img = ""

    if request.method == "POST":

        try:

            if tipo == "dos_puntos":

                x1 = float(request.form.get("x"))
                y1 = float(request.form.get("y"))
                x2 = float(request.form.get("x"))
                y2 = float(request.form.get("y"))

                if x1 == x2:
                    raise ValueError

                m = (y2 - y1) / (x2 - x1)
                b = y1 - m * x1

            else:

                m = float(request.form.get("m"))
                b = float(request.form.get("b"))

            x = -b/m if m != 0 else 0

            resultado = f"x = {x:.2f}"

            fig, ax = grafica_base()

            xs = np.linspace(-10,10,200)
            ax.plot(xs, m*xs + b)

            ax.scatter([x],[0],color="red")

            img = convertir_imagen(fig)

        except:
            resultado = "Datos inválidos"

    html_inputs = """
    <input name="m" placeholder="m">
    <input name="b" placeholder="b">
    """ if tipo=="pendiente" else """
    <input name="x1">
    <input name="y1">
    <input name="x2">
    <input name="y2">
    """

    return render_template_string(f"""
<html>
<head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">

<h2>Ecuación Lineal</h2>

<h2>Las ecuaciones lineales son igualdades matemáticas de primer grado donde las incógnitas tienen exponente 1, representando una línea recta al graficarse.</h2>

<form method="POST">

<select name="tipo" onchange="this.form.submit()">
<option value="pendiente" {"selected" if tipo=="pendiente" else ""}>Pendiente + b</option>
<option value="dos_puntos" {"selected" if tipo=="dos_puntos" else ""}>Dos puntos</option>
</select>

{html_inputs}

<button type="submit">Calcular</button>
<button type="reset">Limpiar</button>

</form>

</div>

<div class="card">
<div class="resultado">{resultado}</div>
<div class="grafica"><img src="data:image/png;base64,{img}"></div>
</div>
<button type="reset">Limpiar</button>
</div>

</body>
</html>
""")

# ================= CUADRATICA =================

@app.route("/cuadratica",methods=["GET","POST"])
def cuadratica():

    img=""
    sol=""

    if request.method=="POST":

        try:

            a = float(request.form.get("a: ej: 2"))
            b = float(request.form.get("b: ej: 8"))
            c = float(request.form.get("c: ej: -10"))

            disc = b**2 - 4*a*c

            if disc < 0:
                sol = "Sin raíces reales"
            else:
                x1 = (-b + np.sqrt(disc)) / (2*a)
                x2 = (-b - np.sqrt(disc)) / (2*a)
                sol = f"x1={x1:.2f}, x2={x2:.2f}"

            fig,ax=grafica_base()
            xs=np.linspace(-10,10,300)
            ax.plot(xs,a*xs**2+b*xs+c)

            img=convertir_imagen(fig)

        except:
            sol="Datos inválidos"

    return render_template_string(f"""
<html>
<head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">
<h2>Cuadrática</h2>

<h2>Una ecuación cuadrática es una ecuación algebraica de segundo grado, es decir, aquella en la que la incógnita (generalmente x) aparece elevada al cuadrado como máximo.</h2>

<form method="POST">
<input name="a">
<input name="b">
<input name="c">
<button>Calcular</button>
<button type="reset">Limpiar</button>
</form>

</div>

<div class="card">
<div class="resultado">{sol}</div>
<div class="grafica"><img src="data:image/png;base64,{img}"></div>
</div>
<button type="reset">Limpiar</button>
</div>

</body>
</html>
""")

# ================= SISTEMA 2X2 =================

@app.route("/sistema2x2",methods=["GET","POST"])
def sistema2x2():

    img=""
    sol=""

    if request.method=="POST":

        try:

            a1=float(request.form.get("a"))
            b1=float(request.form.get("b"))
            c1=float(request.form.get("c"))

            a2=float(request.form.get("a"))
            b2=float(request.form.get("b"))
            c2=float(request.form.get("c"))

            A=np.array([[a1,b1],[a2,b2]])
            B=np.array([c1,c2])

            x,y=np.linalg.solve(A,B)

            sol=f"x={x:.2f}, y={y:.2f}"

            fig,ax=grafica_base()

            xs=np.linspace(-10,10,200)

            ax.plot(xs,(c1-a1*xs)/b1)
            ax.plot(xs,(c2-a2*xs)/b2)

            ax.scatter([x],[y],color="red")

            img=convertir_imagen(fig)

        except:
            sol="Sistema inválido"

    return render_template_string(f"""
<html>
<head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">
<h2>Sistema 2x2</h2>

<h2>Un sistema de ecuaciones 2×2 es un conjunto de dos ecuaciones lineales con dos incógnitas, generalmente x y y, que se deben resolver al mismo tiempo.</h2>

<h2>a1​x + b1​y = c1​​​</h2>
<h2>a2​x + b2​y = c2​​</h2>

<h2>Así como se presentan las ecuaciones favor de meter los datos en ese orden.</h2>

<form method="POST">

<input name="a1"><input name="b1"><input name="c1">
<input name="a2"><input name="b2"><input name="c2">

<button>Resolver</button>
<button type="reset">Limpiar</button>

</form>

</div>

<div class="card">
<div class="resultado">{sol}</div>
<div class="grafica"><img src="data:image/png;base64,{img}"></div>
</div>
<button type="reset">Limpiar</button>
</div>

</body>
</html>
""")

# ================= SISTEMA 3X3 =================

@app.route("/sistema3x3",methods=["GET","POST"])
def sistema3x3():

    sol=""

    if request.method=="POST":

        try:

            A=np.array([
                [float(request.form.get("a")),float(request.form.get("b")),float(request.form.get("c"))],
                [float(request.form.get("a")),float(request.form.get("b")),float(request.form.get("c"))],
                [float(request.form.get("a")),float(request.form.get("b")),float(request.form.get("c"))]
            ])

            B=np.array([
                float(request.form.get("d")),
                float(request.form.get("d")),
                float(request.form.get("d"))
            ])

            x=np.linalg.solve(A,B)

            sol=f"x={x[0]:.2f}, y={x[1]:.2f}, z={x[2]:.2f}"

        except:
            sol="Sistema inválido"

    return render_template_string(f"""
<html>
<head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">
<h2>Sistema 3x3</h2>

<h2>Un sistema de ecuaciones 3×3 es un conjunto de tres ecuaciones lineales con tres incógnitas, normalmente (x), (y) y (z), que se resuelven simultáneamente.</h2>

<h2>​a1​x + b1​y + c1​z = d1​​</h2>
<h2> a2​x + b2​y + c2​z = d2</h2>
<h2>​a3​x + b3​y + c3​z = d3</h2>

<h2>Así como se presentan las ecuaciones favor de meter los datos en ese orden.</h2>

<form method="POST">

<input name="a1"><input name="b1"><input name="c1"><input name="d1">
<input name="a2"><input name="b2"><input name="c2"><input name="d2">
<input name="a3"><input name="b3"><input name="c3"><input name="d3">

<button>Resolver</button>
<button type="reset">Limpiar</button>

</form>

</div>

<div class="card">
<div class="resultado">{sol}</div>
</div>
<button type="reset">Limpiar</button>
</div>

</body>
</html>
""")

# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)
