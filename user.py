from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    password: str

  # print our string object
    def __repr__(self):
        return f'<User id:{self.id}, username:{self.username}, password:{self.password}>'
