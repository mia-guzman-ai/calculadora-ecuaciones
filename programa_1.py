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

ESTILO = """TU CSS EXACTO SIN CAMBIOS"""

# ================= MENU =================

MENU = """TU MENU EXACTO SIN CAMBIOS"""

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
""")

# ================= LINEAL =================

@app.route("/lineal", methods=["GET","POST"])
def lineal():

    tipo = request.form.get("tipo","pendiente")

    resultado = ""
    img = ""

    # mantener valores (ARREGLA QUE SE BORRAN)
    m_val = fget("m","")
    b_val = fget("b","")
    x1_val = fget("x1","")
    y1_val = fget("y1","")
    x2_val = fget("x2","")
    y2_val = fget("y2","")

    if request.method == "POST":

        try:

            if tipo == "dos_puntos":

                x1 = float(x1_val)
                y1 = float(y1_val)
                x2 = float(x2_val)
                y2 = float(y2_val)

                if x1 == x2:
                    resultado = "Error: x1 = x2"
                else:
                    m = (y2 - y1) / (x2 - x1)
                    b = y1 - m * x1

                    x = -b/m if m != 0 else 0
                    resultado = f"x = {x:.2f}"

                    fig, ax = grafica_base()
                    xs = np.linspace(-10,10,200)
                    ax.plot(xs, m*xs + b)
                    ax.scatter([x],[0],color="red")
                    img = convertir_imagen(fig)

            else:

                m = float(m_val)
                b = float(b_val)

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
    <input name="m" placeholder="m" value="{m_val}">
    <input name="b" placeholder="b" value="{b_val}">
    """ if tipo=="pendiente" else f"""
    <input name="x1" placeholder="x1" value="{x1_val}">
    <input name="y1" placeholder="y1" value="{y1_val}">
    <input name="x2" placeholder="x2" value="{x2_val}">
    <input name="y2" placeholder="y2" value="{y2_val}">
    """

    return render_template_string(f"""
<html>
<head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">

<h2>Ecuación Lineal</h2>

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

</div>

</body>
</html>
""")

# ================= CUADRATICA =================

@app.route("/cuadratica",methods=["GET","POST"])
def cuadratica():

    a_val = fget("a","")
    b_val = fget("b","")
    c_val = fget("c","")

    sol = ""
    img = ""

    if request.method=="POST":
        try:

            a = float(a_val)
            b = float(b_val)
            c = float(c_val)

            if a == 0:
                sol = "No es cuadrática"
            else:
                disc = b**2 - 4*a*c

                if disc < 0:
                    sol = "Sin raíces reales"
                else:
                    x1 = (-b + np.sqrt(disc)) / (2*a)
                    x2 = (-b - np.sqrt(disc)) / (2*a)
                    sol = f"x1={x1:.2f}, x2={x2:.2f}"

                fig, ax = grafica_base()
                xs = np.linspace(-10,10,300)
                ax.plot(xs, a*xs**2 + b*xs + c)
                img = convertir_imagen(fig)

        except:
            sol = "Datos inválidos"

    return render_template_string(f"""
<html>
<head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">

<h2>Cuadrática</h2>

<form method="POST">
<input name="a" value="{a_val}">
<input name="b" value="{b_val}">
<input name="c" value="{c_val}">
<button>Calcular</button>
<button type="reset">Limpiar</button>
</form>

</div>

<div class="card">
<div class="resultado">{sol}</div>
<div class="grafica"><img src="data:image/png;base64,{img}"></div>
</div>

</div>

</body>
</html>
""")

# ================= SISTEMA 2X2 =================

@app.route("/sistema2x2",methods=["GET","POST"])
def sistema2x2():

    vals = {k: fget(k,"") for k in ["a1","b1","c1","a2","b2","c2"]}

    sol = ""
    img = ""

    if request.method=="POST":
        try:

            a1 = float(vals["a1"])
            b1 = float(vals["b1"])
            c1 = float(vals["c1"])
            a2 = float(vals["a2"])
            b2 = float(vals["b2"])
            c2 = float(vals["c2"])

            A = np.array([[a1,b1],[a2,b2]])
            B = np.array([c1,c2])

            x,y = np.linalg.solve(A,B)
            sol = f"x={x:.2f}, y={y:.2f}"

            fig, ax = grafica_base()
            xs = np.linspace(-10,10,200)

            if b1 != 0:
                ax.plot(xs,(c1-a1*xs)/b1)
            if b2 != 0:
                ax.plot(xs,(c2-a2*xs)/b2)

            ax.scatter([x],[y],color="red")
            img = convertir_imagen(fig)

        except:
            sol = "Sistema inválido"

    return render_template_string(f"""
<html>
<head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">

<h2>Sistema 2x2</h2>

<form method="POST">

<input name="a1" value="{vals['a1']}">
<input name="b1" value="{vals['b1']}">
<input name="c1" value="{vals['c1']}">
<input name="a2" value="{vals['a2']}">
<input name="b2" value="{vals['b2']}">
<input name="c2" value="{vals['c2']}">

<button>Resolver</button>
<button type="reset">Limpiar</button>

</form>

</div>

<div class="card">
<div class="resultado">{sol}</div>
<div class="grafica"><img src="data:image/png;base64,{img}"></div>
</div>

</div>

</body>
</html>
""")

# ================= SISTEMA 3X3 =================

@app.route("/sistema3x3",methods=["GET","POST"])
def sistema3x3():

    vals = {k: fget(k,"") for k in ["a1","b1","c1","d1","a2","b2","c2","d2","a3","b3","c3","d3"]}

    sol = ""

    if request.method=="POST":
        try:

            A = np.array([
                [float(vals["a1"]),float(vals["b1"]),float(vals["c1"])],
                [float(vals["a2"]),float(vals["b2"]),float(vals["c2"])],
                [float(vals["a3"]),float(vals["b3"]),float(vals["c3"])]
            ])

            B = np.array([
                float(vals["d1"]),
                float(vals["d2"]),
                float(vals["d3"])
            ])

            x = np.linalg.solve(A,B)

            sol = f"x={x[0]:.2f}, y={x[1]:.2f}, z={x[2]:.2f}"

        except:
            sol = "Sistema inválido"

    return render_template_string(f"""
<html>
<head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">

<h2>Sistema 3x3</h2>

<form method="POST">

<input name="a1" value="{vals['a1']}">
<input name="b1" value="{vals['b1']}">
<input name="c1" value="{vals['c1']}">
<input name="d1" value="{vals['d1']}">

<input name="a2" value="{vals['a2']}">
<input name="b2" value="{vals['b2']}">
<input name="c2" value="{vals['c2']}">
<input name="d2" value="{vals['d2']}">

<input name="a3" value="{vals['a3']}">
<input name="b3" value="{vals['b3']}">
<input name="c3" value="{vals['c3']}">
<input name="d3" value="{vals['d3']}">

<button>Resolver</button>
<button type="reset">Limpiar</button>

</form>

</div>

<div class="card">
<div class="resultado">{sol}</div>
</div>

</div>

</body>
</html>
""")

# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)

