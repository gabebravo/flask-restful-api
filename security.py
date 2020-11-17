
# safe_str_cmp : better for comparing differnt kinds of strings and encodings
from werkzeug.security import safe_str_cmp
from user import User  # syntax from <file> import <class>
from typing import Union  # for potential multiple types

# mock table of users
users = [
    User(1, 'bob', 'foo'),
    User(2, 'jenny', 'bar'),
    User(1, 'will', 'baz'),
]

# mapping functions : using set comprehensions
username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


# return a User or None
def authenticate(username: str, password: str) -> Union[User, None]:
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


#  unique to Flask JWT - passes in JWT and extracts user_id
def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
