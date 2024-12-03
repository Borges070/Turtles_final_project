## Bibliotecas
from flask import Flask, render_template, request, redirect, flash, url_for
import os

from task import Task
from db import DB
from task import Task
#

## Declarações
app = Flask(__name__)
app.secret_key = os.urandom(24).hex()
#

## Algoritmo

# Rotas
@app.route("/", methods=("POST", "GET"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        print(email)
        print(password)

    return render_template("login.html")

@app.route("/sign-up")
def sign_up():
    return render_template("sign-up.html")
@app.route("/to-do", methods=("GET", "POST"))
def to_do():
    if request.method == "POST":
        descricao = request.form["descricao"]
        if not descricao: 
            flash("Descrição vazia!", "error") 
        else: 
            db = DB()
            Task(db).nova_tarefa(descricao, "placeholder")
            db.fecharDB()
            
            return redirect("/to-do")

    # GET
    db = DB()
    tarefas = db.listQuery("tarefa")
    db.fecharDB()

    return render_template("to-do.html", tarefas = tarefas)

@app.route("/criadores")
def criadores():
    return render_template("criadores.html")
#

# "FIM DO ALGORITMO" #


if __name__ == "__main__": 
    db = DB()
    db.criarDB(db.tarefaModelagem)
    # db.criarDB(db.clienteModelagem)
    db.fecharDB()
    app.run(debug=True)