from .LoxCallable import LoxCallable
from .Stmt import Function
from .Environment import Environment
from .ReturnEx import ReturnEx

class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function):
        self.declaration = declaration

    def call(self, interpreter, args):
        environment = Environment(interpreter.globals)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, args[i])
        try:
            interpreter.executeBlock(self.declaration.body, environment)
        except ReturnEx as err:
            return err.value

    def arity(self) -> int:
        return len(self.declaration.params)

    def __repr__(self) -> str:
        return f'<fn {self.declaration.name.lexeme} >'

    