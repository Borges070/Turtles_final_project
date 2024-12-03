## Biblioteca
from db import DB
#

## Constantes
db = DB(
"""
CREATE TABLE tarefa(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
concluido BOOLEAN DEFAULT(FALSE), 
descricao VARCHAR(30)
);
"""
)
#


## Declarações
