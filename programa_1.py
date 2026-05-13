from flask import Flask, render_template_string, request
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# ================= IMAGEN =================

def convertir_imagen(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

# ================= SEGURIDAD =================

def fget(key, default=""):
    val = request.form.get(key)
    return val if val not in [None,""] else default

# ================= ESTILO (NO TOCADO) =================

ESTILO = """ TU CSS EXACTO (NO SE TOCA) """

MENU = """ TU MENU EXACTO (NO SE TOCA) """

# ================= GRAFICA =================

def grafica_base():
    fig, ax = plt.subplots(figsize=(8,5))
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
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
<html><head>{ESTILO}</head>
<body>{MENU}
<div class="main">
<div class="card">
<h1>Bienvenido 👋</h1>
<p>Plataforma matemática funcional</p>
</div>
</div>
</body></html>
""")

# ================= LINEAL (MEJORADO) =================

@app.route("/lineal", methods=["GET","POST"])
def lineal():

    tipo = request.form.get("tipo","pendiente")

    m = fget("m")
    b = fget("b")
    x1 = fget("x1")
    y1 = fget("y1")
    x2 = fget("x2")
    y2 = fget("y2")

    resultado = ""
    img = ""

    if request.method == "POST":

        try:
            if tipo == "dos_puntos":
                x1f, y1f = float(x1), float(y1)
                x2f, y2f = float(x2), float(y2)

                m_calc = (y2f - y1f) / (x2f - x1f)
                b_calc = y1f - m_calc * x1f

            else:
                m_calc = float(m)
                b_calc = float(b)

            x_sol = -b_calc / m_calc if m_calc != 0 else 0
            resultado = f"x = {x_sol:.2f}"

            fig, ax = grafica_base()
            xs = np.linspace(-10,10,200)
            ax.plot(xs, m_calc*xs + b_calc)
            ax.scatter([x_sol],[0],color="red")

            img = convertir_imagen(fig)

        except:
            resultado = "Datos inválidos"

    return render_template_string(f"""
<html><head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">
<h2>Ecuación Lineal</h2>

<form method="POST">

<select name="tipo">
<option value="pendiente" {"selected" if tipo=="pendiente" else ""}>Pendiente + b</option>
<option value="dos_puntos" {"selected" if tipo=="dos_puntos" else ""}>Dos puntos</option>
</select>

{""
if tipo=="dos_puntos" else
f'''
<input name="m" placeholder="Pendiente (m)" value="{m}">
<input name="b" placeholder="Intersección (b)" value="{b}">
'''
}

{""
if tipo!="dos_puntos" else
f'''
<input name="x1" placeholder="x1" value="{x1}">
<input name="y1" placeholder="y1" value="{y1}">
<input name="x2" placeholder="x2" value="{x2}">
<input name="y2" placeholder="y2" value="{y2}">
'''
}

<button type="submit">Calcular</button>
<button type="reset" onclick="window.location.reload()">Limpiar</button>

</form>

</div>

<div class="card">
<div class="resultado">{resultado}</div>
<div class="grafica"><img src="data:image/png;base64,{img}"></div>
</div>

</div>

</body></html>
""")

# ================= CUADRATICA (MEJORADA) =================

@app.route("/cuadratica",methods=["GET","POST"])
def cuadratica():

    a=fget("a")
    b=fget("b")
    c=fget("c")

    sol=""
    img=""

    if request.method=="POST":
        try:
            a1,b1,c1=float(a),float(b),float(c)

            disc=b1**2-4*a1*c1

            if disc<0:
                sol="Sin raíces reales"
            else:
                x1=(-b1+np.sqrt(disc))/(2*a1)
                x2=(-b1-np.sqrt(disc))/(2*a1)
                sol=f"x1={x1:.2f}, x2={x2:.2f}"

            fig,ax=grafica_base()
            xs=np.linspace(-10,10,300)
            ax.plot(xs,a1*xs**2+b1*xs+c1)
            img=convertir_imagen(fig)

        except:
            sol="Datos inválidos"

    return render_template_string(f"""
<html><head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">
<h2>Cuadrática</h2>

<form method="POST">

<input name="a" placeholder="Coeficiente a" value="{a}">
<input name="b" placeholder="Coeficiente b" value="{b}">
<input name="c" placeholder="Coeficiente c" value="{c}">

<button>Calcular</button>
<button type="reset" onclick="window.location.reload()">Limpiar</button>

</form>

</div>

<div class="card">
<div class="resultado">{sol}</div>
<div class="grafica"><img src="data:image/png;base64,{img}"></div>
</div>

</div>

</body></html>
""")

# ================= SISTEMA 2X2 (MEJORADO) =================

@app.route("/sistema2x2",methods=["GET","POST"])
def sistema2x2():

    sol=""
    img=""

    vals = {k:fget(k) for k in ["a1","b1","c1","a2","b2","c2"]}

    if request.method=="POST":
        try:
            a1,b1,c1 = float(vals["a1"]),float(vals["b1"]),float(vals["c1"])
            a2,b2,c2 = float(vals["a2"]),float(vals["b2"]),float(vals["c2"])

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
<html><head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">
<h2>Sistema 2x2</h2>

<form method="POST">

<input name="a1" placeholder="a1" value="{vals['a1']}">
<input name="b1" placeholder="b1" value="{vals['b1']}">
<input name="c1" placeholder="c1" value="{vals['c1']}">

<input name="a2" placeholder="a2" value="{vals['a2']}">
<input name="b2" placeholder="b2" value="{vals['b2']}">
<input name="c2" placeholder="c2" value="{vals['c2']}">

<button>Resolver</button>
<button type="reset" onclick="window.location.reload()">Limpiar</button>

</form>

</div>

<div class="card">
<div class="resultado">{sol}</div>
<div class="grafica"><img src="data:image/png;base64,{img}"></div>
</div>

</div>

</body></html>
""")

# ================= SISTEMA 3X3 (MEJORADO) =================

@app.route("/sistema3x3",methods=["GET","POST"])
def sistema3x3():

    sol=""

    vals={k:fget(k) for k in ["a1","b1","c1","d1","a2","b2","c2","d2","a3","b3","c3","d3"]}

    if request.method=="POST":
        try:

            A=np.array([
                [float(vals["a1"]),float(vals["b1"]),float(vals["c1"])],
                [float(vals["a2"]),float(vals["b2"]),float(vals["c2"])],
                [float(vals["a3"]),float(vals["b3"]),float(vals["c3"])]
            ])

            B=np.array([float(vals["d1"]),float(vals["d2"]),float(vals["d3"])])

            x=np.linalg.solve(A,B)

            sol=f"x={x[0]:.2f}, y={x[1]:.2f}, z={x[2]:.2f}"

        except:
            sol="Sistema inválido"

    return render_template_string(f"""
<html><head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">
<h2>Sistema 3x3</h2>

<form method="POST">

<input name="a1" placeholder="a1" value="{vals['a1']}">
<input name="b1" placeholder="b1" value="{vals['b1']}">
<input name="c1" placeholder="c1" value="{vals['c1']}">
<input name="d1" placeholder="d1" value="{vals['d1']}">

<input name="a2" placeholder="a2" value="{vals['a2']}">
<input name="b2" placeholder="b2" value="{vals['b2']}">
<input name="c2" placeholder="c2" value="{vals['c2']}">
<input name="d2" placeholder="d2" value="{vals['d2']}">

<input name="a3" placeholder="a3" value="{vals['a3']}">
<input name="b3" placeholder="b3" value="{vals['b3']}">
<input name="c3" placeholder="c3" value="{vals['c3']}">
<input name="d3" placeholder="d3" value="{vals['d3']}">

<button>Resolver</button>
<button type="reset" onclick="window.location.reload()">Limpiar</button>

</form>

</div>

<div class="card">
<div class="resultado">{sol}</div>
</div>

</div>

</body></html>
""")

# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)
