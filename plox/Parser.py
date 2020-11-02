from typing import List
from .Expr import Expr
from .TokenType import *
from .Util import Util
from .Stmt import *

class ParseError(Exception):
    def __init__(self):
        self.hadError = False

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.hadError = False

    def parse(self):
        statements = list()
        while not self.isAtEnd():
            statements.append(self.declaration())
        return statements

    def declaration(self):
        try:
            if self.match(TokenType.VAR):
                return self.varDeclaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def varDeclaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name")
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expected ';' after var declaration")
        return Var(name, initializer)

    def statement(self):
        if self.match(TokenType.IF):
            return self.ifStatement()
        if self.match(TokenType.PRINT):
            return self.printStatement()
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        return self.expressionStatement()
    
    def printStatement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value")
        return Print(value)

    def expressionStatement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression")
        return Expression(expr)

    def block(self):
        statements = list()
        while (not self.check(TokenType.RIGHT_BRACE)) and (not self.isAtEnd()):
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expected '}' after block.")
        return statements

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self):
        expr = self.equality()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            self.error(equals, "Invalid assignment target.")
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            op = self.previous()
            right = self.comparison()
            expr = Binary(expr, op, right)
        return expr


    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GREATER,
                         TokenType.GREATER_EQUAL,
                         TokenType.LESS,
                         TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.previous()
            right = self.factor()
            expr = Binary(expr, op, right)

        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            op = self.previous()
            right = self.unary()
            expr = Binary(expr, op, right)

        return expr

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
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, 'Expect `)` after expression')
            return Grouping(expr)

        raise self.error(self.peek(), 'Expect expression')

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type: TokenType):
        if self.isAtEnd():
            return False
        return self.peek().type == type

    def consume(self, type: TokenType, message: str):
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str):
        Util.error(token, f'<Parsing>{message}')
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
