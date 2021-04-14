# Partial implementation of parsing SQLite language:
# For full specification see https://sqlite.org/syntax/select-stmt.html

from enum import Enum
import pprint
import time
from typing import Tuple, List, Union, NamedTuple, TypedDict, NamedTuple, Iterator, Optional
import subprocess


class ParsedField(TypedDict):
    name: str
    type: str

class ParsedTable(TypedDict):
    name: str
    fields: List[ParsedField]

ParsedSchema = List[ParsedTable]

class ParsedQueryTypes(NamedTuple):
    inputs: List[ParsedField]
    outputs: List[ParsedField]


def tokenize_sql(text) -> Iterator[str]:
    l = 0
    r = 0
    special_tokens = [
        '<>', '<=', '>=', '=', '<', '>', '!=',
        '(', ')', ';', '+', '-', '*', '/', '\'',
        '.', ',', '?',
    ]

    while r < len(text):

        # skip whitespace
        while r < len(text) and text[r].isspace():
            r += 1

        # EOF
        if r >= len(text):
            pass

        # word token
        elif text[r].isalpha() or text[r] == '_':
            l = r
            r += 1
            while r < len(text) and (text[r].isalnum() or text[r] == '_'):
                r += 1
            yield text[l:r]

        # number token
        elif text[r].isnumeric():
            l = r
            r += 1
            while r < len(text) and text[r].isnumeric():
                r += 1
            yield text[l:r]

        # special token
        elif any(text[r:].startswith(tok) for tok in special_tokens):
            l = r
            for tok in special_tokens:
                if text[r:].startswith(tok):
                    r = l + len(tok)
                    yield text[l:r]
                    break

        else:
            raise ValueError(f'Invalid query: {text}\n  tokenize_sql() :: Invalid character \'{text[r]}\'')


def equal_tokens(a: List[str], b: List[str]) -> bool:
    """
    Case sensitive equality of two token streams.

    """

    if len(a) != len(b):
        return False
    for toka, tokb in zip(a, b):
        if toka != tokb:
            return False
    return True


def consume_token(tokens: str, idx: int) -> Tuple[Optional[str], int]:
    if idx == len(tokens):
        return None, idx
    else:
        return tokens[idx], idx + 1


def schema_type2type_hint(schema_type_text: str) -> str:
    """
    Map an SQLite type (from a schema) to a Python type hint.

    VARCHAR(200) -> str
    INTEGER, INT -> int
    BOOLEAN -> bool

    """

    tokens = list(tokenize_sql(schema_type_text))
    idx = 0
    tok, idx = consume_token(tokens, idx)
    if not tok:
        raise ValueError('Expected at least one token in schema type')
    low = tok.lower()
    if low.startswith('varchar'):
        return 'str'
    elif low == 'text':
        return 'str'
    elif low.startswith('int'):
        return 'int'
    elif low == 'boolean':
        return 'bool'
    else:
        raise ValueError(f'Invalid type "{tok}"')


def type_hint2schema_type(type_hint: str) -> str:
    """
    Map a Python type hint to an SQLite schema type.

    str -> VARCHAR(200)
    int -> INTEGER
    bool -> BOOLEAN

    """

    if type_hint == 'str':
        return 'VARCHAR'
    elif type_hint == 'int':
        return 'INTEGER'
    elif type_hint == 'bool':
        return 'BOOLEAN'
    else:
        raise ValueError(f'Invalid type "{type_hint}"')


def parse_schema(schema_text: str) -> ParsedSchema:
    """
    An SQL parser that takes a database schema text and parses it.

    """

    tables_text = [s.strip() for s in schema_text.strip().split(';')]
    tables_text = [s for s in tables_text if len(s) > 0]
    tables = []
    for text in tables_text:
        table_name = text.split(' ')[2].strip()
        table_fields_text = ' '.join(text.split(' ')[3:])[1:-1].split(',')
        table_fields_text = [s.strip() for s in table_fields_text]
        table_fields_text = [s for s in table_fields_text if len(s) > 0]
        fields = []
        for text in table_fields_text:
            tokens = text.split(' ')
            name = tokens[0]
            type = tokens[1]
            attributes = ' '.join(tokens[2:])
            fields.append({
                'name': name,
                'type': schema_type2type_hint(type),
            })
        tables.append({'table_name': table_name, 'fields': fields})
    return tables


def get_columns_for_table(schema_text: str, table_name: str) -> List[dict]:
    tables = parse_schema(schema_text)
    res = [table for table in tables if table['table_name'] == table_name]
    if len(res) != 1:
        raise ValueError(f'Invalid table name {table_name}')
    return res[0]['fields']


def parse_query_types(query_text: str, schema_text: str) -> ParsedQueryTypes:
    """
    An SQL parser that parses an SQL query and an SQL query
    into a list of dicts representing the input and output types respectively.

    A bit more formally:
    (
        # inputs:
        [
            {
                'name': <str>,
                'type': <str>
            },
            ...
        ],
        # outputs:
        [
            {
                'name': <str>,
                'type': <str>,
            },
            ...
        ]
    )

    """
    # TODO: This implementation is just the bare minimum to get
    #       this to work. This should eventually be expanded to a full SQL parser.

    tokens = list(tokenize_sql(query_text))
    idx = 0
    tok, idx = consume_token(tokens, idx)
    if not tok:
        raise ValueError('Invalid query: {query_text}\n  Expected statement')
    elif tok.upper() == 'SELECT':
        tok, idx = consume_token(tokens, idx)
        if not tok:
            raise ValueError(f'Invalid query: {query_text}\n  Expected token after SELECT')
        if tok == '*':
            all_columns = True
            column_names = []
        else:
            all_columns = False
            column_names = [tok]
            while True:
                tok, idx = consume_token(tokens, idx)
                if not tok:
                    break
                elif tok == ',':
                    tok, idx = consume_token(tokens, idx)
                    if not tok:
                        raise ValueError(f'Invalid query: {query_text}\n  Expected token after \',\' token')
                    column_names.append(tok)
                else:
                    idx -= 1
                    break
        tok, idx = consume_token(tokens, idx)
        if not tok or tok.upper() != 'FROM':
            raise ValueError(f'Invalid query: {query_text}\n  Expected FROM token after column names in SELECT statement')
        tok, idx = consume_token(tokens, idx)
        if not tok:
            raise ValueError(f'Invalid query: {query_text}\n  Expected table name after FROM in SELECT statement')
        table_name = tok
        schema_columns = get_columns_for_table(schema_text, table_name)
        # filter the columns we want
        if all_columns:
            chosen_columns = schema_columns
        else:
            chosen_columns = []
            for name in column_names:
                schema_column = [c for c in schema_columns if c['name'] == name]
                if len(schema_column) == 0:
                    raise ValueError(f'Invalid query: {query_text}\n  No such column \'{name}\' in the schema')
                else:
                    chosen_columns.append(schema_column[0])
        # Now, parse inputs (VERY rudimentary)
        num_inputs = query_text.count('?')
        # TODO: we should probably at least get the names of the inputs...
        input_types = [{'name': f'in{i}', 'type': 'str'} for i in range(1, num_inputs+1)]
        return input_types, chosen_columns

    elif tok.upper() == 'INSERT':
        tok, idx = consume_token(tokens, idx)
        if not tok or tok.upper() != 'INTO':
            raise ValueError(f'Invalid query: {query_text}\n  Expected INTO token after INSERT')
        tok, idx = consume_token(tokens, idx)
        if not tok:
            raise ValueError(f'Invalid query: {query_text}\n  Expected table name after INTO token')
        table_name = tok
        tok, idx = consume_token(tokens, idx)
        if not tok or tok != '(':
            raise ValueError(f'Invalid query: {query_text}\n  Expected open paren')
        column_names = []
        tok, idx = consume_token(tokens, idx)
        if not tok:
            raise ValueError(f'Invalid query: {query_text}\n  Expected column name after open paren')
        column_names.append(tok)
        while True:
            tok, idx = consume_token(tokens, idx)
            if not tok:
                raise ValueError(f'Invalid query: {query_text}\n  Expected token after first column name')
            if tok == ')':
                break
            elif tok == ',':
                tok, idx = consume_token(tokens, idx)
                if not tok:
                    raise ValueError(f'Invalid query: {query_text}\n  Expected another column name after comma')
                column_names.append(tok)
            else:
                raise ValueError(f'Invalid query: {query_text}\n  Unexpected token {tok}')
        tok, idx = consume_token(tokens, idx)
        if not tok or tok.upper() != 'VALUES':
            raise ValueError(f'Invalid query: {query_text}\n  Expected VALUES token after column specifiers')
        tok, idx = consume_token(tokens, idx)
        if not tok or tok != '(':
            raise ValueError(f'Invalid query: {query_text}\n  Expected open paren')
        values = []
        tok, idx = consume_token(tokens, idx)
        if not tok:
            raise ValueError(f'Invalid query: {query_text}\n  Expected value after open paren')
        values.append(tok)
        while True:
            tok, idx = consume_token(tokens, idx)
            if not tok:
                raise ValueError(f'Invalid query: {query_text}\n  Expected token after value')
            elif tok == ')':
                break
            elif tok == ',':
                tok, idx = consume_token(tokens, idx)
                if not tok:
                    raise ValueError(f'Invalid query: {query_text}\n  Expected another value after comma')
                values.append(tok)
            else:
                raise ValueError(f'{query_text}\n  Unexpected token {tok}')
        if len(column_names) != len(values):
            raise ValueError(f'Invalid query: {query_text}\n  Unexpected number of column names')
        schema_columns = get_columns_for_table(schema_text, table_name)
        input_types = []
        for column_name, value in zip(column_names, values):
            if value == '?':
                res = [sc for sc in schema_columns if sc['name'] == column_name]
                if len(res) != 1:
                    raise ValueError(f'Invalid query: {query_text}\n  Invalid column {column_name}')
                input_types.append(res[0])
            else:
                pass
        output_types = []
        return input_types, output_types

    else:
        raise ValueError(f'Invalid query: {query_text}\n  Invalid token \'{tok}\' at beginning of SQL query')


def get_db_schema_text(db_filename: str) -> str:
    """
    Get the schema of an SQL query.

    """

    return str(subprocess.check_output(['sqlite3', db_filename, '.schema']), 'utf-8')

