import sys
from plox.plox.TokenType import *
from plox.plox.RuntimeError import RuntimeError

def errorPrint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def atLineError(lineNumber: int, message: str):
    report(lineNumber, "", message)

def report(lineNumber: int, where: str, message: str):
    errorPrint(f'\n[Line {lineNumber}] Error {where} : {message}\n')
    # self.hadError = True

def error(token: Token, message: str):
    if token.type == TokenType.EOF:
        report(token.line, " at end", message)
    else:
        report(token.line, f"at'{token.lexeme}'", message)

def runtimeError(error: RuntimeError):
    print(f'{error.message}\n[line {error.token.line}+]')