import sys
from .TokenType import *

def errorPrint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def atLineError(lineNumber: int, message: str):
    report(lineNumber, "", message)

def report(lineNumber: int, where: str, message: str):
    errorPrint(f'\n[Line {lineNumber}] Error {where} : {message}\n')

def error(token: Token, message: str, reportObj=None):
    if token.type == TokenType.EOF:
        report(token.line, " at end", message)
    else:
        report(token.line, f"at'{token.lexeme}'", message)
    if reportObj:
        reportObj.hadError = True
