from Mizan.Ast.nodes import *
from Mizan.semantic.environment import Environment, SemanticError
from Mizan.semantic.symbols import (
    VariableSymbol, ConstSymbol, ProcedureSymbol,
    SensorSymbol, ActuatorSymbol, DeviceSymbol, ModeSymbol
)

# ✅ FIX: Import EVERYTHING from the exact same module path!
from Mizan.semantic.types_system import (
    BOOL_TYPE, INT_TYPE, FLOAT_TYPE, STRING_TYPE, ERROR_TYPE,
    UnitType, get_result_type, types_compatible, units_compatible_for_op,
    FloatType, IntType 
)

# =====================================================================
# المحلل الدلالي الكامل لـ Mizan (النسخة النهائية المطابقة للمواصفات)
# =====================================================================

class SemanticAnalyzer:

    def __init__(self):
        self.current_scope: Environment = Environment(name="Global")
        self.all_scopes: list[Environment] = [self.current_scope]
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self._defined_modes: set[str] = set()
        self._defined_procs: set[str] = set()
        self.current_mode: str = None

    # ─────────────────────────────────────────────────────────────────
    # البنية التحتية للزيارة
    # ─────────────────────────────────────────────────────────────────

    def visit(self, node):
        if node is None: return None
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for item in node: self.visit(item)
            return None
        return None

    def log_error(self, node, message: str):
        if isinstance(node, int): line, col = node, 0
        else: line, col = getattr(node, 'line', 0), getattr(node, 'column', 0)
        self.errors.append(f"❌ خطأ دلالي في السطر {line}:{col} -> {message}")

    def _enter_scope(self, name: str) -> Environment:
        new_scope = Environment(name=name, enclosing=self.current_scope)
        self.all_scopes.append(new_scope)
        self.current_scope = new_scope
        return new_scope

    def _exit_scope(self, target_scope):
        self.current_scope = target_scope

    def resolve_type(self, type_node) -> object:
        if type_node is None: return ERROR_TYPE
        if isinstance(type_node, ArrayTypeNode):
            return self.resolve_type(type_node.element_type)  
        if isinstance(type_node, BaseTypeNode):
            name = type_node.type_name
            if name in ('منطقي',): return BOOL_TYPE
            if name in ('صحيح', 'عدد_صحيح'): return INT_TYPE
            if name in ('حقيقي', 'عدد_حقيقي'): return FLOAT_TYPE
            unit_names = {
                'سيلزيوس', 'بار', 'باسكال', 'فولت', 'امبير',
                'دورة_في_الدقيقة', 'لتر_في_الدقيقة', 'بالمئة',
                'متر', 'NTU', 'لا_وحدة', 'بار_في_الثانية', 'سيلزيوس_في_الثانية',
            }
            if name in unit_names: return UnitType(name)
            sym = self.current_scope.resolve(name)
            if sym is not None: return UnitType(name)
            self.log_error(type_node, f"النوع '{name}' غير معرّف.")
            return ERROR_TYPE
        return ERROR_TYPE

    def resolve_symbol(self, identifier: str, line: int = 0):
        sym = self.current_scope.resolve(identifier)
        if sym is None: self.log_error(line, f"المعرّف '{identifier}' غير معرّف.")
        return sym

    def print_report(self):
        print("\n" + "=" * 60)
        print("📊 تقرير التحليل الدلالي")
        print("=" * 60)
        if self.errors:
            print(f"\n🔴 الأخطاء ({len(self.errors)}):")
            for e in self.errors: print(f"  {e}")
        else:
            print("\n✅ لا توجد أخطاء دلالية.")
        print(f"\n📦 النطاقات المُنشأة ({len(self.all_scopes)}):")
        for scope in self.all_scopes:
            print(f"  • {scope.name} — {len(scope.symbols)} رمز")
        print("=" * 60 + "\n")

    # ─────────────────────────────────────────────────────────────────
    # الهيكل الأساسي والإجراءات
    # ─────────────────────────────────────────────────────────────────

    def visit_ProgramNode(self, node: ProgramNode):
        for decl in node.declarations:
            if isinstance(decl, ProcedureDefNode):
                self._defined_procs.add(decl.identifier)
                sym = ProcedureSymbol(decl.identifier, return_type=None, params=len(decl.params))
                self.current_scope.define(decl.identifier, sym)
            elif isinstance(decl, ModeBlockNode):
                self._defined_modes.add(decl.mode_name)
        for decl in node.declarations: self.visit(decl)
        return None

    def visit_ProgramDeclNode(self, node: ProgramDeclNode):
        print(f"📁 بدء تحليل البرنامج: {node.name}")
        return None

    def visit_ProcedureDefNode(self, node: ProcedureDefNode):
        return_type = self.resolve_type(node.return_type) if node.return_type else None
        sym = ProcedureSymbol(node.identifier, return_type=return_type, params=len(node.params))
        self.current_scope.define(node.identifier, sym)
        old_scope = self.current_scope
        self._enter_scope(f"Proc_{node.identifier}")
        for param in node.params: self.visit(param)
        for stmt in node.body:
            ret_type = self.visit(stmt)
            if isinstance(stmt, ReturnStmtNode) and return_type:
                if ret_type and ret_type != ERROR_TYPE:
                    if not self._types_compatible(return_type, ret_type):
                        self.log_error(stmt, f"نوع الإرجاع '{ret_type}' لا يتوافق مع '{return_type}' في '{node.identifier}'.")
        self._exit_scope(old_scope)
        return None

    def visit_ParamNode(self, node: ParamNode):
        param_type = self.resolve_type(node.var_type)
        sym = VariableSymbol(node.identifier, param_type)
        self.current_scope.define(node.identifier, sym)
        return param_type

    # ─────────────────────────────────────────────────────────────────
    # الأجهزة والعتاد (Hardware Validation)
    # ─────────────────────────────────────────────────────────────────

    def visit_DeviceBlockNode(self, node: DeviceBlockNode):
        fields_dict, has_ip, has_port, protocol = {}, False, False, None
        for field in node.fields:
            if isinstance(field.value, DurationNode): fields_dict[field.key] = f"{field.value.value} {field.value.unit}"
            else: fields_dict[field.key] = field.value
            if field.key == 'IP': has_ip = True
            elif field.key == 'PORT': has_port = True
            elif field.key == 'PROTOCOL': protocol = field.value
        
        if protocol and protocol.lower() in ['modbus_tcp', 'mqtt', 'opcua']:
            if not has_ip: self.log_error(node, f"جهاز '{node.identifier}' يفتقر إلى IP.")
            if not has_port: self.log_error(node, f"جهاز '{node.identifier}' يفتقر إلى منفذ.")
        
        sym = DeviceSymbol(node.identifier, fields_dict.get('TYPE', 'Unknown'), fields_dict.get('PROTOCOL', 'N/A'), fields_dict)
        self.current_scope.define(node.identifier, sym)
        return None

    def visit_SensorDeclNode(self, node: SensorDeclNode):
        sensor_type, sensor_address = None, None
        for field in node.fields:
            if field.key == 'TYPE': sensor_type = self.resolve_type(field.value)
            elif field.key == 'ADDRESS': sensor_address = field.value
            elif field.key == 'HEALTH':
                for rule in field.value: self.visit(rule)
        if sensor_address is None: self.log_error(node, f"حساس '{node.identifier}' يفتقر إلى عنوان (Address).")
        sym = SensorSymbol(node.identifier, sensor_type, None, sensor_address)
        self.current_scope.define(node.identifier, sym)
        return None

    def visit_ActuatorDeclNode(self, node: ActuatorDeclNode):
        actuator_type, actuator_address = None, None
        for field in node.fields:
            if field.key == 'TYPE': actuator_type = self.resolve_type(field.value)
            elif field.key == 'ADDRESS': actuator_address = field.value
        if actuator_address is None: self.log_error(node, f"مشغل '{node.identifier}' يفتقر إلى عنوان (Address).")
        sym = ActuatorSymbol(node.identifier, actuator_type, None, actuator_address)
        self.current_scope.define(node.identifier, sym)
        return None

    # ─────────────────────────────────────────────────────────────────
    # المتغيرات والثوابت والأنواع
    # ─────────────────────────────────────────────────────────────────

    def visit_VarDeclNode(self, node: VarDeclNode):
        declared_type = self.resolve_type(node.var_type)
        expr_type = self.visit(node.expr)
        if expr_type and expr_type != ERROR_TYPE and declared_type != ERROR_TYPE:
            if not self._types_compatible(declared_type, expr_type):
                self.log_error(node, f"نوع التعبير '{expr_type}' لا يتوافق مع '{declared_type}'.")
        sym = VariableSymbol(node.identifier, declared_type)
        try: self.current_scope.define_strict(node.identifier, sym, node)
        except SemanticError as e: self.log_error(node, str(e))
        return declared_type

    def visit_ConstDeclNode(self, node: ConstDeclNode):
        declared_type = self.resolve_type(node.var_type) 
        expr_type = self.visit(node.expr)               
        if not types_compatible(declared_type, expr_type):
            self.log_error(node, f"نوع قيمة الثابت '{expr_type}' لا يتوافق مع '{declared_type}'.")
        sym = ConstSymbol(node.identifier, declared_type)
        self.current_scope.define_strict(node.identifier, sym, node)
        return declared_type

    def _types_compatible(self, declared, actual) -> bool:
        if declared == actual: return True
        if isinstance(declared, FloatType) and isinstance(actual, IntType): return True
        if isinstance(declared, UnitType) and isinstance(actual, (IntType, FloatType)): return True
        if isinstance(declared, (FloatType, IntType)) and isinstance(actual, UnitType): return True
        return False

    # ─────────────────────────────────────────────────────────────────
    # الأوضاع وقواعد الأمان (IEC 62443)
    # ─────────────────────────────────────────────────────────────────

    def visit_ModeBlockNode(self, node: ModeBlockNode):
        self._defined_modes.add(node.mode_name)
        self.current_scope.define(node.mode_name, ModeSymbol(node.mode_name))
        old_scope, old_mode = self.current_scope, self.current_mode
        self.current_mode = node.mode_name    
        self._enter_scope(f"Mode_{node.mode_name}")
        for stmt in node.on_start_statements: self.visit(stmt)
        for rule in node.rules: self.visit(rule)
        self._exit_scope(old_scope)
        self.current_mode = old_mode          
        return None

    def visit_RuleBlockNode(self, node: RuleBlockNode):
        old_scope = self.current_scope
        self._enter_scope(f"Rule_{node.identifier}")
        for decl in node.local_declarations: self.visit(decl)
        cond_type = self.visit(node.condition)
        if cond_type and cond_type != ERROR_TYPE and cond_type != BOOL_TYPE:
            self.log_error(node, f"شرط القاعدة يجب أن يكون منطقياً.")
        for action in node.actions: self.visit(action)
        self._exit_scope(old_scope)
        return None

    # ─────────────────────────────────────────────────────────────────
    # الجمل البرمجية (Statements)
    # ─────────────────────────────────────────────────────────────────

    def visit_CommandStmtNode(self, node: CommandStmtNode):
        if self.current_mode == 'صيانة':
            self.log_error(node, f"أوامر المشغلات محظورة تماماً في وضع الصيانة (IEC 62443).")
        sym = self.resolve_symbol(node.identifier, node.line)
        if sym is not None and not isinstance(sym, ActuatorSymbol):
            self.log_error(node, f"'{node.identifier}' ليس مشغّلاً.")
        if isinstance(node.value, ASTNode): self.visit(node.value)
        return None

    def visit_AssignStmtNode(self, node: AssignStmtNode):
        sym = self.resolve_symbol(node.identifier, node.line)
        if sym is None: return ERROR_TYPE
        if isinstance(sym, SensorSymbol):
            self.log_error(node, f"لا يمكن إسناد قيمة لحساس (القراءة فقط).")
            return ERROR_TYPE
        if isinstance(sym, ConstSymbol):
            self.log_error(node, f"لا يمكن إسناد قيمة للثابت.")
            return ERROR_TYPE
        var_type = sym.type
        val_type = self.visit(node.expr)
        if val_type and val_type != ERROR_TYPE and var_type != ERROR_TYPE:
            if not self._types_compatible(var_type, val_type):
                self.log_error(node, f"لا يمكن إسناد '{val_type}' إلى '{var_type}'.")
        return var_type

    def visit_IfStmtNode(self, node: IfStmtNode):
        cond_type = self.visit(node.condition)
        if cond_type and cond_type != ERROR_TYPE and cond_type != BOOL_TYPE:
            self.log_error(node, f"شرط 'اذا' يجب أن يكون منطقياً.")
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
            self.log_error(node, f"شرط 'طالما' يجب أن يكون منطقياً.")
        old_scope = self.current_scope
        self._enter_scope(f"While_{node.line}")
        for stmt in node.body: self.visit(stmt)
        self._exit_scope(old_scope)
        return None

    # ─────────────────────────────────────────────────────────────────
    # الشروط والتعبيرات المنطقية
    # ─────────────────────────────────────────────────────────────────

    def visit_CompExprNode(self, node: CompExprNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type == ERROR_TYPE or right_type == ERROR_TYPE: return BOOL_TYPE
        if not self._types_compatible_for_comp(left_type, right_type):
            self.log_error(node, f"لا يمكن مقارنة '{left_type}' مع '{right_type}'.")
            return ERROR_TYPE
        return BOOL_TYPE

    def _types_compatible_for_comp(self, left, right) -> bool:
        if isinstance(left, FloatType) and isinstance(right, IntType): return True
        if isinstance(left, IntType) and isinstance(right, FloatType): return True
        return units_compatible_for_op(left, right, '==')

    # ✅ FIX: التصويت الزائد (Voting) - التحقق من تطابق الوحدات الفيزيائية
    def visit_VotingCondNode(self, node: VotingCondNode):
        if node.threshold > node.total:
            self.log_error(node, f"عتبة التصويت ({node.threshold}) أكبر من العدد الكلي ({node.total}).")
        if node.threshold <= 0:
            self.log_error(node, f"عتبة التصويت يجب أن تكون أكبر من صفر.")
        if node.total <= 0:
            self.log_error(node, f"العدد الكلي للتصويت يجب أن يكون أكبر من صفر.")

        # المواصفات: "يتحقق المجمِّع أن جميع المستشعرات في التصويت تشترك في نفس نوع الوحدة الفيزيائية"
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

    def visit_VariableExprNode(self, node: VariableExprNode):
        sym = self.resolve_symbol(node.identifier, node.line)
        if sym is None: return ERROR_TYPE
        if isinstance(sym, ActuatorSymbol):
            self.log_error(node, f"لا يمكن القراءة من مشغّل (الكتابة فقط).")
            return ERROR_TYPE
        return sym.type if hasattr(sym, 'type') else ERROR_TYPE

    def visit_BinaryOpNode(self, node: BinaryOpNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type == ERROR_TYPE or right_type == ERROR_TYPE: return ERROR_TYPE
        if not units_compatible_for_op(left_type, right_type, node.op):
            self.log_error(node, f"وحدات غير متوافقة للعملية '{node.op}'.")
            return ERROR_TYPE
        return get_result_type(left_type, node.op, right_type)

    # ✅ FIX: النصوص يجب أن تُعيد STRING_TYPE
    def visit_StringLiteralNode(self, node: StringLiteralNode):
        return STRING_TYPE

    def visit_NumberLiteralNode(self, node: NumberLiteralNode):
        if isinstance(node.value, int): return INT_TYPE
        if isinstance(node.value, float): return FLOAT_TYPE
        return ERROR_TYPE

    def visit_BooleanLiteralNode(self, node: BooleanLiteralNode):
        return BOOL_TYPE

    # ─────────────────────────────────────────────────────────────────
    # التصعيد (Escalation) مع خوارزمية DFS لاكتشاف الدورات
    # ─────────────────────────────────────────────────────────────────

    def visit_EscalationDefNode(self, node: EscalationDefNode):
        temp_levels = set()
        for level in node.levels: temp_levels.add(level.level_name)
        self._defined_modes.update(temp_levels)

        graph = {}
        for level in node.levels:
            for field in level.fields:
                if field.key == 'IF_NO_RESP' and isinstance(field.value, GotoStmtNode):
                    graph[level.level_name] = field.value.target_mode

        # ✅ FIX: استدعاء خوارزمية DFS بعد تعريفها
        if self._has_escalation_cycle(graph):
            self.log_error(node, f"سلسلة التصعيد '{node.identifier}' تحتوي على دورة لانهائية (Infinite Cycle).")

        for level in node.levels: self.visit(level)
        self._defined_modes.difference_update(temp_levels)

    # ✅ FIX: إضافة خوارزمية DFS المفقودة
    def _has_escalation_cycle(self, graph: dict) -> bool:
        """
        Performs a Depth-First Search (DFS) to detect cycles in the escalation graph.
        """
        visited = set()
        rec_stack = set()

        def dfs(node_name):
            visited.add(node_name)
            rec_stack.add(node_name)
            if node_name in graph:
                neighbor = graph[node_name]
                if neighbor not in visited:
                    if dfs(neighbor): return True
                elif neighbor in rec_stack:
                    return True  # Cycle detected!
            rec_stack.remove(node_name)
            return False

        for node_name in graph:
            if node_name not in visited:
                if dfs(node_name): return True
        return False

    # ─────────────────────────────────────────────────────────────────
    # عقد أخرى (Pass-through)
    # ─────────────────────────────────────────────────────────────────
    def visit_DeviceFieldNode(self, node): return None
    def visit_SensorFieldNode(self, node): return None
    def visit_ActuatorFieldNode(self, node): return None
    def visit_RangeSpecNode(self, node): return None
    def visit_HealthRuleNode(self, node): return None
    def visit_BaseTypeNode(self, node): return self.resolve_type(node)
    def visit_ArrayTypeNode(self, node): return self.resolve_type(node)
    def visit_CustomUnitsBlockNode(self, node): return None
    def visit_CustomUnitDefNode(self, node): return None
    def visit_DimensionExprNode(self, node): return None
    def visit_CustomModesBlockNode(self, node): return None
    def visit_AlertStmtNode(self, node): return None
    def visit_LogStmtNode(self, node): return None
    def visit_ExecProcStmtNode(self, node): return None
    def visit_GotoStmtNode(self, node): return None
    def visit_WaitStmtNode(self, node): return None
    def visit_DefaultValStmtNode(self, node): return None
    def visit_ExprStmtNode(self, node): return self.visit(node.expr)
    def visit_NotCondNode(self, node): return BOOL_TYPE
    def visit_BinaryCondNode(self, node): return BOOL_TYPE
    def visit_TemporalCondNode(self, node): return BOOL_TYPE
    def visit_VariableCondNode(self, node): return BOOL_TYPE
    def visit_UnaryMinusNode(self, node): return self.visit(node.operand)
    def visit_AggregateExprNode(self, node): return FLOAT_TYPE
    def visit_ProcCallExprNode(self, node): return None
    def visit_ReturnStmtNode(self, node): return self.visit(node.expr) if node.expr else None
    def visit_EscalationLevelNode(self, node): return None
    def visit_EscalationFieldNode(self, node): return None
    def visit_ReportDefNode(self, node): return None
    def visit_ReportFieldNode(self, node): return None
    def visit_ScheduleSpecNode(self, node): return None
    def visit_ReportItemNode(self, node): return None
    def visit_TransitionTableNode(self, node): return None
    def visit_TransitionRuleNode(self, node): return None
    def visit_DurationNode(self, node): return None