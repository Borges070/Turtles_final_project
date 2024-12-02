import sqlite3
from sqlite3 import Connection

class DB:
    ## Atributos
    _db: Connection
    _typesdata = ("?", "?, ?", "?, ?, ?", "?, ?, ?, ?")
    #

    ## Métodos
    def __init__(self, query_criacao:str) -> None:
        if (not isinstance(query_criacao, str)): exit(1)

        try: self._db = sqlite3.connect("armazenamento_aplicacao.db")
        except sqlite3.Error as e: print("Erro Operacional ", e)
    
        try: self._db.execute(query_criacao)
        except sqlite3.Error as e: print("Erro no DB: ", e) 
    
    def insertQuery(self, tabela:str, colunas:tuple[str], valores:tuple[str]) -> int:
        query = f"""
        INSERT INTO {tabela}({", ".join(colunas)}) VALUES({self._typesdata[len(valores)-1]})
        """
        print(query)

        valor = self._db.execute(query, valores)
        self._db.commit()

        return valor.lastrowid 
    
    def listQuery(self, tabela:str) -> list[str]:
        return self._db.execute(f"SELECT * FROM {tabela}").fetchall()
    
    def updateQuery(self, tabela:str, coluna:str, valor:str, id:int) -> None:
        query:str = f"""
        UPDATE {tabela} SET {coluna} = ? WHERE id = ?
        """
        print(query)

        self._db.execute(query, (valor, str(id)))
        self._db.commit()
    
    def delQuery(self, tabela:str, id:int):
        query:str = f"""
        DELETE FROM {tabela} WHERE id = ?
        """
        print(query)

        self._db.execute(query, str(id))
        self._db.commit()

    def resetarDB(self, tabela:str) -> None:
        self._db.execute(f"DROP TABLE {tabela}")
        self._db.commit()


    def selectQuery(self, tabela:str, colunas:tuple[str], id:int) -> list[str]:
        query:str = f"""
        SELECT {", ".join(colunas)} FROM {tabela} WHERE id = ?;
        """
        print(query)

        return self._db.execute(query, str(id)).fetchall()
    #