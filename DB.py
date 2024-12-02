import sqlite3

class DB:
    ## Atributos #
    def __init__(self, nome_db):
        self.nome_db = nome_db


    ## Métodos #
    
conexao = DB("armazenamento_aplicacao.db")
conexao.iniciar_db()