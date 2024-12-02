import sqlite3
from sqlite3 import Connection

class Task:
    completion: bool
    description: str
    date: str
    id: int
    
    db: Connection 
    #constructor:
    def __init__(self):
        pass
    
    # métodos:
    def iniciar_db(self) -> None:

        try: self.db = sqlite3.connect("armazenamento_aplicacao.db")
        except sqlite3.OperationalError as e: print("Erro Operacional ", e)
    
        try: self.db.execute(
        """
        CREATE TABLE tarefa(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        completion BOOLEAN DEFAULT(FALSE), 
        description VARCHAR(30), 
        date VARCHAR(8)
        );
        """
            )
        except sqlite3.DatabaseError as e: print("Erro no DB: ", e)
        
    def completionId(self, id:int) -> bool:
        valor = self.db.execute(
        """
        SELECT completion FROM tarefa WHERE id = ?;
        """
        , (str(id)))
        self.db.commit()

        return valor.fetchone()

    def descriptionId(self, id:int) -> str:
        valor = self.db.execute(
        """
        SELECT description FROM tarefa WHERE id = ?;
        """
        , (str(id)))
        self.db.commit()

        return valor.fetchone()
    
    def dateId(self, id:int)-> str:
        valor = self.db.execute(
        """
        SELECT date FROM tarefa WHERE id = ?;
        """
        , (str(id)))
        self.db.commit()

        return valor.fetchone()
    
    def nova_tarefa(self, completion:bool, description:str, date:str, id):
        if not (isinstance(completion, bool) and 
            isinstance(description, str) and
            isinstance(date, str)
            ):
            raise ValueError("Erro no tipo dos dados")
        
        self.db.execute("""
        INSERT INTO tarefa VALUES(?, ?, ?, ?)     
        """,
        (completion, description, date, id))
        self.db.commit()
    """
    @completion.setter
    def completion(self,new_completion ):
        if not isinstance(new_completion, bool):
            raise ValueError("task completion can only have the values true or false")
        
    @date.setter
    def dateTime(self,new_date ):
        if isinstance(new_date, str): 
            self._date = new_date  
        else:
            raise ValueError("date and time must be presented in string format")
    """     

tarefa = Task()
tarefa.iniciar_db()
# tarefa.nova_tarefa(True, "oi", "hoje", 1)

print(tarefa.dateId(1))