# This file has been generated by sql2py. DO NOT EDIT MANUALLY!

import sqlite3
from typing import cast, List, TypedDict, Any, Literal

con = sqlite3.connect('example.db')


class ReturnType_select_all_users(TypedDict):
    id: int
    email: str
    nickname: str
    age: int
    is_admin: bool


def select_all_from_users() -> TypedDict('select_all_users_type', { 'id': int, 'email': str, 'nickname': str, 'age': int, 'is_admin': bool }):
    '''
    Select all users
    ---
    SQL: SELECT * FROM users;
    '''

    cur = con.cursor()
    cur.execute('SELECT * FROM users;', )
    res: List[Any] = []
    output_names: List[str] = ['id', 'email', 'nickname', 'age', 'is_admin']
    for row in cur.fetchall():
        row_dict = dict()
        for k, v in zip(output_names, row):
            row_dict[k] = v
        res.append(row_dict)
    return cast(List[ReturnType_select_all_users], res)



def create_a_new_user(email: str, nickname: str, age: int, is_admin: bool) -> None:
    '''
    create a new user
    ---
    SQL: INSERT INTO users (email, nickname, age, is_admin) VALUES (?, ?, ?, ?);
    '''

    cur = con.cursor()
    cur.execute('INSERT INTO users (email, nickname, age, is_admin) VALUES (?, ?, ?, ?);', (email, nickname, age, is_admin,))
    res: List[Any] = []
    output_names: List[str] = []
    for row in cur.fetchall():
        row_dict = dict()
        for k, v in zip(output_names, row):
            row_dict[k] = v
        res.append(row_dict)
    return None

class ReturnType_determine_if_user_is_admin(TypedDict):
    is_admin: bool


def determine_if_user_is_admin(in1: str) -> List[ReturnType_determine_if_user_is_admin]:
    '''
    determine if user is admin
    ---
    SQL: SELECT is_admin FROM users WHERE id = ?;
    '''

    cur = con.cursor()
    cur.execute('SELECT is_admin FROM users WHERE id = ?;', (in1,))
    res: List[Any] = []
    output_names: List[str] = ['is_admin']
    for row in cur.fetchall():
        row_dict = dict()
        for k, v in zip(output_names, row):
            row_dict[k] = v
        res.append(row_dict)
    return cast(List[ReturnType_determine_if_user_is_admin], res)

class ReturnType_get_a_user_by_email(TypedDict):
    id: int
    email: str
    nickname: str
    age: int
    is_admin: bool


def get_a_user_by_email(in1: str) -> List[ReturnType_get_a_user_by_email]:
    '''
    get a user by email
    ---
    SQL: SELECT * FROM users WHERE email = ?;
    '''

    cur = con.cursor()
    cur.execute('SELECT * FROM users WHERE email = ?;', (in1,))
    res: List[Any] = []
    output_names: List[str] = ['id', 'email', 'nickname', 'age', 'is_admin']
    for row in cur.fetchall():
        row_dict = dict()
        for k, v in zip(output_names, row):
            row_dict[k] = v
        res.append(row_dict)
    return cast(List[ReturnType_get_a_user_by_email], res)
