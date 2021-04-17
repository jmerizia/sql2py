from typing import List, TypedDict
from sqlgood import sqlite

import queries


db = sqlite.connect('example.db')

class User(TypedDict):
    id: int
    email: str
    age: int

users = db.query('SELECT id, email, age FROM users;')

print(users[0])

#print(f'There are {len(users)} users in the database:')
#for user in users:
#    print('  ', user['id'], user['email'], user['age'])
#
#res = db.query('INSERT INTO users (email, age) VALUES (?, ?)', ('Jake', 10))


#with db.transaction() as t:
#    users: None = t.query('SELECT id, nickname FROM users;')
#    t.query('INSERT INTO users (nickname) VALUES (?)', ('Jake',))

