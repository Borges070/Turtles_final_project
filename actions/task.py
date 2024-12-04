from db import DB

class Task:
    ## Declarações
    __db: DB
    #
    
    ## Métodos 
    def __init__(self, __db:DB):
        if not isinstance(__db, DB): exit(1)
        self.__db = __db

    def listar_tarefas(self) -> list[tuple]:
        return self.__db.listQuery("tarefa")

    def dados_tarefa(self, id:int) -> list[tuple]:
        return self.__db.selectQuery("tarefa", ("descricao", "concluido"), ("id",), (int(id),))

    def nova_tarefa(self, descricao:str) -> int:
        if not isinstance(descricao, str):
            raise ValueError("Erro no tipo dos dados")
        return self.__db.insertQuery("tarefa", ("descricao", "concluido"), (descricao, False))

    def deletar_tarefa(self, id:int) -> None:
        self.__db.delQuery("tarefa", id)

    def modificar_tarefa(self, id:int, tipo:int, dado:any) -> None:
        self.__db.updateQuery("tarefa", 
                              "concluido" if tipo == 0 else "descricao", 
                              dado, id)
    #