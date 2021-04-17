import sqlite3


con = sqlite3.connect('example.db')
con.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        email TEXT,
        nickname TEXT,
        age INT,
        is_admin BOOLEAN
    );
''')

