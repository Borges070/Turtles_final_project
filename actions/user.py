## Bibliotecas
from db import DB
#

class User:
    ## Atributos 
    __db: DB
    #

    ## Métodos
    def __init__(self, __db:DB):
        if not isinstance(__db, DB): exit(1)
        self.__db = __db

    def dados_usuario(self, senha:str, email:str = "", nome:str = "") -> list[tuple]:
        if email == "":
            return self.__db.selectQuery("usuario", ("nome",), ("nome", "senha"), (nome, senha))
        elif nome == "":
            return self.__db.selectQuery("usuario", ("email",), ("email", "senha"), (email, senha))
        else:
            return [()]
        
    def authenticar_usuario(self, senha:str, email:str) -> bool:
        query = self.__db.selectQuery("usuario", ("email",), ("email", "senha"), (email, senha))
        for user in query:
            for val in user:
                if val == email:
                    return True
        return False

    def novo_usuario(self, nome:str, email:str, senha:str) -> None:
        self.__db.insertQuery("usuario", ("nome", "email", "senha"), (nome, email, senha))
    #