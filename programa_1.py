from flask import Flask, request, jsonify, send_from_directory
import math

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# ======================
# LINEAL
# ======================
@app.route("/lineal", methods=["POST"])
def lineal():
    data = request.json

    x_vals = list(range(-10, 11))

    try:
        m = data["m"]
        b = data["b"]

        y_vals = [m*x + b for x in x_vals]
        resultado = f"La solución es una recta con pendiente {m} y corte en {b}."

        return jsonify({
            "x": x_vals,
            "y": y_vals,
            "resultado": resultado
        })

    except:
        return jsonify({"resultado": "Error en datos"})


# ======================
# CUADRATICA
# ======================
@app.route("/cuadratica", methods=["POST"])
def cuadratica():
    data = request.json
    x_vals = list(range(-10, 11))

    try:
        a = data["a"]
        b = data["b"]
        c = data["c"]

        y_vals = [a*x**2 + b*x + c for x in x_vals]

        d = b**2 - 4*a*c

        if d > 0:
            r1 = (-b + math.sqrt(d))/(2*a)
            r2 = (-b - math.sqrt(d))/(2*a)
            res = f"La parábola corta al eje X en dos puntos: {r1:.2f} y {r2:.2f}"
        elif d == 0:
            r = -b/(2*a)
            res = f"La parábola toca el eje X en un punto: {r:.2f}"
        else:
            res = "La parábola no corta el eje X (raíces complejas)"

        return jsonify({"x": x_vals, "y": y_vals, "resultado": res})

    except:
        return jsonify({"resultado": "Error en datos"})


# ======================
# SISTEMA 2x2
# ======================
@app.route("/sistema", methods=["POST"])
def sistema():
    data = request.json

    a,b,c = data["a"], data["b"], data["c"]
    d,e,f = data["d"], data["e"], data["f"]

    det = a*e - b*d

    if det == 0:
        return jsonify({"resultado": "El sistema no tiene solución única."})

    x = (c*e - b*f)/det
    y = (a*f - c*d)/det

    x_vals = list(range(-10,11))
    y1 = [(-a*x + c)/b for x in x_vals]
    y2 = [(-d*x + f)/e for x in x_vals]

    return jsonify({
        "resultado": f"La solución del sistema es el punto de intersección: x={x:.2f}, y={y:.2f}",
        "x": x_vals,
        "y1": y1,
        "y2": y2
    })


# ======================
# SISTEMA 3x3 (GAUSS)
# ======================
@app.route("/sistema3", methods=["POST"])
def sistema3():
    data = request.json

    try:
        a1,b1,c1,d1 = data["a1"],data["b1"],data["c1"],data["d1"]
        a2,b2,c2,d2 = data["a2"],data["b2"],data["c2"],data["d2"]
        a3,b3,c3,d3 = data["a3"],data["b3"],data["c3"],data["d3"]

        # Eliminación de Gauss básica
        m1 = a2/a1
        m2 = a3/a1

        b2 -= m1*b1
        c2 -= m1*c1
        d2 -= m1*d1

        b3 -= m2*b1
        c3 -= m2*c1
        d3 -= m2*d1

        m3 = b3/b2
        c3 -= m3*c2
        d3 -= m3*d2

        z = d3/c3
        y = (d2 - c2*z)/b2
        x = (d1 - b1*y - c1*z)/a1

        return jsonify({
            "resultado": f"Solución única: x={x:.2f}, y={y:.2f}, z={z:.2f}"
        })

    except:
        return jsonify({"resultado": "Error en el sistema"})
        

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
