from Task import Task
from db import DB

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

tarefa = Task(db)
id = tarefa.nova_tarefa("Oiii", "12/12/12")
tarefa.modificar_tarefa(19, 1, "voce chegou para alegrar o dia")
print(db.listQuery("tarefa"))

