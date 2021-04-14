from typing import TypedDict
from sqlgood import connect_sqlite
from typing import List


db = connect_sqlite('example.db')

class User(TypedDict):
    id: int
    name: str

with db.transaction() as t:
    users: List[User] = t.query('SELECT id, nickname FROM users;')
    t.query('INSERT INTO users (nickname) VALUES (?)', ('Jake',))

