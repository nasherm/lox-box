from typing import Any
from .TokenType import Token
from .RuntimeError import RuntimeError

class Environment:
    def __init__(self, enclosing=None):
        self.values = dict()
        self.enclosing: Environment = enclosing

    def define(self, name: str, value: Any):
        self.values[name] = value

    def get(self, name: Token):
        if self.values.get(name.lexeme) is not None:
            return self.values[name.lexeme]
        if self.enclosing:
            return self.enclosing.get(name)
        raise RuntimeError(name, f'Undefined variable {name.lexeme}.')

    def assign(self, name: Token, value: Any):
        if self.values.get(name.lexeme) is not None:
            self.values[name.lexeme] = value
            return
        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")