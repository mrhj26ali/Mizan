# =====================================================================
# MIZAN SEMANTIC ANALYZER (v1.6 - Industrial Standard Edition)
# Strict Validation, Detailed Errors, and Canonical Base Unit Atoms
# =====================================================================

import re
from Ast.nodes import *
from semantic.environment import Environment, SemanticError
from semantic.symbols import (
    VariableSymbol, ConstSymbol, ProcedureSymbol,
    SensorSymbol, ActuatorSymbol, DeviceSymbol, ModeSymbol,
    RuleSymbol, EscalationSymbol,
)
from semantic.types_system import (
    BOOL_TYPE, INT_TYPE, FLOAT_TYPE, STRING_TYPE, ERROR_TYPE,
    UnitType, get_result_type, types_compatible, units_compatible_for_op,
    FloatType, IntType, compute_unit_signature, dimension_signatures_equal,
    UNIT_TO_DIMENSION, UNIT_TO_ATOMS
)

_BUILTIN_MODES = {'اقلاع', 'تشغيل', 'صيانة', 'طوارئ'}


class SemanticAnalyzer:

    def __init__(self):
        self.current_scope: Environment = Environment(name="Global")
        self.all_scopes: list[Environment] = [self.current_scope]
        self.errors: list[str] = []
        self.warnings: list[str] = []
        
        # Global Definition Registries
        self._defined_modes: set[str] = set(_BUILTIN_MODES)
        self._defined_procs: set[str] = set()
        self._custom_units: dict[str, UnitType] = {}  # Stores computed custom unit types
        
        # ✅ FSM WHITELIST ENFORCEMENT: Track allowed transitions
        self._allowed_transitions: set[tuple[str, str]] = set()
        
        # Context Tracking
        self.current_mode: str = None
        self._mode_nodes: dict[str, ModeBlockNode] = {}

    def visit(self, node):
        if node is None:
            return None
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for item in node:
                self.visit(item)
        return None

    def log_error(self, node, message: str):
        line, col = 0, 0
        if isinstance(node, int): line = node
        else:
            line, col = getattr(node, 'line', 0), getattr(node, 'column', 0)
        self.errors.append(f"❌ خطأ دلالي في السطر {line}:{col} -> {message}")

    def log_warning(self, node, message: str):
        line, col = getattr(node, 'line', 0), getattr(node, 'column', 0)
        self.warnings.append(f"⚠️ تحذير في السطر {line}:{col} -> {message}")

    def _enter_scope(self, name: str) -> Environment:
        new_scope = Environment(name=name, enclosing=self.current_scope)
        self.all_scopes.append(new_scope)
        self.current_scope = new_scope
        return new_scope

    def _exit_scope(self):
        if self.current_scope.enclosing:
            self.current_scope = self.current_scope.enclosing
        else:
            self.log_error(0, "محاولة الخروج من النطاق الجذري (Global).")

    def resolve_type(self, type_node) -> object:
        if type_node is None:
            return ERROR_TYPE
        if isinstance(type_node, ArrayTypeNode):
            return self.resolve_type(type_node.element_type)
        if isinstance(type_node, BaseTypeNode):
            name = type_node.type_name
            if name in ('منطقي',): return BOOL_TYPE
            if name in ('صحيح', 'عدد_صحيح'): return INT_TYPE
            if name in ('حقيقي', 'عدد_حقيقي'): return FLOAT_TYPE
            
            # ✅ Check Custom Units (Canonical Base Atoms)
            if name in self._custom_units:
                return self._custom_units[name]
            
            # ✅ Check Builtin Units
            if name in UnitType.BUILTIN_UNITS:
                # Construct UnitType with precomputed dims/atoms from registry
                dim_str = UNIT_TO_DIMENSION.get(name)
                dim = {dim_str: 1} if dim_str else {}
                atoms = UNIT_TO_ATOMS.get(name, {name})
                return UnitType(name, dim, atoms)
            
            self.log_error(type_node, f"النوع '{name}' غير معرّف. تأكد من صحة الاسم أو تعريفه في 'وحدات_مخصصة'.")
            return ERROR_TYPE
        return ERROR_TYPE

    def resolve_symbol(self, identifier: str, line: int = 0):
        sym = self.current_scope.resolve(identifier)
        if sym is None:
            self.log_error(line, f"المعرّف '{identifier}' غير معرّف. هل قمت بتعريفه في هذا النطاق؟")
        return sym

    def print_report(self):
        print("\n" + "=" * 60 + "\n📊 تقرير التحليل الدلالي\n" + "=" * 60)
        if self.errors:
            print(f"\n🔴 الأخطاء ({len(self.errors)}):")
            for e in self.errors: print(f"  {e}")
        else:
            print("\n✅ لا توجد أخطاء دلالية. الكود آمن ومتوافق مع المعايير.")
        if self.warnings:
            print(f"\n🟡 التحذيرات ({len(self.warnings)}):")
            for w in self.warnings: print(f"  {w}")
        print(f"\n📦 النطاقات المُنشأة ({len(self.all_scopes)}):")
        for scope in self.all_scopes:
            print(f"  • {scope.name} — {len(scope.symbols)} رمز")
        print("=" * 60 + "\n")

    # ── Program structure & procedures ──────────────────────────────

    def visit_ProgramNode(self, node: ProgramNode):
        # ✅ PASS 1: Collect Definitions (Units, Modes, Procs, Transitions) before analyzing logic
        for decl in node.declarations:
            if isinstance(decl, ProcedureDefNode):
                self._defined_procs.add(decl.identifier)
                self.current_scope.define(decl.identifier,
                    ProcedureSymbol(decl.identifier, return_type=None, params=len(decl.params)))
            elif isinstance(decl, ModeBlockNode):
                self._defined_modes.add(decl.mode_name)
                self._mode_nodes[decl.mode_name] = decl
            elif isinstance(decl, CustomModesBlockNode):
                self._defined_modes.update(decl.modes)
            elif isinstance(decl, CustomUnitsBlockNode):
                for u in decl.units:
                    # ✅ Compute Canonical Signature from AST Node
                    dim, atoms = compute_unit_signature(u.unit_expr)
                    if not dim:
                        self.log_error(u, f"تعريف الوحدة '{u.identifier}' غير صالح فيزيائياً.")
                    self._custom_units[u.identifier] = UnitType(u.identifier, dim, atoms)
            elif isinstance(decl, EscalationDefNode):
                level_names = [lv.level_name for lv in decl.levels]
                self.current_scope.define(decl.identifier, EscalationSymbol(decl.identifier, level_names))
            # ✅ FSM WHITELIST ENFORCEMENT: Pre-load allowed transitions
            elif isinstance(decl, TransitionTableNode):
                for rule in decl.rules:
                    self._allowed_transitions.add((rule.from_mode, rule.to_mode))

        # PASS 2: Deep Analysis
        for decl in node.declarations:
            self.visit(decl)
        return None

    def visit_ProgramDeclNode(self, node: ProgramDeclNode):
        # Just metadata
        return None

    def visit_ProcedureDefNode(self, node: ProcedureDefNode):
        return_type = self.resolve_type(node.return_type) if node.return_type else None
        # Redefine symbol with return type
        sym = self.current_scope.resolve(node.identifier)
        if sym: sym.return_type = return_type
        
        old_scope = self.current_scope
        self._enter_scope(f"Proc_{node.identifier}")
        
        for param in node.params:
            self.visit(param)
            
        for stmt in node.body:
            ret_type = self.visit(stmt)
            if isinstance(stmt, ReturnStmtNode) and return_type:
                if ret_type and ret_type != ERROR_TYPE and not self._types_compatible(return_type, ret_type):
                    self.log_error(stmt, f"نوع الإرجاع '{ret_type}' لا يتوافق مع '{return_type}' المحدد في تعريف الإجراء.")
        
        self._exit_scope()
        return None

    def visit_ParamNode(self, node: ParamNode):
        param_type = self.resolve_type(node.var_type)
        self.current_scope.define(node.identifier, VariableSymbol(node.identifier, param_type))
        return param_type

    # ── Hardware validation (Strict Industrial Checks) ──────────────

    def visit_DeviceBlockNode(self, node: DeviceBlockNode):
        fields_dict, has_ip, has_port = {}, False, False
        
        for field in node.fields:
            fields_dict[field.key] = field.value
            if field.key == 'IP': 
                has_ip = True
                # ✅ Check IP Format
                if not re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", field.value):
                    self.log_error(field, f"عنوان IP '{field.value}' غير صالح. الصيغة الصحيحة هي x.x.x.x")
            elif field.key == 'PORT': 
                has_port = True
                # ✅ Check Port Range
                try:
                    port = int(field.value)
                    if not (0 <= port <= 65535):
                        self.log_error(field, f"رقم المنفذ '{field.value}' غير صالح. يجب أن يكون بين 0 و 65535.")
                except ValueError:
                    self.log_error(field, "قيمة المنفذ يجب أن تكون رقماً.")
            elif field.key == 'PROTOCOL':
                if field.value.lower() not in ['modbus_tcp', 'mqtt', 'opcua', 'http']:
                    self.log_warning(field, f"البروتوكول '{field.value}' قد لا يكون مدعوماً افتراضياً.")

        if not has_ip: self.log_error(node, f"جهاز '{node.identifier}' يفتقر إلى عنوان IP وهو مطلوب للاتصال.")
        if not has_port: self.log_error(node, f"جهاز '{node.identifier}' يفتقر إلى رقم المنفذ (Port).")

        self.current_scope.define(node.identifier,
            DeviceSymbol(node.identifier, fields_dict.get('TYPE', 'Unknown'), fields_dict.get('PROTOCOL', 'N/A'), fields_dict))
        return None

    def visit_SensorDeclNode(self, node: SensorDeclNode):
        sensor_type, sensor_address, health_rules = None, None, []
        
        for field in node.fields:
            if field.key == 'TYPE':
                sensor_type = self.resolve_type(field.value)
            elif field.key == 'ADDRESS':
                sensor_address = field.value
                # ✅ Check Address Format (Hex)
                if not str(sensor_address).startswith('0x') or not all(c in '0123456789abcdefABCDEF' for c in str(sensor_address)[2:]):
                     self.log_warning(field, f"عنوان الحساس '{sensor_address}' لا يبدو بصيغة Hex قياسية (0x...).")
            elif field.key == 'RANGE':
                if isinstance(field.value, RangeSpecNode):
                    if field.value.min_val >= field.value.max_val:
                        self.log_error(field, f"نطاق الحساس غير صالح: القيمة الدنيا ({field.value.min_val}) يجب أن تكون أصغر من العليا ({field.value.max_val}).")
            elif field.key == 'HEALTH':
                health_rules = field.value
                for rule in health_rules:
                    self.visit(rule)
        
        if sensor_address is None:
            self.log_error(node, f"حساس '{node.identifier}' يفتقر إلى عنوان (Address). لا يمكن قراءته من PLC.")
        
        self.current_scope.define(node.identifier,
            SensorSymbol(node.identifier, sensor_type, None, sensor_address, health_rules))
        return None

    def visit_ActuatorDeclNode(self, node: ActuatorDeclNode):
        actuator_type, actuator_address = None, None
        for field in node.fields:
            if field.key == 'TYPE':
                actuator_type = self.resolve_type(field.value)
            elif field.key == 'ADDRESS':
                actuator_address = field.value
            elif field.key == 'RANGE':
                if isinstance(field.value, RangeSpecNode):
                    if field.value.min_val >= field.value.max_val:
                        self.log_error(field, f"نطاق المشغل غير صالح.")
                        
        if actuator_address is None:
            self.log_error(node, f"مشغل '{node.identifier}' يفتقر إلى عنوان (Address). لا يمكن التحكم به.")
        
        self.current_scope.define(node.identifier,
            ActuatorSymbol(node.identifier, actuator_type, None, actuator_address))
        return None

    # ── Variables, constants & types ──────────────────────────────────

    def visit_VarDeclNode(self, node: VarDeclNode):
        declared_type = self.resolve_type(node.var_type)
        expr_type = self.visit(node.expr)
        if expr_type and expr_type != ERROR_TYPE and declared_type != ERROR_TYPE:
            if not self._types_compatible(declared_type, expr_type):
                self.log_error(node, f"عدم توافق الأنواع: لا يمكن إسناد نوع '{expr_type}' إلى المتغير '{node.identifier}' المعرّف بـ '{declared_type}'.")
        
        is_array = isinstance(node.var_type, ArrayTypeNode)
        array_size = node.var_type.size if is_array else 0
        try:
            self.current_scope.define_strict(node.identifier,
                VariableSymbol(node.identifier, declared_type, is_array=is_array, array_size=array_size), node)
        except SemanticError as e:
            self.log_error(node, str(e))
        return declared_type

    def visit_ConstDeclNode(self, node: ConstDeclNode):
        declared_type = self.resolve_type(node.var_type)
        expr_type = self.visit(node.expr)
        if not types_compatible(declared_type, expr_type):
            self.log_error(node, f"نوع قيمة الثابت '{expr_type}' لا يتوافق مع '{declared_type}'.")
        try:
            self.current_scope.define_strict(node.identifier, ConstSymbol(node.identifier, declared_type), node)
        except SemanticError as e:
            self.log_error(node, str(e))
        return declared_type

    def _types_compatible(self, declared, actual) -> bool:
        # Updated to support the new UnitType logic
        if declared == actual: return True
        if isinstance(declared, FloatType) and isinstance(actual, IntType): return True
        if isinstance(declared, UnitType) and isinstance(actual, (IntType, FloatType)): return True
        if isinstance(declared, (FloatType, IntType)) and isinstance(actual, UnitType): return True
        if isinstance(declared, UnitType) and isinstance(actual, UnitType):
            # Allow assignment if dimensions and atoms match
            return dimension_signatures_equal(declared.dimension, actual.dimension) and declared.atoms == actual.atoms
        return False

    # ── Operating modes & safety rules ────────────────────────────────

    def visit_ModeBlockNode(self, node: ModeBlockNode):
        self._defined_modes.add(node.mode_name)
        self.current_scope.define(node.mode_name, ModeSymbol(node.mode_name, is_builtin=(node.mode_name in _BUILTIN_MODES)))

        old_scope, old_mode = self.current_scope, self.current_mode
        self.current_mode = node.mode_name
        self._enter_scope(f"Mode_{node.mode_name}")

        for stmt in node.on_start_statements:
            self.visit(stmt)

        seen_rule_names = set()
        for rule in node.rules:
            if rule.identifier in seen_rule_names:
                self.log_error(rule, f"القاعدة '{rule.identifier}' مُعرَّفة أكثر من مرة في وضع '{node.mode_name}'. يجب أن يكون لكل قاعدة اسم فريد.")
            seen_rule_names.add(rule.identifier)
            self.visit(rule)

        self._exit_scope()
        self.current_mode = old_mode
        return None

    def visit_RuleBlockNode(self, node: RuleBlockNode):
        # ✅ UPDATED: Rules are now just blocks of statements. No separate condition/action clauses.
        old_scope = self.current_scope
        self._enter_scope(f"Rule_{node.identifier}")
        self.current_scope.define(node.identifier, RuleSymbol(node.identifier, self.current_mode or "؟"))
        
        for decl in node.local_declarations:
            self.visit(decl)
            
        for stmt in node.statements:
            self.visit(stmt)
            
        self._exit_scope()
        return None

    # ── Statements ───────────────────────────────────────────────────

    def visit_CommandStmtNode(self, node: CommandStmtNode):
        if self.current_mode == 'صيانة':
            self.log_error(node, "🚫 مخالفات أمان: أوامر المشغلات محظورة تماماً في وضع الصيانة (IEC 62443).")
        
        sym = self.resolve_symbol(node.identifier, node.line)
        if sym is not None and not isinstance(sym, ActuatorSymbol):
            self.log_error(node, f"'{node.identifier}' ليس مشغّلاً (Actuator). لا يمكن إرسال أمر له.")
        if isinstance(node.value, ASTNode):
            self.visit(node.value)
        return None

    def visit_AssignStmtNode(self, node: AssignStmtNode):
        sym = self.resolve_symbol(node.identifier, node.line)
        if sym is None: return ERROR_TYPE
        if isinstance(sym, SensorSymbol):
            self.log_error(node, "❌ لا يمكن إسناد قيمة لحساس (Sensors) لأن القراءة منه فقط.")
            return ERROR_TYPE
        if isinstance(sym, ConstSymbol):
            self.log_error(node, "❌ لا يمكن تعديل الثابت (Const) بعد تعريفه.")
            return ERROR_TYPE
        if node.index_expr is not None and not getattr(sym, 'is_array', False):
            self.log_error(node, f"'{node.identifier}' ليس مصفوفة، لا يمكن الفهرسة عليه.")
        
        var_type = sym.type
        val_type = self.visit(node.expr)
        if val_type and val_type != ERROR_TYPE and var_type != ERROR_TYPE:
            if not self._types_compatible(var_type, val_type):
                self.log_error(node, f"عدم توافق الأنواع: لا يمكن إسناد '{val_type}' إلى '{var_type}'.")
        return var_type

    def visit_IfStmtNode(self, node: IfStmtNode):
        cond_type = self.visit(node.condition)
        if cond_type and cond_type != ERROR_TYPE and cond_type != BOOL_TYPE:
            self.log_error(node, "❌ خطأ منطقي: شرط 'اذا' يجب أن يكون منطقياً (Boolean).")
        old_scope = self.current_scope
        self._enter_scope(f"If_then_{node.line}")
        for stmt in node.then_branch: self.visit(stmt)
        self._exit_scope()
        if node.else_branch:
            self._enter_scope(f"If_else_{node.line}")
            for stmt in node.else_branch: self.visit(stmt)
            self._exit_scope()
        return None

    def visit_WhileStmtNode(self, node: WhileStmtNode):
        cond_type = self.visit(node.condition)
        if cond_type and cond_type != ERROR_TYPE and cond_type != BOOL_TYPE:
            self.log_error(node, "❌ خطأ منطقي: شرط 'طالما' يجب أن يكون منطقياً (Boolean).")
        old_scope = self.current_scope
        self._enter_scope(f"While_{node.line}")
        for stmt in node.body: self.visit(stmt)
        self._exit_scope()
        return None

    # ✅ FSM WHITELIST ENFORCEMENT: Check Goto against the Transition Table
    def visit_GotoStmtNode(self, node: GotoStmtNode):
        # 1. Check if target mode exists
        if node.target_mode not in self._defined_modes:
            self.log_error(node, f"❌ وضع التشغيل الهدف '{node.target_mode}' غير معرّف. تأكد من وجوده قبل الانتقال.")
            return None
            
        # 2. Enforce the whitelist!
        current_mode = self.current_mode
        if current_mode and (current_mode, node.target_mode) not in self._allowed_transitions:
            self.log_error(node, 
                f"🚫 انتقال غير مسموح: الانتقال من '{current_mode}' إلى '{node.target_mode}' غير مُعرّف في جدول 'انتقالات'. "
                f"يجب إضافة هذا المسار في الجدول العلوي للسماح به.")
        return None

    def visit_WaitStmtNode(self, node: WaitStmtNode):
        self.visit(node.duration)
        return None

    def visit_DefaultValStmtNode(self, node: DefaultValStmtNode):
        # Value is just a number, no type check needed really
        return None

    def visit_ExprStmtNode(self, node: ExprStmtNode):
        return self.visit(node.expr)

    def visit_ReturnStmtNode(self, node: ReturnStmtNode):
        return self.visit(node.expr) if node.expr else None

    def visit_AlertStmtNode(self, node: AlertStmtNode):
        # Message is string, level is enum
        return None

    def visit_LogStmtNode(self, node: LogStmtNode):
        return None

    # ✅ DELETED: visit_ExecProcStmtNode (Procedures are now native expressions)

    # ── Conditions & boolean expressions ──────────────────────────────

    def visit_CompExprNode(self, node: CompExprNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type == ERROR_TYPE or right_type == ERROR_TYPE:
            return BOOL_TYPE
        
        # ✅ Use the updated compatibility check that enforces Atom matching
        if not units_compatible_for_op(left_type, right_type, node.op):
            self.log_error(node, f"❌ عدم توافق فيزيائي: لا يمكن مقارنة '{left_type}' مع '{right_type}'. يجب أن تكون الأبعاد والوحدات الذرية متطابقة تماماً.")
            return ERROR_TYPE
        return BOOL_TYPE

    def visit_VotingCondNode(self, node: VotingCondNode):
        if node.threshold > node.total:
            self.log_error(node, f"❌ منطق التصويت: العتبة ({node.threshold}) أكبر من العدد الكلي ({node.total}).")
        if node.threshold <= 0:
            self.log_error(node, "❌ منطق التصويت: العتبة يجب أن تكون أكبر من صفر.")
            
        units_in_vote = set()
        for comp in node.comparisons:
            self.visit(comp)
            if hasattr(comp.left, 'identifier'):
                sym = self.current_scope.resolve(comp.left.identifier)
                if sym and hasattr(sym, 'type') and isinstance(sym.type, UnitType):
                    units_in_vote.add(sym.type.unit_name)
        if len(units_in_vote) > 1:
            self.log_error(node, f"❌ التصويت يتطلب وحدات متطابقة. الوحدات المكتشفة: {units_in_vote}")
        return BOOL_TYPE

    def visit_TemporalCondNode(self, node: TemporalCondNode):
        cond_type = self.visit(node.condition)
        self.visit(node.duration)
        if cond_type and cond_type != ERROR_TYPE and cond_type != BOOL_TYPE:
            self.log_error(node, "❌ الشرط داخل 'عند_استمرار' يجب أن يكون منطقياً.")
        return BOOL_TYPE

    def visit_NotCondNode(self, node: NotCondNode):
        self.visit(node.operand)
        return BOOL_TYPE

    def visit_BinaryCondNode(self, node: BinaryCondNode):
        self.visit(node.left)
        self.visit(node.right)
        return BOOL_TYPE

    def visit_VariableCondNode(self, node: VariableCondNode):
        sym = self.resolve_symbol(node.identifier, node.line)
        if sym is not None and hasattr(sym, 'type') and sym.type != BOOL_TYPE and sym.type != ERROR_TYPE:
            self.log_warning(node, f"⚠️ المتغير '{node.identifier}' من نوع '{sym.type}' وليس منطقياً، يُستخدم كشرط.")
        return BOOL_TYPE

    def visit_VariableExprNode(self, node: VariableExprNode):
        sym = self.resolve_symbol(node.identifier, node.line)
        if sym is None:
            return ERROR_TYPE
        if isinstance(sym, ActuatorSymbol):
            self.log_error(node, "❌ لا يمكن القراءة من مشغّل (Actuator) لأنه للكتابة فقط.")
            return ERROR_TYPE
        if node.index_expr is not None:
            if not getattr(sym, 'is_array', False):
                self.log_error(node, f"'{node.identifier}' ليس مصفوفة، لا يمكن الفهرسة عليه.")
            self.visit(node.index_expr)
        return sym.type if hasattr(sym, 'type') else ERROR_TYPE

    def visit_BinaryOpNode(self, node: BinaryOpNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type == ERROR_TYPE or right_type == ERROR_TYPE:
            return ERROR_TYPE
        if not units_compatible_for_op(left_type, right_type, node.op):
            self.log_error(node, f"❌ وحدات غير متوافقة للعملية '{node.op}'. تأكد من تطابق الأبعاد.")
            return ERROR_TYPE
        return get_result_type(left_type, node.op, right_type)

    def visit_UnaryMinusNode(self, node: UnaryMinusNode):
        return self.visit(node.operand)

    def visit_StringLiteralNode(self, node: StringLiteralNode):
        return STRING_TYPE

    def visit_NumberLiteralNode(self, node: NumberLiteralNode):
        if isinstance(node.value, int): return INT_TYPE
        if isinstance(node.value, float): return FLOAT_TYPE
        return ERROR_TYPE

    def visit_BooleanLiteralNode(self, node: BooleanLiteralNode):
        return BOOL_TYPE

    def visit_AggregateExprNode(self, node: AggregateExprNode):
        sym = self.resolve_symbol(node.identifier, node.line)
        if sym is None:
            return ERROR_TYPE
        if not isinstance(sym, SensorSymbol):
            self.log_error(node, f"❌ الدوال التجميعية ({node.function_name}) تتطلب حساساً، لكن '{node.identifier}' ليس كذلك.")
        self.visit(node.duration)
        return FLOAT_TYPE

    def visit_ProcCallExprNode(self, node: ProcCallExprNode):
        sym = self.current_scope.resolve(node.identifier)
        if sym is None or not isinstance(sym, ProcedureSymbol):
            self.log_error(node, f"❌ الإجراء '{node.identifier}' غير معرّف. هل نسيت تعريفه؟")
            return ERROR_TYPE
        if sym.params != len(node.arguments):
            self.log_error(node, f"❌ عدد المعاملات غير متطابق: الإجراء '{node.identifier}' يتطلب {sym.params} معامل، لكن تم تمرير {len(node.arguments)}.")
        for arg in node.arguments:
            self.visit(arg)
        return sym.return_type if sym.return_type else ERROR_TYPE

    # ── Sensor health rules ───────────────────────────────────────────

    def visit_HealthRuleNode(self, node: HealthRuleNode):
        if node.kind == 'STUCK':
            if node.duration is None:
                self.log_error(node, "❌ قاعدة 'عند_قيمة_ثابتة' تتطلب تحديد مدة (duration).")
            elif node.duration.to_seconds() <= 0:
                self.log_error(node, "❌ مدة قاعدة 'عند_قيمة_ثابتة' يجب أن تكون أكبر من صفر.")
        if not node.statements:
            self.log_warning(node, f"⚠️ قاعدة صحة من نوع '{node.kind}' لا تحتوي على أي إجراء استجابة.")
        for s in node.statements:
            self.visit(s)
        return None

    # ── Escalation chains with DFS cycle detection ─────────────────────

    def visit_EscalationDefNode(self, node: EscalationDefNode):
        temp_levels = {level.level_name for level in node.levels}
        self._defined_modes.update(temp_levels)

        graph = {}
        for level in node.levels:
            for field in level.fields:
                # ✅ UPDATED: Use 'ON_TIMEOUT'
                if field.key == 'ON_TIMEOUT' and isinstance(field.value, GotoStmtNode):
                    graph[level.level_name] = field.value.target_mode
                    if field.value.target_mode not in temp_levels:
                        self.log_error(node, f"❌ التصعيد '{node.identifier}': المستوى الهدف '{field.value.target_mode}' غير معرّف ضمن نفس السلسلة.")

        if self._has_escalation_cycle(graph):
            self.log_error(node, f"❌ سلسلة التصعيد '{node.identifier}' تحتوي على دورة لانهائية (Infinite Cycle) ستؤدي لتعليق النظام.")

        for level in node.levels:
            self.visit(level)
        self._defined_modes.difference_update(temp_levels)
        return None

    def _has_escalation_cycle(self, graph: dict) -> bool:
        visited, rec_stack = set(), set()
        def dfs(node_name):
            visited.add(node_name); rec_stack.add(node_name)
            if node_name in graph:
                neighbor = graph[node_name]
                if neighbor not in visited:
                    if dfs(neighbor): return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(node_name)
            return False
        for node_name in graph:
            if node_name not in visited and dfs(node_name):
                return True
        return False

    def visit_EscalationLevelNode(self, node: EscalationLevelNode):
        for f in node.fields:
            self.visit(f)
        return None

    def visit_EscalationFieldNode(self, node: EscalationFieldNode):
        # ✅ UPDATED: Check ON_TIMEOUT and handle ProcCallExprNode
        if node.key == 'ON_TIMEOUT':
            if isinstance(node.value, ASTNode):
                self.visit(node.value)
        elif node.key == 'TIMEOUT':
             if isinstance(node.value, DurationNode):
                 self.visit(node.value)
        return None

    # ── Reports (Enterprise Scheduling & Maintenance) ───────────────

    def visit_ReportDefNode(self, node: ReportDefNode):
        for f in node.fields: self.visit(f)
        for item in node.content: self.visit(item)
        return None

    def visit_ReportFieldNode(self, node: ReportFieldNode):
        if isinstance(node.value, ScheduleSpecNode):
            self.visit(node.value)
        return None

    # ✅ NEW: Validate Schedule Spec details
    def visit_ScheduleSpecNode(self, node: ScheduleSpecNode):
        if node.frequency == 'INTERVAL':
            if node.interval_ms is not None and node.interval_ms < 0:
                self.log_error(node, "فاصل زمني غير صالح: يجب أن تكون القيمة أكبر من صفر.")
        elif node.frequency in ['DAILY', 'WEEKLY', 'MONTHLY']:
            # Validate Time Format HH:MM
            time_pattern = re.compile(r'^([01]\d|2[0-3]):([0-5]\d)$')
            if not time_pattern.match(node.time_str):
                self.log_error(node, f"وقت غير صالح '{node.time_str}'. الصيغة الصحيحة هي HH:MM (ساعة:دقيقة) بنظام 24 ساعة.")
            
            if node.frequency == 'WEEKLY':
                if node.target_day not in range(0, 7):
                    self.log_error(node, "يوم الأسبوع غير صالح. يجب أن يكون رقماً بين 0 (الأحد) و 6 (السبت).")
                    
            if node.frequency == 'MONTHLY':
                if node.is_last_day:
                    pass # Valid
                elif not (1 <= node.target_day <= 31):
                    self.log_error(node, "يوم الشهر غير صالح. يجب أن يكون رقماً بين 1 و 31.")
        return None

    # ✅ NEW: Validate Report Item types against Hardware
    def visit_ReportItemNode(self, node: ReportItemNode):
        if node.identifier:
            sym = self.current_scope.resolve(node.identifier)
            if sym is None:
                self.log_error(node, f"التقرير يشير إلى معرّف غير موجود: '{node.identifier}'.")
            else:
                # Check specific item types against symbol types
                if node.kind in ['CYCLE_COUNT', 'ACTUATOR_STATE']:
                    if not isinstance(sym, ActuatorSymbol):
                        self.log_error(node, f"عنصر التقرير '{node.kind}' يتطلب مشغلاً (Actuator)، لكن '{node.identifier}' هو '{sym.__class__.__name__}'.")
                elif node.kind == 'SENSOR_HEALTH':
                    if not isinstance(sym, SensorSymbol):
                        self.log_error(node, f"عنصر التقرير '{node.kind}' يتطلب حساساً (Sensor)، لكن '{node.identifier}' هو '{sym.__class__.__name__}'.")
                elif node.kind in ['AGGREGATE', 'INSTANT']:
                    if not isinstance(sym, SensorSymbol):
                        self.log_error(node, f"عنصر التقرير '{node.kind}' يتطلب عادةً حساساً، لكن '{node.identifier}' هو '{sym.__class__.__name__}'.")
                        
        if node.duration is not None:
            self.visit(node.duration)
        return None

    # ── Transition table (FSM) ──────────────────────────────────────

    def visit_TransitionTableNode(self, node: TransitionTableNode):
        seen_pairs = set()
        for rule in node.rules:
            self.visit(rule)
            pair = (rule.from_mode, rule.to_mode)
            if pair in seen_pairs:
                self.log_warning(rule, f"الانتقال {rule.from_mode} → {rule.to_mode} مكرر في جدول الانتقالات.")
            seen_pairs.add(pair)
        return None

    def visit_TransitionRuleNode(self, node: TransitionRuleNode):
        if node.from_mode not in self._defined_modes:
            self.log_error(node, f"وضع المصدر '{node.from_mode}' في جدول الانتقالات غير معرّف.")
        if node.to_mode not in self._defined_modes:
            self.log_error(node, f"وضع الهدف '{node.to_mode}' في جدول الانتقالات غير معرّف.")
        if node.from_mode == node.to_mode:
            self.log_warning(node, f"انتقال ذاتي من '{node.from_mode}' إلى نفسه (لا تأثير له).")
        return None

    # ── Leaf Nodes & Detailed Checks ────────────────────────────────

    def visit_DeviceFieldNode(self, node): 
        # Validation is done in visit_DeviceBlockNode
        return None
    
    def visit_SensorFieldNode(self, node): 
        # Validation is done in visit_SensorDeclNode
        return None
    
    def visit_ActuatorFieldNode(self, node): 
        # Validation is done in visit_ActuatorDeclNode
        return None
    
    def visit_RangeSpecNode(self, node):
        # Validation is done in Hardware visitors
        return None
    
    def visit_BaseTypeNode(self, node): 
        return self.resolve_type(node)
    
    def visit_ArrayTypeNode(self, node): 
        return self.resolve_type(node)

    # ✅ NEW: Check for valid unit names in expressions
    def visit_UnitBaseNode(self, node: UnitBaseNode):
        name = node.unit_name
        if name not in UnitType.BUILTIN_UNITS and name not in self._custom_units:
             self.log_error(node, f"الوحدة '{name}' غير معرّفة ولا توجد في الوحدات المدمجة.")
        return None

    def visit_UnitMathExprNode(self, node: UnitMathExprNode):
        # Logic is handled by compute_unit_signature in ProgramNode pass,
        # but we visit children to catch errors in them.
        self.visit(node.left)
        self.visit(node.right)
        return None
    
    def visit_CustomUnitsBlockNode(self, node: CustomUnitsBlockNode):
        # Check for duplicate unit names
        seen = set()
        for u in node.units:
            if u.identifier in seen:
                self.log_error(u, f"الوحدة '{u.identifier}' مُعرَّفة أكثر من مرة في نفس الكتلة.")
            seen.add(u.identifier)
            self.visit(u.unit_expr) # Visits UnitMathExprNode or UnitBaseNode
        return None

    def visit_CustomUnitDefNode(self, node: CustomUnitDefNode):
        # Logic handled in CustomUnitsBlockNode and ProgramNode
        return None

    def visit_CustomModesBlockNode(self, node): return None
    
    def visit_DurationNode(self, node): 
        if node.value <= 0:
            self.log_warning(node, f"مدة '{node.value} {node.unit}' تساوي صفراً أو أقل. قد لا يكون لها تأثير.")
        return None