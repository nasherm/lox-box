from enum import Enum

class Token:
    def __init__(self,
                 type=None,
                 lexeme="",
                 literal=None,
                 line=-1):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def toString(self):
        return f"TYPE={self.type} LEXEME={self.lexeme} LITERAL={self.literal}"

class TokenType(Enum):
  # Single-character tokens.
  LEFT_PAREN = 1
  RIGHT_PAREN = 2
  LEFT_BRACE = 3
  RIGHT_BRACE = 4
  COMMA = 5
  DOT = 6
  MINUS = 7
  PLUS = 8
  SEMICOLON = 9
  SLASH = 10
  STAR = 11

  # One or two character tokens.
  BANG = 12
  BANG_EQUAL = 13
  EQUAL = 14
  EQUAL_EQUAL = 15
  GREATER = 16
  GREATER_EQUAL = 17
  LESS = 18
  LESS_EQUAL = 19

  # Literals.
  IDENTIFIER = 20
  STRING = 21
  NUMBER = 22

  # Keywords.
  AND = 23
  CLASS = 24
  ELSE = 25
  FALSE = 26
  FUN = 27
  FOR = 28
  IF = 29
  NIL = 30
  OR = 31
  PRINT = 32
  RETURN = 33
  SUPER = 34
  THIS = 35
  TRUE = 36
  VAR = 37
  WHILE = 38

  EOF = 0

def simpleCharsMap():
    d = dict()
    d['('] = TokenType.LEFT_PAREN
    d[')'] = TokenType.RIGHT_PAREN
    d['{'] = TokenType.LEFT_BRACE
    d['}'] = TokenType.RIGHT_BRACE
    d[','] = TokenType.COMMA
    d['.'] = TokenType.DOT
    d['-'] = TokenType.MINUS
    d['+'] = TokenType.PLUS
    d[';'] = TokenType.SEMICOLON
    d['*'] = TokenType.STAR
    return d

def maybeTwoCharacterMap():
    d = dict()
    d['!'] = (TokenType.BANG, TokenType.BANG_EQUAL)
    d['='] = (TokenType.EQUAL, TokenType.EQUAL_EQUAL)
    d['<'] = (TokenType.LESS, TokenType.LESS_EQUAL)
    d['>'] = (TokenType.GREATER, TokenType.GREATER_EQUAL)
    return d

def whiteSpaceMap():
    d = dict()
    d[' '] = True
    d['\r'] = True
    d['\t'] = True
    return d
