import sys
from Scanner import Scanner
from TokenType import *
from Util import *
from Parser import Parser
from AstPrinter import AstPrinter
from Interpreter import Interpreter

class Lox:
    def __init__(self):
        self.hadError = False
        self.hadRuntimeError = False
        self.interpreter = Interpreter()

    def runFile(self, path: str):
        f = open(path, 'r')
        self.run(str(f.read()))
        if self.hadError:
            sys.exit(65)
        if self.hadRuntimeError:
            sys.exit(70)

    def runPrompt(self):
        while True:
            inputData = input("> ")
            if inputData == ":q":
                break
            self.run(inputData)
            self.hadError = False

    def run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scanTokens()
        parser = Parser(tokens)
        statements = parser.parse()
        if parser.hadError: return
        # astPrinter = AstPrinter()
        # astPrinter.print(expr)
        self.interpreter.interpret(statements)

if __name__ == "__main__":
    args = sys.argv
    argsLen = len(args)
    lox = Lox()
    if argsLen > 2:
        print("Usage: lox [script]")
    elif argsLen == 2:
        print(args[1])
        lox.runFile(args[1])
    else:
        lox.runPrompt()

