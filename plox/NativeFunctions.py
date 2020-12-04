from datetime import datetime
from .LoxCallable import LoxCallable

class ClockNative(LoxCallable):
    def arity(self) -> int:
        return 0
    def call(self, interpreter, args):
        return datetime.now().microsecond /1000.
    def __repr__(self) -> str:
        return '<native fn>'

