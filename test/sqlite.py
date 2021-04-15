import unittest
import sqlite3
import os

from sqlgood.parsing import get_db_schema_text
from sqlgood.parsing import tokenize_sql
from sqlgood.parsing import parse_query_types


TEST_DB = 'test.db'


class TestSQLite(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        self.con = sqlite3.connect(TEST_DB)
        self.cur = self.con.cursor()
        self.cur.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY, email TEXT, nickname TEXT, age INT, is_admin BOOLEAN
            );
        ''')

    def tearDown(self):
        self.con.close()
        os.remove(TEST_DB)

    def test_tokenize1(self):
        sql = 'SELECT * FROM users WHERE id != 0 and age > 30'
        tokens = list(tokenize_sql(sql))
        expected = ['SELECT', '*', 'FROM', 'users', 'WHERE', 'id', '!=', '0', 'and', 'age', '>', '30']
        self.assertEqual(tokens, expected)

    def test_get_db_schema_text(self):
        schema = get_db_schema_text(TEST_DB)
        expected = 'CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, nickname TEXT, age INT, is_admin BOOLEAN);'
        self.assertEqual(list(tokenize_sql(schema)), list(tokenize_sql(expected)))

    def test_parse_query_types_select1(self):
        schema = get_db_schema_text(TEST_DB)
        sql = "SELECT * FROM users;"
        inputs, outputs = parse_query_types(sql, schema)
        self.assertEqual(inputs, [])
        self.assertEqual(outputs, [
            { "name": "id",       "type": "int"  },
            { "name": "email",    "type": "str"  },
            { "name": "nickname", "type": "str"  },
            { "name": "age",      "type": "int"  },
            { "name": "is_admin", "type": "bool" },
        ])

    def test_parse_query_types_select2(self):
        schema = get_db_schema_text(TEST_DB)
        sql = "SELECT email, nickname FROM users WHERE id = ?;"
        inputs, outputs = parse_query_types(sql, schema)
        self.assertEqual(inputs, [
            { "name": "in1", "type": "str" },
        ])
        self.assertEqual(outputs, [
            { "name": "email",    "type": "str"  },
            { "name": "nickname", "type": "str"  },
        ])

    def test_parse_query_types_insert1(self):
        schema = get_db_schema_text(TEST_DB)
        sql = "INSERT INTO users (email, nickname, age, is_admin) VALUES (?, ?, ?, ?);"
        inputs, outputs = parse_query_types(sql, schema)
        self.assertEqual(inputs, [
            { "name": "email",    "type": "str"  },
            { "name": "nickname", "type": "str"  },
            { "name": "age",      "type": "int"  },
            { "name": "is_admin", "type": "bool" },
        ])
        self.assertEqual(outputs, [])


if __name__ == '__main__':
    unittest.main()

