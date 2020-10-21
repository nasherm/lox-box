from plox.plox.TokenType import *
from plox.plox.Util import atLineError

class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens = list()
        self.start = 0
        self.current = 0
        self.line = 1
        self.keywords = {
            "and": TokenType.AND,
            "class":TokenType.CLASS,
            "else": TokenType.ELSE,
            "false":TokenType.FALSE,
            "for":TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE
        }

    def isAtEnd(self):
        return self.current >= len(self.source)

    def scanTokens(self)->list:
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scanToken(self):
        char = self.advance()
        _charMap = simpleCharsMap()
        _twoCharMap = maybeTwoCharacterMap()
        _whiteSpace = whiteSpaceMap()
        if _charMap.get(char):
            self.addToken(_charMap.get(char))
        elif _twoCharMap.get(char):
            (l, r) = _twoCharMap.get(char)
            if self.match('='):
                self.addToken(l)
            else:
                self.addToken(r)
        elif char == '/':
            if self.match('/'):
                while self.peek() != '\n' and (not self.isAtEnd):
                    self.advance
            else:
                self.addToken(TokenType.SLASH)
        elif char == '\n':
            self.line += 1
        elif _whiteSpace.get(char):
            pass
        elif char == '"':
            self.string()
        elif self.isDigit(char):
            self.number()
        elif self.isAlpha(char):
            self.identifier()
        else:
            atLineError(self.line, "Unexpected character.")

    def match(self, expected):
        if self.isAtEnd(): return False
        if self.source[self.current] != expected: return False

        self.current += 1
        return True

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def addToken(self, tokenType: TokenType, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(tokenType, text, literal, self.line))

    def peek(self):
        if self.isAtEnd(): return '\0'
        return self.source[self.current]

    def string(self):
        while (self.peek() != '"') and (not self.isAtEnd()):
            if self.peek() == '\n':
                self.line += 1;
            self.advance()

        if self.isAtEnd():
            atLineError(self.line, "Unterminated string")
            return

        # closing comma
        self.advance()

        value = self.source[self.start:self.current]
        self.addToken(TokenType.STRING, value)

    def isDigit(self, char: chr):
        return ord('0') <= ord(char) <= ord('9')

    def number(self):
        while self.isDigit(self.peek()):
            self.advance()

        if (self.peek() == '.') and self.isDigit(self.peekNext()):
            self.advance()
            while self.isDigit(self.peek()):
                self.advance()

        self.addToken(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def peekNext(self) -> chr:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def identifier(self):
        while self.isAlphaNumeric(self.peek()):
            self.advance()

        text = self.source[self.start:self.current]
        type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.addToken(type)

    def isAlpha(self, char: chr):
        return (ord('a') <= ord(char) <= ord('z'))\
               or (ord('A') <= ord(char) <= ord('Z'))\
               or (ord(char) == ord('_'))

    def isAlphaNumeric(self, char: chr):
        return self.isAlpha(char) or self.isDigit(char)
