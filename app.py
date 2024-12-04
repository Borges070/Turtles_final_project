## Bibliotecas
from functools import wraps
from flask import Flask, jsonify, render_template, request, redirect, flash, url_for, make_response, abort
import os
import time

from actions import task
from actions import user
from db import DB
#

## Declarações
app = Flask(__name__)
app.secret_key = os.urandom(24).hex()
#

## Algoritmo
def inversor(valor:str) -> bool: ## Gambiarra de leves
    if valor == "0":
        return True
    return False

def authUser(email:str = "", password:str = "") -> True:
    if email == "" and password == "":
        email = request.cookies.get("email")
        password = request.cookies.get("password")

        db = DB()
        usuario = user.User(db).authenticar_usuario(password, email)
        db.fecharDB()

        if usuario:
            return True
        return False
    
    elif email != "" and password != "":
        db = DB()
        usuario = user.User(db).authenticar_usuario(password, email)
        db.fecharDB()

        if usuario:
            return True
        return False
    
    else: return False

def protetorRotas(f):
    @wraps(f)
    def authorize(*args, **kwargs):
        if not authUser():
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return authorize
            

# /* Rotas */
@app.route("/", methods=("POST", "GET"))
def login():
# Para testar várias vezes a funcionalidade de login, é necessário limpar os cookies no navegador!
# -> Serve essencialmente para bloquear as páginas (acesso restrito)

    if authUser():
        return redirect(url_for("to_do"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        
        usuario = authUser(email, password)
        if usuario:
            response = make_response(redirect(url_for("to_do")))
            response.set_cookie("email", email)
            response.set_cookie("password", password)
            return response
        else: 
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/sign-up", methods=("GET","POST"))
def sign_up():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        password = request.form["password"]

        db = DB()
        user.User(db).novo_usuario(nome, email, password)
        db.fecharDB()

        response = make_response(redirect(url_for("login")))
        response.set_cookie("email", email)
        response.set_cookie("password", password)

        return response

    return render_template("sign-up.html")

@app.route("/to-do", methods=("GET", "POST"))
@protetorRotas
def to_do():
    if request.method == "POST":
        descricao = request.form["descricao"]
        if not descricao: 
            flash("Descrição vazia!", "error") 
        else: 
            db = DB()
            task.Task(db).nova_tarefa(descricao)
            db.fecharDB()
            
            return redirect(url_for("to_do"))

    # GET
    db = DB()
    tarefas = task.Task(db).listar_tarefas()
    db.fecharDB()

    return render_template("to-do.html", tarefas = tarefas)

@app.route("/todo-edit/<int:id>", methods=["GET", "POST"])
@protetorRotas
def todoedit(id:int):
    db = DB()
    dados = task.Task(db).dados_tarefa(int(id))
    db.fecharDB()

    if request.method == "POST":
        descricao = request.form["descricao"]

        db = DB()
        task.Task(db).modificar_tarefa(id, 1, descricao)
        db.fecharDB()

        return redirect(url_for("to_do"))
        
    return render_template("todo-edit.html", dados = dados)

@app.route("/criadores")
@protetorRotas
def criadores():
    return render_template("criadores.html")
# /* FIM */

# /* API's */
@app.route("/apagar_do_db", methods=["POST"])
@protetorRotas
def apagarDoDB():
    if request.method == "POST":
        data = request.get_json(force=True)
        if data is None: return redirect(url_for("to_do"))
        data = int(data['0'])

        db = DB()
        task.Task(db).deletar_tarefa(data)
        db.fecharDB()

    return redirect(url_for("to_do"))

@app.route("/mudar_estado_do_db", methods=["POST"])
@protetorRotas
def mudarEstadoDoDB():
    if request.method == "POST":
        data = request.get_json(force=True)
        if data is None: return redirect(url_for("to_do"))

        db = DB()
        task.Task(db).modificar_tarefa(int(data['0']), 0, inversor(data['1']))
        db.fecharDB()
        
    return redirect(url_for("to_do"))

# /* FIM */ 
# "FIM DO ALGORITMO" #

if __name__ == "__main__": 
    db = DB()
    db.criarDB(db.tarefaModelagem)
    db.criarDB(db.clienteModelagem)
    db.fecharDB()
    app.run(debug=True)

# :)
## Música do Momento -> If You... - Radio Remix, Magic Box (2003)
"""
...
If you love me, if you love me now
I'll be your star
...
"""
# :)