from typing import List, TypedDict
from sqlgood import sqlite


db = sqlite.connect('example.db')

class User(TypedDict):
    id: int
    email: str
    age: str

things = db.query('SELECT id, email, age FROM users;')

#with db.transaction() as t:
#    users: None = t.query('SELECT id, nickname FROM users;')
#    t.query('INSERT INTO users (nickname) VALUES (?)', ('Jake',))

