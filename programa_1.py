from flask import Flask, render_template_string, request, send_file
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64
import tempfile
from fpdf import FPDF

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

def guardar_imagen_temp(fig):
    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    fig.savefig(tmp.name, format='png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)
    return tmp.name

# ================= SEGURIDAD INPUTS =================

def fget(key, default=""):
    val = request.form.get(key)
    if val is None or val == "":
        return default
    return val

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
    z-index:10;
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
    font-size:15px;
}

input::placeholder{
    color:#64748b;
    font-style:italic;
}

button, .btn{
    padding:15px 25px;
    border:none;
    border-radius:16px;
    background:linear-gradient(135deg,#2563eb,#60a5fa);
    color:white;
    font-weight:600;
    cursor:pointer;
    margin-top:15px;
    font-size:15px;
    display:inline-block;
    text-decoration:none;
    text-align:center;
    transition:0.3s;
}

button:hover, .btn:hover{
    transform:translateY(-2px);
    box-shadow:0 4px 15px rgba(59,130,246,0.4);
}

.btn-limpiar{
    background:linear-gradient(135deg,#475569,#64748b);
}

.btn-pdf{
    background:linear-gradient(135deg,#059669,#34d399);
}

.grafica img{
    width:100%;
    border-radius:15px;
    margin-top:15px;
}

.resultado{
    font-size:28px;
    color:#7dd3fc;
    font-weight:700;
    margin-bottom:10px;
}

/* ===== PROCESO (step-by-step) ===== */

.proceso{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.1);
    border-radius:18px;
    padding:25px 30px;
    margin:20px 0;
}

.proceso h3{
    color:#93c5fd;
    font-size:20px;
    margin-bottom:15px;
}

.paso{
    background:rgba(255,255,255,0.03);
    border-left:3px solid #60a5fa;
    padding:12px 18px;
    margin-bottom:10px;
    border-radius:0 12px 12px 0;
    color:#e2e8f0;
    font-size:15px;
    line-height:1.7;
}

.paso strong{
    color:#60a5fa;
}

.paso .formula{
    color:#fbbf24;
    font-weight:600;
    font-size:16px;
}

.buttons-row{
    display:flex;
    gap:12px;
    flex-wrap:wrap;
    margin-top:15px;
}

.input-label{
    color:#94a3b8;
    font-size:13px;
    margin-top:6px;
    margin-bottom:2px;
    display:block;
}

.input-row{
    display:flex;
    gap:12px;
    align-items:flex-end;
    margin-top:10px;
}

.input-row .input-group{
    flex:1;
}

.input-row .input-group input{
    width:100%;
    margin-top:4px;
}

</style>
"""

# ================= MENU =================

MENU = """
<div class="sidebar">

    <div class="logo">
        <h1>Math App</h1>
        <p>Matematica Interactiva</p>
    </div>

    <a href="/">Inicio</a>
    <a href="/lineal">🔢Ecuación Lineal</a>
    <a href="/cuadratica">🧮Ecuación Cuadratica</a>
    <a href="/sistema2x2">📊Sistema 2 x 2</a>
    <a href="/sistema3x3">📏Sistema 3 x 3</a>

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

# ================= PDF HELPER =================

class MathPDF(FPDF):
    def header(self):
        self.set_fill_color(15, 23, 42)
        self.rect(0, 0, 210, 30, 'F')
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(96, 165, 250)
        self.cell(0, 25, 'Math App', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f'Pagina {self.page_no()}  |  Mia Guzman Mosqueda', align='C')

    def add_title(self, title):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(30, 58, 138)
        self.cell(0, 12, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def add_subtitle(self, text):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(37, 99, 235)
        self.cell(0, 10, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def add_step(self, label, content):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(37, 99, 235)
        self.cell(40, 7, label, new_x="END")
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 41, 59)
        self.multi_cell(0, 7, content, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def add_result(self, text):
        self.set_fill_color(219, 234, 254)
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(30, 58, 138)
        self.cell(0, 14, f'  Resultado: {text}', fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

    def add_data_row(self, label, value):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(71, 85, 105)
        self.cell(50, 7, label + ":", new_x="END")
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 41, 59)
        self.cell(0, 7, str(value), new_x="LMARGIN", new_y="NEXT")


# ================= HOME =================

@app.route("/")
def inicio():
    return render_template_string(f"""
<html>
<head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">
<h1>¡Bienvenido! 👋</h1>

<p>
Plataforma matemática interactiva diseñada para resolver
ecuaciones lineales, cuadráticas y sistemas de ecuaciones.
</p>

<p>
El sistema calcula automaticamente soluciones,
genera graficas e interpreta resultados.
</p>

<h3>Desarrollado por:</h3>
<h2>MÍA GUZMÁN MOSQUEDA</h2>

</div>

<div class="card">

<h2>¿Qué puedes hacer aquí?</h2>

<ul>
<li>Resolver ecuaciones lineales</li>
<li>Resolver ecuaciones cuadraticas</li>
<li>Resolver sistemas 2 x 2</li>
<li>Resolver sistemas 3 x 3</li>
<li>Visualizar graficas automáticas</li>
<li>Descargar resultados en PDF</li>
</ul>

</div>

</div>

</body>
</html>
""")

# ================= LINEAL =================

@app.route("/lineal", methods=["GET","POST"])
def lineal():

    tipo = request.form.get("tipo", "pendiente")

    resultado = ""
    img = ""
    proceso = ""
    val_m = fget("m")
    val_b = fget("b")
    val_x1 = fget("x1")
    val_y1 = fget("y1")
    val_x2 = fget("x2")
    val_y2 = fget("y2")

    if request.method == "POST" and request.form.get("_action") != "limpiar":

        try:

            if tipo == "dos_puntos":

                x1 = float(val_x1)
                y1 = float(val_y1)
                x2 = float(val_x2)
                y2 = float(val_y2)

                if x1 == x2:
                    raise ValueError("Los puntos tienen la misma x")

                m = (y2 - y1) / (x2 - x1)
                b = y1 - m * x1

                proceso = f"""
                <div class="proceso">
                <h3>Proceso de solucion</h3>

                <div class="paso"><strong>Paso 1:</strong> Datos ingresados: Punto 1 ({x1}, {y1}) y Punto 2 ({x2}, {y2})</div>

                <div class="paso"><strong>Paso 2:</strong> Calcular la pendiente con la formula:
                <br><span class="formula">m = (y2 - y1) / (x2 - x1)</span></div>

                <div class="paso"><strong>Paso 3:</strong> Sustituir valores:
                <br><span class="formula">m = ({y2} - {y1}) / ({x2} - {x1}) = {y2 - y1} / {x2 - x1} = {m:.4f}</span></div>

                <div class="paso"><strong>Paso 4:</strong> Calcular la intercepcion b usando y = mx + b:
                <br><span class="formula">b = y1 - m * x1 = {y1} - ({m:.4f})({x1}) = {b:.4f}</span></div>

                <div class="paso"><strong>Paso 5:</strong> La ecuacion de la recta es:
                <br><span class="formula">y = {m:.4f}x + {b:.4f}</span></div>
                """

            elif tipo == "punto_pendiente":

                x1 = float(val_x1)
                y1 = float(val_y1)
                m = float(val_m)
                b = y1 - m * x1

                proceso = f"""
                <div class="proceso">
                <h3>Proceso de solucion</h3>

                <div class="paso"><strong>Paso 1:</strong> Datos ingresados: Punto ({x1}, {y1}), Pendiente m = {m}</div>

                <div class="paso"><strong>Paso 2:</strong> Forma punto-pendiente:
                <br><span class="formula">y - y1 = m(x - x1)</span></div>

                <div class="paso"><strong>Paso 3:</strong> Sustituir valores:
                <br><span class="formula">y - {y1} = {m}(x - {x1})</span></div>

                <div class="paso"><strong>Paso 4:</strong> Expandir y simplificar:
                <br><span class="formula">y = {m}x - {m}({x1}) + {y1}</span>
                <br><span class="formula">y = {m}x + {b:.4f}</span></div>

                <div class="paso"><strong>Paso 5:</strong> La ecuacion de la recta es:
                <br><span class="formula">y = {m:.4f}x + {b:.4f}</span></div>
                """

            elif tipo == "forma_general":

                ga = float(fget("ga", "0"))
                gb = float(fget("gb", "0"))
                gc = float(fget("gc", "0"))

                if ga == 0 and gb == 0:
                    raise ValueError("a y b no pueden ser ambos 0")

                if gb != 0:
                    m = -ga / gb
                    b = -gc / gb
                else:
                    m = float('inf')
                    b = 0

                proceso = f"""
                <div class="proceso">
                <h3>Proceso de solucion</h3>

                <div class="paso"><strong>Paso 1:</strong> Forma general: ax + by + c = 0
                <br><span class="formula">{ga}x + {gb}y + {gc} = 0</span></div>

                <div class="paso"><strong>Paso 2:</strong> Convertir a forma pendiente-intercepto y = mx + b:
                <br><span class="formula">{gb}y = -{ga}x - {gc}</span></div>
                """

                if gb != 0:
                    proceso += f"""
                    <div class="paso"><strong>Paso 3:</strong> Dividir entre b = {gb}:
                    <br><span class="formula">y = ({-ga}/{gb})x + ({-gc}/{gb})</span>
                    <br><span class="formula">y = {m:.4f}x + {b:.4f}</span></div>
                    """
                else:
                    proceso += f"""
                    <div class="paso"><strong>Paso 3:</strong> Como b = 0, la recta es vertical:
                    <br><span class="formula">x = {-gc/ga:.4f}</span></div>
                    """

            else:

                m = float(val_m)
                b = float(val_b)

                proceso = f"""
                <div class="proceso">
                <h3>Proceso de solucion</h3>

                <div class="paso"><strong>Paso 1:</strong> Ecuacion lineal dada:
                <br><span class="formula">y = mx + b</span></div>

                <div class="paso"><strong>Paso 2:</strong> Sustituir valores: m = {m}, b = {b}
                <br><span class="formula">y = ({m})x + ({b})</span></div>

                <div class="paso"><strong>Paso 3:</strong> Para encontrar la raiz (donde y = 0):
                <br><span class="formula">0 = ({m})x + ({b})</span></div>

                <div class="paso"><strong>Paso 4:</strong> Despejar x:
                <br><span class="formula">({m})x = -({b}) = {-b}</span></div>
                """

            if tipo == "forma_general" and gb == 0:
                x = -gc / ga
                proceso += f"""
                <div class="paso"><strong>Resultado:</strong> Recta vertical en x = {x:.4f}</div>
                </div>
                """
                resultado = f"x = {x:.2f} (recta vertical)"
            elif m != 0:
                x = -b / m
                proceso += f"""
                <div class="paso"><strong>Paso {'6' if tipo in ['dos_puntos','punto_pendiente','forma_general'] else '5'}:</strong> Dividir ambos lados entre m:
                <br><span class="formula">x = {-b} / {m} = {x:.4f}</span></div>
                </div>
                """
                resultado = f"x = {x:.2f}"
            else:
                x = 0
                proceso += f"""
                <div class="paso"><strong>Paso 5:</strong> La pendiente es 0, la linea es horizontal en y = {b}</div>
                </div>
                """
                resultado = f"x = {x:.2f}"

            fig, ax = grafica_base(title="Ecuacion Lineal", ylabel="f(x)")

            xs = np.linspace(-10, 10, 400)

            if tipo == "forma_general" and gb == 0:
                ax.axvline(x=x, color=CHART_COLORS['accent1'], linewidth=2.5,
                           label=f'x = {x:.2f}', zorder=3)
            else:
                ys = m * xs + b
                ax.plot(xs, ys, color=CHART_COLORS['accent1'], linewidth=2.5,
                        label=f'y = {m:.1f}x + {b:.1f}', zorder=3)
                ax.fill_between(xs, ys, alpha=0.08, color=CHART_COLORS['accent1'])

            ax.scatter([x], [0], color=CHART_COLORS['highlight'], s=120,
                       zorder=5, edgecolors='white', linewidths=1.5,
                       label=f'Raiz x = {x:.2f}')
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
            resultado = "Datos invalidos"

    if tipo == "pendiente":
        html_inputs = f"""
        <div class="input-row">
        <div class="input-group"><span class="input-label">Pendiente (m)</span>
        <input name="m" placeholder="ej: 2" value="{val_m}"></div>
        <div class="input-group"><span class="input-label">Intercepcion (b)</span>
        <input name="b" placeholder="ej: -3" value="{val_b}"></div>
        </div>
        """
    elif tipo == "dos_puntos":
        html_inputs = f"""
        <p style="color:#94a3b8; font-size:14px; margin-top:10px;">Punto 1</p>
        <div class="input-row">
        <div class="input-group"><span class="input-label">X1</span>
        <input name="x1" placeholder="ej: 1" value="{val_x1}"></div>
        <div class="input-group"><span class="input-label">Y1</span>
        <input name="y1" placeholder="ej: 2" value="{val_y1}"></div>
        </div>
        <p style="color:#94a3b8; font-size:14px; margin-top:10px;">Punto 2</p>
        <div class="input-row">
        <div class="input-group"><span class="input-label">X2</span>
        <input name="x2" placeholder="ej: 4" value="{val_x2}"></div>
        <div class="input-group"><span class="input-label">Y2</span>
        <input name="y2" placeholder="ej: 8" value="{val_y2}"></div>
        </div>
        """
    elif tipo == "punto_pendiente":
        html_inputs = f"""
        <div class="input-row">
        <div class="input-group"><span class="input-label">Pendiente (m)</span>
        <input name="m" placeholder="ej: 3" value="{val_m}"></div>
        <div class="input-group"><span class="input-label">X1</span>
        <input name="x1" placeholder="ej: 2" value="{val_x1}"></div>
        <div class="input-group"><span class="input-label">Y1</span>
        <input name="y1" placeholder="ej: 5" value="{val_y1}"></div>
        </div>
        """
    else:
        val_ga = fget("ga")
        val_gb = fget("gb")
        val_gc = fget("gc")
        html_inputs = f"""
        <p style="color:#94a3b8; font-size:14px; margin-top:10px;">ax + by + c = 0</p>
        <div class="input-row">
        <div class="input-group"><span class="input-label">a</span>
        <input name="ga" placeholder="ej: 3" value="{val_ga}"></div>
        <div class="input-group"><span class="input-label">b</span>
        <input name="gb" placeholder="ej: -2" value="{val_gb}"></div>
        <div class="input-group"><span class="input-label">c</span>
        <input name="gc" placeholder="ej: 6" value="{val_gc}"></div>
        </div>
        """

    pdf_btn = ""
    if resultado and resultado != "Datos invalidos":
        pdf_btn = """
        <form method="POST" action="/pdf/lineal" style="display:inline">
        """ + (f'<input type="hidden" name="tipo" value="{tipo}">' +
               f'<input type="hidden" name="m" value="{val_m}">' +
               f'<input type="hidden" name="b" value="{val_b}">' +
               f'<input type="hidden" name="x1" value="{val_x1}">' +
               f'<input type="hidden" name="y1" value="{val_y1}">' +
               f'<input type="hidden" name="x2" value="{val_x2}">' +
               f'<input type="hidden" name="y2" value="{val_y2}">' +
               f'<input type="hidden" name="ga" value="{fget("ga")}">' +
               f'<input type="hidden" name="gb" value="{fget("gb")}">' +
               f'<input type="hidden" name="gc" value="{fget("gc")}">') + """
        <button type="submit" class="btn btn-pdf">Descargar PDF</button>
        </form>
        """

    return render_template_string(f"""
<html>
<head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">

<h2>Ecuacion Lineal</h2>

<h2>Las ecuaciones lineales son igualdades matematicas de primer grado donde las incognitas tienen exponente 1, representando una linea recta al graficarse.</h2>

<h2>Elige los datos que tienes...</h2>

<form method="POST">

<select name="tipo" onchange="this.form.submit()">
<option value="pendiente" {"selected" if tipo=="pendiente" else ""}>Pendiente + b</option>
<option value="dos_puntos" {"selected" if tipo=="dos_puntos" else ""}>Dos puntos</option>
<option value="punto_pendiente" {"selected" if tipo=="punto_pendiente" else ""}>Punto + Pendiente</option>
<option value="forma_general" {"selected" if tipo=="forma_general" else ""}>Forma General (ax+by+c=0)</option>
</select>

{html_inputs}

<div class="buttons-row">
<button type="submit">Calcular</button>
<a href="/lineal" class="btn btn-limpiar">Limpiar</a>
</div>

</form>

</div>

{"<div class='card'>" + proceso + "<div class='resultado'>" + resultado + "</div><div class='grafica'><img src=\"data:image/png;base64," + img + "\"></div><div class='buttons-row'>" + pdf_btn + "</div></div>" if resultado else ""}

</div>

</body>
</html>
""")

# ================= CUADRATICA =================

@app.route("/cuadratica", methods=["GET","POST"])
def cuadratica():

    tipo = request.form.get("tipo", "general")

    img = ""
    sol = ""
    proceso = ""
    val_a = fget("a")
    val_b = fget("b")
    val_c = fget("c")
    val_h = fget("h")
    val_k = fget("k")
    val_r1 = fget("r1")
    val_r2 = fget("r2")

    if request.method == "POST" and request.form.get("_action") != "limpiar":

        try:

            if tipo == "vertice":

                a = float(val_a)
                h = float(val_h)
                k = float(val_k)

                if a == 0:
                    raise ValueError("a no puede ser 0")

                b = -2 * a * h
                c = a * h**2 + k

                disc = b**2 - 4*a*c

                proceso = f"""
                <div class="proceso">
                <h3>Proceso de solucion</h3>

                <div class="paso"><strong>Paso 1:</strong> Forma vertice:
                <br><span class="formula">y = a(x - h)2 + k</span></div>

                <div class="paso"><strong>Paso 2:</strong> Valores ingresados: a = {a}, h = {h}, k = {k}
                <br><span class="formula">y = {a}(x - {h})2 + {k}</span></div>

                <div class="paso"><strong>Paso 3:</strong> Expandir a forma general:
                <br><span class="formula">y = {a}(x2 - {2*h}x + {h**2}) + {k}</span>
                <br><span class="formula">y = {a}x2 + ({b:.4f})x + ({c:.4f})</span></div>

                <div class="paso"><strong>Paso 4:</strong> Vertice de la parabola:
                <br><span class="formula">Vertice = ({h}, {k})</span></div>

                <div class="paso"><strong>Paso 5:</strong> Discriminante:
                <br><span class="formula">D = b2 - 4ac = ({b:.4f})2 - 4({a})({c:.4f}) = {disc:.4f}</span></div>
                """

                vx = h
                vy = k

            elif tipo == "raices":

                a = float(val_a)
                r1 = float(val_r1)
                r2 = float(val_r2)

                if a == 0:
                    raise ValueError("a no puede ser 0")

                b = -a * (r1 + r2)
                c = a * r1 * r2

                disc = b**2 - 4*a*c

                proceso = f"""
                <div class="proceso">
                <h3>Proceso de solucion</h3>

                <div class="paso"><strong>Paso 1:</strong> Forma factorizada:
                <br><span class="formula">y = a(x - r1)(x - r2)</span></div>

                <div class="paso"><strong>Paso 2:</strong> Valores ingresados: a = {a}, r1 = {r1}, r2 = {r2}
                <br><span class="formula">y = {a}(x - {r1})(x - {r2})</span></div>

                <div class="paso"><strong>Paso 3:</strong> Expandir:
                <br><span class="formula">y = {a}(x2 - {r1+r2:.4f}x + {r1*r2:.4f})</span>
                <br><span class="formula">y = {a}x2 + ({b:.4f})x + ({c:.4f})</span></div>

                <div class="paso"><strong>Paso 4:</strong> Las raices son:
                <br><span class="formula">x1 = {r1}, x2 = {r2}</span></div>
                """

                vx = -b / (2 * a)
                vy = a * vx**2 + b * vx + c

                proceso += f"""
                <div class="paso"><strong>Vertice:</strong>
                <br><span class="formula">xv = -(r1+r2)/2 = {vx:.4f}</span>
                <br><span class="formula">yv = f({vx:.4f}) = {vy:.4f}</span>
                <br><span class="formula">Vertice = ({vx:.4f}, {vy:.4f})</span></div>
                </div>
                """

                x1, x2 = r1, r2
                sol = f"x1 = {x1:.2f}, x2 = {x2:.2f}"

            else:

                a = float(val_a)
                b = float(val_b)
                c = float(val_c)

                if a == 0:
                    raise ValueError("a no puede ser 0")

                disc = b**2 - 4*a*c

                proceso = f"""
                <div class="proceso">
                <h3>Proceso de solucion</h3>

                <div class="paso"><strong>Paso 1:</strong> Ecuacion cuadratica general:
                <br><span class="formula">ax2 + bx + c = 0</span></div>

                <div class="paso"><strong>Paso 2:</strong> Valores ingresados: a = {a}, b = {b}, c = {c}
                <br><span class="formula">{a}x2 + ({b})x + ({c}) = 0</span></div>

                <div class="paso"><strong>Paso 3:</strong> Calcular el discriminante:
                <br><span class="formula">D = b2 - 4ac</span>
                <br><span class="formula">D = ({b})2 - 4({a})({c})</span>
                <br><span class="formula">D = {b**2} - {4*a*c} = {disc:.4f}</span></div>
                """

                vx = -b / (2 * a)
                vy = a * vx**2 + b * vx + c

            if tipo != "raices":
                if disc < 0:
                    sol = "Sin raices reales"
                    proceso += f"""
                    <div class="paso"><strong>Paso {'6' if tipo=='vertice' else '4'}:</strong> Como D = {disc:.4f} < 0, no existen raices reales.
                    <br>La parabola no cruza el eje x.</div>
                    """
                elif disc == 0:
                    x1 = -b / (2*a)
                    x2 = x1
                    sol = f"x = {x1:.2f} (raiz doble)"
                    proceso += f"""
                    <div class="paso"><strong>Paso {'6' if tipo=='vertice' else '4'}:</strong> Como D = 0, hay una raiz doble:
                    <br><span class="formula">x = -b / (2a) = -({b}) / (2 * {a}) = {x1:.4f}</span></div>
                    """
                else:
                    x1 = (-b + np.sqrt(disc)) / (2*a)
                    x2 = (-b - np.sqrt(disc)) / (2*a)
                    sol = f"x1 = {x1:.2f}, x2 = {x2:.2f}"
                    paso_n = 6 if tipo=='vertice' else 4
                    proceso += f"""
                    <div class="paso"><strong>Paso {paso_n}:</strong> Como D = {disc:.4f} > 0, hay dos raices reales:
                    <br><span class="formula">x = (-b +/- sqrt(D)) / (2a)</span></div>

                    <div class="paso"><strong>Paso {paso_n+1}:</strong> Calcular x1:
                    <br><span class="formula">x1 = (-({b}) + sqrt({disc:.4f})) / (2 * {a})</span>
                    <br><span class="formula">x1 = ({-b} + {np.sqrt(disc):.4f}) / {2*a}</span>
                    <br><span class="formula">x1 = {x1:.4f}</span></div>

                    <div class="paso"><strong>Paso {paso_n+2}:</strong> Calcular x2:
                    <br><span class="formula">x2 = (-({b}) - sqrt({disc:.4f})) / (2 * {a})</span>
                    <br><span class="formula">x2 = ({-b} - {np.sqrt(disc):.4f}) / {2*a}</span>
                    <br><span class="formula">x2 = {x2:.4f}</span></div>
                    """

                if tipo != "vertice":
                    proceso += f"""
                    <div class="paso"><strong>Vertice:</strong> El vertice de la parabola se encuentra en:
                    <br><span class="formula">xv = -b / (2a) = -({b}) / (2 * {a}) = {vx:.4f}</span>
                    <br><span class="formula">yv = f({vx:.4f}) = {vy:.4f}</span>
                    <br><span class="formula">Vertice = ({vx:.4f}, {vy:.4f})</span></div>
                    """

                proceso += "</div>"

            fig, ax = grafica_base(title="Ecuacion Cuadratica", ylabel="f(x)")
            xs = np.linspace(-10, 10, 400)
            ys = a * xs**2 + b * xs + c

            ax.plot(xs, ys, color=CHART_COLORS['accent2'], linewidth=2.5,
                    label=f'f(x) = {a:.1f}x2 + {b:.1f}x + {c:.1f}', zorder=3)
            ax.fill_between(xs, ys, alpha=0.10, color=CHART_COLORS['accent2'])

            ax.scatter([vx], [vy], color=CHART_COLORS['warn'], s=100,
                       zorder=5, edgecolors='white', linewidths=1.5, marker='D',
                       label=f'Vertice ({vx:.2f}, {vy:.2f})')

            if disc >= 0:
                roots_x = [x1]
                if abs(x1 - x2) > 1e-9:
                    roots_x.append(x2)
                ax.scatter(roots_x, [0]*len(roots_x), color=CHART_COLORS['highlight'],
                           s=120, zorder=5, edgecolors='white', linewidths=1.5,
                           label='Raices')
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
            sol = "Datos invalidos"

    if tipo == "general":
        html_inputs = f"""
        <div class="input-row">
        <div class="input-group"><span class="input-label">Coeficiente a (x2)</span>
        <input name="a" placeholder="ej: 1" value="{val_a}"></div>
        <div class="input-group"><span class="input-label">Coeficiente b (x)</span>
        <input name="b" placeholder="ej: -2" value="{val_b}"></div>
        <div class="input-group"><span class="input-label">Termino c</span>
        <input name="c" placeholder="ej: -3" value="{val_c}"></div>
        </div>
        """
    elif tipo == "vertice":
        html_inputs = f"""
        <p style="color:#94a3b8; font-size:14px; margin-top:10px;">y = a(x - h)2 + k</p>
        <div class="input-row">
        <div class="input-group"><span class="input-label">a</span>
        <input name="a" placeholder="ej: 1" value="{val_a}"></div>
        <div class="input-group"><span class="input-label">h (x del vertice)</span>
        <input name="h" placeholder="ej: 3" value="{val_h}"></div>
        <div class="input-group"><span class="input-label">k (y del vertice)</span>
        <input name="k" placeholder="ej: -4" value="{val_k}"></div>
        </div>
        """
    else:
        html_inputs = f"""
        <p style="color:#94a3b8; font-size:14px; margin-top:10px;">y = a(x - r1)(x - r2)</p>
        <div class="input-row">
        <div class="input-group"><span class="input-label">a</span>
        <input name="a" placeholder="ej: 1" value="{val_a}"></div>
        <div class="input-group"><span class="input-label">Raiz 1 (r1)</span>
        <input name="r1" placeholder="ej: -1" value="{val_r1}"></div>
        <div class="input-group"><span class="input-label">Raiz 2 (r2)</span>
        <input name="r2" placeholder="ej: 3" value="{val_r2}"></div>
        </div>
        """

    pdf_btn = ""
    if sol and sol != "Datos invalidos":
        pdf_btn = f"""
        <form method="POST" action="/pdf/cuadratica" style="display:inline">
        <input type="hidden" name="tipo" value="{tipo}">
        <input type="hidden" name="a" value="{val_a}">
        <input type="hidden" name="b" value="{val_b}">
        <input type="hidden" name="c" value="{val_c}">
        <input type="hidden" name="h" value="{val_h}">
        <input type="hidden" name="k" value="{val_k}">
        <input type="hidden" name="r1" value="{val_r1}">
        <input type="hidden" name="r2" value="{val_r2}">
        <button type="submit" class="btn btn-pdf">Descargar PDF</button>
        </form>
        """

    return render_template_string(f"""
<html>
<head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">
<h2>Cuadratica</h2>

<h2>Una ecuacion cuadratica es una ecuacion algebraica de segundo grado donde la variable esta elevada al cuadrado.</h2>

<h2>Elige los datos que tienes...</h2>

<form method="POST">

<select name="tipo" onchange="this.form.submit()">
<option value="general" {"selected" if tipo=="general" else ""}>Forma General (ax2+bx+c=0)</option>
<option value="vertice" {"selected" if tipo=="vertice" else ""}>Forma Vertice (a,h,k)</option>
<option value="raices" {"selected" if tipo=="raices" else ""}>Forma Factorizada (raices)</option>
</select>

{html_inputs}

<div class="buttons-row">
<button>Calcular</button>
<a href="/cuadratica" class="btn btn-limpiar">Limpiar</a>
</div>
</form>

</div>

{"<div class='card'>" + proceso + "<div class='resultado'>" + sol + "</div><div class='grafica'><img src=\"data:image/png;base64," + img + "\"></div><div class='buttons-row'>" + pdf_btn + "</div></div>" if sol else ""}

</div>

</body>
</html>
""")

# ================= SISTEMA 2X2 =================

@app.route("/sistema2x2", methods=["GET","POST"])
def sistema2x2():

    tipo = request.form.get("tipo", "estandar")

    img = ""
    sol = ""
    proceso = ""
    va1 = fget("a1"); vb1 = fget("b1"); vc1 = fget("c1")
    va2 = fget("a2"); vb2 = fget("b2"); vc2 = fget("c2")
    vm1 = fget("m1"); vn1 = fget("n1")
    vm2 = fget("m2"); vn2 = fget("n2")

    if request.method == "POST" and request.form.get("_action") != "limpiar":

        try:

            if tipo == "pendiente_intercepto":

                m1 = float(vm1); n1 = float(vn1)
                m2 = float(vm2); n2 = float(vn2)

                a1 = m1; b1 = -1.0; c1 = -n1
                a2 = m2; b2 = -1.0; c2 = -n2

                proceso = f"""
                <div class="proceso">
                <h3>Proceso de solucion</h3>

                <div class="paso"><strong>Paso 1:</strong> Sistema en forma pendiente-intercepto:
                <br><span class="formula">y = {m1}x + {n1}</span>
                <br><span class="formula">y = {m2}x + {n2}</span></div>

                <div class="paso"><strong>Paso 2:</strong> Igualar ambas ecuaciones (y = y):
                <br><span class="formula">{m1}x + {n1} = {m2}x + {n2}</span></div>

                <div class="paso"><strong>Paso 3:</strong> Despejar x:
                <br><span class="formula">{m1}x - {m2}x = {n2} - {n1}</span>
                <br><span class="formula">({m1 - m2:.4f})x = {n2 - n1:.4f}</span></div>
                """

                if abs(m1 - m2) < 1e-10:
                    raise ValueError("Las rectas son paralelas")

                x = (n2 - n1) / (m1 - m2)
                y = m1 * x + n1

                proceso += f"""
                <div class="paso"><strong>Paso 4:</strong> Calcular x:
                <br><span class="formula">x = {n2 - n1:.4f} / {m1 - m2:.4f} = {x:.4f}</span></div>

                <div class="paso"><strong>Paso 5:</strong> Sustituir x en la primera ecuacion:
                <br><span class="formula">y = {m1}({x:.4f}) + {n1} = {y:.4f}</span></div>

                <div class="paso"><strong>Verificacion:</strong>
                <br><span class="formula">Ec.1: y = {m1}({x:.4f}) + {n1} = {m1*x + n1:.4f}</span>
                <br><span class="formula">Ec.2: y = {m2}({x:.4f}) + {n2} = {m2*x + n2:.4f}</span></div>
                </div>
                """

                sol = f"x = {x:.2f}, y = {y:.2f}"

                fig, ax = grafica_base(title="Sistema 2x2 (Pendiente-Intercepto)", ylabel="y")
                xs_plot = np.linspace(-10, 10, 400)

                ax.plot(xs_plot, m1 * xs_plot + n1, color=CHART_COLORS['accent1'],
                        linewidth=2.5, label=f'y = {m1:.1f}x + {n1:.1f}', zorder=3)
                ax.plot(xs_plot, m2 * xs_plot + n2, color=CHART_COLORS['accent3'],
                        linewidth=2.5, label=f'y = {m2:.1f}x + {n2:.1f}', zorder=3)

            else:

                a1 = float(va1); b1 = float(vb1); c1 = float(vc1)
                a2 = float(va2); b2 = float(vb2); c2 = float(vc2)

                det = a1*b2 - a2*b1

                proceso = f"""
                <div class="proceso">
                <h3>Proceso de solucion</h3>

                <div class="paso"><strong>Paso 1:</strong> Sistema de ecuaciones:
                <br><span class="formula">{a1}x + {b1}y = {c1}</span>
                <br><span class="formula">{a2}x + {b2}y = {c2}</span></div>

                <div class="paso"><strong>Paso 2:</strong> Forma matricial Ax = B:
                <br><span class="formula">|{a1}  {b1}| |x|   |{c1}|</span>
                <br><span class="formula">|{a2}  {b2}| |y| = |{c2}|</span></div>

                <div class="paso"><strong>Paso 3:</strong> Calcular el determinante:
                <br><span class="formula">det(A) = ({a1})({b2}) - ({a2})({b1})</span>
                <br><span class="formula">det(A) = {a1*b2} - {a2*b1} = {det:.4f}</span></div>
                """

                if abs(det) < 1e-10:
                    raise ValueError("Sistema sin solucion unica")

                A = np.array([[a1, b1], [a2, b2]])
                B = np.array([c1, c2])
                x, y = np.linalg.solve(A, B)

                proceso += f"""
                <div class="paso"><strong>Paso 4:</strong> Usando la Regla de Cramer:
                <br><span class="formula">x = (c1*b2 - c2*b1) / det(A)</span>
                <br><span class="formula">x = ({c1}*{b2} - {c2}*{b1}) / {det:.4f}</span>
                <br><span class="formula">x = ({c1*b2} - {c2*b1}) / {det:.4f} = {x:.4f}</span></div>

                <div class="paso"><strong>Paso 5:</strong> Calcular y:
                <br><span class="formula">y = (a1*c2 - a2*c1) / det(A)</span>
                <br><span class="formula">y = ({a1}*{c2} - {a2}*{c1}) / {det:.4f}</span>
                <br><span class="formula">y = ({a1*c2} - {a2*c1}) / {det:.4f} = {y:.4f}</span></div>

                <div class="paso"><strong>Verificacion:</strong>
                <br><span class="formula">Ec.1: {a1}({x:.4f}) + {b1}({y:.4f}) = {a1*x + b1*y:.4f} (debe ser {c1})</span>
                <br><span class="formula">Ec.2: {a2}({x:.4f}) + {b2}({y:.4f}) = {a2*x + b2*y:.4f} (debe ser {c2})</span></div>
                </div>
                """

                sol = f"x = {x:.2f}, y = {y:.2f}"

                fig, ax = grafica_base(title="Sistema de Ecuaciones 2x2", ylabel="y")
                xs_plot = np.linspace(-10, 10, 400)

                ax.plot(xs_plot, (c1 - a1 * xs_plot) / b1, color=CHART_COLORS['accent1'],
                        linewidth=2.5, label=f'{a1:.0f}x + {b1:.0f}y = {c1:.0f}', zorder=3)
                ax.plot(xs_plot, (c2 - a2 * xs_plot) / b2, color=CHART_COLORS['accent3'],
                        linewidth=2.5, label=f'{a2:.0f}x + {b2:.0f}y = {c2:.0f}', zorder=3)

            ax.scatter([x], [y], color=CHART_COLORS['highlight'], s=150,
                       zorder=5, edgecolors='white', linewidths=2,
                       label=f'Solucion ({x:.2f}, {y:.2f})')
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
            sol = "Sistema invalido"

    if tipo == "estandar":
        html_inputs = f"""
        <p style="color:#94a3b8; font-size:14px; margin-top:10px;">Ecuacion 1: a1*x + b1*y = c1</p>
        <div class="input-row">
        <div class="input-group"><span class="input-label">a1</span>
        <input name="a1" placeholder="ej: 2" value="{va1}"></div>
        <div class="input-group"><span class="input-label">b1</span>
        <input name="b1" placeholder="ej: 3" value="{vb1}"></div>
        <div class="input-group"><span class="input-label">c1</span>
        <input name="c1" placeholder="ej: 8" value="{vc1}"></div>
        </div>

        <p style="color:#94a3b8; font-size:14px; margin-top:20px;">Ecuacion 2: a2*x + b2*y = c2</p>
        <div class="input-row">
        <div class="input-group"><span class="input-label">a2</span>
        <input name="a2" placeholder="ej: 1" value="{va2}"></div>
        <div class="input-group"><span class="input-label">b2</span>
        <input name="b2" placeholder="ej: -1" value="{vb2}"></div>
        <div class="input-group"><span class="input-label">c2</span>
        <input name="c2" placeholder="ej: 1" value="{vc2}"></div>
        </div>
        """
    else:
        html_inputs = f"""
        <p style="color:#94a3b8; font-size:14px; margin-top:10px;">Linea 1: y = m1*x + b1</p>
        <div class="input-row">
        <div class="input-group"><span class="input-label">m1 (pendiente)</span>
        <input name="m1" placeholder="ej: 2" value="{vm1}"></div>
        <div class="input-group"><span class="input-label">b1 (intercepto)</span>
        <input name="n1" placeholder="ej: 1" value="{vn1}"></div>
        </div>

        <p style="color:#94a3b8; font-size:14px; margin-top:20px;">Linea 2: y = m2*x + b2</p>
        <div class="input-row">
        <div class="input-group"><span class="input-label">m2 (pendiente)</span>
        <input name="m2" placeholder="ej: -1" value="{vm2}"></div>
        <div class="input-group"><span class="input-label">b2 (intercepto)</span>
        <input name="n2" placeholder="ej: 4" value="{vn2}"></div>
        </div>
        """

    pdf_btn = ""
    if sol and sol != "Sistema invalido":
        pdf_btn = f"""
        <form method="POST" action="/pdf/sistema2x2" style="display:inline">
        <input type="hidden" name="tipo" value="{tipo}">
        <input type="hidden" name="a1" value="{va1}">
        <input type="hidden" name="b1" value="{vb1}">
        <input type="hidden" name="c1" value="{vc1}">
        <input type="hidden" name="a2" value="{va2}">
        <input type="hidden" name="b2" value="{vb2}">
        <input type="hidden" name="c2" value="{vc2}">
        <input type="hidden" name="m1" value="{vm1}">
        <input type="hidden" name="n1" value="{vn1}">
        <input type="hidden" name="m2" value="{vm2}">
        <input type="hidden" name="n2" value="{vn2}">
        <button type="submit" class="btn btn-pdf">Descargar PDF</button>
        </form>
        """

    return render_template_string(f"""
<html>
<head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">
<h2>Sistema 2x2</h2>

<h2>Un sistema de ecuaciones 2x2 con dos ecuaciones y dos incognitas.</h2>

<h2>Elige los datos que tienes...</h2>

<form method="POST">

<select name="tipo" onchange="this.form.submit()">
<option value="estandar" {"selected" if tipo=="estandar" else ""}>Forma Estandar (ax+by=c)</option>
<option value="pendiente_intercepto" {"selected" if tipo=="pendiente_intercepto" else ""}>Pendiente-Intercepto (y=mx+b)</option>
</select>

{html_inputs}

<div class="buttons-row">
<button>Resolver</button>
<a href="/sistema2x2" class="btn btn-limpiar">Limpiar</a>
</div>

</form>

</div>

{"<div class='card'>" + proceso + "<div class='resultado'>" + sol + "</div><div class='grafica'><img src=\"data:image/png;base64," + img + "\"></div><div class='buttons-row'>" + pdf_btn + "</div></div>" if sol else ""}

</div>

</body>
</html>
""")

# ================= SISTEMA 3X3 =================

@app.route("/sistema3x3", methods=["GET","POST"])
def sistema3x3():

    sol = ""
    proceso = ""
    va1 = fget("a1"); vb1 = fget("b1"); vc1 = fget("c1"); vd1 = fget("d1")
    va2 = fget("a2"); vb2 = fget("b2"); vc2 = fget("c2"); vd2 = fget("d2")
    va3 = fget("a3"); vb3 = fget("b3"); vc3 = fget("c3"); vd3 = fget("d3")

    if request.method == "POST" and request.form.get("_action") != "limpiar":

        try:

            a1=float(va1); b1=float(vb1); c1=float(vc1); d1=float(vd1)
            a2=float(va2); b2=float(vb2); c2=float(vc2); d2=float(vd2)
            a3=float(va3); b3=float(vb3); c3=float(vc3); d3=float(vd3)

            A = np.array([[a1,b1,c1],[a2,b2,c2],[a3,b3,c3]])
            B = np.array([d1,d2,d3])

            det_val = np.linalg.det(A)

            proceso = f"""
            <div class="proceso">
            <h3>Proceso de solución</h3>

            <div class="paso"><strong>Paso 1:</strong> Sistema de ecuaciones:
            <br><span class="formula">{a1}x + {b1}y + {c1}z = {d1}</span>
            <br><span class="formula">{a2}x + {b2}y + {c2}z = {d2}</span>
            <br><span class="formula">{a3}x + {b3}y + {c3}z = {d3}</span></div>

            <div class="paso"><strong>Paso 2:</strong> Forma matricial Ax = B:
            <br><span class="formula">|{a1}  {b1}  {c1}| |x|   |{d1}|</span>
            <br><span class="formula">|{a2}  {b2}  {c2}| |y| = |{d2}|</span>
            <br><span class="formula">|{a3}  {b3}  {c3}| |z|   |{d3}|</span></div>

            <div class="paso"><strong>Paso 3:</strong> Calcular el determinante de A:
            <br><span class="formula">det(A) = {det_val:.4f}</span></div>
            """

            if abs(det_val) < 1e-10:
                raise ValueError("Sistema sin solucion unica")

            result = np.linalg.solve(A, B)
            xv, yv, zv = result

            proceso += f"""
            <div class="paso"><strong>Paso 4:</strong> Resolver el sistema usando eliminación gaussiana:
            <br>Como det(A) != 0, el sistema tiene solución única.</div>

            <div class="paso"><strong>Paso 5:</strong> Soluciones:
            <br><span class="formula">x = {xv:.4f}</span>
            <br><span class="formula">y = {yv:.4f}</span>
            <br><span class="formula">z = {zv:.4f}</span></div>

            <div class="paso"><strong>Verificacion:</strong>
            <br><span class="formula">Ec.1: {a1}({xv:.4f}) + {b1}({yv:.4f}) + {c1}({zv:.4f}) = {a1*xv + b1*yv + c1*zv:.4f} (debe ser {d1})</span>
            <br><span class="formula">Ec.2: {a2}({xv:.4f}) + {b2}({yv:.4f}) + {c2}({zv:.4f}) = {a2*xv + b2*yv + c2*zv:.4f} (debe ser {d2})</span>
            <br><span class="formula">Ec.3: {a3}({xv:.4f}) + {b3}({yv:.4f}) + {c3}({zv:.4f}) = {a3*xv + b3*yv + c3*zv:.4f} (debe ser {d3})</span></div>
            </div>
            """

            sol = f"x = {xv:.2f}, y = {yv:.2f}, z = {zv:.2f}"

        except:
            sol = "Sistema inválido"

    pdf_btn = ""
    if sol and sol != "Sistema inválido":
        pdf_btn = f"""
        <form method="POST" action="/pdf/sistema3x3" style="display:inline">
        <input type="hidden" name="a1" value="{va1}"><input type="hidden" name="b1" value="{vb1}">
        <input type="hidden" name="c1" value="{vc1}"><input type="hidden" name="d1" value="{vd1}">
        <input type="hidden" name="a2" value="{va2}"><input type="hidden" name="b2" value="{vb2}">
        <input type="hidden" name="c2" value="{vc2}"><input type="hidden" name="d2" value="{vd2}">
        <input type="hidden" name="a3" value="{va3}"><input type="hidden" name="b3" value="{vb3}">
        <input type="hidden" name="c3" value="{vc3}"><input type="hidden" name="d3" value="{vd3}">
        <button type="submit" class="btn btn-pdf">Descargar PDF</button>
        </form>
        """

    return render_template_string(f"""
<html>
<head>{ESTILO}</head>
<body>{MENU}

<div class="main">

<div class="card">
<h2>Sistema 3 x 3</h2>

<h2>Un sistema de ecuaciones 3x3 con tres ecuaciones y tres incognitas.</h2>

<form method="POST">

<p style="color:#94a3b8; font-size:14px; margin-top:10px;">Ecuación 1: a1·x + b1·y + c1·z = d1</p>
<div class="input-row">
<div class="input-group"><span class="input-label">a1</span>
<input name="a1" placeholder="ej: 2" value="{va1}"></div>
<div class="input-group"><span class="input-label">b1</span>
<input name="b1" placeholder="ej: 1" value="{vb1}"></div>
<div class="input-group"><span class="input-label">c1</span>
<input name="c1" placeholder="ej: -1" value="{vc1}"></div>
<div class="input-group"><span class="input-label">d1</span>
<input name="d1" placeholder="ej: 8" value="{vd1}"></div>
</div>

<p style="color:#94a3b8; font-size:14px; margin-top:20px;">Ecuación 2: a2·x + b2·y + c2·z = d2</p>
<div class="input-row">
<div class="input-group"><span class="input-label">a2</span>
<input name="a2" placeholder="ej: -3" value="{va2}"></div>
<div class="input-group"><span class="input-label">b2</span>
<input name="b2" placeholder="ej: -1" value="{vb2}"></div>
<div class="input-group"><span class="input-label">c2</span>
<input name="c2" placeholder="ej: 2" value="{vc2}"></div>
<div class="input-group"><span class="input-label">d2</span>
<input name="d2" placeholder="ej: -11" value="{vd2}"></div>
</div>

<p style="color:#94a3b8; font-size:14px; margin-top:20px;">Ecuación 3: a3·x + b3·y + c3·z = d3</p>
<div class="input-row">
<div class="input-group"><span class="input-label">a3</span>
<input name="a3" placeholder="ej: -2" value="{va3}"></div>
<div class="input-group"><span class="input-label">b3</span>
<input name="b3" placeholder="ej: 1" value="{vb3}"></div>
<div class="input-group"><span class="input-label">c3</span>
<input name="c3" placeholder="ej: 2" value="{vc3}"></div>
<div class="input-group"><span class="input-label">d3</span>
<input name="d3" placeholder="ej: -3" value="{vd3}"></div>
</div>

<div class="buttons-row">
<button>Resolver</button>
<a href="/sistema3x3" class="btn btn-limpiar">Limpiar</a>
</div>

</form>

</div>

{"<div class='card'>" + proceso + "<div class='resultado'>" + sol + "</div><div class='buttons-row'>" + pdf_btn + "</div></div>" if sol else ""}

</div>

</body>
</html>
""")


# ================= PDF ROUTES =================

@app.route("/pdf/lineal", methods=["POST"])
def pdf_lineal():
    tipo = request.form.get("tipo", "pendiente")
    pdf = MathPDF()
    pdf.add_page()
    pdf.add_title("Ecuacion Lineal")

    if tipo == "dos_puntos":
        x1v = float(request.form.get("x1"))
        y1v = float(request.form.get("y1"))
        x2v = float(request.form.get("x2"))
        y2v = float(request.form.get("y2"))
        m = (y2v - y1v) / (x2v - x1v)
        b = y1v - m * x1v

        pdf.add_subtitle("Datos ingresados (Dos Puntos)")
        pdf.add_data_row("Punto 1", f"({x1v}, {y1v})")
        pdf.add_data_row("Punto 2", f"({x2v}, {y2v})")
        pdf.ln(5)

        pdf.add_subtitle("Proceso de solucion")
        pdf.add_step("Paso 1:", f"Calcular la pendiente: m = (y2-y1)/(x2-x1)")
        pdf.add_step("Paso 2:", f"m = ({y2v}-{y1v})/({x2v}-{x1v}) = {y2v-y1v}/{x2v-x1v} = {m:.4f}")
        pdf.add_step("Paso 3:", f"Calcular b: b = y1 - m*x1 = {y1v} - ({m:.4f})({x1v}) = {b:.4f}")
        pdf.add_step("Paso 4:", f"Ecuacion: y = {m:.4f}x + {b:.4f}")

    elif tipo == "punto_pendiente":
        x1v = float(request.form.get("x1"))
        y1v = float(request.form.get("y1"))
        m = float(request.form.get("m"))
        b = y1v - m * x1v

        pdf.add_subtitle("Datos ingresados (Punto-Pendiente)")
        pdf.add_data_row("Punto", f"({x1v}, {y1v})")
        pdf.add_data_row("Pendiente (m)", str(m))
        pdf.ln(5)

        pdf.add_subtitle("Proceso de solucion")
        pdf.add_step("Paso 1:", f"Forma punto-pendiente: y - y1 = m(x - x1)")
        pdf.add_step("Paso 2:", f"y - {y1v} = {m}(x - {x1v})")
        pdf.add_step("Paso 3:", f"y = {m}x - {m}({x1v}) + {y1v} = {m}x + {b:.4f}")
        pdf.add_step("Paso 4:", f"Ecuacion: y = {m:.4f}x + {b:.4f}")

    elif tipo == "forma_general":
        ga = float(request.form.get("ga"))
        gb = float(request.form.get("gb"))
        gc = float(request.form.get("gc"))

        pdf.add_subtitle("Datos ingresados (Forma General)")
        pdf.add_data_row("a", str(ga))
        pdf.add_data_row("b", str(gb))
        pdf.add_data_row("c", str(gc))
        pdf.ln(5)

        pdf.add_subtitle("Proceso de solucion")
        pdf.add_step("Paso 1:", f"Forma general: {ga}x + {gb}y + {gc} = 0")

        if gb != 0:
            m = -ga / gb
            b = -gc / gb
            pdf.add_step("Paso 2:", f"Convertir: y = ({-ga}/{gb})x + ({-gc}/{gb})")
            pdf.add_step("Paso 3:", f"y = {m:.4f}x + {b:.4f}")
        else:
            m = 0
            b = 0
            x = -gc / ga
            pdf.add_step("Paso 2:", f"Recta vertical: x = {x:.4f}")
            pdf.ln(3)
            pdf.add_result(f"Recta vertical x = {x:.4f}")

            buf = io.BytesIO()
            pdf.output(buf)
            buf.seek(0)
            return send_file(buf, as_attachment=True, download_name="ecuacion_lineal.pdf", mimetype="application/pdf")

    else:
        m = float(request.form.get("m"))
        b = float(request.form.get("b"))

        pdf.add_subtitle("Datos ingresados (Pendiente + b)")
        pdf.add_data_row("Pendiente (m)", str(m))
        pdf.add_data_row("Intercepto (b)", str(b))
        pdf.ln(5)

        pdf.add_subtitle("Proceso de solucion")
        pdf.add_step("Paso 1:", f"Ecuacion: y = ({m})x + ({b})")
        pdf.add_step("Paso 2:", f"Para encontrar la raiz: 0 = ({m})x + ({b})")
        pdf.add_step("Paso 3:", f"({m})x = {-b}")

    if m != 0:
        x = -b / m
        pdf.add_step("Raiz:", f"x = {-b}/{m} = {x:.4f}")
        pdf.ln(3)
        pdf.add_result(f"x = {x:.4f}")
    else:
        x = 0
        pdf.add_step("Resultado:", f"m=0, linea horizontal en y={b}")
        pdf.ln(3)
        pdf.add_result(f"Linea horizontal y = {b}")

    fig, ax = grafica_base(title="Ecuacion Lineal", ylabel="f(x)")
    xs = np.linspace(-10, 10, 400)
    ax.plot(xs, m*xs+b, color=CHART_COLORS['accent1'], linewidth=2.5, label=f'y = {m:.1f}x + {b:.1f}', zorder=3)
    ax.fill_between(xs, m*xs+b, alpha=0.08, color=CHART_COLORS['accent1'])
    ax.scatter([x], [0], color=CHART_COLORS['highlight'], s=120, zorder=5, edgecolors='white', linewidths=1.5)
    ax.legend(loc='upper left', fontsize=10, facecolor=CHART_COLORS['surface'],
              edgecolor=CHART_COLORS['grid'], labelcolor=CHART_COLORS['text'], framealpha=0.9)
    img_path = guardar_imagen_temp(fig)

    pdf.ln(5)
    pdf.add_subtitle("Grafica")
    pdf.image(img_path, x=15, w=180)

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name="ecuacion_lineal.pdf", mimetype="application/pdf")


@app.route("/pdf/cuadratica", methods=["POST"])
def pdf_cuadratica():
    tipo = request.form.get("tipo", "general")

    pdf = MathPDF()
    pdf.add_page()
    pdf.add_title("Ecuacion Cuadratica")

    if tipo == "vertice":
        a = float(request.form.get("a"))
        h = float(request.form.get("h"))
        k = float(request.form.get("k"))
        b = -2 * a * h
        c = a * h**2 + k

        pdf.add_subtitle("Datos ingresados (Forma Vertice)")
        pdf.add_data_row("a", str(a))
        pdf.add_data_row("h", str(h))
        pdf.add_data_row("k", str(k))
        pdf.ln(5)

        pdf.add_subtitle("Proceso de solucion")
        pdf.add_step("Forma vertice:", f"y = {a}(x - {h})2 + {k}")
        pdf.add_step("Expandir:", f"y = {a}x2 + ({b:.4f})x + ({c:.4f})")
        pdf.add_step("Vertice:", f"({h}, {k})")

    elif tipo == "raices":
        a = float(request.form.get("a"))
        r1 = float(request.form.get("r1"))
        r2 = float(request.form.get("r2"))
        b = -a * (r1 + r2)
        c = a * r1 * r2

        pdf.add_subtitle("Datos ingresados (Forma Factorizada)")
        pdf.add_data_row("a", str(a))
        pdf.add_data_row("Raiz 1", str(r1))
        pdf.add_data_row("Raiz 2", str(r2))
        pdf.ln(5)

        pdf.add_subtitle("Proceso de solucion")
        pdf.add_step("Forma factorizada:", f"y = {a}(x - {r1})(x - {r2})")
        pdf.add_step("Expandir:", f"y = {a}x2 + ({b:.4f})x + ({c:.4f})")
        pdf.add_step("Raices:", f"x1 = {r1}, x2 = {r2}")

    else:
        a = float(request.form.get("a"))
        b = float(request.form.get("b"))
        c = float(request.form.get("c"))

        pdf.add_subtitle("Datos ingresados (Forma General)")
        pdf.add_data_row("a", str(a))
        pdf.add_data_row("b", str(b))
        pdf.add_data_row("c", str(c))
        pdf.ln(5)

        pdf.add_subtitle("Proceso de solucion")
        pdf.add_step("Ecuacion:", f"{a}x2 + ({b})x + ({c}) = 0")

    disc = b**2 - 4*a*c
    pdf.add_step("Discriminante:", f"D = b2 - 4ac = ({b:.4f})2 - 4({a})({c:.4f}) = {disc:.4f}")

    if disc < 0:
        pdf.add_step("Resultado:", f"D < 0, no existen raices reales")
        pdf.ln(3)
        pdf.add_result("Sin raices reales")
        x1, x2 = 0, 0
    elif disc == 0:
        x1 = -b / (2*a)
        x2 = x1
        pdf.add_step("Raiz doble:", f"x = -b/(2a) = -({b:.4f})/(2*{a}) = {x1:.4f}")
        pdf.ln(3)
        pdf.add_result(f"x = {x1:.4f} (raiz doble)")
    else:
        x1 = (-b + np.sqrt(disc)) / (2*a)
        x2 = (-b - np.sqrt(disc)) / (2*a)
        pdf.add_step("Formula:", "x = (-b +/- sqrt(D)) / (2a)")
        pdf.add_step("x1:", f"(-({b:.4f}) + sqrt({disc:.4f})) / (2*{a}) = {x1:.4f}")
        pdf.add_step("x2:", f"(-({b:.4f}) - sqrt({disc:.4f})) / (2*{a}) = {x2:.4f}")
        pdf.ln(3)
        pdf.add_result(f"x1 = {x1:.4f}, x2 = {x2:.4f}")

    vx = -b / (2*a)
    vy = a*vx**2 + b*vx + c
    pdf.add_step("Vertice:", f"({vx:.4f}, {vy:.4f})")

    fig, ax = grafica_base(title="Ecuacion Cuadratica", ylabel="f(x)")
    xs = np.linspace(-10, 10, 400)
    ys = a*xs**2 + b*xs + c
    ax.plot(xs, ys, color=CHART_COLORS['accent2'], linewidth=2.5, zorder=3)
    ax.fill_between(xs, ys, alpha=0.10, color=CHART_COLORS['accent2'])
    ax.scatter([vx], [vy], color=CHART_COLORS['warn'], s=100, zorder=5, edgecolors='white', linewidths=1.5, marker='D')
    if disc >= 0:
        roots = [x1]
        if abs(x1-x2) > 1e-9:
            roots.append(x2)
        ax.scatter(roots, [0]*len(roots), color=CHART_COLORS['highlight'], s=120, zorder=5, edgecolors='white', linewidths=1.5)
    img_path = guardar_imagen_temp(fig)

    pdf.ln(5)
    pdf.add_subtitle("Grafica")
    pdf.image(img_path, x=15, w=180)

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name="ecuacion_cuadratica.pdf", mimetype="application/pdf")


@app.route("/pdf/sistema2x2", methods=["POST"])
def pdf_sistema2x2():
    tipo = request.form.get("tipo", "estandar")

    pdf = MathPDF()
    pdf.add_page()
    pdf.add_title("Sistema de Ecuaciones 2x2")

    if tipo == "pendiente_intercepto":
        m1 = float(request.form.get("m1")); n1 = float(request.form.get("n1"))
        m2 = float(request.form.get("m2")); n2 = float(request.form.get("n2"))

        pdf.add_subtitle("Datos ingresados (Pendiente-Intercepto)")
        pdf.add_data_row("Linea 1", f"y = {m1}x + {n1}")
        pdf.add_data_row("Linea 2", f"y = {m2}x + {n2}")
        pdf.ln(5)

        x = (n2 - n1) / (m1 - m2)
        y = m1 * x + n1

        pdf.add_subtitle("Proceso de solucion")
        pdf.add_step("Paso 1:", f"Igualar: {m1}x + {n1} = {m2}x + {n2}")
        pdf.add_step("Paso 2:", f"({m1-m2:.4f})x = {n2-n1:.4f}")
        pdf.add_step("Paso 3:", f"x = {n2-n1:.4f}/{m1-m2:.4f} = {x:.4f}")
        pdf.add_step("Paso 4:", f"y = {m1}({x:.4f}) + {n1} = {y:.4f}")
        pdf.ln(3)
        pdf.add_result(f"x = {x:.4f}, y = {y:.4f}")

        fig, ax = grafica_base(title="Sistema 2x2", ylabel="y")
        xs_p = np.linspace(-10, 10, 400)
        ax.plot(xs_p, m1*xs_p+n1, color=CHART_COLORS['accent1'], linewidth=2.5, zorder=3)
        ax.plot(xs_p, m2*xs_p+n2, color=CHART_COLORS['accent3'], linewidth=2.5, zorder=3)

    else:
        a1=float(request.form.get("a1")); b1=float(request.form.get("b1")); c1=float(request.form.get("c1"))
        a2=float(request.form.get("a2")); b2=float(request.form.get("b2")); c2=float(request.form.get("c2"))

        pdf.add_subtitle("Datos ingresados (Forma Estandar)")
        pdf.add_data_row("Ecuacion 1", f"{a1}x + {b1}y = {c1}")
        pdf.add_data_row("Ecuacion 2", f"{a2}x + {b2}y = {c2}")
        pdf.ln(5)

        det = a1*b2 - a2*b1
        A = np.array([[a1,b1],[a2,b2]])
        B = np.array([c1,c2])
        x, y = np.linalg.solve(A, B)

        pdf.add_subtitle("Proceso de solucion")
        pdf.add_step("Paso 1:", f"Determinante: det = ({a1})({b2}) - ({a2})({b1}) = {det:.4f}")
        pdf.add_step("Paso 2:", f"x = ({c1}*{b2} - {c2}*{b1}) / {det:.4f} = {x:.4f}")
        pdf.add_step("Paso 3:", f"y = ({a1}*{c2} - {a2}*{c1}) / {det:.4f} = {y:.4f}")
        pdf.add_step("Verificar:", f"Ec.1: {a1}({x:.4f})+{b1}({y:.4f}) = {a1*x+b1*y:.4f}")
        pdf.add_step("", f"Ec.2: {a2}({x:.4f})+{b2}({y:.4f}) = {a2*x+b2*y:.4f}")
        pdf.ln(3)
        pdf.add_result(f"x = {x:.4f}, y = {y:.4f}")

        fig, ax = grafica_base(title="Sistema 2x2", ylabel="y")
        xs_p = np.linspace(-10, 10, 400)
        ax.plot(xs_p, (c1-a1*xs_p)/b1, color=CHART_COLORS['accent1'], linewidth=2.5, zorder=3)
        ax.plot(xs_p, (c2-a2*xs_p)/b2, color=CHART_COLORS['accent3'], linewidth=2.5, zorder=3)

    ax.scatter([x], [y], color=CHART_COLORS['highlight'], s=150, zorder=5, edgecolors='white', linewidths=2)
    img_path = guardar_imagen_temp(fig)

    pdf.ln(5)
    pdf.add_subtitle("Grafica")
    pdf.image(img_path, x=15, w=180)

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name="sistema_2x2.pdf", mimetype="application/pdf")


@app.route("/pdf/sistema3x3", methods=["POST"])
def pdf_sistema3x3():
    a1=float(request.form.get("a1")); b1=float(request.form.get("b1")); c1=float(request.form.get("c1")); d1=float(request.form.get("d1"))
    a2=float(request.form.get("a2")); b2=float(request.form.get("b2")); c2=float(request.form.get("c2")); d2=float(request.form.get("d2"))
    a3=float(request.form.get("a3")); b3=float(request.form.get("b3")); c3=float(request.form.get("c3")); d3=float(request.form.get("d3"))

    pdf = MathPDF()
    pdf.add_page()
    pdf.add_title("Sistema de Ecuaciones 3x3")

    pdf.add_subtitle("Datos ingresados")
    pdf.add_data_row("Ecuacion 1", f"{a1}x + {b1}y + {c1}z = {d1}")
    pdf.add_data_row("Ecuacion 2", f"{a2}x + {b2}y + {c2}z = {d2}")
    pdf.add_data_row("Ecuacion 3", f"{a3}x + {b3}y + {c3}z = {d3}")
    pdf.ln(5)

    A = np.array([[a1,b1,c1],[a2,b2,c2],[a3,b3,c3]])
    B = np.array([d1,d2,d3])
    det_val = np.linalg.det(A)
    result = np.linalg.solve(A, B)
    xv, yv, zv = result

    pdf.add_subtitle("Proceso de solucion")
    pdf.add_step("Paso 1:", f"Determinante: det(A) = {det_val:.4f}")
    pdf.add_step("Paso 2:", "Resolver usando eliminacion gaussiana")
    pdf.add_step("Resultado:", f"x = {xv:.4f}, y = {yv:.4f}, z = {zv:.4f}")
    pdf.add_step("Verificar:", f"Ec.1: {a1}({xv:.2f})+{b1}({yv:.2f})+{c1}({zv:.2f}) = {a1*xv+b1*yv+c1*zv:.4f}")
    pdf.add_step("", f"Ec.2: {a2}({xv:.2f})+{b2}({yv:.2f})+{c2}({zv:.2f}) = {a2*xv+b2*yv+c2*zv:.4f}")
    pdf.add_step("", f"Ec.3: {a3}({xv:.2f})+{b3}({yv:.2f})+{c3}({zv:.2f}) = {a3*xv+b3*yv+c3*zv:.4f}")
    pdf.ln(3)
    pdf.add_result(f"x = {xv:.4f}, y = {yv:.4f}, z = {zv:.4f}")

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name="sistema_3x3.pdf", mimetype="application/pdf")


# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)
