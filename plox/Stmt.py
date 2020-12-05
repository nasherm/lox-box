from typing import *
from .TokenType import Token
from .Expr import *
class Stmt:
	def init(self): pass
	def accept(self,visitor): pass
class StmtVisitor:
	def visitBlockStmt(self,stmt:Stmt): pass
	def visitClassStmt(self,stmt:Stmt): pass
	def visitExpressionStmt(self,stmt:Stmt): pass
	def visitIfStmt(self,stmt:Stmt): pass
	def visitFunctionStmt(self,stmt:Stmt): pass
	def visitPrintStmt(self,stmt:Stmt): pass
	def visitReturnStmt(self,stmt:Stmt): pass
	def visitVarStmt(self,stmt:Stmt): pass
	def visitWhileStmt(self,stmt:Stmt): pass

class Block(Stmt):
	def __init__(self,statements:List[Stmt]):
		self.statements = statements
	def accept(self, visitor:StmtVisitor):
		return visitor.visitBlockStmt(self)

class Class(Stmt):
	def __init__(self,name:Token, methods:List):
		self.name = name
		self. methods =  methods
	def accept(self, visitor:StmtVisitor):
		return visitor.visitClassStmt(self)

class Expression(Stmt):
	def __init__(self,expression:Expr):
		self.expression = expression
	def accept(self, visitor:StmtVisitor):
		return visitor.visitExpressionStmt(self)

class If(Stmt):
	def __init__(self,condition:Expr, thenBranch:Stmt, elseBranch:Stmt):
		self.condition = condition
		self. thenBranch =  thenBranch
		self. elseBranch =  elseBranch
	def accept(self, visitor:StmtVisitor):
		return visitor.visitIfStmt(self)

class Function(Stmt):
	def __init__(self,name:Token, params:List[Token], body:List[Stmt]):
		self.name = name
		self. params =  params
		self. body =  body
	def accept(self, visitor:StmtVisitor):
		return visitor.visitFunctionStmt(self)

class Print(Stmt):
	def __init__(self,expression:Expr):
		self.expression = expression
	def accept(self, visitor:StmtVisitor):
		return visitor.visitPrintStmt(self)

class Return(Stmt):
	def __init__(self,keyword:Token, value:Expr):
		self.keyword = keyword
		self. value =  value
	def accept(self, visitor:StmtVisitor):
		return visitor.visitReturnStmt(self)

class Var(Stmt):
	def __init__(self,name:Token, initializer:Expr):
		self.name = name
		self. initializer =  initializer
	def accept(self, visitor:StmtVisitor):
		return visitor.visitVarStmt(self)

class While(Stmt):
	def __init__(self,condition:Expr, body:Stmt):
		self.condition = condition
		self. body =  body
	def accept(self, visitor:StmtVisitor):
		return visitor.visitWhileStmt(self)


