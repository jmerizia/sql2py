from typing import List, TypedDict

import queries

# Although this type class is not necessary,
# it helps to have these types here anyways.
# If this type class is ever wrong, mypy will
# rightfully complain.
class User(TypedDict):
    id: int
    email: str
    nickname: str
    age: int
    is_admin: bool

existing = queries.get_a_user_by_email(in1='a@example.com')
if len(existing) == 0:
    queries.create_a_new_user(email='a@example.com', age=25, nickname='a', is_admin=False)

users: List[User] = queries.select_all_users()
print([user['id'] for user in users])

new_user = queries.get_a_user_by_email(in1='a@example.com')[0]
print(new_user['nickname'])
