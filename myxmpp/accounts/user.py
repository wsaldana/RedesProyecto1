from dataclasses import dataclass


@dataclass
class User:
    username: str
    password: str
    state: int = 0
