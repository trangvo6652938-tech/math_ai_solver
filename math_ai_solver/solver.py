import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

x=sp.symbols('x')

def solve_math(expr):

    try:

        expr=expr.strip()

        if expr.startswith("plot"):

            f=sp.sympify(expr.replace("plot",""))

            xs=np.linspace(-10,10,400)

            ys=[f.subs(x,i) for i in xs]

            plt.plot(xs,ys)
            plt.grid()
            plt.title("Graph")
            plt.show()

            return "Đã vẽ đồ thị"

        if expr.startswith("diff"):

            f=expr.replace("diff","")

            return sp.diff(sp.sympify(f),x)

        if expr.startswith("integrate"):

            f=expr.replace("integrate","")

            return sp.integrate(sp.sympify(f),x)

        if expr.startswith("limit"):

            f=expr.replace("limit","")

            return sp.limit(sp.sympify(f),x,0)

        if "x" in expr:

            return sp.solve(sp.sympify(expr),x)

        return sp.simplify(expr)

    except:

        return "AI chưa hiểu dạng toán"