from typing import *
from plox.plox.TokenType import Token
from plox.tool.Expr import *
class Stmt:
	def init(self): pass
	def accept(self,visitor): pass
class StmtVisitor:
	def visitBlockStmt(self,stmt:Stmt): pass
	def visitExpressionStmt(self,stmt:Stmt): pass
	def visitPrintStmt(self,stmt:Stmt): pass
	def visitVarStmt(self,stmt:Stmt): pass

class Block(Stmt):
	def __init__(self,statements:List[Stmt]):
		self.statements = statements
	def accept(self, visitor:StmtVisitor):
		return visitor.visitBlockStmt(self)

class Expression(Stmt):
	def __init__(self,expression:Expr):
		self.expression = expression
	def accept(self, visitor:StmtVisitor):
		return visitor.visitExpressionStmt(self)

class Print(Stmt):
	def __init__(self,expression:Expr):
		self.expression = expression
	def accept(self, visitor:StmtVisitor):
		return visitor.visitPrintStmt(self)

class Var(Stmt):
	def __init__(self,name:Token, initializer:Expr):
		self.name = name
		self. initializer =  initializer
	def accept(self, visitor:StmtVisitor):
		return visitor.visitVarStmt(self)


