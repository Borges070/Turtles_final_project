from db import DB

class Task:
    ## Declarações
    __db: DB
    #
    
    ## Métodos 
    def __init__(self, __db:DB):
        if isinstance(__db, DB):
            self.__db = __db
        else: exit(1)

    def dados_tarefa(self, id:int) -> list[str]:
        return self.__db.selectQuery("tarefa", ("descricao"), id)

    def nova_tarefa(self, descricao:str) -> int:
        if not isinstance(descricao, str):
            raise ValueError("Erro no tipo dos dados")

        return self.__db.insertQuery("tarefa", ("descricao"), (descricao))
    
    def modificar_tarefa(self, id:int, dado:str) -> None:
        self.__db.updateQuery("tarefa", "descricao", dado, id)
        
    #