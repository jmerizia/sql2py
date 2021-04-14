from typing import List, Any, Optional, Tuple
#from mypy import Plugin
from abc import ABC
import os
import sqlite3
from functools import lru_cache

from .parsing import get_db_schema_text
from .parsing import parse_query_types
from .parsing import parse_schema
from .parsing import ParsedSchema
from .parsing import ParsedQueryTypes


@lru_cache(maxsize=None)
def parse_query_types_cached(query_text: str, schema_text: str) -> ParsedQueryTypes:
    return parse_query_types(query_text, schema_text)


class SQLiteTransaction:
    _db: 'SQLiteDatabase'

    def __init__(self, db: 'SQLiteDatabase'):
        self._db = db

    def query(self, sql: str, params: Optional[Tuple] = None):
        return self._db._query_in_transaction(sql, params)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is None:
            self._db._con.commit()


class SQLiteDatabase:
    _db_filename: str
    _con: Any
    _cur: Any
    _schema_text: str

    def __init__(self, db_filename: str):
        self._db_filename = None
        self._con = None
        self._cur = None
        if not os.path.exists(db_filename):
            raise ValueError(f'No such SQLite database file \'{db_filename}\'')
        if self._db_filename == ':memory:':
            raise ValueError('The \':memory:\' database is not supported.')
        self._db_filename = db_filename
        self._con = sqlite3.connect(self._db_filename)
        self._cur = self._con.cursor()
        self._schema_text = get_db_schema_text(self._db_filename)

    def query(self, sql: str, params: Optional[Tuple] = None):
        results = self._query_in_transaction(sql)
        self._con.commit()
        return results

    def _query_in_transaction(self, sql: str, params: Optional[Tuple] = None):
        inputs, outputs = parse_query_types_cached(sql, self._schema_text)
        results = []
        output_names = [c['name'] for c in outputs]
        if not params:
            params = tuple()
        self._cur.execute(sql, params)
        for row in self._cur.fetchall():
            row_dict = dict()
            for k, v in zip(output_names, row):
                row_dict[k] = v
            results.append(row_dict)
        return results

    def transaction(self) -> SQLiteTransaction:
        return SQLiteTransaction(self)

    def __del__(self):
        if self._con:
            self._con.close()


def connect_sqlite(db_filename: str) -> SQLiteDatabase:
    return SQLiteDatabase(db_filename)


#class CustomPlugin(Plugin):
#    def get_type_analyze_hook
