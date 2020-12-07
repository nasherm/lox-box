from typing import Dict
from .LoxFunction import LoxFunction
from .LoxCallable import LoxCallable
from . import LoxInstance

class LoxClass(LoxCallable):
    def __init__(self, name:str, methods:Dict[str, LoxFunction]):
        self.name = name
        self.methods = methods

    def __repr__(self):
        return f'<class {self.name}>'

    def call(self, interpreter, args):
        instance = LoxInstance.LoxInstance(self)
        initializer = self.findMethod("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, args)
        return LoxInstance.LoxInstance(self)

    def arity(self) -> int:
        initializer = self.findMethod("init")
        if initializer is None:
            return 0
        return initializer.arity()

    def findMethod(self, name:str):
        return self.methods.get(name)