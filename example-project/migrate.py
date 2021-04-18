import sqlite3

# This is done with the raw sqlite3 library for
# simplicity, but any database migration manager
# can be used.
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

