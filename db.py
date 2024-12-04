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
    CREATE TABLE usuario(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(70),
    email VARCHAR(100),
    senha VARCHAR(60)
    );
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
    def insertQuery(self, tabela:str, colunas:tuple, valores:tuple) -> int:
        query = f"""
        INSERT INTO {tabela}({", ".join(colunas)}) VALUES({self._typesdata[len(valores)-1]})
        """
        print(query)

        valor = self.__db.execute(query, valores)
        self.__db.commit()

        return valor.lastrowid 
    
    def listQuery(self, tabela:str) -> list[tuple]:
        return self.__db.execute(f"SELECT * FROM {tabela}").fetchall()
    
    def updateQuery(self, tabela:str, coluna:str, valor:any, id:int) -> None:
        query:str = f"""
        UPDATE {tabela} SET {coluna} = ? WHERE id = ?
        """
        print(query)

        self.__db.execute(query, (valor, id))
        self.__db.commit()
    
    def delQuery(self, tabela:str, id:int) -> None:
        query:str = f"""
        DELETE FROM {tabela} WHERE id = ?
        """
        print(query)

        self.__db.execute(query, (id,))
        self.__db.commit()

    def selectQuery(self, tabela:str, coluna_retorno:tuple, comparativo_coluna:tuple, comparativo_valor:tuple) -> list[tuple]:
        query:str = f'SELECT {", ".join(coluna_retorno)} FROM {tabela} WHERE'
        
        for col in comparativo_coluna:
            query = query+f" {col} = ? AND"
        
        i = query.rfind("AND")
        if i != -1:
            query = query[:i] + query[i + len("AND"):]
        else:
            raise SystemError("Erro na criação da query")


        print(query)
        return self.__db.execute(query, comparativo_valor).fetchall()
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