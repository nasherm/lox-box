import sys
from src.plox.Scanner import Scanner

class Lox:
    def __init__(self):
        self.hadError = False

    def runFile(self, path: str):
        f = open(path, 'rb')
        self.run(str(f.read()))
        if self.hadError:
            sys.exit(65)

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
        for token in tokens:
            print(token.toString())

if __name__ == "__main__":
    args = sys.argv
    argsLen = len(args)
    lox = Lox()
    if argsLen > 2:
        print("Usage: lox [script]")
    elif argsLen == 2:
        lox.runFile(args[0])
    else:
        lox.runPrompt()
