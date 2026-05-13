from flask import Flask, render_template_string, request
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64

app = Flask(__name__)

# ================= GRAFICA BASE =================

def fig_to_img(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight', facecolor='white')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

def geo_style():
    fig, ax = plt.subplots(figsize=(7,5))
    ax.set_facecolor("white")

    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")

    ax.grid(True, linestyle="--", alpha=0.4)
    ax.set_xlim(-10,10)
    ax.set_ylim(-10,10)

    return fig, ax

# ================= ESTILO =================

STYLE = """
<style>
body{
    margin:0;
    font-family:Arial;
    background:#0b1b33;
    color:white;
}

.sidebar{
    position:fixed;
    width:250px;
    height:100vh;
    background:#081427;
    padding:20px;
}

.sidebar a{
    display:block;
    padding:12px;
    color:white;
    text-decoration:none;
    margin-bottom:10px;
    background:#0f2a4d;
    border-radius:8px;
}

.sidebar a:hover{background:#1d4e89;}

.main{
    margin-left:270px;
    padding:30px;
}

.card{
    background:#122a4a;
    padding:20px;
    border-radius:12px;
    margin-bottom:20px;
}

input,select{
    width:100%;
    padding:10px;
    margin-top:8px;
    border-radius:6px;
    border:none;
}

button{
    margin-top:10px;
    padding:10px;
    width:48%;
    border:none;
    border-radius:6px;
    background:#1d4e89;
    color:white;
}

button:hover{background:#2563eb;}

.flex{
    display:flex;
    gap:10px;
}

img{
    width:100%;
    border-radius:10px;
    margin-top:10px;
}
</style>
"""

MENU = """
<div class="sidebar">
<h2>Math App</h2>
<a href="/">Inicio</a>
<a href="/lineal">Lineal</a>
<a href="/cuadratica">Cuadrática</a>
<a href="/sistema2x2">2x2</a>
<a href="/sistema3x3">3x3</a>
</div>
"""

# ================= HOME =================

@app.route("/")
def home():
    return render_template_string(f"""
    <html><head>{STYLE}</head>
    <body>{MENU}
    <div class="main">
        <div class="card">
            <h1>Bienvenido</h1>
            <p>App matemática profesional con gráficas tipo GeoGebra</p>
        </div>
    </div></body></html>
    """)

# ================= LINEAL =================

@app.route("/lineal", methods=["GET","POST"])
def lineal():

    result = graph = None

    if request.method == "POST":

        tipo = request.form["tipo"]

        if tipo == "ab":

            a = float(request.form["a"])
            b = float(request.form["b"])

            if a == 0:
                result = "a no puede ser 0"
            else:
                x = -b/a
                result = f"x = {x:.2f}"

                fig, ax = geo_style()
                xs = np.linspace(-10,10,200)
                ys = a*xs + b

                ax.plot(xs, ys)
                ax.scatter([x],[0],color="red")

                graph = fig_to_img(fig)

    return render_template_string(f"""
    <html><head>{STYLE}</head>
    <body>{MENU}
    <div class="main">

    <div class="card">
    <h2>Lineal</h2>

    <form method="POST">

    <select name="tipo" onchange="this.form.submit()">
        <option value="">Tipo de datos</option>
        <option value="ab">Tengo a y b</option>
    </select>

    <input name="a" placeholder="a">
    <input name="b" placeholder="b">

    <div class="flex">
        <button type="submit">Calcular</button>
        <button type="reset">Limpiar</button>
    </div>

    </form>

    <h3>{result if result else ""}</h3>

    </div>

    {f'<div class="card"><img src="data:image/png;base64,{graph}"></div>' if graph else ""}

    </div></body></html>
    """)

# ================= CUADRATICA =================

@app.route("/cuadratica", methods=["GET","POST"])
def cuadratica():

    result = graph = None

    if request.method == "POST":

        a = float(request.form["a"])
        b = float(request.form["b"])
        c = float(request.form["c"])

        d = b**2 - 4*a*c

        if d >= 0:

            x1 = (-b + np.sqrt(d))/(2*a)
            x2 = (-b - np.sqrt(d))/(2*a)

            result = f"x1={x1:.2f} | x2={x2:.2f}"

            fig, ax = geo_style()

            xs = np.linspace(-10,10,300)
            ys = a*xs**2 + b*xs + c

            ax.plot(xs, ys)
            ax.scatter([x1,x2],[0,0],color="red")

            graph = fig_to_img(fig)

        else:
            result = "Sin raíces reales"

    return render_template_string(f"""
    <html><head>{STYLE}</head>
    <body>{MENU}
    <div class="main">

    <div class="card">
    <h2>Cuadrática</h2>

    <form method="POST">

    <input name="a" placeholder="a">
    <input name="b" placeholder="b">
    <input name="c" placeholder="c">

    <div class="flex">
        <button>Calcular</button>
        <button type="reset">Limpiar</button>
    </div>

    </form>

    <h3>{result if result else ""}</h3>

    </div>

    {f'<div class="card"><img src="data:image/png;base64,{graph}"></div>' if graph else ""}

    </div></body></html>
    """)

# ================= SISTEMA 2X2 =================

@app.route("/sistema2x2", methods=["GET","POST"])
def sistema2x2():

    result = None

    if request.method == "POST":

        A = np.array([
            [float(request.form["a1"]), float(request.form["b1"])],
            [float(request.form["a2"]), float(request.form["b2"])]
        ])

        B = np.array([float(request.form["c1"]), float(request.form["c2"])])

        sol = np.linalg.solve(A,B)

        result = f"x={sol[0]:.2f}, y={sol[1]:.2f}"

    return render_template_string(f"""
    <html><head>{STYLE}</head>
    <body>{MENU}
    <div class="main">

    <div class="card">
    <h2>Sistema 2x2</h2>

    <form method="POST">

    <input name="a1" placeholder="a1">
    <input name="b1" placeholder="b1">
    <input name="c1" placeholder="c1">

    <input name="a2" placeholder="a2">
    <input name="b2" placeholder="b2">
    <input name="c2" placeholder="c2">

    <div class="flex">
        <button>Calcular</button>
        <button type="reset">Limpiar</button>
    </div>

    </form>

    <h3>{result if result else ""}</h3>

    </div>

    </div></body></html>
    """)

# ================= SISTEMA 3X3 =================

@app.route("/sistema3x3", methods=["GET","POST"])
def sistema3x3():

    result = None

    if request.method == "POST":

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

        result = f"x={sol[0]:.2f}, y={sol[1]:.2f}, z={sol[2]:.2f}"

    return render_template_string(f"""
    <html><head>{STYLE}</head>
    <body>{MENU}
    <div class="main">

    <div class="card">
    <h2>Sistema 3x3</h2>

    <form method="POST">

    <input name="a11"><input name="a12"><input name="a13">
    <input name="a21"><input name="a22"><input name="a23">
    <input name="a31"><input name="a32"><input name="a33">

    <input name="b1">
    <input name="b2">
    <input name="b3">

    <div class="flex">
        <button>Calcular</button>
        <button type="reset">Limpiar</button>
    </div>

    </form>

    <h3>{result if result else ""}</h3>

    </div>

    </div></body></html>
    """)

# ================= RUN =================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
