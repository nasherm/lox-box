from TokenType import TokenType, simpleCharsMap, maybeTwoCharacterMap, whiteSpaceMap
from Token import Token
from Util import *

class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens = list()
        self.start = 0
        self.current = 0
        self.line = 1

    def isAtEnd(self):
        return self.current >= len(self.source)

    def scanTokens(self)->list:
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        self.tokens.add(Token(TokenType.EOF, "", None, self.line))
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
        else:
            error(self.line, "Unexpected character.")

    def match(self, expected):
        if self.isAtEnd(): return False
        if self.source[self.current] != expected: return False

        self.current += 1
        return True

    def advance(self):
        self.current += 1
        return source[self.current - 1]

    def addToken(self, tokenType: TokenType, literal=None):
        text = source[self.start:start.current]
        self.tokens.append(Token(tokenType, text, literal, self.line))

    def peek(self):
        if self.isAtEnd: return '\0'
        return self.source[self.current]
