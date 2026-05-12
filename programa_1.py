from flask import Flask, request, jsonify, send_file
import math
import os

app = Flask(__name__)

@app.route("/")
def home():
    return send_file("index.html")


# ======================
# LINEAL (3 FORMAS)
# ======================
@app.route("/lineal", methods=["POST"])
def lineal():
    data = request.json
    tipo = data["tipo"]

    x_vals = list(range(-10, 11))

    try:
        # ax + b = 0
        if tipo == "general":
            a = data["a"]
            b = data["b"]

            if a == 0:
                return jsonify({"resultado": "No válida"})

            y_vals = [a*x + b for x in x_vals]
            resultado = f"x = {-b/a:.2f}"

        # dos puntos
        elif tipo == "dos_puntos":
            x1, y1 = data["x1"], data["y1"]
            x2, y2 = data["x2"], data["y2"]

            if x1 == x2:
                return jsonify({"resultado": "Recta vertical"})

            m = (y2 - y1)/(x2 - x1)
            b = y1 - m*x1

            y_vals = [m*x + b for x in x_vals]
            resultado = f"y = {m:.2f}x + {b:.2f}"

        # punto pendiente
        elif tipo == "punto_pendiente":
            m = data["m"]
            x1 = data["x1"]
            y1 = data["y1"]

            b = y1 - m*x1
            y_vals = [m*x + b for x in x_vals]
            resultado = f"y = {m:.2f}x + {b:.2f}"

        else:
            return jsonify({"resultado": "Tipo inválido"})

        return jsonify({"x": x_vals, "y": y_vals, "resultado": resultado})

    except:
        return jsonify({"resultado": "Error en datos"})


# ======================
# CUADRATICA (2 FORMAS)
# ======================
@app.route("/cuadratica", methods=["POST"])
def cuadratica():
    data = request.json
    tipo = data["tipo"]

    x_vals = list(range(-10, 11))

    try:
        if tipo == "general":
            a, b, c = data["a"], data["b"], data["c"]

        elif tipo == "tres_puntos":
            x1,y1 = data["x1"], data["y1"]
            x2,y2 = data["x2"], data["y2"]
            x3,y3 = data["x3"], data["y3"]

            a = ((y3 - ((y2-y1)/(x2-x1)*(x3-x1)+y1)) / ((x3-x1)*(x3-x2)))
            b = (y2-y1)/(x2-x1) - a*(x1+x2)
            c = y1 - a*x1**2 - b*x1

        else:
            return jsonify({"resultado": "Tipo inválido"})

        if a == 0:
            return jsonify({"resultado": "No es cuadrática"})

        y_vals = [a*x**2 + b*x + c for x in x_vals]

        d = b**2 - 4*a*c

        if d > 0:
            r1 = (-b + math.sqrt(d))/(2*a)
            r2 = (-b - math.sqrt(d))/(2*a)
            res = f"Raíces: {r1:.2f}, {r2:.2f}"
        elif d == 0:
            r = -b/(2*a)
            res = f"Raíz: {r:.2f}"
        else:
            res = "No reales"

        return jsonify({"x": x_vals, "y": y_vals, "resultado": res})

    except:
        return jsonify({"resultado": "Error en datos"})


# ======================
# SISTEMA
# ======================
@app.route("/sistema", methods=["POST"])
def sistema():
    data = request.json

    a,b,c = data["a"], data["b"], data["c"]
    d,e,f = data["d"], data["e"], data["f"]

    det = a*e - b*d

    if det == 0:
        return jsonify({"resultado": "Sin solución"})

    x = (c*e - b*f)/det
    y = (a*f - c*d)/det

    # para graficar
    x_vals = list(range(-10,11))
    y1 = [(-a*x + c)/b for x in x_vals]
    y2 = [(-d*x + f)/e for x in x_vals]

    return jsonify({
        "resultado": f"x={x:.2f}, y={y:.2f}",
        "x": x_vals,
        "y1": y1,
        "y2": y2
    })


if __name__ == "__main__":
    app.run(debug=True)
