from flask import Flask,render_template,request
from solver import solve_math

app = Flask(__name__)

history=[]

@app.route("/",methods=["GET","POST"])
def home():

    result=""
    expr=""

    if request.method=="POST":

        expr=request.form["expr"]

        result=solve_math(expr)

        history.append((expr,result))

    return render_template("index.html",
                           result=result,
                           history=history)

if __name__=="__main__":
    app.run(debug=True)