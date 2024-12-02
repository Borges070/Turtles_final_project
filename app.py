## Bibliotecas
from flask import Flask, render_template, request
from task import Task
from db import DB
from task import Task
#

## Declarações
app = Flask(__name__)
#

## Algoritmo

# Rotas
@app.route("/")
def home():
    return render_template("login.html")
@app.route("/sign-up")
def sign_up():
    return render_template("sign-up.html")
@app.route("/to-do")
def to_do():
    return render_template("to-do.html")
@app.route("/criadores")
def criadores():
    return render_template("criadores.html")


#
# "FIM DO ALGORITMO" #


if __name__ == "__main__": app.run(debug=True)