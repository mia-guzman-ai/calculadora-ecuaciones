from flask import Flask, render_template_string, request
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# ================= FUNCION IMAGEN =================

CHART_COLORS = {
    'bg': '#0f172a',
    'surface': '#1e293b',
    'grid': '#334155',
    'axis': '#64748b',
    'text': '#e2e8f0',
    'accent1': '#60a5fa',
    'accent2': '#a78bfa',
    'accent3': '#34d399',
    'highlight': '#f472b6',
    'warn': '#fbbf24',
}

def convertir_imagen(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png', dpi=200, bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    img.seek(0)
    plt.close(fig)
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

def grafica_base(title="", xlabel="x", ylabel="y"):
    fig, ax = plt.subplots(figsize=(9, 5.5))

    fig.patch.set_facecolor(CHART_COLORS['bg'])
    ax.set_facecolor(CHART_COLORS['surface'])

    for spine in ax.spines.values():
        spine.set_color(CHART_COLORS['grid'])
        spine.set_linewidth(0.8)

    ax.axhline(0, color=CHART_COLORS['axis'], linewidth=1.0, alpha=0.6)
    ax.axvline(0, color=CHART_COLORS['axis'], linewidth=1.0, alpha=0.6)

    ax.grid(True, color=CHART_COLORS['grid'], linewidth=0.4, alpha=0.5, linestyle='--')

    ax.tick_params(colors=CHART_COLORS['text'], labelsize=10, length=4, width=0.6)
    ax.set_xlabel(xlabel, color=CHART_COLORS['text'], fontsize=12, fontweight='bold', labelpad=10)
    ax.set_ylabel(ylabel, color=CHART_COLORS['text'], fontsize=12, fontweight='bold', labelpad=10)

    if title:
        ax.set_title(title, color=CHART_COLORS['text'], fontsize=15, fontweight='bold', pad=15)

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

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

                x1 = float(request.form.get("x1"))
                y1 = float(request.form.get("y1"))
                x2 = float(request.form.get("x2"))
                y2 = float(request.form.get("y2"))

                if x1 == x2:
                    raise ValueError

                m = (y2 - y1) / (x2 - x1)
                b = y1 - m * x1

            else:

                m = float(request.form.get("m"))
                b = float(request.form.get("b"))

            x = -b/m if m != 0 else 0

            resultado = f"x = {x:.2f}"

            fig, ax = grafica_base(title="Ecuación Lineal", ylabel="f(x)")

            xs = np.linspace(-10, 10, 400)
            ys = m * xs + b

            ax.plot(xs, ys, color=CHART_COLORS['accent1'], linewidth=2.5,
                    label=f'y = {m:.1f}x + {b:.1f}', zorder=3)
            ax.fill_between(xs, ys, alpha=0.08, color=CHART_COLORS['accent1'])

            ax.scatter([x], [0], color=CHART_COLORS['highlight'], s=120,
                       zorder=5, edgecolors='white', linewidths=1.5,
                       label=f'Raíz x = {x:.2f}')
            ax.annotate(f'({x:.2f}, 0)', (x, 0), textcoords='offset points',
                        xytext=(12, 14), fontsize=10, color=CHART_COLORS['highlight'],
                        fontweight='bold',
                        arrowprops=dict(arrowstyle='->', color=CHART_COLORS['highlight'],
                                        lw=1.5))

            ax.legend(loc='upper left', fontsize=10, facecolor=CHART_COLORS['surface'],
                      edgecolor=CHART_COLORS['grid'], labelcolor=CHART_COLORS['text'],
                      framealpha=0.9)

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

            a = float(request.form.get("a"))
            b = float(request.form.get("b"))
            c = float(request.form.get("c"))

            disc = b**2 - 4*a*c

            if disc < 0:
                sol = "Sin raíces reales"
            else:
                x1 = (-b + np.sqrt(disc)) / (2*a)
                x2 = (-b - np.sqrt(disc)) / (2*a)
                sol = f"x1={x1:.2f}, x2={x2:.2f}"

            fig, ax = grafica_base(title="Ecuación Cuadrática", ylabel="f(x)")
            xs = np.linspace(-10, 10, 400)
            ys = a * xs**2 + b * xs + c

            ax.plot(xs, ys, color=CHART_COLORS['accent2'], linewidth=2.5,
                    label=f'f(x) = {a:.1f}x² + {b:.1f}x + {c:.1f}', zorder=3)
            ax.fill_between(xs, ys, alpha=0.10, color=CHART_COLORS['accent2'])

            vx = -b / (2 * a)
            vy = a * vx**2 + b * vx + c
            ax.scatter([vx], [vy], color=CHART_COLORS['warn'], s=100,
                       zorder=5, edgecolors='white', linewidths=1.5, marker='D',
                       label=f'Vértice ({vx:.2f}, {vy:.2f})')

            if disc >= 0:
                roots_x = [x1]
                if abs(x1 - x2) > 1e-9:
                    roots_x.append(x2)
                ax.scatter(roots_x, [0]*len(roots_x), color=CHART_COLORS['highlight'],
                           s=120, zorder=5, edgecolors='white', linewidths=1.5,
                           label='Raíces')
                for rx in roots_x:
                    ax.annotate(f'({rx:.2f}, 0)', (rx, 0), textcoords='offset points',
                                xytext=(10, 14), fontsize=9, color=CHART_COLORS['highlight'],
                                fontweight='bold',
                                arrowprops=dict(arrowstyle='->', color=CHART_COLORS['highlight'],
                                                lw=1.5))

            ax.legend(loc='upper left', fontsize=9, facecolor=CHART_COLORS['surface'],
                      edgecolor=CHART_COLORS['grid'], labelcolor=CHART_COLORS['text'],
                      framealpha=0.9)

            img = convertir_imagen(fig)

        except:
            sol="Datos inválidos"

    return render_template_string(f"""
<html>
<head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">
<h2>Cuadrática</h2>

<h2>Una ecuación cuadrática es una ecuación algebraica de segundo grado...</h2>

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

            a1=float(request.form.get("a1"))
            b1=float(request.form.get("b1"))
            c1=float(request.form.get("c1"))

            a2=float(request.form.get("a2"))
            b2=float(request.form.get("b2"))
            c2=float(request.form.get("c2"))

            A=np.array([[a1,b1],[a2,b2]])
            B=np.array([c1,c2])

            x,y=np.linalg.solve(A,B)

            sol=f"x={x:.2f}, y={y:.2f}"

            fig, ax = grafica_base(title="Sistema de Ecuaciones 2×2", ylabel="y")

            xs = np.linspace(-10, 10, 400)

            ax.plot(xs, (c1 - a1 * xs) / b1, color=CHART_COLORS['accent1'],
                    linewidth=2.5, label=f'{a1:.0f}x + {b1:.0f}y = {c1:.0f}', zorder=3)
            ax.plot(xs, (c2 - a2 * xs) / b2, color=CHART_COLORS['accent3'],
                    linewidth=2.5, label=f'{a2:.0f}x + {b2:.0f}y = {c2:.0f}', zorder=3)

            ax.scatter([x], [y], color=CHART_COLORS['highlight'], s=150,
                       zorder=5, edgecolors='white', linewidths=2,
                       label=f'Solución ({x:.2f}, {y:.2f})')
            ax.annotate(f'({x:.2f}, {y:.2f})', (x, y), textcoords='offset points',
                        xytext=(14, 14), fontsize=10, color=CHART_COLORS['highlight'],
                        fontweight='bold',
                        arrowprops=dict(arrowstyle='->', color=CHART_COLORS['highlight'],
                                        lw=1.5))

            ax.legend(loc='upper left', fontsize=9, facecolor=CHART_COLORS['surface'],
                      edgecolor=CHART_COLORS['grid'], labelcolor=CHART_COLORS['text'],
                      framealpha=0.9)

            img = convertir_imagen(fig)

        except:
            sol="Sistema inválido"

    return render_template_string(f"""
<html>
<head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">
<h2>Sistema 2x2</h2>

<h2>Un sistema de ecuaciones 2×2...</h2>

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
                [float(request.form.get("a1")),float(request.form.get("b1")),float(request.form.get("c1"))],
                [float(request.form.get("a2")),float(request.form.get("b2")),float(request.form.get("c2"))],
                [float(request.form.get("a3")),float(request.form.get("b3")),float(request.form.get("c3"))]
            ])

            B=np.array([
                float(request.form.get("d1")),
                float(request.form.get("d2")),
                float(request.form.get("d3"))
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

<h2>Un sistema de ecuaciones 3×3...</h2>

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
