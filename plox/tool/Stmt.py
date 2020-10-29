from typing import Any
from plox.plox.TokenType import Token
from plox.tool.Expr import *
class Stmt:
	def init(self): pass
	def accept(self,visitor): pass
class StmtVisitor:
	def visitExpressionStmt(self,stmt:Stmt): pass
	def visitPrintStmt(self,stmt:Stmt): pass
	def visitVarStmt(self,stmt:Stmt): pass

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
	def __init__(self,name:Token, initialized:Expr):
		self.name = name
		self. initialized =  initialized
	def accept(self, visitor:StmtVisitor):
		return visitor.visitVarStmt(self)


