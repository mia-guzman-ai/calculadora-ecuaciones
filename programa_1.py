from flask import Flask, render_template_string, request
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64

app = Flask(__name__)

# ================= IMAGEN =================

def convertir_imagen(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

# ================= ESTILO =================

ESTILO = """<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

*{margin:0;padding:0;box-sizing:border-box;font-family:Poppins}

body{
background:radial-gradient(circle,#1e3a8a,#020617);
color:white;
}

.sidebar{
position:fixed;width:270px;height:100vh;
background:rgba(15,23,42,0.95);
padding:25px;
}

.sidebar a{
display:block;padding:14px;margin:10px 0;
background:rgba(255,255,255,0.05);
border-radius:12px;color:white;text-decoration:none;
}

.main{margin-left:290px;padding:30px;}

.card{
background:rgba(255,255,255,0.07);
padding:25px;border-radius:20px;margin-bottom:20px;
}

input,select{
width:100%;padding:12px;margin-top:10px;
border-radius:10px;border:none;
}

button{
padding:12px;border:none;border-radius:12px;
background:#2563eb;color:white;font-weight:bold;
cursor:pointer;margin-top:10px;
}

.grafica img{width:100%;border-radius:12px;}

.resultado{font-size:22px;color:#7dd3fc;font-weight:bold;}
</style>"""

# ================= MENU =================

MENU = """
<div class="sidebar">
<h2>Math App</h2>
<a href="/">Inicio</a>
<a href="/lineal">Lineal</a>
<a href="/cuadratica">Cuadrática</a>
<a href="/sistema2x2">Sistema 2x2</a>
<a href="/sistema3x3">Sistema 3x3</a>
</div>
"""

# ================= GRAFICA =================

def grafica_base():
    fig, ax = plt.subplots(figsize=(7,5))
    ax.set_facecolor("white")
    ax.grid(True)
    ax.axhline(0,color="black")
    ax.axvline(0,color="black")
    return fig, ax

# ================= HOME =================

@app.route("/")
def home():
    return render_template_string(f"""
<html><head>{ESTILO}</head>
<body>{MENU}
<div class="main">
<div class="card">
<h1>Math App</h1>
<p>Plataforma matemática interactiva mejorada</p>
</div>
</div>
</body></html>
""")

# ================= LINEAL =================

@app.route("/lineal", methods=["GET","POST"])
def lineal():

    tipo = request.form.get("tipo","pendiente")

    x1=x2=y1=y2=m=b=x=y=None

    img=""

    if request.method=="POST":

        if tipo=="dos_puntos":
            x1=float(request.form["x1"])
            y1=float(request.form["y1"])
            x2=float(request.form["x2"])
            y2=float(request.form["y2"])

            m=(y2-y1)/(x2-x1)
            b=y1-m*x1

        else:
            m=float(request.form["m"])
            b=float(request.form["b"])

        x=-b/m

        fig,ax=grafica_base()
        xs=np.linspace(-10,10,100)
        ax.plot(xs,m*xs+b)
        ax.scatter([x],[0],color="red")

        img=convertir_imagen(fig)

    return render_template_string(f"""
<html><head>{ESTILO}</head>
<body>{MENU}
<div class="main">

<div class="card">
<h2>Lineal</h2>

<form method="POST">

<select name="tipo" onchange="this.form.submit()">
<option value="pendiente" {"selected" if tipo=="pendiente" else ""}>Pendiente + Intersección</option>
<option value="dos_puntos" {"selected" if tipo=="dos_puntos" else ""}>Dos puntos</option>
</select>

{""
if tipo=="pendiente" else
'''
<input name="x1" placeholder="x1">
<input name="y1" placeholder="y1">
<input name="x2" placeholder="x2">
<input name="y2" placeholder="y2">
'''
}

{""
if tipo!="pendiente" else
'''
<input name="m" placeholder="pendiente m">
<input name="b" placeholder="intersección b">
'''
}

<button type="submit">Calcular</button>
<button type="reset">Limpiar</button>

</form>

</div>

<div class="card">
<div class="resultado">{x if x else ""}</div>
<div class="grafica"><img src="data:image/png;base64,{img}"></div>
</div>

</div>
</body></html>
""")

# ================= CUADRATICA =================

@app.route("/cuadratica",methods=["GET","POST"])
def cuadratica():

    img=""
    x_sol=None

    if request.method=="POST":

        a=float(request.form["a"])
        b=float(request.form["b"])
        c=float(request.form["c"])

        disc=b**2-4*a*c
        x_sol=(-b+np.sqrt(disc))/(2*a)

        fig,ax=grafica_base()
        xs=np.linspace(-10,10,200)
        ax.plot(xs,a*xs**2+b*xs+c)
        img=convertir_imagen(fig)

    return render_template_string(f"""
<html><head>{ESTILO}</head>
<body>{MENU}
<div class="main">

<div class="card">
<h2>Cuadrática</h2>
<form method="POST">

<input name="a" placeholder="a">
<input name="b" placeholder="b">
<input name="c" placeholder="c">

<button>Calcular</button>
<button type="reset">Limpiar</button>

</form>
</div>

<div class="card">
<div class="resultado">{x_sol if x_sol else ""}</div>
<div class="grafica"><img src="data:image/png;base64,{img}"></div>
</div>

</div>
</body></html>
""")

# ================= SISTEMA 2X2 =================

@app.route("/sistema2x2",methods=["GET","POST"])
def sistema2x2():

    img=""
    sol=""

    if request.method=="POST":

        a1,b1,c1=float(request.form["a1"]),float(request.form["b1"]),float(request.form["c1"])
        a2,b2,c2=float(request.form["a2"]),float(request.form["b2"]),float(request.form["c2"])

        A=np.array([[a1,b1],[a2,b2]])
        B=np.array([c1,c2])

        x,y=np.linalg.solve(A,B)
        sol=f"x={x:.2f}, y={y:.2f}"

        fig,ax=grafica_base()

        xs=np.linspace(-10,10,100)
        ax.plot(xs,(c1-a1*xs)/b1)
        ax.plot(xs,(c2-a2*xs)/b2)
        ax.scatter([x],[y],color="red")

        img=convertir_imagen(fig)

    return render_template_string(f"""
<html><head>{ESTILO}</head>
<body>{MENU}
<div class="main">

<div class="card">
<h2>Sistema 2x2</h2>

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

</div>
</body></html>
""")

# ================= SISTEMA 3X3 =================

@app.route("/sistema3x3",methods=["GET","POST"])
def sistema3x3():

    sol=""

    if request.method=="POST":

        A=np.array([
            [float(request.form["a1"]),float(request.form["b1"]),float(request.form["c1"])],
            [float(request.form["a2"]),float(request.form["b2"]),float(request.form["c2"])],
            [float(request.form["a3"]),float(request.form["b3"]),float(request.form["c3"])]
        ])

        B=np.array([
            float(request.form["d1"]),
            float(request.form["d2"]),
            float(request.form["d3"])
        ])

        x=np.linalg.solve(A,B)
        sol=f"x={x[0]:.2f}, y={x[1]:.2f}, z={x[2]:.2f}"

    return render_template_string(f"""
<html><head>{ESTILO}</head>
<body>{MENU}
<div class="main">

<div class="card">
<h2>Sistema 3x3</h2>

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

</div>
</body></html>
""")

# ================= RUN =================

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)
