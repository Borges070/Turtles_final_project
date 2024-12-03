## Bibliotecas
from flask import Flask, render_template, request, redirect, flash, url_for
import os
import time

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
            Task(db).nova_tarefa(descricao)
            db.fecharDB()
            
            return redirect("/to-do")

    # GET
    db = DB()
    tarefas = db.listQuery("tarefa")
    db.fecharDB()

    print(tarefas)

    return render_template("to-do.html", tarefas = tarefas)

@app.route("/apagar_do_db", methods=["POST"])
def apagarDoDB():
    if request.method == "POST":
        data = request.get_json(force=True)
        if data is None: return redirect("/to-do")
        data = int(data["id_banco"])

        db = DB()
        Task(db).deletar_tarefa(data)
        db.fecharDB()

    return redirect(url_for("to_do"))

@app.route("/mudar_estado_do_db", methods=["POST"])
def mudarEstadoDoDB():
    if request.method == "POST":
        data = request.get_json(force=True)
        if data is None: return redirect("/to-do")
        data = [int(data["id_banco"]), not bool(data["estado_banco"])]

        db = DB()
        Task(db).modificar_tarefa(data[0], 0, data[1])
        db.fecharDB()

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