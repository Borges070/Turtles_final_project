import sqlite3
from sqlite3 import Connection

class DB:
    ## Atributos
    __db: Connection
    _typesdata = ("?", "?, ?", "?, ?, ?", "?, ?, ?, ?")

    __tarefaModelagem = """
    CREATE TABLE tarefa(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    descricao VARCHAR(30),
    concluido BOOLEAN DEFAULT(FALSE)
    );
    """
    __clienteModelagem = """
    """
    #

    ## Métodos

    def __init__(self) -> None:
        try: self.__db = sqlite3.connect("armazenamento_aplicacao.db")
        except sqlite3.Error as e: print("Erro Operacional ", e)
    
    # /* Funções básicas do DB */ #
    def criarDB(self, query_criacao:str) -> None:
        if (not isinstance(query_criacao, str)): exit(1)

        try: self.__db.execute(query_criacao)
        except sqlite3.Error as e: print("Erro no DB: ", e) 

    def fecharDB(self) -> None:
        self.__db.close()

    def resetarDB(self, tabela:str) -> None:
        self.__db.execute(f"DROP TABLE {tabela}")
        self.__db.commit()
    # /* FIM  */ #

    # /* Funções Query -> Operações no DB */ #
    def insertQuery(self, tabela:str, colunas:tuple[str], valores:tuple[any]) -> int:
        query = f"""
        INSERT INTO {tabela}({", ".join(colunas)}) VALUES({self._typesdata[len(valores)-1]})
        """
        print(query)

        valor = self.__db.execute(query, valores)
        self.__db.commit()

        return valor.lastrowid 
    
    def listQuery(self, tabela:str) -> list[str]:
        return self.__db.execute(f"SELECT * FROM {tabela}").fetchall()
    
    def updateQuery(self, tabela:str, coluna:str, valor:any, id:int) -> None:
        query:str = f"""
        UPDATE {tabela} SET {coluna} = ? WHERE id = ?
        """
        print(query)

        self.__db.execute(query, (valor, id))
        self.__db.commit()
    
    def delQuery(self, tabela:str, id:int):
        query:str = f"""
        DELETE FROM {tabela} WHERE id = ?
        """
        print(query)

        self.__db.execute(query, (id,))
        self.__db.commit()

    def selectQuery(self, tabela:str, colunas:tuple[str], id:int) -> list[str]:
        query:str = f"""
        SELECT {", ".join(colunas)} FROM {tabela} WHERE id = ?;
        """
        print(query)

        return self.__db.execute(query, (id,)).fetchall()

    # /* FIM */ #
    #

    ## Get
    @property
    def tarefaModelagem(self) -> None:
        return self.__tarefaModelagem
    
    @property
    def clienteModelagem(self) -> None:
        return self.__clienteModelagem
    #