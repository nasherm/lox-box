import sys
from types import resolve_bases
from .Scanner import Scanner
from .TokenType import *
from .Util import *
from .Parser import Parser
from .AstPrinter import AstPrinter
from .Interpreter import Interpreter
from .Resolver import Resolver
import traceback

class Lox:
    def __init__(self):
        self.hadError = False
        self.hadRuntimeError = False
        self.interpreter = Interpreter()

    def runFile(self, path: str):
        try:
            f = open(path, 'r')
            self.run(str(f.read()))
        except:
            print(f"Some failure occured: {sys.exc_info()[0]}")
            traceback.print_exc()

    def runPrompt(self):
        while True:
            inputData = input("> ")
            if inputData == ":q":
                break
            if inputData == ":l":
                filePath = input("Path: ")
                self.runFile(filePath)
            else:
                self.run(inputData)
                self.hadError = False

    def run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scanTokens()
        print("Tokens scanning complete")

        parser = Parser(tokens)
        statements = parser.parse()
        if parser.hadError: return
        print("Parsing complete")

        resolver = Resolver(self.interpreter)
        resolver.resolve(statements)
        if resolver.hadError: return
        print("Variable resolution complete")

        self.interpreter.interpret(statements)

def main():
    args = sys.argv
    argsLen = len(args)
    lox = Lox()
    if argsLen > 2:
        print("Usage: ./plox.py [script]")
    elif argsLen == 2:
        print(f'Executing file: {args[1]}')
        lox.runFile(args[1])
    else:
        lox.runPrompt()

