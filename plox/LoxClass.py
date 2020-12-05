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
        return LoxInstance.LoxInstance(self)

    def arity(self) -> int:
        return 0

    def findMethod(self, name:str):
        return self.methods.get(name)