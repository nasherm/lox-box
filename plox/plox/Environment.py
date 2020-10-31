from typing import Any
from plox.plox.TokenType import Token
from plox.plox.RuntimeError import RuntimeError

class Environment:
    def __init__(self):
        self.values = dict()

    def define(self, name: str, value: Any):
        self.values[name] = value

    def get(self, name: Token):
        if self.values.get(name.lexeme):
            return self.values[name.lexeme]
        raise RuntimeError(name, f'Undefined variable {name.lexeme}.')