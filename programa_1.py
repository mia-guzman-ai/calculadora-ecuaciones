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

# ================= ESTILO =================

ESTILO = """<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:'Poppins',sans-serif;
}

body{
    background: radial-gradient(circle at top left,#1e3a8a,#020617 70%);
    color:white;
    overflow-x:hidden;
}

.sidebar{
    position:fixed;
    width:270px;
    height:100vh;
    background:rgba(15,23,42,0.95);
    backdrop-filter:blur(15px);
    padding:25px;
    border-right:1px solid rgba(255,255,255,0.1);
}

.logo{text-align:center;margin-bottom:40px;}
.logo h1{color:#60a5fa;font-size:32px;}
.logo p{color:#94a3b8;font-size:14px;}

.sidebar a{
    display:block;
    padding:16px;
    margin-bottom:12px;
    border-radius:14px;
    text-decoration:none;
    color:white;
    background:rgba(255,255,255,0.03);
}

.sidebar a:hover{
    background:linear-gradient(135deg,#2563eb,#3b82f6);
}

.main{margin-left:290px;padding:40px;}

.card{
    background:rgba(255,255,255,0.06);
    border-radius:25px;
    padding:35px;
    margin-bottom:35px;
}

.resultado{font-size:28px;color:#7dd3fc;}

.grafica img{width:100%;}
</style>
"""

# ================= MENU =================

MENU = """
<div class="sidebar">
<div class="logo">
<h1>Math App</h1>
<p>Matemática Interactiva</p>
</div>
<a href="/">Inicio</a>
<a href="/lineal">Lineal</a>
<a href="/cuadratica">Cuadrática</a>
<a href="/sistema2x2">2x2</a>
<a href="/sistema3x3">3x3</a>
</div>
"""

# ================= GRAFICA =================

def grafica_base():
    fig, ax = plt.subplots(figsize=(8,5))
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
<html><head>{ESTILO}</head><body>{MENU}
<div class="main">
<div class="card">
<h1>Bienvenido</h1>
<p>App matemática interactiva</p>
</div>
</div>
</body></html>
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

                m = (y2-y1)/(x2-x1)
                b = y1 - m*x1
            else:
                m = float(request.form.get("m"))
                b = float(request.form.get("b"))

            x = -b/m if m != 0 else 0
            resultado = f"x = {x:.2f}"

            fig,ax = grafica_base()
            xs = np.linspace(-10,10,200)

            ax.plot(xs,m*xs+b)
            ax.scatter([x],[0],color="red")

            img = convertir_imagen(fig)

        except:
            resultado = "Error"

    inputs = """
    <input name="m">
    <input name="b">
    """ if tipo=="pendiente" else """
    <input name="x1">
    <input name="y1">
    <input name="x2">
    <input name="y2">
    """

    return render_template_string(f"""
<html><head>{ESTILO}</head><body>{MENU}
<div class="main">

<div class="card">
<form method="POST">
<select name="tipo" onchange="this.form.submit()">
<option value="pendiente" {"selected" if tipo=="pendiente" else ""}>Pendiente</option>
<option value="dos_puntos" {"selected" if tipo=="dos_puntos" else ""}>Dos puntos</option>
</select>

{inputs}

<button>Calcular</button>
</form>
</div>

<div class="card">
<div class="resultado">{resultado}</div>
<div class="grafica"><img src="data:image/png;base64,{img}"></div>
</div>

</div>
</body></html>
""")

# ================= CUADRATICA =================

@app.route("/cuadratica",methods=["GET","POST"])
def cuadratica():

    sol=""
    img=""

    if request.method=="POST":
        try:
            a=float(request.form.get("a"))
            b=float(request.form.get("b"))
            c=float(request.form.get("c"))

            disc=b**2-4*a*c

            if disc>=0:
                x1=(-b+np.sqrt(disc))/(2*a)
                x2=(-b-np.sqrt(disc))/(2*a)
                sol=f"x1={x1:.2f}, x2={x2:.2f}"
            else:
                sol="Sin reales"

            fig,ax=grafica_base()
            xs=np.linspace(-10,10,300)
            ax.plot(xs,a*xs**2+b*xs+c)

            img=convertir_imagen(fig)

        except:
            sol="Error"

    return render_template_string(f"""
<html><head>{ESTILO}</head><body>{MENU}
<div class="main">

<div class="card">
<form method="POST">
<input name="a">
<input name="b">
<input name="c">
<button>Calcular</button>
</form>
</div>

<div class="card">
<div class="resultado">{sol}</div>
<div class="grafica"><img src="data:image/png;base64,{img}"></div>
</div>

</div>
</body></html>
""")

# ================= 2X2 =================

@app.route("/sistema2x2",methods=["GET","POST"])
def sistema2x2():

    sol=""
    img=""

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

            fig,ax=grafica_base()
            xs=np.linspace(-10,10,200)

            ax.plot(xs,(c1-a1*xs)/b1)
            ax.plot(xs,(c2-a2*xs)/b2)
            ax.scatter([x],[y],color="red")

            img=convertir_imagen(fig)

        except:
            sol="Error"

    return render_template_string(f"""
<html><head>{ESTILO}</head><body>{MENU}
<div class="main">

<div class="card">
<form method="POST">
<input name="a1"><input name="b1"><input name="c1">
<input name="a2"><input name="b2"><input name="c2">
<button>Resolver</button>
</form>
</div>

<div class="card">
<div class="resultado">{sol}</div>
<div class="grafica"><img src="data:image/png;base64,{img}"></div>
</div>

</div>
</body></html>
""")

# ================= 3X3 =================

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
            sol="Error"

    return render_template_string(f"""
<html><head>{ESTILO}</head><body>{MENU}
<div class="main">

<div class="card">
<form method="POST">
<input name="a1"><input name="b1"><input name="c1"><input name="d1">
<input name="a2"><input name="b2"><input name="c2"><input name="d2">
<input name="a3"><input name="b3"><input name="c3"><input name="d3">
<button>Resolver</button>
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
