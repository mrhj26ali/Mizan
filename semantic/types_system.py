from enum import Enum, auto
from typing import Optional, Dict


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


class UnitType(Type):
    """Physical unit type (ISO 80000 dimensional safety). Two UnitTypes are
    equal iff their names match — the mechanism that prevents unit-confusion
    bugs at compile time (the spec's core safety requirement)."""
    kind = MizanType.UNIT
    BUILTIN_UNITS = {
        'سيلزيوس', 'بار', 'باسكال', 'فولت', 'امبير',
        'دورة_في_الدقيقة', 'لتر_في_الدقيقة', 'بالمئة',
        'متر', 'NTU', 'لا_وحدة', 'بار_في_الثانية', 'سيلزيوس_في_الثانية',
    }

    def __init__(self, unit_name: str, dimension: Optional[Dict[str, int]] = None):
        self.unit_name = unit_name
        self.is_builtin = unit_name in self.BUILTIN_UNITS
        self.dimension = dimension

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
            return UnitType(f"{left_type.unit_name}·{right_type.unit_name}")
        if op == '/':
            return UnitType(f"{left_type.unit_name}/{right_type.unit_name}")
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
            return left.unit_name == right.unit_name
        elif op in ('*', '/'):
            return True
        elif op in ('==', '!=', '>', '<', '>=', '<='):
            return left.unit_name == right.unit_name
    if isinstance(left, UnitType) and is_literal_number(right):
        return True
    if is_literal_number(left) and isinstance(right, UnitType):
        return True
    if is_literal_number(left) and is_literal_number(right):
        return True
    return False


# ── Dimensional algebra for custom units (وحدات_مخصصة) ─────────────

_DIM_KEYWORD_AXES = {
    'MASS_KW': 'mass', 'كتلة': 'mass', 'VOLUME_KW': 'volume', 'حجم': 'volume',
    'TIME_DIM_KW': 'time', 'زمن': 'time', 'LENGTH_KW': 'length', 'طول': 'length',
    'TEMP_DIM_KW': 'temperature', 'درجة_حرارة': 'temperature',
    'CURRENT_DIM_KW': 'current', 'تيار': 'current', 'VOLTAGE_DIM_KW': 'voltage', 'جهد': 'voltage',
    'PRESSURE_DIM_KW': 'pressure', 'ضغط': 'pressure', 'COUNT_DIM_KW': 'count', 'عدد': 'count',
    'ENERGY_KW': 'energy', 'طاقة': 'energy',
}


def compute_dimension_signature(elements) -> Dict[str, int]:
    """Converts DimensionExprNode.elements (e.g. ['كتلة','/','حجم']) into a
    dimensional exponent signature {'mass': 1, 'volume': -1}, so two custom
    units defined independently with the same physical basis are recognized
    as equivalent regardless of the identifier name chosen."""
    signature: Dict[str, int] = {}
    pending_op = '*'
    for el in elements:
        if el in ('/', 'DIV'):
            pending_op = '/'
        elif el in ('*', 'MUL'):
            pending_op = '*'
        else:
            axis = _DIM_KEYWORD_AXES.get(el)
            if axis is None:
                continue
            delta = 1 if pending_op == '*' else -1
            signature[axis] = signature.get(axis, 0) + delta
            pending_op = '*'
    return {k: v for k, v in signature.items() if v != 0}


def dimension_signatures_equal(sig_a: Dict[str, int], sig_b: Dict[str, int]) -> bool:
    return sig_a == sig_b