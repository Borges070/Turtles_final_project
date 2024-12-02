## Biblioteca
from db import DB
#

## Constantes
db = DB(
"""
CREATE TABLE tarefa(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
completion BOOLEAN DEFAULT(FALSE), 
description VARCHAR(30), 
date VARCHAR(8)
);
"""
)
#


## Declarações
