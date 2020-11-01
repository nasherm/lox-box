from plox.tool.Expr import *
from plox.plox.TokenType import *
from plox.plox.RuntimeError import *
from plox.plox.Util import runtimeError
from plox.tool.Stmt import *
from typing import List
from plox.plox.Environment import Environment

class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.hadRuntimeError = False
        self.environment = Environment()

    def interpret(self, statements: List[Stmt]):
        try:
            # value = self.evaluate(expr)
            # if isinstance(value, str):
            #     value = f'"{value}"'
            # print(value)
            for stmt in statements:
                self.execute(stmt)
        except RuntimeError as e:
            runtimeError(e)
            self.hadRuntimeError = True

    def execute(self, statement: Stmt):
        statement.accept(self)

    def executeBlock(self, statements:List[Stmt], environment: Environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visitVarStmt(self,stmt:Var):
        value = None
        if stmt.initializer:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None

    def visitLiteralExpr(self,expr: Literal):
        return expr.value

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def visitExpressionStmt(self,stmt:Expression):
        self.evaluate(stmt.expression)
        return None

    def visitPrintStmt(self,stmt:Print):
        value = self.evaluate(stmt.expression)
        print(value)
        return None

    def visitBlockStmt(self,stmt:Block):
        self.executeBlock(stmt.statements, Environment(self.environment))
        return

    def visitGroupingExpr(self,expr:Grouping):
        return self.evaluate(expr.expression)

    def checkNumberOperands(self, operator, *operands):
        allFloats = True
        for operand in operands:
            allFloats &= isinstance(operand, float)
        if allFloats:
            return
        raise RuntimeError(operator, 'Operand must be a number')

    def isTruthy(self, obj):
        if isinstance(obj, bool):
            return obj
        elif obj is None:
            return False
        return True

    def visitUnaryExpr(self,expr:Unary):
        right = self.evaluate(expr.right)

        if expr.operator is TokenType.MINUS:
            self.checkNumberOperands(expr.operator, right)
            right = right * -1.0
        elif expr.operator is TokenType.BANG:
            right = not self.isTruthy(right)

        return right

    def visitVariableExpr(self,expr:Variable):
        return self.environment.get(expr.name)

    def visitAssignExpr(self,expr:Assign):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visitBinaryExpr(self,expr:Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        opType = expr.operator.type
        if opType is TokenType.GREATER:
            self.checkNumberOperands(opType, left, right)
            return left > right
        elif opType is TokenType.GREATER_EQUAL:
            self.checkNumberOperands(opType, left, right)
            return left >= right
        elif opType is TokenType.LESS:
            self.checkNumberOperands(opType, left, right)
            return left < right
        elif opType is TokenType.LESS_EQUAL:
            self.checkNumberOperands(opType, left, right)
            return left <= right
        elif opType is TokenType.MINUS:
            self.checkNumberOperands(opType, left, right)
            return left - right
        elif opType is TokenType.PLUS:
            isTwoNumbers = isinstance(left, float) and isinstance(right, float)
            isTwoStrings = isinstance(left, str) and isinstance(right, str)
            if not (isTwoStrings or isTwoNumbers):
                raise RuntimeError(opType, "Operands must be two strings or two numbers")
            return left + right
        elif opType is TokenType.SLASH:
            self.checkNumberOperands(opType, left, right)
            if right == 0:
                raise RuntimeError(opType, "Divide by zero is not allowed")
            return left / right
        elif opType is TokenType.STAR:
            self.checkNumberOperands(opType, left, right)
            return left * right
        elif opType is TokenType.BANG_EQUAL:
            # print(f"left == right = {left == right}")
            return not (left == right)
        elif opType is TokenType.EQUAL_EQUAL:
            return (left == right)
