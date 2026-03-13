from flask import Flask, render_template, request
import sympy as sp
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

x, y = sp.symbols('x y')

history = []

@app.route("/", methods=["GET","POST"])
def home():

    result = ""
    graph = None

    if request.method == "POST":

        expression = request.form.get("expression","").strip()

        if expression == "":
            result = "Hãy nhập bài toán"
            return render_template("index.html", result=result, graph=None, history=history)

        expression = expression.replace("^","**")

        try:

            # VẼ ĐỒ THỊ
            if expression.startswith("plot"):

                expr = expression.replace("plot","").strip()

                f = sp.sympify(expr)

                f_lam = sp.lambdify(x,f,"numpy")

                xs = np.linspace(-10,10,400)
                ys = f_lam(xs)

                plt.figure()

                plt.plot(xs,ys)

                plt.axhline(0)
                plt.axvline(0)

                filename = "graph"+str(len(history))+".png"

                graph_path = os.path.join("static",filename)

                plt.savefig(graph_path)

                plt.close()

                graph = graph_path

                result = "Đã vẽ đồ thị"

            # GIẢI PHƯƠNG TRÌNH
            elif expression.startswith("solve"):

                expr = expression.replace("solve","").strip()

                result = sp.solve(sp.sympify(expr),x)

            # HỆ PHƯƠNG TRÌNH
            elif expression.startswith("system"):

                parts = expression.replace("system","").split(",")

                if len(parts) != 2:
                    result = "Nhập dạng: system x+y-3,x-y-1"
                else:

                    eq1 = sp.sympify(parts[0])
                    eq2 = sp.sympify(parts[1])

                    result = sp.solve((eq1,eq2),(x,y))

            # ĐẠO HÀM
            elif expression.startswith("diff"):

                expr = expression.replace("diff","").strip()

                result = sp.diff(sp.sympify(expr),x)

            # TÍCH PHÂN
            elif expression.startswith("integrate"):

                expr = expression.replace("integrate","").strip()

                result = sp.integrate(sp.sympify(expr),x)

            # GIỚI HẠN
            elif expression.startswith("limit"):

                expr = expression.replace("limit","").strip()

                result = sp.limit(sp.sympify(expr),x,0)

            # RÚT GỌN
            elif expression.startswith("simplify"):

                expr = expression.replace("simplify","").strip()

                result = sp.simplify(sp.sympify(expr))

            # MA TRẬN
            elif expression.startswith("matrix"):

                expr = expression.replace("matrix","").strip()

                result = sp.Matrix(sp.sympify(expr))
# ĐỊNH THỨC
            elif expression.startswith("det"):

                expr = expression.replace("det","").strip()

                matrix = sp.Matrix(sp.sympify(expr))

                result = matrix.det()

            # CẤP SỐ CỘNG
            elif expression.startswith("arithmetic"):

                try:

                    a1,d,n = map(float,expression.replace("arithmetic","").split(","))

                    result = a1 + (n-1)*d

                except:

                    result = "Nhập dạng: arithmetic a1,d,n"

            # CẤP SỐ NHÂN
            elif expression.startswith("geometric"):

                try:

                    a1,q,n = map(float,expression.replace("geometric","").split(","))

                    result = a1*(q**(n-1))

                except:

                    result = "Nhập dạng: geometric a1,q,n"

            # TÍNH TOÁN BÌNH THƯỜNG
            else:

                result = sp.sympify(expression)

        except Exception as e:

            result = "AI chưa hiểu dạng toán"

        history.append(expression + " = " + str(result))

        history[:] = history[-20:]

    return render_template(
        "index.html",
        result=result,
        graph=graph,
        history=history
    )

if __name__ == "__main__":
import os
    port = int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0", port=port)
           
