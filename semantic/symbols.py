from typing import Any, Dict, List, Optional


# =====================================================================
# الصنف الأساسي لكل الرموز
# =====================================================================

class Symbol:
    """الصنف الأب لجميع أنواع الرموز في جدول الرموز."""

    def __init__(self, name: str, sym_type: Any = None):
        self.name = name
        self.type = sym_type  

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name} ({self.type})>"

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(self.name)


# =====================================================================
# رموز المتغيرات والثوابت
# =====================================================================

class VariableSymbol(Symbol):
    """متغير قابل للتعديل مُعرَّف بـ متغير."""

    def __init__(self, name: str, sym_type: Any,
                 is_array: bool = False, array_size: int = 0):
        super().__init__(name, sym_type)
        self.is_array = is_array
        self.array_size = array_size  
    def __repr__(self):
        arr = f"[{self.array_size}]" if self.is_array else ""
        return f"<VariableSymbol: {self.name}{arr} ({self.type})>"


class ConstSymbol(Symbol):
    """ثابت غير قابل للتعديل مُعرَّف بـ ثابت."""

    def __init__(self, name: str, sym_type: Any, value: Any = None):
        super().__init__(name, sym_type)
        self.value = value 

    def __repr__(self):
        return f"<ConstSymbol: {self.name} = {self.value} ({self.type})>"


# =====================================================================
# رمز الإجراء
# =====================================================================

class ProcedureSymbol(Symbol):
    """
    إجراء مُعرَّف بـ اجراء.
    - return_type: كائن Type أو None للإجراءات التي لا تُعيد قيمة
    - params: عدد المعاملات (int) — يُستخدم للتحقق عند الاستدعاء
    - param_types: قائمة بأنواع المعاملات بالترتيب (اختياري للتحقق الدقيق)
    """

    def __init__(self, name: str, return_type: Any = None,
                 params: int = 0, param_types: Optional[List[Any]] = None):
        super().__init__(name, return_type)
        self.return_type = return_type
        self.params = params                         
        self.param_types: List[Any] = param_types or [] 

    def __repr__(self):
        ret = str(self.return_type) if self.return_type else "لا_قيمة"
        return f"<ProcedureSymbol: {self.name}({self.params} معامل) → {ret}>"


# =====================================================================
# رموز العتاد الصناعي
# =====================================================================

class SensorSymbol(Symbol):
    """
    حساس مُعرَّف بـ حساس.
    - sensor_type: نوع البيانات التي يقرأها (UnitType أو BaseType)
    - range_spec: كائن RangeSpecNode أو None
    - address: عنوان السجل (register) كنص مثل '0x0200'
    """

    def __init__(self, name: str, sensor_type: Any = None,
                 range_spec: Any = None, address: Optional[str] = None):
        super().__init__(name, sensor_type)
        self.range_spec = range_spec
        self.address = address

    def __repr__(self):
        addr = f" @{self.address}" if self.address else ""
        return f"<SensorSymbol: {self.name}{addr} ({self.type})>"


class ActuatorSymbol(Symbol):
    """
    مشغّل مُعرَّف بـ مشغل.
    - actuator_type: نوع القيمة التي يقبلها
    - range_spec: كائن RangeSpecNode أو None
    - address: عنوان السجل
    """

    def __init__(self, name: str, actuator_type: Any = None,
                 range_spec: Any = None, address: Optional[str] = None):
        super().__init__(name, actuator_type)
        self.range_spec = range_spec
        self.address = address

    def __repr__(self):
        addr = f" @{self.address}" if self.address else ""
        return f"<ActuatorSymbol: {self.name}{addr} ({self.type})>"


class DeviceSymbol(Symbol):
    """
    جهاز مُعرَّف بـ جهاز (PLC، حاسوب صناعي، إلخ).
    - category: نوع الجهاز (نص من حقل 'نوع')
    - protocol: بروتوكول التواصل
    - fields: قاموس بجميع حقول الجهاز المُعرَّفة
    """

    def __init__(self, name: str, category: str = "Unknown",
                 protocol: str = "N/A", fields: Optional[Dict[str, Any]] = None):
        super().__init__(name, category)
        self.category = category
        self.protocol = protocol
        self.fields: Dict[str, Any] = fields or {}

    def __repr__(self):
        return (f"<DeviceSymbol: {self.name} "
                f"نوع={self.category} بروتوكول={self.protocol}>")


class ModeSymbol(Symbol):
    """
    وضع تشغيل مُعرَّف بـ وضع.
    يُستخدم للتحقق من صحة أوامر انتقل_الى وجداول الانتقال.
    """

    def __init__(self, name: str):
        super().__init__(name, sym_type="وضع")

    def __repr__(self):
        return f"<ModeSymbol: {self.name}>"