from .LoxCallable import LoxCallable
import time

class ClockNative(LoxCallable):
    def arity(self) -> int:
        return 0
    def call(self, interpreter, args):
        return time.time()*1000.0
    def __repr__(self) -> str:
        return '<native fn>'

