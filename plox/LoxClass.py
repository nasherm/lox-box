from typing import Dict
from .LoxFunction import LoxFunction
from .LoxCallable import LoxCallable
from . import LoxInstance

class LoxClass(LoxCallable):
    def __init__(self, name:str, superclass, methods:Dict[str, LoxFunction]):
        self.name = name
        self.methods = methods
        self.superclass: LoxClass = superclass

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
        method = self.methods.get(name)
        if method is not None:
            return method
        if self.superclass is not None:
            return self.superclass.findMethod(name)