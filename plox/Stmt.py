from typing import *
<<<<<<< HEAD:plox/Stmt.py
from .TokenType import Token
=======
from TokenType import Token
>>>>>>> 8110f251c957b682aac4980aeb2d2ca8cd22bb21:plox/tool/Stmt.py
from .Expr import *
class Stmt:
	def init(self): pass
	def accept(self,visitor): pass
class StmtVisitor:
	def visitBlockStmt(self,stmt:Stmt): pass
	def visitExpressionStmt(self,stmt:Stmt): pass
	def visitIfStmt(self,stmt:Stmt): pass
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

class If(Stmt):
	def __init__(self,condition:Expr, thenBranch:Stmt, elseBranch:Stmt):
		self.condition = condition
		self. thenBranch =  thenBranch
		self. elseBranch =  elseBranch
	def accept(self, visitor:StmtVisitor):
		return visitor.visitIfStmt(self)

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


