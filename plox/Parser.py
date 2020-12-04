from typing import List
from .Expr import Expr, Logical
from .TokenType import *
from . import Util
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
            if self.match(TokenType.FUN):
                return self.function('function')
            if self.match(TokenType.VAR):
                return self.varDeclaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def function(self, kind:str):
        name = self.consume(TokenType.IDENTIFIER, f'Expect {kind} name.')
        self.consume(TokenType.LEFT_PAREN, f'Expect "(" after {kind} name.')

        def readParams(params):
            if len(params) >= 255:
                self.error(self.peek(), "Can't have more than 255 params")
            params.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name"))

        params= list()
        if not self.check(TokenType.RIGHT_PAREN):
            readParams(params)
            while self.match(TokenType.COMMA):
                readParams(params)
        
        self.consume(TokenType.RIGHT_PAREN, 'Expect ")" after parameters.')

        self.consume(TokenType.LEFT_BRACE, f'Expect "{{" before {kind} body.')
        body = self.block()
        return Function(name, params, body)

    def varDeclaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name")
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expected ';' after var declaration")
        return Var(name, initializer)

    def statement(self):
        if self.match(TokenType.FOR):
            return self.forStatement()
        if self.match(TokenType.IF):
            return self.ifStatement()
        if self.match(TokenType.PRINT):
            return self.printStatement()
        if self.match(TokenType.WHILE):
            return self.whileStatement()
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        return self.expressionStatement()

    def forStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        initializer = None
        if self.match(TokenType.VAR):
            initializer = self.varDeclaration()
        else:
            initializer = self.expressionStatement()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition")

        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after clauses")

        body = self.statement()
        if increment:
            body = Block([body, Expression(increment)])
        
        if not condition:
            condition = Literal(True)
        body = While(condition, body)

        if initializer:
            body = Block([initializer, body])
        
        return body

    def ifStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
        thenBranch = self.statement()
        elseBranch = None
        if self.match(TokenType.ELSE):
            elseBranch = self.statement()
        return If(condition, thenBranch, elseBranch)

    def whileStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()
        return While(condition, body)

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
        expr = self.orExpr()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            self.error(equals, "Invalid assignment target.")
        return expr

    def orExpr(self):
        expr = self.andExpr()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.andExpr()
            expr = Logical(expr, operator, right)
        return expr

    def andExpr(self):
        expr= self.equality()
        while self.match(TokenType.AND):
            op = self.previous()
            right = self.equality()
            expr = Logical(expr, op, right)
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
        return self.call()
    
    def call(self):
        expr = self.primary()

        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finishCall(expr)
            else:
                break

        return expr

    def finishCall(self, callee: Expr):
        args = list()
        if not self.check(TokenType.RIGHT_PAREN):
            args.append(self.expression())
            while self.match(TokenType.COMMA):
                if len(args) >= 255:
                    self.error(self.peek(), "No more than 255 arguments.")
                args.append(self.expression())
        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        return Call(callee, paren, args)

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
