from typing import List
from plox.tool.Expr import *
from plox.plox.Scanner import *
from plox.plox.TokenType import *
import plox.plox.Util as Util
class ParseError(Exception):
    def __init__(self):
        pass

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            return self.expression()
        except ParseError:
            return None

    def expression(self) -> Expr:
        return self.equality()

    def parseLeftAssocBinaryExpr(self, expr, recurse_expr, *matchArgs):
        new_expr = expr()
        while self.match(matchArgs):
            op = self.previous()
            right = expr()
            new_expr = recurse_expr(new_expr, op, right)
        return new_expr

    def equality(self):
        # expr = self.comparison(self)
        # while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
        #     op = self.previous()
        #     right = self.comparison
        #     expr = Binary(expr, op, right)
        # return expr
        return self.parseLeftAssocBinaryExpr(
            self.comparison,
            Binary,
            TokenType.BANG_EQUAL,
            TokenType.EQUAL_EQUAL)

    def comparison(self):
        # expr = self.term()
        # while self.match(TokenType.GREATER,
        #                  TokenType.GREATER_EQUAL,
        #                  TokenType.LESS,
        #                  TokenType.LESS_EQUAL):
        #     operator = self.previous()
        #     right = self.term()
        #     expr = Binary(expr, operator, right)
        #
        # return expr
        return self.parseLeftAssocBinaryExpr(
            self.term,
            Binary,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL
        )

    def term(self):
        return self.parseLeftAssocBinaryExpr(
            self.factor,
            Binary,
            TokenType.MINUS,
            TokenType.PLUS
        )

    def factor(self):
        return self.parseLeftAssocBinaryExpr(
            self.unary,
            Binary,
            TokenType.SLASH,
            TokenType.STAR
        )

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE): return Literal(False)
        if self.match(TokenType.TRUE): return Literal(True)
        if self.match(TokenType.NIL): return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if (self.match(TokenType.LEFT_PAREN)):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, 'Expect `)` after expression')
            return Grouping(expr)

        raise self.error(self.peek(), '<Parsing>Expect expression')

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type: TokenType):
        if self.isAtEnd(): return False
        return self.peek().type == type

    def consume(self, type: TokenType, message: str):
        if self.check(type): return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str):
        Util.error(token, message)
        return ParseError()

    def synchronize(self):
        self.advance()

        nextStatements = {
            TokenType.CLASS,
            TokenType.FUN,
            TokenType.VAR,
            TokenType.FOR,
            TokenType.IF,
            TokenType.WHILE,
            TokenType.PRINT,
            TokenType.RETURN
        }
        while not self.isAtEnd():
            if self.previous().type == TokenType.SEMICOLON:
                return

            if self.peek().type in nextStatements:
                return

            self.advance()

    def advance(self):
        if not self.isAtEnd(): self.current += 1
        return self.previous()

    def isAtEnd(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]
