from typing import List, Any, Optional, Tuple, Union
from abc import ABC
import os
import sqlite3
from functools import lru_cache

from sqlgood.parse_sqlite import get_db_schema_text
from sqlgood.parse_sqlite import parse_query_types
from sqlgood.parse_sqlite import parse_schema
from sqlgood.parse_sqlite import ParsedSchema
from sqlgood.parse_sqlite import ParsedQueryTypes


@lru_cache(maxsize=None)
def parse_query_types_cached(query_text: str, schema_text: str) -> ParsedQueryTypes:
    return parse_query_types(query_text, schema_text)


class SQLiteTransaction:
    _db: 'SQLiteDatabase'

    def __init__(self, db: 'SQLiteDatabase'):
        self._db = db

    def query(self, sql: str, params: Optional[Tuple] = None) -> Any:
        return self._db._query_in_transaction(sql, params)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is None:
            self._db._con.commit()


class SQLiteDatabase:
    _db_filename: Optional[str] = None
    _con: Optional[Any] = None
    _cur: Optional[Any] = None
    _schema_text: Optional[str] = None

    def __init__(self, db_filename: str):
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
        if self._con is not None:
            self._con.commit()
        return results

    def _query_in_transaction(self, sql: str, params: Optional[Tuple] = None) -> Any:
        inputs, outputs = parse_query_types_cached(sql, self._schema_text)
        results = []
        output_names = [c['name'] for c in outputs]
        if not params:
            params = tuple()
        if self._cur is not None:
            self._cur.execute(sql, params)
        else:
            raise ValueError('Internal: SQLiteDatabase not initialized')
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


def connect(db_filename: str) -> SQLiteDatabase:
    return SQLiteDatabase(db_filename)

