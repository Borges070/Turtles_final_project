## Bibliotecas
from flask import Flask, jsonify, render_template, request, redirect, flash, url_for
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