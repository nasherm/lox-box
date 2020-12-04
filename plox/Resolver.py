from .Expr import *
from .Stmt import *
from .Interpreter import Interpreter
from .Util import error

from enum import Enum
class FunctionType(Enum):
    NONE = 1,
    FUNCTION = 2

class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.scopes: List[dict[str, bool]] = []
        self.currentFunction = FunctionType.NONE
        self.hadError = False

    def visitBlockStmt(self, stmt: Block):
        self.beginScope()
        self.resolveStmts(stmt.statements)
        self.endScope()

    def visitVarStmt(self, stmt: Var):
        self.declare(stmt.name)
        if stmt.initializer:
            self.resolveStmt(stmt.initializer)
        self.define(stmt.name)

    def visitVariableExpr(self, expr: Variable):
        if len(self.scopes) > 0 and (self.scopes[-1].get(expr.name.lexeme) == False):
            self.error(expr.name, "Can't read local variable in it's own initializer")
        self.resolveLocal(expr, expr.name)

    def resolveLocal(self, expr: Expr, name: Token):
        for i in range(len(self.scopes) - 1, -1, -1):
            if self.scopes[i].get(name.lexeme):
                self.interpreter.resolve(expr, len(self.scopes) -1 -i)
                return

    def visitAssignExpr(self, expr: Assign):
        self.resolveExpr(expr)
        self.resolveLocal(expr, expr.name)

    def visitFunctionStmt(self, stmt: Function):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolveFunction(stmt, FunctionType.FUNCTION)

    def resolveFunction(self, stmt: Function, type: FunctionType):
        enclosingFunction = self.currentFunction
        self.currentFunction = type
        self.beginScope()
        for param in stmt.params:
            self.declare(param)
            self.define(param)
        self.resolve(stmt.body)
        self.endScope()
        self.currentFunction = enclosingFunction

    def visitExpressionStmt(self, stmt: Expression):
        self.resolveExpr(stmt.expression)

    def visitIfStmt(self, stmt:If):
        self.resolve(stmt.condition)
        self.resolve(stmt.thenBranch)
        if stmt.elseBranch: self.resolve(stmt.elseBranch)

    def visitPrintStmt(self, stmt: Print):
        self.resolve(stmt.expression)

    def visitReturnStmt(self, stmt: Return):
        if self.currentFunction == FunctionType.NONE:
            self.error(stmt.keyword, "Can't return from top-level")

        if stmt.value:
            self.resolve(stmt.value)

    def visitWhileStmt(self, stmt: While):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)

    def visitBinaryExpr(self, expr: Binary):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visitCallExpr(self, expr: Call):
        self.resolve(expr.callee)

        for arg in expr.args:
            self.resolve(arg)

    def visitGroupingExpr(self, expr: Grouping):
        self.resolve(expr.expression)

    def visitLiteralExpr(self, expr: Literal):
        pass

    def visitLogicalExpr(self, expr: Logical):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visitUnaryExpr(self, expr: Unary):
        self.resolve(expr.right)

    def resolve(self, val):
        if isinstance(val, Stmt):
            self.resolveStmt(val)
        elif isinstance(val, Expr):
            self.resolveExpr(val)
        else:
            self.resolveStmts(val)

    def resolveStmts(self, stmts: List[Stmt]):
        for stmt in stmts:
            self.resolveStmt(stmt)

    def resolveStmt(self, stmt: Stmt):
        stmt.accept(self)

    def resolveExpr(self, expr: Expr):
        expr.accept(self)

    def beginScope(self):
        newScope : dict[str, bool] = {}
        self.scopes.append(newScope)

    def endScope(self):
        self.scopes.pop()

    def declare(self, name: Token):
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        if scope.get(name.lexeme) is not None:
            self.error(name, "Already variable with this name in scope")
        scope[name.lexeme] = False
        self.scopes[-1] = scope


    def define(self, name: Token):
        if len(self.scopes) == 0:
            return
        self.scopes[-1][name.lexeme] = True

    def error(self, token, errorMessage):
        error(token, f'<Semantic Analysis> {errorMessage}', self)
