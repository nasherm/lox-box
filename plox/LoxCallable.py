from abc import abstractmethod, ABCMeta
class LoxCallable:
    __metaclass__ = ABCMeta
    @abstractmethod
    def call(self, interpreter, args):
        raise NotImplementedError

    @abstractmethod
    def arity(self) -> int:
        raise NotImplementedError