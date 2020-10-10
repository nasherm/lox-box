def errorPrint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def error(lineNumber: int, message: str):
    report(lineNumber, "", message)

def report(lineNumber: int, where: str, message: str):
    errorPrint(f'[Line {lineNumber}] Error {where} : {message}')
    #self.hadError = True


