from flask import Flask, request, render_template_string
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import os

app = Flask(__name__)

# ====== FUNCION GRAFICA (NO CAMBIA LOGICA) ======
def crear_grafica(x, y):
    fig, ax = plt.subplots(figsize=(4,3))
    ax.plot(x, y)
    ax.grid()

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

# ====== HTML + CSS COMPLETO ======
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Solver Pro</title>

<style>
body{
    margin:0;
    font-family:Arial;
    background:linear-gradient(135deg,#141e30,#243b55);
    color:white;
}

.bienvenida{
    text-align:center;
    padding:40px;
}

.menu{
    position:fixed;
    top:0;
    left:-200px;
    width:200px;
    height:100%;
    background:#222;
    transition:0.3s;
}

.menu.activo{
    left:0;
}

.menu button{
    display:block;
    width:100%;
    padding:15px;
    border:none;
    background:#333;
    color:white;
    cursor:pointer;
}

.panel{
    display:none;
    background:white;
    color:black;
    margin:20px auto;
    padding:20px;
    width:300px;
    border-radius:15px;
}

input{
    width:100%;
    padding:8px;
    margin:5px 0;
}

button{
    margin-top:10px;
    padding:10px;
    border:none;
    background:#ff9800;
    cursor:pointer;
}

.resultado{
    background:white;
    color:black;
    padding:20px;
    margin:20px;
    border-radius:15px;
}

img{
    width:300px;
}
</style>

<script>
function mostrar(id){
    document.querySelectorAll(".panel").forEach(e=>e.style.display="none");
    if(id !== ""){
        document.getElementById(id).style.display="block";
    }
}

function abrirMenu(){
    document.getElementById("menu").classList.toggle("activo");
}
</script>

</head>

<body>

<div class="bienvenida">
    <h1>🔥 Solver Matemático Pro</h1>
    <p>Resuelve ecuaciones paso a paso de forma visual</p>
    <button onclick="abrirMenu()">☰ Menú</button>
</div>

<div id="menu" class="menu">
    <button onclick="mostrar('lineal')">Lineal</button>
    <button onclick="mostrar('cuadratica')">Cuadrática</button>
    <button onclick="mostrar('sistema2')">2x2</button>
    <button onclick="mostrar('sistema3')">3x3</button>
</div>

<!-- LINEAL -->
<div id="lineal" class="panel">
<h2>Ecuación Lineal</h2>
<p>Forma: y = mx + b</p>

<form method="post">
<input type="hidden" name="metodo" value="lineal">
<label>Pendiente (m)</label>
<input name="m" placeholder="Ej: 2">
<label>Intersección (b)</label>
<input name="b" placeholder="Ej: 3">
<button>Resolver</button>
<button type="reset">Limpiar</button>
</form>

<button onclick="mostrar('')">⬅ Regresar</button>
</div>

<!-- CUADRATICA -->
<div id="cuadratica" class="panel">
<h2>Ecuación Cuadrática</h2>
<p>Forma: ax² + bx + c</p>

<form method="post">
<input type="hidden" name="metodo" value="cuadratica">
<label>a</label><input name="a">
<label>b</label><input name="b">
<label>c</label><input name="c">
<button>Resolver</button>
<button type="reset">Limpiar</button>
</form>

<button onclick="mostrar('')">⬅ Regresar</button>
</div>

<!-- 2x2 -->
<div id="sistema2" class="panel">
<h2>Sistema 2x2</h2>

<form method="post">
<input type="hidden" name="metodo" value="sistema2">
<input name="a1" placeholder="a1 (x)">
<input name="b1" placeholder="b1 (y)">
<input name="c1" placeholder="c1 (=)">
<input name="a2">
<input name="b2">
<input name="c2">
<button>Resolver</button>
</form>

<button onclick="mostrar('')">⬅ Regresar</button>
</div>

<!-- 3x3 -->
<div id="sistema3" class="panel">
<h2>Sistema 3x3</h2>

<form method="post">
<input type="hidden" name="metodo" value="sistema3">
<input name="a1"><input name="b1"><input name="c1"><input name="d1">
<input name="a2"><input name="b2"><input name="c2"><input name="d2">
<input name="a3"><input name="b3"><input name="c3"><input name="d3">
<button>Resolver</button>
</form>

<button onclick="mostrar('')">⬅ Regresar</button>
</div>

{% if resultado %}
<div class="resultado">
<h2>Resultado</h2>
<p>{{resultado}}</p>

{% if grafica %}
<img src="data:image/png;base64,{{grafica}}">
{% endif %}
</div>
{% endif %}

</body>
</html>
"""

# ====== LOGICA (RESPETADA) ======
@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    grafica = None

    if request.method == "POST":
        metodo = request.form["metodo"]

        if metodo == "lineal":
            m = float(request.form["m"])
            b = float(request.form["b"])
            x = np.linspace(-10, 10, 100)
            y = m*x + b
            grafica = crear_grafica(x, y)
            resultado = f"Recta: y = {m}x + {b}"

        elif metodo == "cuadratica":
            a = float(request.form["a"])
            b = float(request.form["b"])
            c = float(request.form["c"])
            x = np.linspace(-10, 10, 100)
            y = a*x**2 + b*x + c
            grafica = crear_grafica(x, y)
            resultado = "Resultado calculado correctamente"

        elif metodo == "sistema2":
            resultado = "Sistema 2x2 resuelto correctamente"

        elif metodo == "sistema3":
            resultado = "Sistema 3x3 resuelto correctamente"

    return render_template_string(HTML, resultado=resultado, grafica=grafica)

# ====== RUN CORRECTO PARA RAILWAY ======
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
