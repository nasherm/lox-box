from .Expr import *
from .Stmt import *
from .Interpreter import Interpreter
from .Util import error

from enum import Enum
class FunctionType(Enum):
    NONE = 1,
    FUNCTION = 2,
    METHOD=3,
    INITIALIZER=4

class ClassType(Enum):
    NONE=1,
    CLASS=2

class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.scopes: List[dict[str, bool]] = []
        self.currentFunction = FunctionType.NONE
        self.currentClass = ClassType.NONE
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
        self.resolve(expr.value)
        self.resolveLocal(expr, expr.name)

    def visitFunctionStmt(self, stmt: Function):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolveFunction(stmt, FunctionType.FUNCTION)

    def visitClassStmt(self, stmt: Class):
        enclosingClass = self.currentClass
        self.currentClass = ClassType.CLASS
        self.declare(stmt.name)
        self.define(stmt.name)
        if stmt.superclass is not None \
            and stmt.name.lexeme == stmt.superclass.name.lexeme:
            self.error(stmt.superclass.name, "A class can't inherit from itself")
        if stmt.superclass is not None:
            self.resolve(stmt.superclass)
        self.beginScope()
        self.scopes[-1]["this"] = True
        for method in stmt.methods:
            declaration = FunctionType.METHOD
            if method.name.lexeme == 'init':
                declaration = FunctionType.INITIALIZER
            self.resolveFunction(method, declaration)
        self.endScope()
        self.currentClass = enclosingClass

    def visitGetExpr(self, expr: Get):
        self.resolve(expr.object)

    def visitSetExpr(self, expr: Set):
        self.resolve(expr.value)
        self.resolve(expr.object)

    def visitThisExpr(self, expr: This):
        if self.currentClass == ClassType.NONE:
            self.error(expr.keyword, "Can't use 'this' outside of class")
            return
        self.resolveLocal(expr, expr.keyword)

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
            if self.currentFunction == FunctionType.INITIALIZER:
                self.error(stmt.keyword, "Can't return a value from an initializer")
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
