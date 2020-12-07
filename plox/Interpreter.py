from os import environ
from plox.LoxInstance import LoxInstance
from .LoxFunction import LoxFunction
from .LoxCallable import LoxCallable
from .Expr import *
from .TokenType import *
from .RuntimeError import *
from .Stmt import *
from .Environment import Environment
from .NativeFunctions import *
from .LoxFunction import LoxFunction
from .ReturnEx import ReturnEx
from .LoxClass import LoxClass

from typing import List

class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.hadRuntimeError = False
        self.globals = Environment()
        self.environment = self.globals
        self.globals.define('clock', ClockNative())
        self.locals: dict[Expr, int] = {}

    def interpret(self, statements: List[Stmt]):
        try:
            for stmt in statements:
                self.execute(stmt)
        except RuntimeError as e:
            pass

    def execute(self, statement: Stmt):
        statement.accept(self)

    def resolve(self, expr: Expr, depth: int):
        self.locals[expr] = depth

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

    def visitLiteralExpr(self,expr: Literal):
        return expr.value

    def visitLogicalExpr(self, expr: Logical):
        left = self.evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if self.isTruthy(left):
                return left
        else:
            if not self.isTruthy(left):
                return left
        return self.evaluate(expr.right)

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def visitExpressionStmt(self,stmt:Expression):
        self.evaluate(stmt.expression)

    def visitFunctionStmt(self, stmt: Function):
        function = LoxFunction(stmt, self.environment, False)
        self.environment.define(stmt.name.lexeme, function)

    def visitClassStmt(self, stmt: Class):
        superclass = None
        if stmt.superclass is not None:
            superclass = self.evaluate(stmt.superclass)
            if not isinstance(superclass, LoxClass):
                self.runtimeError(stmt.superclass.name, "Superclass must be a class")
        self.environment.define(stmt.name.lexeme, (not None))
        if stmt.superclass is not None:
            self.environment = Environment(self.environment)
            self.environment.define("super", superclass)
        methods: dict[str, LoxFunction] = dict()
        for method in stmt.methods:
            function = LoxFunction(method, self.environment,
                (method.name.lexeme == 'init'))
            methods[method.name.lexeme] = function
        klass = LoxClass(stmt.name.lexeme, superclass, methods)
        if superclass is not None:
            self.environment = self.environment.enclosing
        self.environment.assign(stmt.name, klass)

    def visitGetExpr(self, expr: Get):
        object = self.evaluate(expr.object)
        if isinstance(object, LoxInstance):
            return object.get(expr.name)
        raise self.runtimeError(expr.name, "Only instances have properties.")

    def visitSetExpr(self, expr: Set):
        object = self.evaluate(expr.object)
        if not isinstance(object, LoxInstance):
            raise self.runtimeError(expr.name, "Only instances have fields")
        value = self.evaluate(expr.value)
        object.set(expr.name, value)
        return value

    def visitSuperExpr(self, expr: Super):
        distance = self.locals.get(expr)
        superclass = self.environment.getAt(distance, "super")
        obj = self.environment.getAt(distance-1, "this")
        method = superclass.findMethod(expr.method.lexeme)
        if method is None:
            self.runtimeError(expr.method, f'Undefined property {expr.method.lexeme}')
        return method.bind(obj)

    def visitThisExpr(self, expr: This):
        return self.lookupVariable(expr.keyword, expr)

    def visitIfStmt(self, stmt: If):
        eval_result = self.evaluate(stmt.condition)
        if self.isTruthy(eval_result):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch:
            self.execute(stmt.elseBranch)

    def visitWhileStmt(self, stmt: While):
        while self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visitPrintStmt(self,stmt:Print):
        value = self.evaluate(stmt.expression)
        print(value)

    def visitReturnStmt(self, stmt: Return):
        value = None
        if stmt.value:
            value = self.evaluate(stmt.value)
        raise ReturnEx(value)

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
        raise self.runtimeError(operator, 'Operand must be a number')

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

    def visitCallExpr(self, expr: Call):
        callee = self.evaluate(expr.callee)
        args = list()
        for arg in expr.args:
            args.append(self.evaluate(arg))

        if not isinstance(callee, LoxCallable):
            raise self.runtimeError(expr.paren, "Can only call functions and classes")

        fun: LoxCallable = callee
        if len(args) != fun.arity():
            raise self.runtimeError(
                expr.paren,
                f'Expected {fun.arity()} arguments got {len(args)}.')

        return fun.call(self, args)

    def visitVariableExpr(self,expr:Variable):
        return self.lookupVariable(expr.name, expr)

    def lookupVariable(self, name:Token,expr:Expr):
        distance = self.locals.get(expr)
        if distance is not None:
            return self.environment.getAt(distance, name.lexeme)
        else:
            return self.globals.get(name)

    def visitAssignExpr(self,expr:Assign):
        value = self.evaluate(expr.value)
        distance = self.locals.get(expr)
        if distance is not None:
            self.environment.assignAt(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)
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
                raise self.runTimeError(opType, "Operands must be two strings or two numbers")
            return left + right
        elif opType is TokenType.SLASH:
            self.checkNumberOperands(opType, left, right)
            if right == 0:
                raise self.runTimeError(opType, "Divide by zero is not allowed")
            return left / right
        elif opType is TokenType.STAR:
            self.checkNumberOperands(opType, left, right)
            return left * right
        elif opType is TokenType.BANG_EQUAL:
            # print(f"left == right = {left == right}")
            return not (left == right)
        elif opType is TokenType.EQUAL_EQUAL:
            return (left == right)

    def runtimeError(self, token, message):
        return RuntimeError(token, message, 'Interpreter')