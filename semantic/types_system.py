from enum import Enum, auto
from typing import Optional, Dict, Set, Tuple

class MizanType(Enum):
    INT = auto(); FLOAT = auto(); BOOL = auto(); STRING = auto(); UNIT = auto(); ARRAY = auto(); ERROR = auto()

class Type:
    kind: MizanType = None
    def __eq__(self, other): return type(self) is type(other)
    def __hash__(self): return hash(type(self))
    def __repr__(self): return self.__str__()
    def is_numeric(self) -> bool: return isinstance(self, (IntType, FloatType, UnitType))
    def is_comparable(self) -> bool: return isinstance(self, (IntType, FloatType, BoolType, UnitType))

class IntType(Type):
    kind = MizanType.INT
    def __str__(self): return "صحيح"

class FloatType(Type):
    kind = MizanType.FLOAT
    def __str__(self): return "حقيقي"

class BoolType(Type):
    kind = MizanType.BOOL
    def __str__(self): return "منطقي"

class StringType(Type):
    kind = MizanType.STRING
    def __str__(self): return "نص"

class ErrorType(Type):
    kind = MizanType.ERROR
    def __str__(self): return "خطأ_دلالي"
    def __eq__(self, other): return isinstance(other, Type)
    def __hash__(self): return hash(ErrorType)

# ── Concrete Unit System (ISO 80000 & Industrial Standards) ────────
UNIT_TO_DIMENSION = {
    'متر': 'length', 'كيلوجرام': 'mass', 'جرام': 'mass', 'طن': 'mass',
    'ثانية': 'time', 'دقيقة': 'time', 'ساعة': 'time', 'يوم': 'time', 'اسبوع': 'time', 'شهر': 'time', 'مللي_ثانية': 'time',
    'لتر': 'volume', 'متر_مكعب': 'volume',
    'سيلزيوس': 'temperature', 'درجة': 'angle', 'راديان': 'angle',
    'بار': 'pressure', 'باسكال': 'pressure',
    'فولت': 'voltage', 'امبير': 'current', 'أوم': 'resistance',
    'واط': 'power', 'كيلو_واط': 'power', 'جول': 'energy',
    'هرتز': 'frequency', 'دورة': 'count', 'عدد': 'count',
    'لوكس': 'illuminance', 'سيمنز': 'conductance', 'NTU': 'turbidity', 'جزء_في_المليون': 'concentration',
    'بت': 'data', 'بايت': 'data',
    'بالمئة': 'dimensionless', 'لا_وحدة': 'dimensionless',
}

UNIT_TO_ATOMS = {
    # "Famous Mixes" map to their exact decoupled atoms so they are compatible with manual composition
    'دورة_في_الدقيقة': {'دورة', 'دقيقة'}, 'دورة_في_الثانية': {'دورة', 'ثانية'},
    'لتر_في_الدقيقة': {'لتر', 'دقيقة'}, 'لتر_في_الساعة': {'لتر', 'ساعة'},
    'متر_مكعب_في_الساعة': {'متر_مكعب', 'ساعة'}, 'متر_في_الثانية': {'متر', 'ثانية'},
    'متر_في_الدقيقة': {'متر', 'دقيقة'}, 'بار_في_الثانية': {'بار', 'ثانية'},
    'سيلزيوس_في_الثانية': {'سيلزيوس', 'ثانية'},
}

class UnitType(Type):
    """Physical unit type with Canonical Base Unit Atoms tracking."""
    kind = MizanType.UNIT
    BUILTIN_UNITS = {
        # Base Atoms
        'متر', 'لتر', 'متر_مكعب', 'كيلوجرام', 'جرام', 'طن',
        'ثانية', 'دقيقة', 'ساعة', 'يوم', 'اسبوع', 'شهر', 'مللي_ثانية',
        'سيلزيوس', 'درجة', 'راديان', 'بار', 'باسكال', 'فولت', 'امبير', 'أوم',
        'واط', 'كيلو_واط', 'جول', 'هرتز', 'دورة', 'عدد',
        'لوكس', 'سيمنز', 'NTU', 'جزء_في_المليون', 'بت', 'بايت',
        'بالمئة', 'لا_وحدة',
        # Famous Mixes
        'دورة_في_الدقيقة', 'دورة_في_الثانية', 'لتر_في_الدقيقة', 'لتر_في_الساعة',
        'متر_مكعب_في_الساعة', 'متر_في_الثانية', 'متر_في_الدقيقة',
        'بار_في_الثانية', 'سيلزيوس_في_الثانية',
    }

    def __init__(self, unit_name: str, dimension: Optional[Dict[str, int]] = None, atoms: Optional[Set[str]] = None):
        self.unit_name = unit_name
        self.is_builtin = unit_name in self.BUILTIN_UNITS
        self.dimension = dimension or {}
        self.atoms = atoms or UNIT_TO_ATOMS.get(unit_name, {unit_name})

    def __str__(self): return f"وحدة({self.unit_name})"
    def __eq__(self, other):
        return isinstance(other, UnitType) and self.unit_name == other.unit_name
    def __hash__(self): return hash(('UnitType', self.unit_name))

class ArrayType(Type):
    kind = MizanType.ARRAY
    def __init__(self, element_type: Type, size: int):
        self.element_type = element_type
        self.size = size
    def __str__(self): return f"{self.element_type}[{self.size}]"
    def __eq__(self, other):
        return (isinstance(other, ArrayType) and self.element_type == other.element_type
                and self.size == other.size)
    def __hash__(self): return hash(('ArrayType', self.element_type, self.size))

INT_TYPE = IntType()
FLOAT_TYPE = FloatType()
BOOL_TYPE = BoolType()
STRING_TYPE = StringType()
ERROR_TYPE = ErrorType()

_ARITHMETIC_TABLE = {
    (MizanType.INT, '+', MizanType.INT): MizanType.INT,
    (MizanType.INT, '-', MizanType.INT): MizanType.INT,
    (MizanType.INT, '*', MizanType.INT): MizanType.INT,
    (MizanType.INT, '/', MizanType.INT): MizanType.FLOAT,
    (MizanType.INT, '%', MizanType.INT): MizanType.INT,
    (MizanType.FLOAT, '+', MizanType.FLOAT): MizanType.FLOAT,
    (MizanType.FLOAT, '-', MizanType.FLOAT): MizanType.FLOAT,
    (MizanType.FLOAT, '*', MizanType.FLOAT): MizanType.FLOAT,
    (MizanType.FLOAT, '/', MizanType.FLOAT): MizanType.FLOAT,
    (MizanType.FLOAT, '%', MizanType.FLOAT): MizanType.FLOAT,
    (MizanType.INT, '+', MizanType.FLOAT): MizanType.FLOAT,
    (MizanType.INT, '-', MizanType.FLOAT): MizanType.FLOAT,
    (MizanType.INT, '*', MizanType.FLOAT): MizanType.FLOAT,
    (MizanType.INT, '/', MizanType.FLOAT): MizanType.FLOAT,
    (MizanType.FLOAT, '+', MizanType.INT): MizanType.FLOAT,
    (MizanType.FLOAT, '-', MizanType.INT): MizanType.FLOAT,
    (MizanType.FLOAT, '*', MizanType.INT): MizanType.FLOAT,
    (MizanType.FLOAT, '/', MizanType.INT): MizanType.FLOAT,
}

_COMPARISON_OPS = {'==', '!=', '>', '<', '>=', '<='}
_OP_ALIASES = {'MUL': '*', 'DIV': '/', 'MOD': '%', 'PLUS': '+', 'MINUS': '-',
               'EQ': '==', 'NEQ': '!=', 'GT': '>', 'LT': '<', 'GTE': '>=', 'LTE': '<='}
_KIND_TO_SINGLETON = {MizanType.INT: INT_TYPE, MizanType.FLOAT: FLOAT_TYPE, MizanType.BOOL: BOOL_TYPE}

def get_result_type(left_type: Type, operator: str, right_type: Type) -> Type:
    if isinstance(left_type, ErrorType) or isinstance(right_type, ErrorType):
        return ERROR_TYPE
    op = _OP_ALIASES.get(operator, operator)

    if op in _COMPARISON_OPS:
        return BOOL_TYPE if (left_type.is_comparable() and right_type.is_comparable()) else ERROR_TYPE

    if isinstance(left_type, UnitType) and isinstance(right_type, UnitType):
        if left_type == right_type and op in ('+', '-'):
            return left_type
        if op == '*':
            new_dim = left_type.dimension.copy()
            for k, v in right_type.dimension.items():
                new_dim[k] = new_dim.get(k, 0) + v
            new_dim = {k: v for k, v in new_dim.items() if v != 0}
            new_atoms = left_type.atoms.union(right_type.atoms)
            return UnitType(f"{left_type.unit_name}·{right_type.unit_name}", new_dim, new_atoms)
        if op == '/':
            new_dim = left_type.dimension.copy()
            for k, v in right_type.dimension.items():
                new_dim[k] = new_dim.get(k, 0) - v
            new_dim = {k: v for k, v in new_dim.items() if v != 0}
            new_atoms = left_type.atoms.union(right_type.atoms)
            return UnitType(f"{left_type.unit_name}/{right_type.unit_name}", new_dim, new_atoms)
        return ERROR_TYPE

    if isinstance(left_type, UnitType) and isinstance(right_type, (IntType, FloatType)):
        return left_type
    if isinstance(right_type, UnitType) and isinstance(left_type, (IntType, FloatType)):
        return right_type

    key = (left_type.kind, op, right_type.kind)
    result_kind = _ARITHMETIC_TABLE.get(key)
    return _KIND_TO_SINGLETON.get(result_kind, ERROR_TYPE) if result_kind is not None else ERROR_TYPE

def create_unit_type(name: str) -> UnitType:
    return UnitType(name)

def types_compatible(declared: Type, actual: Type) -> bool:
    if isinstance(declared, ErrorType) or isinstance(actual, ErrorType):
        return True
    if declared == actual:
        return True
    if isinstance(declared, FloatType) and isinstance(actual, IntType):
        return True
    if isinstance(declared, UnitType) and isinstance(actual, (IntType, FloatType)):
        return True
    if isinstance(declared, (FloatType, IntType)) and isinstance(actual, UnitType):
        return True
    if isinstance(declared, UnitType) and isinstance(actual, UnitType):
        # Allow assignment if dimensions and atoms match (e.g. custom unit to built-in famous mix)
        return dimension_signatures_equal(declared.dimension, actual.dimension) and declared.atoms == actual.atoms
    return False

def type_from_name(name: str) -> Type:
    mapping = {'منطقي': BOOL_TYPE, 'صحيح': INT_TYPE, 'عدد_صحيح': INT_TYPE,
               'حقيقي': FLOAT_TYPE, 'عدد_حقيقي': FLOAT_TYPE, 'نص': STRING_TYPE}
    if name in mapping:
        return mapping[name]
    if name in UnitType.BUILTIN_UNITS:
        return UnitType(name)
    return ERROR_TYPE

def is_literal_number(type_obj) -> bool:
    return isinstance(type_obj, (IntType, FloatType))

def units_compatible_for_op(left, right, op: str) -> bool:
    if isinstance(left, UnitType) and isinstance(right, UnitType):
        if op in ('+', '-'):
            return dimension_signatures_equal(left.dimension, right.dimension) and left.atoms == right.atoms
        elif op in ('*', '/'):
            return True
        elif op in ('==', '!=', '>', '<', '>=', '<='):
            # ✅ THE GOLDEN RULE: Dimensions must match AND Atoms must match!
            return dimension_signatures_equal(left.dimension, right.dimension) and left.atoms == right.atoms
    if isinstance(left, UnitType) and is_literal_number(right):
        return True
    if is_literal_number(left) and isinstance(right, UnitType):
        return True
    if is_literal_number(left) and is_literal_number(right):
        return True
    return False

# ── Canonical Base Unit Atoms Engine ───────────────────────────────
def compute_unit_signature(unit_expr_node) -> Tuple[Dict[str, int], Set[str]]:
    """Recursively computes the dimensional signature and atomic composition 
    from a UnitMathExprNode or UnitBaseNode."""
    from Ast.nodes import UnitMathExprNode, UnitBaseNode
    
    if isinstance(unit_expr_node, UnitBaseNode):
        name = unit_expr_node.unit_name
        dim_str = UNIT_TO_DIMENSION.get(name, 'unknown')
        atoms = UNIT_TO_ATOMS.get(name, {name})
        return ({dim_str: 1} if dim_str != 'unknown' else {}, atoms)
        
    elif isinstance(unit_expr_node, UnitMathExprNode):
        l_dim, l_atoms = compute_unit_signature(unit_expr_node.left)
        r_dim, r_atoms = compute_unit_signature(unit_expr_node.right)
        
        final_dim = l_dim.copy()
        op = unit_expr_node.op
        for k, v in r_dim.items():
            delta = v if op == '*' else -v
            final_dim[k] = final_dim.get(k, 0) + delta
            
        final_atoms = l_atoms.union(r_atoms)
        return ({k: v for k, v in final_dim.items() if v != 0}, final_atoms)
        
    return ({}, set())

def dimension_signatures_equal(sig_a: Dict[str, int], sig_b: Dict[str, int]) -> bool:
    return sig_a == sig_b