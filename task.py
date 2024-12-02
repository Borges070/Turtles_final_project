from db import DB

class Task:
    ## Declarações
    completion: bool
    description: str
    date: str
    id: int
    
    db: DB
    #
    
    ## Métodos 
    def __init__(self, db:DB):
        if isinstance(db, DB):
            self.db = db
        else: exit(1)

    def dados_tarefa(self, id:int) -> list[str]:
        return self.db.selectQuery("tarefa", ("description", "date"), id)

    def nova_tarefa(self, description:str, date:str) -> int:
        if not (isinstance(description, str) and isinstance(date, str)):
            raise ValueError("Erro no tipo dos dados")

        return self.db.insertQuery("tarefa", ("description", "date"), (description, date))
    
    def modificar_tarefa(self, id:int, tipo:int, dado:str) -> None:
        self.db.updateQuery("tarefa", 
                            "description" if tipo == 1 else "date",
                            dado,
                            id
                            )
        
    #