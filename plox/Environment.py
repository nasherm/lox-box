from typing import Any
from .TokenType import Token
from .RuntimeError import RuntimeError

class Environment:
    def __init__(self, enclosing=None):
        self.values: dict[str, Any] = dict()
        self.enclosing: Environment = enclosing

    def define(self, name: str, value: Any):
        self.values[name] = value

    def getAt(self, distance: int, name: str):
        return self.ancestor(distance).values.get(name)

    def ancestor(self, distance: int):
        environment = self
        for i in range(distance):
            environment = environment.enclosing
        return environment

    def get(self, name: Token):
        if self.values.get(name.lexeme) is not None:
            return self.values[name.lexeme]
        if self.enclosing:
            return self.enclosing.get(name)
        raise self.runtimeError(name, f'Undefined variable {name.lexeme}.')

    def assignAt(self, distance: int, name: Token, value: Any):
        self.ancestor(distance).values[name.lexeme] = value

    def assign(self, name: Token, value: Any):
        if self.values.get(name.lexeme) is not None:
            self.values[name.lexeme] = value
            return
        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        raise self.runtimeError(name, f"Undefined variable '{name.lexeme}'.")

    def runtimeError(self, name, message):
        return RuntimeError(name, message, 'Environment Search')