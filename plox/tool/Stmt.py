from typing import Any
from plox.plox.TokenType import Token
from plox.tool.Expr import *
class Stmt:
	def init(self): pass
	def accept(self,visitor): pass
class Visitor:
	def visitExpressionStmt(self,stmt:Stmt): pass
	def visitPrintStmt(self,stmt:Stmt): pass

class Expression(Stmt):
	def __init__(self,expression:Expr):
		self.expression = expression
	def accept(self, visitor:Visitor):
		return visitor.visitExpressionStmt(self)

class Print(Stmt):
	def __init__(self,expression:Expr):
		self.expression = expression
	def accept(self, visitor:Visitor):
		return visitor.visitPrintStmt(self)


