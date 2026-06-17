from abc import ABC, abstractmethod

class ASTVisitor(ABC):
    """Abstract base class for all AST visitors."""
    
    @abstractmethod
    def visit(self, node):
        pass