from enum import Enum, auto
from typing import Optional


# =====================================================================
# 1. تعداد الأنواع الأساسية (للاستخدام الداخلي والتشخيص)
# =====================================================================

class MizanType(Enum):
    INT    = auto()
    FLOAT  = auto()
    BOOL   = auto()
    STRING = auto()
    UNIT   = auto()
    ARRAY  = auto()
    ERROR  = auto()


# =====================================================================
# 2. الصنف الأب لجميع الأنواع
# =====================================================================

class Type:
    """الصنف الأب لكل أنواع لغة ميزان."""

    kind: MizanType = None  

    def __eq__(self, other):
        return type(self) is type(other)

    def __hash__(self):
        return hash(type(self))

    def __repr__(self):
        return self.__str__()

    def is_numeric(self) -> bool:
        """هل النوع قابل للعمليات الحسابية؟"""
        return isinstance(self, (IntType, FloatType, UnitType))

    def is_comparable(self) -> bool:
        """هل النوع قابل للمقارنة؟"""
        return isinstance(self, (IntType, FloatType, BoolType, UnitType))


# =====================================================================
# 3. الأنواع الأساسية
# =====================================================================

class IntType(Type):
    kind = MizanType.INT

    def __str__(self):
        return "صحيح"


class FloatType(Type):
    kind = MizanType.FLOAT

    def __str__(self):
        return "حقيقي"


class BoolType(Type):
    kind = MizanType.BOOL

    def __str__(self):
        return "منطقي"


class StringType(Type):
    kind = MizanType.STRING

    def __str__(self):
        return "نص"


class ErrorType(Type):
    """نوع خاص يُعاد عند وجود خطأ دلالي — يمنع تكرار الأخطاء."""
    kind = MizanType.ERROR

    def __str__(self):
        return "خطأ_دلالي"

    def __eq__(self, other):
        return isinstance(other, Type)

    def __hash__(self):
        return hash(ErrorType)


# =====================================================================
# 4. نوع الوحدات الفيزيائية (ديناميكي)
# =====================================================================

class UnitType(Type):
    """
    يمثّل وحدات القياس الفيزيائية مثل: سيلزيوس، بار، فولت، ...
    وكذلك الوحدات المخصصة التي يُعرّفها المستخدم.
    """
    kind = MizanType.UNIT

    BUILTIN_UNITS = {
        'سيلزيوس', 'بار', 'باسكال', 'فولت', 'امبير',
        'دورة_في_الدقيقة', 'لتر_في_الدقيقة', 'بالمئة',
        'متر', 'NTU', 'لا_وحدة', 'بار_في_الثانية',
        'سيلزيوس_في_الثانية',
    }

    def __init__(self, unit_name: str):
        self.unit_name = unit_name
        self.is_builtin = unit_name in self.BUILTIN_UNITS

    def __str__(self):
        return f"وحدة({self.unit_name})"

    def __eq__(self, other):
        if isinstance(other, UnitType):
            return self.unit_name == other.unit_name
        return False

    def __hash__(self):
        return hash(('UnitType', self.unit_name))


# =====================================================================
# 5. نوع المصفوفات
# =====================================================================

class ArrayType(Type):
    """
    مصفوفة ذات حجم ثابت.
    مثال: صحيح[10]  →  ArrayType(element_type=INT_TYPE, size=10)
    """
    kind = MizanType.ARRAY

    def __init__(self, element_type: Type, size: int):
        self.element_type = element_type
        self.size = size

    def __str__(self):
        return f"{self.element_type}[{self.size}]"

    def __eq__(self, other):
        return (isinstance(other, ArrayType)
                and self.element_type == other.element_type
                and self.size == other.size)

    def __hash__(self):
        return hash(('ArrayType', self.element_type, self.size))


# =====================================================================
# 6. Singleton Instances (لتقليل استهلاك الذاكرة)
# =====================================================================

INT_TYPE    = IntType()
FLOAT_TYPE  = FloatType()
BOOL_TYPE   = BoolType()
STRING_TYPE = StringType()
ERROR_TYPE  = ErrorType()


# =====================================================================
# 7. جدول العمليات الحسابية
# =====================================================================


_ARITHMETIC_TABLE: dict = {
    (MizanType.INT,   '+', MizanType.INT):   MizanType.INT,
    (MizanType.INT,   '-', MizanType.INT):   MizanType.INT,
    (MizanType.INT,   '*', MizanType.INT):   MizanType.INT,
    (MizanType.INT,   '/', MizanType.INT):   MizanType.FLOAT,  
    (MizanType.INT,   '%', MizanType.INT):   MizanType.INT,

    (MizanType.FLOAT, '+', MizanType.FLOAT): MizanType.FLOAT,
    (MizanType.FLOAT, '-', MizanType.FLOAT): MizanType.FLOAT,
    (MizanType.FLOAT, '*', MizanType.FLOAT): MizanType.FLOAT,
    (MizanType.FLOAT, '/', MizanType.FLOAT): MizanType.FLOAT,
    (MizanType.FLOAT, '%', MizanType.FLOAT): MizanType.FLOAT,

    (MizanType.INT,   '+', MizanType.FLOAT): MizanType.FLOAT,
    (MizanType.INT,   '-', MizanType.FLOAT): MizanType.FLOAT,
    (MizanType.INT,   '*', MizanType.FLOAT): MizanType.FLOAT,
    (MizanType.INT,   '/', MizanType.FLOAT): MizanType.FLOAT,
    (MizanType.FLOAT, '+', MizanType.INT):   MizanType.FLOAT,
    (MizanType.FLOAT, '-', MizanType.INT):   MizanType.FLOAT,
    (MizanType.FLOAT, '*', MizanType.INT):   MizanType.FLOAT,
    (MizanType.FLOAT, '/', MizanType.INT):   MizanType.FLOAT,

}

_COMPARISON_OPS = {'==', '!=', '>', '<', '>=', '<='}

_OP_ALIASES = {
    'MUL': '*', 'DIV': '/', 'MOD': '%',
    'PLUS': '+', 'MINUS': '-',
    'EQ': '==', 'NEQ': '!=',
    'GT': '>', 'LT': '<', 'GTE': '>=', 'LTE': '<=',
}

_KIND_TO_SINGLETON = {
    MizanType.INT:   INT_TYPE,
    MizanType.FLOAT: FLOAT_TYPE,
    MizanType.BOOL:  BOOL_TYPE,
}


# =====================================================================
# 8. دالة التحقق من الأنواع (Type Checking)
# =====================================================================

def get_result_type(left_type: Type, operator: str, right_type: Type) -> Type:
    """
    تُحدّد نوع نتيجة عملية ثنائية بناءً على نوعَي المعاملَين والمشغّل.

    تدعم:
    - العمليات الحسابية: + - * / %
    - عمليات المقارنة:  == != > < >= <=
    - الوحدات الفيزيائية (نفس الوحدة)
    - أسماء مشغّلات الـ Grammar مثل 'MUL', 'PLUS', ...
    - ErrorType يُعيد ErrorType مباشرة (لوقف تسلسل الأخطاء)
    """
    if isinstance(left_type, ErrorType) or isinstance(right_type, ErrorType):
        return ERROR_TYPE

    op = _OP_ALIASES.get(operator, operator)

    if op in _COMPARISON_OPS:
        if left_type.is_comparable() and right_type.is_comparable():
            return BOOL_TYPE
        return ERROR_TYPE

    if isinstance(left_type, UnitType) and isinstance(right_type, UnitType):
        if left_type == right_type and op in ('+', '-'):
            return left_type          
        if op in ('*', '/'):
            if op == '*':
                return UnitType(f"{left_type.unit_name}·{right_type.unit_name}")
            else:
                return UnitType(f"{left_type.unit_name}/{right_type.unit_name}")
        return ERROR_TYPE

    key = (left_type.kind, op, right_type.kind)
    result_kind = _ARITHMETIC_TABLE.get(key)
    if result_kind is not None:
        return _KIND_TO_SINGLETON.get(result_kind, ERROR_TYPE)

    return ERROR_TYPE


# =====================================================================
# 9. دوال مساعدة
# =====================================================================

def create_unit_type(name: str) -> UnitType:
    """ينشئ UnitType جديداً بالاسم المُعطى."""
    return UnitType(name)


def types_compatible(declared: Type, actual: Type) -> bool:
    """
    يتحقق من توافق نوعَين للإسناد والتهيئة.
    - النوعان يجب أن يتطابقا تمامًا.
    - ErrorType متوافق مع أي شيء (لوقف تسلسل الأخطاء).
    """
    if isinstance(declared, ErrorType) or isinstance(actual, ErrorType):
        return True
    return declared == actual


def type_from_name(name: str) -> Type:
    """
    يُعيد كائن Type من اسم النوع العربي.
    مفيد في resolve_type داخل المحلل الدلالي.
    """
    mapping = {
        'منطقي':      BOOL_TYPE,
        'صحيح':       INT_TYPE,
        'عدد_صحيح':   INT_TYPE,
        'حقيقي':      FLOAT_TYPE,
        'عدد_حقيقي':  FLOAT_TYPE,
        'نص':         STRING_TYPE,
    }
    if name in mapping:
        return mapping[name]
    if name in UnitType.BUILTIN_UNITS:
        return UnitType(name)
    return ERROR_TYPE