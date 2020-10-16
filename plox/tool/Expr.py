from typing import Any
class Expr:
	pass
class Binary(Expr):
	def __init__(self,left:Expr, operator:Token, right:Expr):
		self.left = left
		self. operator =  operator
		self. right =  right
class Grouping(Expr):
	def __init__(self,expression:Expr):
		self.expression = expression
class Literal(Expr):
	def __init__(self,value:Any):
		self.value = value
class Unary(Expr):
	def __init__(self,operator:Token, right:Expr):
		self.operator = operator
		self. right =  right
