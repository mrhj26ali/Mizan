from typing import Optional, Dict, List
from semantic.symbols import Symbol


class SemanticError(Exception):
    def __init__(self, message: str, node=None):
        line = getattr(node, 'line', '؟')
        col = getattr(node, 'column', '؟')
        super().__init__(f"❌ خطأ في السطر {line}:{col} -> {message}")


class Environment:
    def __init__(self, name: str, enclosing: Optional['Environment'] = None):
        self.name = name
        self._symbols: Dict[str, Symbol] = {}
        self.enclosing: Optional['Environment'] = enclosing

    @property
    def symbols(self) -> Dict[str, Symbol]:
        return self._symbols

    def define(self, name: str, symbol: Symbol) -> None:
        self._symbols[name] = symbol

    def define_strict(self, name: str, symbol: Symbol, node) -> None:
        if name in self._symbols:
            raise SemanticError(f"الرمز '{name}' مُعرَّف مسبقاً.", node)
        self._symbols[name] = symbol

    def resolve(self, name: str) -> Optional[Symbol]:
        if name in self._symbols:
            return self._symbols[name]
        if self.enclosing is not None:
            return self.enclosing.resolve(name)
        return None

    def resolve_local(self, name: str) -> Optional[Symbol]:
        return self._symbols.get(name)

    def is_defined(self, name: str) -> bool:
        return self.resolve(name) is not None

    def is_defined_local(self, name: str) -> bool:
        return name in self._symbols

    def depth(self) -> int:
        return 0 if self.enclosing is None else 1 + self.enclosing.depth()

    def all_symbols(self) -> Dict[str, Symbol]:
        result: Dict[str, Symbol] = {}
        if self.enclosing is not None:
            result.update(self.enclosing.all_symbols())
        result.update(self._symbols)
        return result

    def ancestor_chain(self) -> List['Environment']:
        chain = [self]
        current = self.enclosing
        while current is not None:
            chain.append(current)
            current = current.enclosing
        return chain

    def print_flat(self) -> None:
        print(f"\n{'─'*50}\n📋 النطاق: '{self.name}' (عمق {self.depth()})\n{'─'*50}")
        if not self._symbols:
            print("  (فارغ)")
        else:
            for name, sym in self._symbols.items():
                print(f"  {name:<30} {repr(sym)}")
        print(f"{'─'*50}\n")

    def __repr__(self) -> str:
        return f"<Environment '{self.name}' depth={self.depth()} symbols={len(self._symbols)}>"

    def __contains__(self, name: str) -> bool:
        return name in self._symbols