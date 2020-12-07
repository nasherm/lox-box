from . import LoxInstance
from .LoxCallable import LoxCallable
from .Stmt import Function
from .Environment import Environment
from .ReturnEx import ReturnEx

class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function, closure: Environment, isInitializer: bool):
        self.declaration = declaration
        self.closure = closure
        self.isInitializer = isInitializer

    def call(self, interpreter, args):
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, args[i])
        try:
            interpreter.executeBlock(self.declaration.body, environment)
        except ReturnEx as err:
            if self.isInitializer:
                return self.closure.getAt(0, "this")
            return err.value
        if self.isInitializer:
            return self.closure.getAt(0, "this")

    def arity(self) -> int:
        return len(self.declaration.params)

    def __repr__(self) -> str:
        return f'<fn {self.declaration.name.lexeme} >'

    def bind(self, instance: LoxInstance):
        environment = Environment(self.closure)
        environment.define("this", instance)
        return LoxFunction(self.declaration, environment, self.isInitializer)