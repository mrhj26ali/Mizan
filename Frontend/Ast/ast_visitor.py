# Ast/ast_visitor.py
from abc import ABC, abstractmethod

class ASTVisitor(ABC):
    @abstractmethod
    def visit(self, node):
        pass