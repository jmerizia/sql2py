import unittest
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

from sql2py.generate import generate


dbname_entry = 'chad'
dbname_test = 'test'
user = 'test'
password = 'asdfasdf'


def test_code_equal(expected: str, actual: str):
    a = expected
    b = actual
    lines_a, lines_b = a.split('\n'), b.split('\n')
    for line_idx, (line_a, line_b) in enumerate(zip(lines_a, lines_b)):
        for col_idx, (c_a, c_b) in enumerate(zip(line_a, line_b)):
            if c_a != c_b:
                raise ValueError(
                    f'Code does not match (line {line_idx+1}, col {col_idx+1}):\n' +
                    f'  {line_b}\n' +
                    f'  ' + (f' ' * col_idx) + '^\n'
                )
        if len(line_a) > len(line_b):
            l = len(line_b)
            raise ValueError(
                f'Unexpected end of line (line {line_idx+1}, col {l}):\n' +
                f'  {line_b}\n' +
                f'  ' + (f' ' * l) + '^\n'
            )
        if len(line_a) < len(line_b):
            l = len(line_a)
            raise ValueError(
                f'Expected end of line (line {line_idx+1}, col {l}):\n' +
                f'  {line_b}\n' +
                f'  ' + (f' ' * l) + '^\n'
            )
    if len(lines_a) > len(lines_b):
        raise ValueError(f'Unexpected end of file\n')
    if len(lines_a) < len(lines_b):
        raise ValueError(f'Expected end of file\n')


class TestPostgresql(unittest.TestCase):

    def setUp(self):
        # create test db
        self.con = psycopg2.connect(f'dbname={dbname_entry} user={user} password={password}')
        self.con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.con.cursor()
        self.cur.execute('create database test;')
        self.con.close()

        # create tables in test db
        self.con = psycopg2.connect(f'dbname={dbname_test} user={user} password={password}')
        self.con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.con.cursor()
        self.cur.execute('''
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                email TEXT not null,
                nickname TEXT,
                age INTEGER,
                is_admin BOOLEAN
            );
        ''')
        self.cur.execute('''
            INSERT INTO users (email, nickname, age, is_admin)
            VALUES ('admin@admin', 'admin', 42, TRUE);
        ''')

    def tearDown(self):
        # close the test db
        self.con.close()

        # delete the text db from the entry db
        self.con = psycopg2.connect(f'dbname={dbname_entry} user={user} password={password}')
        self.con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.con.cursor()
        self.cur.execute('drop database test;')
        self.con.close()

    def test_generate_code(self):
        with open('tests/queries.sql', 'r') as f:
            queries_sql = f.read()
        with open('tests/queries.py', 'r') as f:
            queries_py = f.read()
        generated_py = generate(queries_sql, dbname=dbname_test, user=user, password=password)
        with open('out.py', 'w') as f:
            f.write(generated_py)
        test_code_equal(queries_py, generated_py)


if __name__ == '__main__':
    unittest.main()

