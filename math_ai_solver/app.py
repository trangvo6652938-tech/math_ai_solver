import matplotlib
matplotlib.use('Agg')

from flask import Flask, render_template, request
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

x, y = sp.symbols('x y')

history = []

@app.route("/", methods=["GET","POST"])
def home():

    result = ""
    graph = None

    if request.method == "POST":

        expression = request.form["math"]

        try:

            # VẼ ĐỒ THỊ
            if "plot" in expression:

                expr = expression.replace("plot(","").replace(")","")
                f = sp.sympify(expr)

                x_vals = np.linspace(-10,10,400)
                y_vals = [f.subs(x,val) for val in x_vals]

                plt.figure()
                plt.plot(x_vals,y_vals)
                plt.grid(True)

                plt.savefig("static/graph.png")
                plt.close()

                result = "Đã vẽ đồ thị"
                graph = "graph.png"

            # ĐẠO HÀM
            elif "diff" in expression:

                expr = expression.replace("diff(","").replace(")","")
                result = sp.diff(expr, x)

            # TÍCH PHÂN
            elif "integrate" in expression:

                expr = expression.replace("integrate(","").replace(")","")
                result = sp.integrate(expr, x)

            # GIỚI HẠN
            elif "limit" in expression:

                expr = expression.replace("limit(","").replace(")","")
                result = sp.limit(sp.sympify(expr), x, 0)

            # HỆ PHƯƠNG TRÌNH
            elif "system" in expression:

                eq1, eq2 = expression.replace("system(","").replace(")","").split(",")

                eq1 = sp.Eq(sp.sympify(eq1.split("=")[0]), sp.sympify(eq1.split("=")[1]))
                eq2 = sp.Eq(sp.sympify(eq2.split("=")[0]), sp.sympify(eq2.split("=")[1]))

                result = sp.solve((eq1,eq2),(x,y))

            # GIẢI PHƯƠNG TRÌNH
            elif "=" in expression:

                left, right = expression.split("=")
                eq = sp.Eq(sp.sympify(left), sp.sympify(right))
                result = sp.solve(eq)

            # MA TRẬN
            elif "Matrix" in expression:

                result = eval(expression)

            # ĐỊNH THỨC
            elif "det" in expression:

                matrix = eval(expression.replace("det",""))
                result = matrix.det()

            # TÍNH TOÁN BÌNH THƯỜNG
            else:

                result = sp.sympify(expression)

        except:

            result = "AI chưa hiểu dạng toán"

        history.append(expression + " = " + str(result))

    return render_template(
        "index.html",
        result=result,
        graph=graph,
        history=history
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
