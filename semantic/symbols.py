from typing import Any, Dict, List, Optional


class Symbol:
    def __init__(self, name: str, sym_type: Any = None):
        self.name = name
        self.type = sym_type
    def __repr__(self): return f"<{self.__class__.__name__}: {self.name} ({self.type})>"
    def __eq__(self, other): return isinstance(other, Symbol) and self.name == other.name
    def __hash__(self): return hash(self.name)


class VariableSymbol(Symbol):
    def __init__(self, name: str, sym_type: Any, is_array: bool = False, array_size: int = 0):
        super().__init__(name, sym_type)
        self.is_array = is_array
        self.array_size = array_size
    def __repr__(self):
        arr = f"[{self.array_size}]" if self.is_array else ""
        return f"<VariableSymbol: {self.name}{arr} ({self.type})>"


class ConstSymbol(Symbol):
    def __init__(self, name: str, sym_type: Any, value: Any = None):
        super().__init__(name, sym_type)
        self.value = value
    def __repr__(self): return f"<ConstSymbol: {self.name} = {self.value} ({self.type})>"


class ProcedureSymbol(Symbol):
    def __init__(self, name: str, return_type: Any = None, params: int = 0,
                 param_types: Optional[List[Any]] = None):
        super().__init__(name, return_type)
        self.return_type = return_type
        self.params = params
        self.param_types: List[Any] = param_types or []
    def __repr__(self):
        ret = str(self.return_type) if self.return_type else "لا_قيمة"
        return f"<ProcedureSymbol: {self.name}({self.params} معامل) → {ret}>"


class SensorSymbol(Symbol):
    def __init__(self, name: str, sensor_type: Any = None, range_spec: Any = None,
                 address: Optional[str] = None, health_rules: Optional[List] = None):
        super().__init__(name, sensor_type)
        self.range_spec = range_spec
        self.address = address
        self.health_rules = health_rules or []
    def __repr__(self):
        addr = f" @{self.address}" if self.address else ""
        return f"<SensorSymbol: {self.name}{addr} ({self.type})>"


class ActuatorSymbol(Symbol):
    def __init__(self, name: str, actuator_type: Any = None, range_spec: Any = None,
                 address: Optional[str] = None):
        super().__init__(name, actuator_type)
        self.range_spec = range_spec
        self.address = address
    def __repr__(self):
        addr = f" @{self.address}" if self.address else ""
        return f"<ActuatorSymbol: {self.name}{addr} ({self.type})>"


class DeviceSymbol(Symbol):
    def __init__(self, name: str, category: str = "Unknown", protocol: str = "N/A",
                 fields: Optional[Dict[str, Any]] = None):
        super().__init__(name, category)
        self.category = category
        self.protocol = protocol
        self.fields: Dict[str, Any] = fields or {}
    def __repr__(self): return f"<DeviceSymbol: {self.name} نوع={self.category} بروتوكول={self.protocol}>"


class ModeSymbol(Symbol):
    def __init__(self, name: str, is_builtin: bool = False):
        super().__init__(name, sym_type="وضع")
        self.is_builtin = is_builtin
    def __repr__(self): return f"<ModeSymbol: {self.name}{' (builtin)' if self.is_builtin else ''}>"


class RuleSymbol(Symbol):
    def __init__(self, name: str, mode_name: str):
        super().__init__(name, sym_type="قاعدة")
        self.mode_name = mode_name
    def __repr__(self): return f"<RuleSymbol: {self.name} (في وضع {self.mode_name})>"


class EscalationSymbol(Symbol):
    def __init__(self, name: str, level_names: Optional[List[str]] = None):
        super().__init__(name, sym_type="تصعيد")
        self.level_names = level_names or []
    def __repr__(self): return f"<EscalationSymbol: {self.name} مستويات={self.level_names}>"