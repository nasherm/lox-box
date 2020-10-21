from typing import Any
from plox.plox.TokenType import *
class Expr:
	pass
	def accept(self,visitor): pass
class Visitor:
	def visitBinaryExpr(self,expr:Expr): pass
	def visitGroupingExpr(self,expr:Expr): pass
	def visitLiteralExpr(self,expr:Expr): pass
	def visitUnaryExpr(self,expr:Expr): pass

class Binary(Expr):
	def __init__(self,left:Expr, operator:Token, right:Expr):
		self.left = left
		self. operator =  operator
		self. right =  right
	def accept(self, visitor:Visitor):
		return visitor.visitBinaryExpr(self)

class Grouping(Expr):
	def __init__(self,expression:Expr):
		self.expression = expression
	def accept(self, visitor:Visitor):
		return visitor.visitGroupingExpr(self)

class Literal(Expr):
	def __init__(self,value:Any):
		self.value = value
	def accept(self, visitor:Visitor):
		return visitor.visitLiteralExpr(self)

class Unary(Expr):
	def __init__(self,operator:Token, right:Expr):
		self.operator = operator
		self. right =  right
	def accept(self, visitor:Visitor):
		return visitor.visitUnaryExpr(self)

