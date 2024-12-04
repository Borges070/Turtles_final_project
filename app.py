## Bibliotecas
from flask import Flask, jsonify, render_template, request, redirect, flash, url_for, make_response
import os

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
    def funcao_substituta(*args, **kwargs):
        if not authUser():
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return funcao_substituta

# /* Rotas */
@app.route("/", methods=("POST", "GET"))
def login():

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

@protetorRotas
@app.route("/to-do", methods=("GET", "POST"))
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

    print("tarefas: ", tarefas)


    return render_template("to-do.html", tarefas = tarefas)

@app.route("/criadores")
# @protetorRotas
def criadores():
    return render_template("criadores.html")
# /* FIM */

# /* API's */
def apagarCookieUser():
    response = make_response()
    response.set_cookie("email", "", expires=0)
    response.set_cookie("password", "", expires=0)
    
    return response

@app.route("/apagar_do_db", methods=["POST"])
# @protetorRotas
def apagarDoDB():
    if request.method == "POST":
        data = request.get_json(force=True)
        if data is None: return redirect("/to-do")
        data = int(data['0'])

        db = DB()
        task.Task(db).deletar_tarefa(data)
        db.fecharDB()

    return redirect(url_for("to_do"))

@app.route("/mudar_estado_do_db", methods=["POST"])
# @protetorRotas
def mudarEstadoDoDB():
    if request.method == "POST":
        data = request.get_json(force=True)
        if data is None: return redirect("/to-do")

        db = DB()
        task.Task(db).modificar_tarefa(int(data['0']), 0, inversor(data['1']))
        db.fecharDB()
# Aqui eu só criei essa nova rota.
@app.route("/todo-edit", methods=["GET", "POST"])
def todoedit():
    if request.method == "POST":
        data = request.get_json(force=True)

        if data is None:
            return jsonify({"error": "Invalid request"}), 400

        id_banco = data["id_banco"]
        
        if not id_banco:
            return jsonify({"error": "Missing id_banco"}), 400

        db = DB()
        dados = Task(db).dados_tarefa(int(id_banco))
        db.fecharDB()

        if not dados:
            return jsonify({"error": "Task not found"}), 404

        return jsonify({"message": "Task fetched successfully", "dados": dados})

    # Handle GET request to render the page
    return render_template("todo-edit.html")
#Esse aqui era para o submit, mas n cheguei a testar
"""@app.route("/todo-edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    db = DB()
    dados = Task(db).dados_tarefa(id)  
    db.fecharDB()

    if request.method == "POST":
        new_description = request.form["descricao"]
        
        if not new_description:
            flash("Descrição não pode estar vazia!", "error")
            return redirect(url_for("todo-edit", id=id))
        

        #def modificar_tarefa(self, id:int, tipo:int, dado:any) -> None:
        #self.__db.updateQuery("tarefa", 
        #                      "concluido" if tipo == 0 else "descricao", 
        #                      dado, id)
    
        
        Task(db).modificar_tarefa(id, 1, new_description)  
        db.fecharDB()
        
        return redirect(url_for("to_do"))

   
    

    if not dados:
        flash("Tarefa não encontrada!", "error")
        return redirect(url_for("to_do"))

    return render_template("todo-edit.html", dados=dados)  # pra passar pro template tem q por ="""


    return redirect(url_for("to_do"))
# /* FIM */ 

# "FIM DO ALGORITMO" #


if __name__ == "__main__": 
    db = DB()
    db.criarDB(db.tarefaModelagem)
    db.criarDB(db.clienteModelagem)
    db.fecharDB()
    app.run(debug=True)