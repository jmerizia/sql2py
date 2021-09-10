import argparse
import os
import sys
from typing import Counter, List, Tuple, Union, TypedDict, Literal, Optional
from dataclasses import dataclass
from parsers.PostgresqlLexer import PostgresqlLexer
from parsers.PostgresqlParser import PostgresqlParser
from antlr4 import CommonTokenStream
from antlr4.InputStream import InputStream
import psycopg2
import re


class Sql2pyError(Exception):
    pass


@dataclass
class Field:
    name: str
    data_type: str
    is_nullable: bool
    ordinal_position: int

@dataclass
class Statement:
    ttype: Literal['CREATE', 'DROP', 'SELECT', 'INSERT', 'DELETE']
    inputs: List[Field]
    outputs: List[Field]
    table_name: Optional[str]
    original: str

@dataclass
class Table:
    name: str
    columns: List[Field]


def tokenize(sql: str) -> List[str]:
    i = 0
    tokens: List[str] = []
    while i < len(sql):
        tok = None

        while sql[i] in ' \t\n\r':
            i += 1

        if sql[i] in '()[]{}$%^&*?<>:;\'\",@_+-/.':
            tok = sql[i]
            i += 1
        elif sql[i] == '!':
            i += 1
            if i < len(sql) and sql[i] == '=':
                tok = '!='
                i += 1
            else:
                tok = '!'
        elif sql[i] == '=':
            i += 1
            if i < len(sql) and sql[i] == '=':
                tok = '=='
                i += 1
            else:
                tok = '='
        elif sql[i].isalnum():
            tok = ''
            while i < len(sql) and sql[i].isalnum():
                tok += sql[i]
                i += 1
        if tok is None:
            raise ValueError(f'Unrecognized character {sql[i]}')
        tokens.append(tok)
    return tokens


def to_snake_case(sql: str) -> str:
    sql = sql.strip()
    if sql[0].isnumeric():
        sql = 'a' + sql
    words: List[str] = []
    for tok in tokenize(sql):
        if tok.isalnum():
            words.append(tok.lower())
        elif tok == '?':
            words.append('qm')
        elif tok == '*':
            words.append('all')
        elif tok == '!=':
            words.append('neq')
        elif tok == '>':
            words.append('gt')
        elif tok == '<':
            words.append('lt')
        elif tok == '@':
            words.append('at')
        elif tok == '.':
            words.append('dot')
        elif tok in ['==', '=']:
            words.append('eq')
    name = '_'.join(words)
    return name


def sql_type_to_python_type(data_type: str, is_nullable: bool) -> str:
    if data_type.upper() == 'TEXT':
        t = 'str'
    elif data_type.upper() == 'INTEGER':
        t = 'int'
    elif data_type.upper() == 'BOOLEAN':
        t = 'bool'
    else:
        raise ValueError(f'Unsupported SQL type: {data_type}')
    if is_nullable:
        return f'Optional[{t}]'
    return t


def get_type_from_sql_prim(prim: str) -> str:
    prim = prim.upper()
    if len(prim) == 0:
        raise ValueError(f'Invalid primitive type: {prim}')
    if prim in ['TRUE', 'FALSE']:
        return 'bool'
    elif prim.isdigit():
        return 'int'
    elif prim[0] == '"' and prim[-1]:
        return 'str'
    raise ValueError(f'Invalid primitive type: {prim}')


def get_schema(dbname: str, user: str, password: str) -> List[Table]:
    con = psycopg2.connect(f'dbname={dbname} user={user} password={password}')
    cur = con.cursor()
    cur.execute('''
        SELECT
            table_name,
            column_name,
            data_type,
            is_nullable,
            column_default,
            ordinal_position
        FROM information_schema.columns
        WHERE table_schema not in ('information_schema', 'pg_catalog');
    ''')
    rows = cur.fetchall()
    uniq = set()
    for table_name, column_name, data_type, is_nullable, column_default, ordinal_position in rows:
        uniq.add(table_name)
    tables: List[Table] = []
    for table_name in uniq:
        columns: List[Field] = []
        for _table_name, column_name, data_type, is_nullable, column_default, ordinal_position in rows:
            if table_name == _table_name:
                columns.append(Field(
                    name=column_name,
                    data_type=data_type,
                    is_nullable=is_nullable == 'YES',
                    ordinal_position=ordinal_position
                ))
        columns = list(sorted(columns, key=lambda x: x.ordinal_position))
        tables.append(Table(
            name=table_name,
            columns=columns
        ))
    return tables


def find_table(tables: List[Table], name: str) -> Optional[Table]:
    for table in tables:
        if table.name == name:
            return table
    return None


def find_field(fields: List[Field], name: str) -> Optional[Field]:
    for field in fields:
        if field.name == name:
            return field
    return None


def parse_simple_expr(simple_expr) -> Optional[str]:
    '''
    Returns the column name in the simple expression.

    Note: For now, we assume that simple expressions must contain a column name
    and either a variable argument (?) or primitive
    '''
    atoms = simple_expr.atom()
    assert len(atoms) == 2
    left = atoms[0]
    right = atoms[1]
    left_ID = left.ID()
    right_ID = right.ID()
    left_prim, right_prim = None, None
    if left_ID is None:
        left_prim = left.getText()
    if right_ID is None:
        right_prim = right.getText()
    if left_prim == '?':
        if right_ID is not None:
            column_name = right_ID.getText()
            return column_name
        else:
            raise ValueError('Cannot compare SQL parameter with primitive')
    elif right_prim == '?':
        if left_ID is not None:
            column_name = left_ID.getText()
            return column_name
        else:
            raise ValueError('Cannot compare SQL parameter with primitive')
    else:
        return None


def generate_function(stat: Statement, index: int) -> str:
    '''
    Generates a Python function from a parsed SQL statement.
    '''

    func_name = to_snake_case(stat.original)
    # escaped = stat.original \
    #     .replace('\n', ' ') \
    #     .replace('\r', ' ') \
    #     .replace('\'', '\\\'') \
    #     .replace('\"', '\\\"')
    with_indents = stat.original.replace('\n', '\n    ')
    params = ', '.join(f'{(field.name)}: {field.data_type}' for field in stat.inputs)
    bindings = '[' + ', '.join(field.name for field in stat.inputs) + ']'

    if len(stat.outputs) > 0:
        type_class_name = f'{stat.table_name}_' + '_'.join(field.name for field in stat.outputs) + f'_{index}'
        type_class = '@dataclass\n' + \
            f'class {type_class_name}:\n' + \
            '\n'.join(
                f'    {field.name}: {sql_type_to_python_type(field.data_type, field.is_nullable)}'
                for field in stat.outputs
            ) + '\n\n'
        return_type = f'List[{type_class_name}]'
        return_statement = f'return [{type_class_name}(' + \
             ', '.join(f'{field.name}={field.name}' for field in stat.outputs) + \
            ') for ' + ', '.join(f'{field.name}' for field in stat.outputs) + ' in cur.fetchall()]'
    else:
        type_class = ''
        return_type = 'None'
        return_statement = 'return None'

    return type_class + f'''def {func_name}({params}) -> {return_type}:
    \'\'\'
    {with_indents}
    \'\'\'

    cur = con.cursor()
    cur.execute(\'\'\'
{stat.original}
    \'\'\', {bindings})
    {return_statement}'''


def generate(queries: str, dbname: str, user: str, password: str) -> str:
    '''
    Generates a Python file from an SQL file.
    '''

    schema = get_schema(dbname=dbname, user=user, password=password)
    input_stream = InputStream(queries)
    lexer = PostgresqlLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = PostgresqlParser(token_stream)
    query_list = parser.queries()
    # print(query_list.toStringTree(parser.ruleNames))
    statements: List[Statement] = []
    for query in query_list.query():
        print(' -> ', query.toStringTree(parser.ruleNames))
        create_query = query.create_query()
        drop_query = query.drop_query()
        select_query = query.select_query()
        insert_query = query.insert_query()
        delete_query = query.delete_query()
        update_query = query.update_query()
        empty_query = query.empty_query()

        if empty_query:
            continue

        i = query.getSourceInterval()
        tokens = token_stream.getTokens(i[0], i[1]+1)
        original = queries[tokens[0].start:tokens[-1].stop+1]

        if create_query:
            table_ref = create_query.table_ref()
            table_name = table_ref.ID().getText()
            # column_defs = create_query.column_defs()
            # outputs: List[Field] = []
            # for idx, column_def in enumerate(column_defs.column_def()):
            #     column_type = column_def.column_type()
            #     tokens = [c.getText() for c in column_type.getChildren()]
            #     not_null = len(tokens) == 3 and tokens[1].lower() == 'not' and tokens[2].lower() == 'null'
            #     outputs.append(
            #         Field(
            #             name=column_def.ID().getText(),
            #             data_type=tokens[0],
            #             is_nullable=not not_null,
            #             ordinal_position=idx+1
            #         )
            #     )
            # outputs = list(sorted(outputs, key=lambda x: x.ordinal_position))
            statements.append(Statement(
                ttype='CREATE',
                inputs=[],
                outputs=[],
                table_name=table_name,
                original=original
            ))

        elif drop_query:
            statements.append(Statement(
                ttype='DROP',
                inputs=[],
                outputs=[],
                table_name=drop_query.ID().getText(),
                original=original,
            ))

        elif select_query:
            column_refs = select_query.column_refs()
            column_ref = column_refs.column_ref()
            table_ref = select_query.table_ref()
            table_name = table_ref.ID().getText()
            table = find_table(schema, table_name)
            if table is None:
                raise ValueError(f'No such table {table_name}')
            outputs: List[Field] = []
            if column_ref:
                for ref in column_ref:
                    column_name = ref.ID().getText()
                    field = find_field(table.columns, column_name)
                    if field is None:
                        raise ValueError(f'Table {table_name} does not have column named {column_name}')
                    outputs.append(field)
            else:
                children = [c.getText() for c in column_refs.getChildren()]
                assert len(children) == 1
                assert children[0] == '*'
                outputs += table.columns
            outputs = list(sorted(outputs, key=lambda x: x.ordinal_position))
            simple_expr = select_query.simple_expr()
            inputs: List[Field] = []
            column_name = parse_simple_expr(simple_expr)
            if column_name is not None:
                field = find_field(table.columns, column_name)
                if field is None:
                    raise ValueError('Invalid column name')
                inputs.append(field)
            statements.append(Statement(
                ttype='SELECT',
                inputs=inputs,
                outputs=outputs,
                table_name=table_name,
                original=original
            ))

        elif insert_query:
            table_ref = insert_query.table_ref()
            table_name = table_ref.ID().getText()

        elif delete_query:
            table_ref = delete_query.table_ref()
            table_name = table_ref.ID().getText()
            table = find_table(schema, table_name)
            if table is None:
                raise ValueError('Invalid table')
            simple_expr = delete_query.simple_expr()
            inputs: List[Field] = []
            column_name = parse_simple_expr(simple_expr)
            if column_name is not None:
                field = find_field(table.columns, column_name)
                if field is None:
                    raise ValueError('Invalid column name')
                inputs.append(field)
            statements.append(Statement(
                ttype='DELETE',
                inputs=[],
                outputs=inputs,
                table_name=table_name,
                original=original
            ))

        elif update_query:
            print('update todo')
            pass

        elif empty_query:
            pass

        else:
            raise ValueError('Invalid query type')

    functions = '\n\n\n'.join(generate_function(stat=stat, index=index) for index, stat in enumerate(statements))

    return f'''# This file has been generated by sql2py. DO NOT EDIT MANUALLY!

from typing import Callable, Generic, Optional, TypeVar, cast, List, TypedDict, Any, Literal, Dict
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dataclasses import dataclass
import psycopg2

con = psycopg2.connect('dbname=test, user=test, password=asdfasdf')
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)


{functions}


T = TypeVar('T')
def first(out: List[T]) -> Optional[T]:
    if len(out) == 0:
        return None
    return out[0]
'''



def main():
    parser = argparse.ArgumentParser(description='Convert Postgresql queries to Python functions.')
    parser.add_argument('-f', '--dbname',
                        type=str,
                        help='the Postgresql database filename',
                        required=True)
    parser.add_argument('-f', '--user',
                        type=str,
                        help='the Postgresql username',
                        required=True)
    parser.add_argument('-f', '--password',
                        type=str,
                        help='the Postgresql password',
                        required=True)
    parser.add_argument('-i', '--input',
                        type=str,
                        help='the input SQL file to parse',
                        default='queries.sql')
    parser.add_argument('-o', '--output',
                        type=str,
                        help='the output Python file to generate',
                        default='queries.py')
    args = parser.parse_args()
    with open(args.input, 'r') as f:
        sql = f.read()
    code = generate(sql, dbname=args.dbname, user=args.user, password=args.password)
    with open(args.output, 'w') as f:
        f.write(code)


if __name__ == '__main__':
    main()
