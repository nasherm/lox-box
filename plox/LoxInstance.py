from typing import Any
from . import LoxClass
from .TokenType import Token
from .RuntimeError import RuntimeError

class LoxInstance:
    def __init__(self, klass:LoxClass):
        self.klass = klass
        self.fields: dict[str, Any] = dict()

    def __repr__(self) -> str:
        return f'<class-instance {self.klass.name}>'

    def get(self, name:Token):
        if self.fields.get(name.lexeme) is not None:
            return self.fields.get(name.lexeme)

        method = self.klass.findMethod(name.lexeme)
        if method:
            return method.bind(self)

        raise self.runtimeError(name, f'Undefined property {name.lexeme}')

    def runtimeError(self, token:Token, message:str):
        return RuntimeError(token, message, "Instance Call")

    def set(self, name:Token, value:Any):
        self.fields[name.lexeme] = value
