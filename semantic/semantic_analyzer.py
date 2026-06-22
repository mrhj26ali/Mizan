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
    FloatType, IntType, compute_dimension_signature, dimension_signatures_equal,
)

_BUILTIN_MODES = {'اقلاع', 'تشغيل', 'صيانة', 'طوارئ'}


class SemanticAnalyzer:

    def __init__(self):
        self.current_scope: Environment = Environment(name="Global")
        self.all_scopes: list[Environment] = [self.current_scope]
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self._defined_modes: set[str] = set(_BUILTIN_MODES)
        self._defined_procs: set[str] = set()
        self._custom_unit_signatures: dict[str, dict] = {}
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
        if isinstance(node, int):
            line, col = node, 0
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

    def _exit_scope(self, target_scope):
        self.current_scope = target_scope

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
            if name in UnitType.BUILTIN_UNITS: return UnitType(name)
            if name in self._custom_unit_signatures:
                return UnitType(name, dimension=self._custom_unit_signatures[name])
            sym = self.current_scope.resolve(name)
            if sym is not None:
                return UnitType(name)
            self.log_error(type_node, f"النوع '{name}' غير معرّف.")
            return ERROR_TYPE
        return ERROR_TYPE

    def resolve_symbol(self, identifier: str, line: int = 0):
        sym = self.current_scope.resolve(identifier)
        if sym is None:
            self.log_error(line, f"المعرّف '{identifier}' غير معرّف.")
        return sym

    def print_report(self):
        print("\n" + "=" * 60 + "\n📊 تقرير التحليل الدلالي\n" + "=" * 60)
        if self.errors:
            print(f"\n🔴 الأخطاء ({len(self.errors)}):")
            for e in self.errors: print(f"  {e}")
        else:
            print("\n✅ لا توجد أخطاء دلالية.")
        if self.warnings:
            print(f"\n🟡 التحذيرات ({len(self.warnings)}):")
            for w in self.warnings: print(f"  {w}")
        print(f"\n📦 النطاقات المُنشأة ({len(self.all_scopes)}):")
        for scope in self.all_scopes:
            print(f"  • {scope.name} — {len(scope.symbols)} رمز")
        print("=" * 60 + "\n")

    # ── Program structure & procedures ──────────────────────────────

    def visit_ProgramNode(self, node: ProgramNode):
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
                    self._custom_unit_signatures[u.identifier] = compute_dimension_signature(u.dimension.elements)
            elif isinstance(decl, EscalationDefNode):
                level_names = [lv.level_name for lv in decl.levels]
                self.current_scope.define(decl.identifier, EscalationSymbol(decl.identifier, level_names))

        for decl in node.declarations:
            self.visit(decl)
        return None

    def visit_ProgramDeclNode(self, node: ProgramDeclNode):
        print(f"📁 بدء تحليل البرنامج: {node.name}")
        return None

    def visit_ProcedureDefNode(self, node: ProcedureDefNode):
        return_type = self.resolve_type(node.return_type) if node.return_type else None
        self.current_scope.define(node.identifier,
            ProcedureSymbol(node.identifier, return_type=return_type, params=len(node.params)))
        old_scope = self.current_scope
        self._enter_scope(f"Proc_{node.identifier}")
        for param in node.params:
            self.visit(param)
        for stmt in node.body:
            ret_type = self.visit(stmt)
            if isinstance(stmt, ReturnStmtNode) and return_type:
                if ret_type and ret_type != ERROR_TYPE and not self._types_compatible(return_type, ret_type):
                    self.log_error(stmt, f"نوع الإرجاع '{ret_type}' لا يتوافق مع '{return_type}' في '{node.identifier}'.")
        self._exit_scope(old_scope)
        return None

    def visit_ParamNode(self, node: ParamNode):
        param_type = self.resolve_type(node.var_type)
        self.current_scope.define(node.identifier, VariableSymbol(node.identifier, param_type))
        return param_type

    # ── Hardware validation ──────────────────────────────────────────

    def visit_DeviceBlockNode(self, node: DeviceBlockNode):
        fields_dict, has_ip, has_port, protocol = {}, False, False, None
        for field in node.fields:
            fields_dict[field.key] = (f"{field.value.value} {field.value.unit}"
                                       if isinstance(field.value, DurationNode) else field.value)
            if field.key == 'IP': has_ip = True
            elif field.key == 'PORT': has_port = True
            elif field.key == 'PROTOCOL': protocol = field.value

        if protocol and protocol.lower() in ['modbus_tcp', 'mqtt', 'opcua']:
            if not has_ip:
                self.log_error(node, f"جهاز '{node.identifier}' يفتقر إلى IP.")
            if not has_port:
                self.log_error(node, f"جهاز '{node.identifier}' يفتقر إلى منفذ.")

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
            elif field.key == 'HEALTH':
                health_rules = field.value
                for rule in field.value:
                    self.visit(rule)
        if sensor_address is None:
            self.log_error(node, f"حساس '{node.identifier}' يفتقر إلى عنوان (Address).")
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
        if actuator_address is None:
            self.log_error(node, f"مشغل '{node.identifier}' يفتقر إلى عنوان (Address).")
        self.current_scope.define(node.identifier,
            ActuatorSymbol(node.identifier, actuator_type, None, actuator_address))
        return None

    # ── Variables, constants & types ──────────────────────────────────

    def visit_VarDeclNode(self, node: VarDeclNode):
        declared_type = self.resolve_type(node.var_type)
        expr_type = self.visit(node.expr)
        if expr_type and expr_type != ERROR_TYPE and declared_type != ERROR_TYPE:
            if not self._types_compatible(declared_type, expr_type):
                self.log_error(node, f"نوع التعبير '{expr_type}' لا يتوافق مع '{declared_type}'.")
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
        if declared == actual: return True
        if isinstance(declared, FloatType) and isinstance(actual, IntType): return True
        if isinstance(declared, UnitType) and isinstance(actual, (IntType, FloatType)): return True
        if isinstance(declared, (FloatType, IntType)) and isinstance(actual, UnitType): return True
        if isinstance(declared, UnitType) and isinstance(actual, UnitType):
            if declared.unit_name == actual.unit_name: return True
            if declared.dimension is not None and actual.dimension is not None:
                return dimension_signatures_equal(declared.dimension, actual.dimension)
        return False

    # ── Operating modes & safety rules ────────────────────────────────

    def visit_ModeBlockNode(self, node: ModeBlockNode):
        is_builtin = node.mode_name in _BUILTIN_MODES
        self._defined_modes.add(node.mode_name)
        self.current_scope.define(node.mode_name, ModeSymbol(node.mode_name, is_builtin=is_builtin))

        old_scope, old_mode = self.current_scope, self.current_mode
        self.current_mode = node.mode_name
        self._enter_scope(f"Mode_{node.mode_name}")

        for stmt in node.on_start_statements:
            self.visit(stmt)

        seen_rule_names = set()
        for rule in node.rules:
            if rule.identifier in seen_rule_names:
                self.log_error(rule, f"القاعدة '{rule.identifier}' مُعرَّفة أكثر من مرة في وضع '{node.mode_name}'.")
            seen_rule_names.add(rule.identifier)
            self.visit(rule)

        self._exit_scope(old_scope)
        self.current_mode = old_mode
        return None

    def visit_RuleBlockNode(self, node: RuleBlockNode):
        old_scope = self.current_scope
        self._enter_scope(f"Rule_{node.identifier}")
        self.current_scope.define(node.identifier, RuleSymbol(node.identifier, self.current_mode or "؟"))
        for decl in node.local_declarations:
            self.visit(decl)
        cond_type = self.visit(node.condition)
        if cond_type and cond_type != ERROR_TYPE and cond_type != BOOL_TYPE:
            self.log_error(node, "شرط القاعدة يجب أن يكون منطقياً.")
        if not node.actions:
            self.log_warning(node, f"القاعدة '{node.identifier}' لا تحتوي على أي إجراء تنفيذ.")
        for action in node.actions:
            self.visit(action)
        self._exit_scope(old_scope)
        return None

    # ── Statements ───────────────────────────────────────────────────

    def visit_CommandStmtNode(self, node: CommandStmtNode):
        if self.current_mode == 'صيانة':
            self.log_error(node, "أوامر المشغلات محظورة تماماً في وضع الصيانة (IEC 62443).")
        sym = self.resolve_symbol(node.identifier, node.line)
        if sym is not None and not isinstance(sym, ActuatorSymbol):
            self.log_error(node, f"'{node.identifier}' ليس مشغّلاً.")
        if isinstance(node.value, ASTNode):
            self.visit(node.value)
        return None

    def visit_AssignStmtNode(self, node: AssignStmtNode):
        sym = self.resolve_symbol(node.identifier, node.line)
        if sym is None:
            return ERROR_TYPE
        if isinstance(sym, SensorSymbol):
            self.log_error(node, "لا يمكن إسناد قيمة لحساس (القراءة فقط).")
            return ERROR_TYPE
        if isinstance(sym, ConstSymbol):
            self.log_error(node, "لا يمكن إسناد قيمة للثابت.")
            return ERROR_TYPE
        if node.index_expr is not None and not getattr(sym, 'is_array', False):
            self.log_error(node, f"'{node.identifier}' ليس مصفوفة، لا يمكن الفهرسة عليه.")
        var_type = sym.type
        val_type = self.visit(node.expr)
        if val_type and val_type != ERROR_TYPE and var_type != ERROR_TYPE:
            if not self._types_compatible(var_type, val_type):
                self.log_error(node, f"لا يمكن إسناد '{val_type}' إلى '{var_type}'.")
        return var_type

    def visit_IfStmtNode(self, node: IfStmtNode):
        cond_type = self.visit(node.condition)
        if cond_type and cond_type != ERROR_TYPE and cond_type != BOOL_TYPE:
            self.log_error(node, "شرط 'اذا' يجب أن يكون منطقياً.")
        old_scope = self.current_scope
        self._enter_scope(f"If_then_{node.line}")
        for stmt in node.then_branch: self.visit(stmt)
        self._exit_scope(old_scope)
        if node.else_branch:
            self._enter_scope(f"If_else_{node.line}")
            for stmt in node.else_branch: self.visit(stmt)
            self._exit_scope(old_scope)
        return None

    def visit_WhileStmtNode(self, node: WhileStmtNode):
        cond_type = self.visit(node.condition)
        if cond_type and cond_type != ERROR_TYPE and cond_type != BOOL_TYPE:
            self.log_error(node, "شرط 'طالما' يجب أن يكون منطقياً.")
        old_scope = self.current_scope
        self._enter_scope(f"While_{node.line}")
        for stmt in node.body: self.visit(stmt)
        self._exit_scope(old_scope)
        return None

    def visit_GotoStmtNode(self, node: GotoStmtNode):
        if node.target_mode not in self._defined_modes:
            self.log_error(node, f"وضع التشغيل الهدف '{node.target_mode}' غير معرّف (انتقل_الى).")
        return None

    def visit_WaitStmtNode(self, node: WaitStmtNode):
        self.visit(node.duration)
        return None

    def visit_DefaultValStmtNode(self, node: DefaultValStmtNode):
        return None

    def visit_ExprStmtNode(self, node: ExprStmtNode):
        return self.visit(node.expr)

    def visit_ReturnStmtNode(self, node: ReturnStmtNode):
        return self.visit(node.expr) if node.expr else None

    def visit_AlertStmtNode(self, node: AlertStmtNode):
        return None

    def visit_LogStmtNode(self, node: LogStmtNode):
        return None

    def visit_ExecProcStmtNode(self, node: ExecProcStmtNode):
        sym = self.current_scope.resolve(node.identifier)
        if sym is None or not isinstance(sym, ProcedureSymbol):
            self.log_error(node, f"الإجراء '{node.identifier}' غير معرّف.")
        elif sym.params != len(node.arguments):
            self.log_error(node, f"الإجراء '{node.identifier}' يتطلب {sym.params} معامل، لكن تم تمرير {len(node.arguments)}.")
        for arg in node.arguments:
            self.visit(arg)
        return None

    # ── Conditions & boolean expressions ──────────────────────────────

    def visit_CompExprNode(self, node: CompExprNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type == ERROR_TYPE or right_type == ERROR_TYPE:
            return BOOL_TYPE
        if not self._types_compatible_for_comp(left_type, right_type):
            self.log_error(node, f"لا يمكن مقارنة '{left_type}' مع '{right_type}'.")
            return ERROR_TYPE
        return BOOL_TYPE

    def _types_compatible_for_comp(self, left, right) -> bool:
        if isinstance(left, FloatType) and isinstance(right, IntType): return True
        if isinstance(left, IntType) and isinstance(right, FloatType): return True
        return units_compatible_for_op(left, right, '==')

    def visit_VotingCondNode(self, node: VotingCondNode):
        if node.threshold > node.total:
            self.log_error(node, f"عتبة التصويت ({node.threshold}) أكبر من العدد الكلي ({node.total}).")
        if node.threshold <= 0:
            self.log_error(node, "عتبة التصويت يجب أن تكون أكبر من صفر.")
        if node.total <= 0:
            self.log_error(node, "العدد الكلي للتصويت يجب أن يكون أكبر من صفر.")
        if node.total != len(node.comparisons):
            self.log_error(node, f"عدد المقارنات ({len(node.comparisons)}) لا يطابق العدد الكلي المُعلن ({node.total}).")

        units_in_vote = set()
        for comp in node.comparisons:
            self.visit(comp)
            if hasattr(comp.left, 'identifier'):
                sym = self.current_scope.resolve(comp.left.identifier)
                if sym and hasattr(sym, 'type') and isinstance(sym.type, UnitType):
                    units_in_vote.add(sym.type.unit_name)
        if len(units_in_vote) > 1:
            self.log_error(node, f"التصويت يتطلب أن تكون جميع المستشعرات من نفس الوحدة الفيزيائية. الوحدات المكتشفة: {units_in_vote}")
        return BOOL_TYPE

    def visit_TemporalCondNode(self, node: TemporalCondNode):
        cond_type = self.visit(node.condition)
        self.visit(node.duration)
        if cond_type and cond_type != ERROR_TYPE and cond_type != BOOL_TYPE:
            self.log_error(node, "الشرط داخل 'عند_استمرار' يجب أن يكون منطقياً.")
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
            self.log_warning(node, f"المتغير '{node.identifier}' من نوع '{sym.type}' وليس منطقياً، يُستخدم كشرط.")
        return BOOL_TYPE

    def visit_VariableExprNode(self, node: VariableExprNode):
        sym = self.resolve_symbol(node.identifier, node.line)
        if sym is None:
            return ERROR_TYPE
        if isinstance(sym, ActuatorSymbol):
            self.log_error(node, "لا يمكن القراءة من مشغّل (الكتابة فقط).")
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
            self.log_error(node, f"وحدات غير متوافقة للعملية '{node.op}'.")
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
            self.log_error(node, f"الدوال التجميعية ({node.function_name}) تتطلب حساساً، لكن '{node.identifier}' ليس كذلك.")
        self.visit(node.duration)
        return FLOAT_TYPE

    def visit_ProcCallExprNode(self, node: ProcCallExprNode):
        sym = self.current_scope.resolve(node.identifier)
        if sym is None or not isinstance(sym, ProcedureSymbol):
            self.log_error(node, f"الإجراء '{node.identifier}' غير معرّف.")
            return ERROR_TYPE
        if sym.params != len(node.arguments):
            self.log_error(node, f"الإجراء '{node.identifier}' يتطلب {sym.params} معامل، لكن تم تمرير {len(node.arguments)}.")
        for arg in node.arguments:
            self.visit(arg)
        return sym.return_type if sym.return_type else ERROR_TYPE

    # ── Sensor health rules ───────────────────────────────────────────

    def visit_HealthRuleNode(self, node: HealthRuleNode):
        if node.kind == 'STUCK':
            if node.duration is None:
                self.log_error(node, "قاعدة 'عند_قيمة_ثابتة' تتطلب تحديد مدة.")
            elif node.duration.to_seconds() <= 0:
                self.log_error(node, "مدة قاعدة 'عند_قيمة_ثابتة' يجب أن تكون أكبر من صفر.")
        if not node.statements:
            self.log_warning(node, f"قاعدة صحة من نوع '{node.kind}' لا تحتوي على أي إجراء استجابة.")
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
                if field.key == 'IF_NO_RESP' and isinstance(field.value, GotoStmtNode):
                    graph[level.level_name] = field.value.target_mode
                    if field.value.target_mode not in temp_levels:
                        self.log_error(node, f"التصعيد '{node.identifier}': المستوى الهدف '{field.value.target_mode}' غير معرّف ضمن نفس السلسلة.")

        if self._has_escalation_cycle(graph):
            self.log_error(node, f"سلسلة التصعيد '{node.identifier}' تحتوي على دورة لانهائية (Infinite Cycle).")

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
        if node.key == 'IF_NO_RESP' and isinstance(node.value, ExecProcStmtNode):
            self.visit_ExecProcStmtNode(node.value)
        elif node.key == 'TIMEOUT' and isinstance(node.value, DurationNode):
            self.visit(node.value)
        return None

    # ── Reports ──────────────────────────────────────────────────────

    def visit_ReportDefNode(self, node: ReportDefNode):
        for f in node.fields: self.visit(f)
        for item in node.content: self.visit(item)
        return None

    def visit_ReportFieldNode(self, node: ReportFieldNode):
        if isinstance(node.value, ScheduleSpecNode):
            self.visit(node.value)
        return None

    def visit_ScheduleSpecNode(self, node: ScheduleSpecNode):
        return None

    def visit_ReportItemNode(self, node: ReportItemNode):
        if node.identifier is not None:
            sym = self.current_scope.resolve(node.identifier)
            if sym is None:
                self.log_error(node, f"التقرير يشير إلى معرّف غير موجود: '{node.identifier}'.")
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
            self.log_warning(node, f"انتقال ذاتي من '{node.from_mode}' إلى نفسه.")
        return None

    # ── Remaining structural / pass-through nodes ─────────────────────

    def visit_DeviceFieldNode(self, node): return None
    def visit_SensorFieldNode(self, node): return None
    def visit_ActuatorFieldNode(self, node): return None
    def visit_RangeSpecNode(self, node): return None
    def visit_BaseTypeNode(self, node): return self.resolve_type(node)
    def visit_ArrayTypeNode(self, node): return self.resolve_type(node)
    def visit_CustomUnitsBlockNode(self, node): return None
    def visit_CustomUnitDefNode(self, node): return None
    def visit_DimensionExprNode(self, node): return None
    def visit_CustomModesBlockNode(self, node): return None
    def visit_DurationNode(self, node): return None