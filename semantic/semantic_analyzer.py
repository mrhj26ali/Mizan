from Mizan.Ast.nodes import *
from Mizan.semantic.environment import Environment, SemanticError
from Mizan.semantic.symbols import (
    VariableSymbol, ConstSymbol, ProcedureSymbol,
    SensorSymbol, ActuatorSymbol, DeviceSymbol, ModeSymbol
)
from Mizan.semantic.types_system import (
    BOOL_TYPE, INT_TYPE, FLOAT_TYPE, ERROR_TYPE,
    UnitType, get_result_type
)
from Mizan.semantic.types_system import types_compatible 



# =====================================================================
# المحلل الدلالي الكامل لـ Mizan
# =====================================================================

class SemanticAnalyzer:

    def __init__(self):
        self.current_scope: Environment = Environment(name="Global")
        self.all_scopes: list[Environment] = [self.current_scope]
        self.errors: list[str] = []
        self.warnings: list[str] = []
        # أسماء الأوضاع المعرّفة (للتحقق من goto وtransitions)
        self._defined_modes: set[str] = set()
        # أسماء الإجراءات المعرّفة (للتحقق من الاستدعاء قبل التعريف)
        self._defined_procs: set[str] = set()
        # ✅ FIX: Track the current operating mode for IEC 62443 safety lockout
        self.current_mode: str = None
    # ─────────────────────────────────────────────────────────────────
    # البنية التحتية للزيارة
    # ─────────────────────────────────────────────────────────────────

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
        self.warnings.append(
            f"⚠️ لا يوجد معالج للعقدة: {type(node).__name__}"
        )
        return None

    # ─────────────────────────────────────────────────────────────────
    # دوال مساعدة
    # ─────────────────────────────────────────────────────────────────

    def log_error(self, node, message: str):
        # node may be an AST node or an integer line number
        if isinstance(node, int):
            line = node
            col = 0
        else:
            line = getattr(node, 'line', 0)
            col = getattr(node, 'column', 0)
        self.errors.append(f"❌ خطأ دلالي في السطر {line}:{col} -> {message}")

# مثال للاستخدام داخل الـ visit:
# self.log_error(node, f"المتغير '{node.identifier}' غير معرف.")

    def _enter_scope(self, name: str) -> Environment:
        new_scope = Environment(name=name, enclosing=self.current_scope)
        self.all_scopes.append(new_scope)
        self.current_scope = new_scope
        return new_scope

    def _exit_scope(self, target_scope):
        self.current_scope = target_scope

    def resolve_type(self, type_node) -> object:
        """
        يحوّل BaseTypeNode أو ArrayTypeNode إلى كائن Type.
        يُعيد ERROR_TYPE إذا كان النوع غير معروف.
        """
        if type_node is None:
            return ERROR_TYPE

        if isinstance(type_node, ArrayTypeNode):
            element_type = self.resolve_type(type_node.element_type)
            return element_type  

        if isinstance(type_node, BaseTypeNode):
            name = type_node.type_name
            if name in ('منطقي',):
                return BOOL_TYPE
            if name in ('صحيح', 'عدد_صحيح'):
                return INT_TYPE
            if name in ('حقيقي', 'عدد_حقيقي'):
                return FLOAT_TYPE
            # أنواع الوحدات الفيزيائية
            unit_names = {
                'سيلزيوس', 'بار', 'باسكال', 'فولت', 'امبير',
                'دورة_في_الدقيقة', 'لتر_في_الدقيقة', 'بالمئة',
                'متر', 'NTU', 'لا_وحدة', 'بار_في_الثانية',
                'سيلزيوس_في_الثانية',
            }
            if name in unit_names:
                return UnitType(name)
            # وحدة مخصصة مُعرَّفة من قبل المستخدم
            sym = self.current_scope.resolve(name)
            if sym is not None:
                return UnitType(name)
            self.log_error(type_node, f"النوع '{name}' غير معرّف.")
            return ERROR_TYPE

        return ERROR_TYPE

    def resolve_symbol(self, identifier: str, line: int = 0):
        """يبحث عن رمز في النطاق الحالي والنطاقات المحيطة.
        إذا لم يُعثر على الرمز، يستخدم رقم السطر الممرَّر للإبلاغ عن الخطأ.
        """
        sym = self.current_scope.resolve(identifier)
        if sym is None:
            # نمرر رقم السطر مباشرة إلى log_error ليُسجَّل الموضع الصحيح
            self.log_error(line, f"المعرّف '{identifier}' غير معرّف.")
        return sym

    def print_report(self):
        """يطبع تقرير التحليل الدلالي."""
        print("\n" + "=" * 60)
        print("📊 تقرير التحليل الدلالي")
        print("=" * 60)
        if self.errors:
            print(f"\n🔴 الأخطاء ({len(self.errors)}):")
            for e in self.errors:
                print(f"  {e}")
        else:
            print("\n✅ لا توجد أخطاء دلالية.")
        if self.warnings:
            print(f"\n🟡 التحذيرات ({len(self.warnings)}):")
            for w in self.warnings:
                print(f"  {w}")
        print(f"\n📦 النطاقات المُنشأة ({len(self.all_scopes)}):")
        for scope in self.all_scopes:
            print(f"  • {scope.name} — {len(scope.symbols)} رمز")
        print("=" * 60 + "\n")


    def visit_VariableAccessNode(self, node):
    # البحث يبدأ من النطاق الحالي ويصعد للأعلى
        symbol = self.current_scope.resolve(node.identifier)
    
        if symbol is None:
        # هنا الخطأ: المتغير لم يُعرف في أي نطاق مرئي!
            self.log_error(node, f"المتغير '{node.identifier}' غير معرّف في هذا النطاق.")
            return ERROR_TYPE # أرجع نوع الخطأ لمنع أخطاء تابعة
        
        return symbol.type # أرجع نوع المتغير إذا وجدته
    # ─────────────────────────────────────────────────────────────────
    # الهيكل الأساسي للبرنامج
    # ─────────────────────────────────────────────────────────────────

    def visit_ProgramNode(self, node: ProgramNode):
        # المرور الأول: تسجيل الإجراءات والأوضاع قبل زيارة الجسم
        # (يحل مشكلة الاستخدام قبل التعريف)
        for decl in node.declarations:
            if isinstance(decl, ProcedureDefNode):
                self._defined_procs.add(decl.identifier)
                sym = ProcedureSymbol(
                    decl.identifier,
                    return_type=None,
                    params=len(decl.params)
                )
                self.current_scope.define(decl.identifier, sym)
            elif isinstance(decl, ModeBlockNode):
                self._defined_modes.add(decl.mode_name)

        for decl in node.declarations:
            self.visit(decl)
        return None

    def visit_ProgramDeclNode(self, node: ProgramDeclNode):
        print(f"📁 بدء تحليل البرنامج: {node.name}")
        return None

    # ─────────────────────────────────────────────────────────────────
    # إعدادات الأجهزة
    # ─────────────────────────────────────────────────────────────────

    def visit_DeviceBlockNode(self, node: DeviceBlockNode):
        fields_dict = {}
        for field in node.fields:
            if isinstance(field.value, DurationNode):
                fields_dict[field.key] = f"{field.value.value} {field.value.unit}"
            else:
                fields_dict[field.key] = field.value
        sym = DeviceSymbol(node.identifier, fields_dict.get('TYPE', 'Unknown'),
                           fields_dict.get('PROTOCOL', 'N/A'), fields_dict)
        self.current_scope.define(node.identifier, sym)
        return None

    def visit_DeviceFieldNode(self, node: DeviceFieldNode):
        if isinstance(node.value, DurationNode):
            self.visit(node.value)
        return None

    # ─────────────────────────────────────────────────────────────────
    # الوحدات والأوضاع المخصصة
    # ─────────────────────────────────────────────────────────────────

    def visit_CustomUnitsBlockNode(self, node: CustomUnitsBlockNode):
        for unit_def in node.units:
            self.visit(unit_def)
        return None

    def visit_CustomUnitDefNode(self, node: CustomUnitDefNode):
        sym = VariableSymbol(node.identifier, UnitType(node.identifier))
        self.current_scope.define(node.identifier, sym)
        return None

    def visit_DimensionExprNode(self, node: DimensionExprNode):
        return None 

    def visit_CustomModesBlockNode(self, node: CustomModesBlockNode):
        for mode_name in node.modes:
            self._defined_modes.add(mode_name)
        return None

    # ─────────────────────────────────────────────────────────────────
    # تعريف العتاد (Sensors & Actuators)
    # ─────────────────────────────────────────────────────────────────

    def visit_SensorDeclNode(self, node: SensorDeclNode):
        sensor_type = None
        sensor_range = None
        sensor_address = None
        for field in node.fields:
            if field.key == 'TYPE':
                sensor_type = self.resolve_type(field.value)
            elif field.key == 'RANGE':
                sensor_range = field.value
            elif field.key == 'ADDRESS':
                sensor_address = field.value
            elif field.key == 'HEALTH':
                for rule in field.value:
                    self.visit(rule)

        sym = SensorSymbol(node.identifier, sensor_type, sensor_range, sensor_address)
        self.current_scope.define(node.identifier, sym)
        return None

    def visit_ActuatorDeclNode(self, node: ActuatorDeclNode):
        actuator_type = None
        actuator_range = None
        actuator_address = None
        for field in node.fields:
            if field.key == 'TYPE':
                actuator_type = self.resolve_type(field.value)
            elif field.key == 'RANGE':
                actuator_range = field.value
            elif field.key == 'ADDRESS':
                actuator_address = field.value

        sym = ActuatorSymbol(node.identifier, actuator_type, actuator_range, actuator_address)
        self.current_scope.define(node.identifier, sym)
        return None

    def visit_SensorFieldNode(self, node: SensorFieldNode):
        """تُزار ضمن visit_SensorDeclNode — هذا المسار الاحتياطي."""
        if node.key == 'HEALTH' and isinstance(node.value, list):
            for rule in node.value:
                self.visit(rule)
        elif isinstance(node.value, ASTNode):
            self.visit(node.value)
        return None

    def visit_ActuatorFieldNode(self, node: ActuatorFieldNode):
        """تُزار ضمن visit_ActuatorDeclNode — هذا المسار الاحتياطي."""
        if isinstance(node.value, ASTNode):
            self.visit(node.value)
        return None

    def visit_RangeSpecNode(self, node: RangeSpecNode):
        if node.min_val >= node.max_val:
            self.log_error(node, f"القيمة الدنيا {node.min_val} يجب أن تكون أقل من القيمة العليا {node.max_val}.")
        return None

    def visit_HealthRuleNode(self, node: HealthRuleNode):
        old_scope = self.current_scope
        self._enter_scope(f"Health_{node.kind}_{node.line}")
        if node.duration:
            self.visit(node.duration)
        for stmt in node.statements:
            self.visit(stmt)
        self._exit_scope(old_scope)
        return None

    # ─────────────────────────────────────────────────────────────────
    # الأنواع
    # ─────────────────────────────────────────────────────────────────

    def visit_BaseTypeNode(self, node: BaseTypeNode):
        return self.resolve_type(node)

    def visit_ArrayTypeNode(self, node: ArrayTypeNode):
        if node.size <= 0:
            self.log_error(node, f"حجم المصفوفة يجب أن يكون أكبر من صفر.")
        return self.resolve_type(node)

    # ─────────────────────────────────────────────────────────────────
    # المتغيرات والثوابت
    # ─────────────────────────────────────────────────────────────────

    def visit_VarDeclNode(self, node: VarDeclNode):
        declared_type = self.resolve_type(node.var_type)
        expr_type = self.visit(node.expr)

    # 1. التحقق من التوافق النوعي
        if expr_type and expr_type != ERROR_TYPE and declared_type != ERROR_TYPE:
            if not self._types_compatible(declared_type, expr_type):
                self.log_error(node, f"نوع التعبير '{expr_type}' لا يتوافق مع '{declared_type}' للمتغير '{node.identifier}'.")

    # 2. استخدام define_strict لضمان عدم إعادة التعريف في نفس النطاق
        sym = VariableSymbol(node.identifier, declared_type)
        try:
            self.current_scope.define_strict(node.identifier, sym, node)
        except SemanticError as e:
            self.log_error(node, str(e))
    
        return declared_type

    def visit_ConstDeclNode(self, node: ConstDeclNode):
        declared_type = self.resolve_type(node.var_type) 
        expr_type = self.visit(node.expr)               

    
        if not types_compatible(declared_type, expr_type):
            self.log_error(node, f"نوع قيمة الثابت '{expr_type}' لا يتوافق مع '{declared_type}' للثابت '{node.identifier}'.")

        sym = ConstSymbol(node.identifier, declared_type)
        self.current_scope.define_strict(node.identifier, sym, node)
        return declared_type

    def _types_compatible(self, declared, actual) -> bool:
        """يتحقق من توافق الأنواع بشكل صارم للإسناد والتهيئة."""
        if declared == actual:
            return True
        return False


    # ─────────────────────────────────────────────────────────────────
    # الإجراءات
    # ─────────────────────────────────────────────────────────────────

    def visit_ProcedureDefNode(self, node: ProcedureDefNode):
        # الرمز سُجّل في المرور الأول — نُحدّث عدد المعاملات ونوع الإرجاع
        return_type = self.resolve_type(node.return_type) if node.return_type else None
        sym = ProcedureSymbol(node.identifier, return_type=return_type,
                              params=len(node.params))
        self.current_scope.define(node.identifier, sym)  # تحديث

        old_scope = self.current_scope
        self._enter_scope(f"Proc_{node.identifier}")

        for param in node.params:
            self.visit(param)

        for stmt in node.body:
            ret_type = self.visit(stmt)
            if isinstance(stmt, ReturnStmtNode) and return_type:
                if ret_type and ret_type != ERROR_TYPE:
                    if not self._types_compatible(return_type, ret_type):
                        self.log_error(stmt, f"نوع الإرجاع '{ret_type}' لا يتوافق مع النوع المُعلَن '{return_type}'"
                            f" في الإجراء '{node.identifier}'.")

        self._exit_scope(old_scope)
        return None

    def visit_ParamNode(self, node: ParamNode):
        param_type = self.resolve_type(node.var_type)
        sym = VariableSymbol(node.identifier, param_type)
        self.current_scope.define(node.identifier, sym)
        return param_type

    # ─────────────────────────────────────────────────────────────────
    # الأوضاع وقواعد الأمان
    # ─────────────────────────────────────────────────────────────────

    def visit_ModeBlockNode(self, node: ModeBlockNode):
        self._defined_modes.add(node.mode_name)
        sym = ModeSymbol(node.mode_name)
        self.current_scope.define(node.mode_name, sym)

        old_scope = self.current_scope
        
        # ✅ FIX: Save the previous mode and set the new one
        old_mode = self.current_mode          
        self.current_mode = node.mode_name    
        
        self._enter_scope(f"Mode_{node.mode_name}")

        for stmt in node.on_start_statements:
            self.visit(stmt)

        for rule in node.rules:
            self.visit(rule)

        self._exit_scope(old_scope)
        
        # ✅ FIX: Restore the previous mode when exiting the block
        self.current_mode = old_mode          
        return None

    def visit_RuleBlockNode(self, node: RuleBlockNode):
        old_scope = self.current_scope
        self._enter_scope(f"Rule_{node.identifier}")

        for decl in node.local_declarations:
            self.visit(decl)

        cond_type = self.visit(node.condition)
        if cond_type and cond_type != ERROR_TYPE and cond_type != BOOL_TYPE:
            self.log_error(node, f"شرط القاعدة '{node.identifier}' يجب أن يكون من نوع منطقي"
                           f" وليس '{cond_type}'.")

        for action in node.actions:
            self.visit(action)

        self._exit_scope(old_scope)
        return None


    def visit_EllipsisNode(self, node): 
        return None
    # ─────────────────────────────────────────────────────────────────
    # الجمل البرمجية
    # ─────────────────────────────────────────────────────────────────

    def visit_CommandStmtNode(self, node: CommandStmtNode):
        # ✅ FIX: IEC 62443 - Hard lockout of actuators in Maintenance Mode
        # Note: The AST builder extracts the exact Arabic text 'صيانة' for this mode.
        if self.current_mode == 'صيانة':
            self.log_error(node, f"أوامر المشغلات محظورة تماماً في وضع الصيانة .")
            
        sym = self.resolve_symbol(node.identifier, node.line)
        if sym is not None and not isinstance(sym, ActuatorSymbol):
            self.log_error(node, f"'{node.identifier}' ليس مشغّلاً (Actuator)، لا يمكن إصدار أمر له.")
    
        if isinstance(node.value, ASTNode):
            self.visit(node.value)
        return None

    def visit_AlertStmtNode(self, node: AlertStmtNode):
        return None

    def visit_LogStmtNode(self, node: LogStmtNode):
        return None

    def visit_ExecProcStmtNode(self, node: ExecProcStmtNode):
        sym = self.resolve_symbol(node.identifier, node.line)
        if sym is not None:
            if not isinstance(sym, ProcedureSymbol):
                self.log_error(node, f"'{node.identifier}' ليس إجراءً.")
            elif sym.params != len(node.arguments):
                self.log_error(node, f"الإجراء '{node.identifier}' يتوقع {sym.params} معامل"
                                f" لكن تم تمرير {len(node.arguments)}.")
        for arg in node.arguments:
            self.visit(arg)
        return None

    def visit_GotoStmtNode(self, node: GotoStmtNode):
        if node.target_mode not in self._defined_modes:
            self.log_error(node, f"الوضع '{node.target_mode}' غير معرّف.")
        return None

    def visit_WaitStmtNode(self, node: WaitStmtNode):
        self.visit(node.duration)
        return None

    def visit_AssignStmtNode(self, node: AssignStmtNode):
        sym = self.resolve_symbol(node.identifier, node.line)
        if sym is None:
            return ERROR_TYPE

        # ✅ FIX: Directional Safety - Sensors are READ-ONLY
        if isinstance(sym, SensorSymbol):
            self.log_error(node, f"لا يمكن إسناد قيمة لحساس '{node.identifier}' (الحساسات للقراءة فقط).")
            return ERROR_TYPE

        if isinstance(sym, ConstSymbol):
            self.log_error(node, f"لا يمكن إسناد قيمة للثابت '{node.identifier}'.")
            return ERROR_TYPE
        
        var_type = sym.type

        if node.index_expr:
            idx_type = self.visit(node.index_expr)
            if idx_type and idx_type not in (INT_TYPE, ERROR_TYPE):
                self.log_error(node, f"فهرس المصفوفة يجب أن يكون من نوع صحيح.")

        val_type = self.visit(node.expr)

        if val_type and val_type != ERROR_TYPE and var_type != ERROR_TYPE:
            if not self._types_compatible(var_type, val_type):
                self.log_error(node, f"لا يمكن إسناد '{val_type}' إلى متغير من نوع '{var_type}'"
                                    f" (المتغير: '{node.identifier}').")

        return var_type

    def visit_DefaultValStmtNode(self, node: DefaultValStmtNode):
        return None

    def visit_ExprStmtNode(self, node: ExprStmtNode):
        return self.visit(node.expr)

    def visit_IfStmtNode(self, node: IfStmtNode):
        cond_type = self.visit(node.condition)
        if cond_type and cond_type != ERROR_TYPE and cond_type != BOOL_TYPE:
            self.log_error(node, f"شرط 'اذا' يجب أن يكون من نوع منطقي وليس '{cond_type}'.")

        old_scope = self.current_scope
        self._enter_scope(f"If_then_{node.line}")
        for stmt in node.then_branch:
            self.visit(stmt)
        self._exit_scope(old_scope)

        if node.else_branch:
            self._enter_scope(f"If_else_{node.line}")
            for stmt in node.else_branch:
                self.visit(stmt)
            self._exit_scope(old_scope)

        return None

    def visit_WhileStmtNode(self, node: WhileStmtNode):
        cond_type = self.visit(node.condition)
        if cond_type and cond_type != ERROR_TYPE and cond_type != BOOL_TYPE:
            self.log_error(node, f"شرط 'طالما' يجب أن يكون من نوع منطقي وليس '{cond_type}'.")

        old_scope = self.current_scope
        self._enter_scope(f"While_{node.line}")
        for stmt in node.body:
            self.visit(stmt)
        self._exit_scope(old_scope)
        return None

    def visit_ReturnStmtNode(self, node: ReturnStmtNode):
        if node.expr:
            return self.visit(node.expr)
        return None

    # ─────────────────────────────────────────────────────────────────
    # الشروط
    # ─────────────────────────────────────────────────────────────────

    def visit_BinaryCondNode(self, node: BinaryCondNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        for side, t in (('يسار', left_type), ('يمين', right_type)):
            if t and t != ERROR_TYPE and t != BOOL_TYPE:
                self.log_error(node, f"الطرف {side} في '{node.op}' يجب أن يكون منطقياً وليس '{t}'.")
        return BOOL_TYPE

    def visit_NotCondNode(self, node: NotCondNode):
        operand_type = self.visit(node.operand)
        if operand_type and operand_type != ERROR_TYPE and operand_type != BOOL_TYPE:
            self.log_error(node, f"معامل 'ليس' يجب أن يكون منطقياً وليس '{operand_type}'.")
                
        return BOOL_TYPE

    def visit_CompExprNode(self, node: CompExprNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type == ERROR_TYPE or right_type == ERROR_TYPE:
            return BOOL_TYPE

        if not self._types_compatible_for_comp(left_type, right_type):
            self.log_error(node, f"لا يمكن مقارنة النوع '{left_type}' مع '{right_type}' (عملية: {node.op}).")
            return ERROR_TYPE
        
        return BOOL_TYPE

    def _types_compatible_for_comp(self, left, right) -> bool:
        """يتحقق من توافق الأنواع للمقارنة المنطقية."""
        if left == right:
            return True
        if isinstance(left, UnitType) and isinstance(right, UnitType):
            return left.name == right.name
        return False

    def visit_TemporalCondNode(self, node: TemporalCondNode):
        cond_type = self.visit(node.condition)
        if cond_type and cond_type != ERROR_TYPE and cond_type != BOOL_TYPE:
            self.log_error(node, f"شرط 'عند_استمرار' يجب أن يكون منطقياً وليس '{cond_type}'.")
                
        self.visit(node.duration)
        return BOOL_TYPE

    def visit_VotingCondNode(self, node: VotingCondNode):
        if node.threshold > node.total:
            self.log_error(node, f"عتبة التصويت ({node.threshold}) أكبر من العدد الكلي ({node.total}).")
        if node.threshold <= 0:
            self.log_error(node, f"عتبة التصويت يجب أن تكون أكبر من صفر.")

        for comp in node.comparisons:
            self.visit(comp)
        return BOOL_TYPE

    def visit_BooleanLiteralNode(self, node: BooleanLiteralNode):
        return BOOL_TYPE

    def visit_VariableCondNode(self, node: VariableCondNode):
        sym = self.resolve_symbol(node.identifier, node.line)
        if sym is None:
            return ERROR_TYPE
        if sym.type != BOOL_TYPE:
            self.log_error(node, f"المتغير '{node.identifier}' ليس منطقياً، لا يمكن استخدامه كشرط.")
        return BOOL_TYPE

    # ─────────────────────────────────────────────────────────────────
    # التعابير الحسابية
    # ─────────────────────────────────────────────────────────────────

    def visit_BinaryOpNode(self, node: BinaryOpNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type is None or right_type is None:
            return ERROR_TYPE
        if left_type == ERROR_TYPE or right_type == ERROR_TYPE:
            return ERROR_TYPE

        result_type = get_result_type(left_type, node.op, right_type)
        if result_type == ERROR_TYPE:
            self.log_error(node, f"العملية '{node.op}' غير مدعومة بين '{left_type}' و '{right_type}'.")
        return result_type

    def visit_UnaryMinusNode(self, node: UnaryMinusNode):
        operand_type = self.visit(node.operand)
        if operand_type == BOOL_TYPE:
            self.log_error(node, f"لا يمكن تطبيق السالب الأحادي على نوع منطقي.")
            return ERROR_TYPE
        return operand_type

    def visit_AggregateExprNode(self, node: AggregateExprNode):
        sym = self.resolve_symbol(node.identifier, node.line)
        if sym is not None and not isinstance(sym, (SensorSymbol, VariableSymbol)):
            self.log_error(node, f"'{node.identifier}' ليس حساساً أو متغيراً، لا يمكن تطبيق '{node.function_name}' عليه.")
        self.visit(node.duration)
        if node.function_name in ('معدل_التغيير', 'متوسط'):
            return FLOAT_TYPE
        if sym and hasattr(sym, 'type'):
            return sym.type
        return FLOAT_TYPE

    def visit_ProcCallExprNode(self, node: ProcCallExprNode):
        sym = self.resolve_symbol(node.identifier, node.line)
        if sym is None:
            return ERROR_TYPE
        if not isinstance(sym, ProcedureSymbol):
            self.log_error(node, f"'{node.identifier}' ليس إجراءً.")
            return ERROR_TYPE
        if sym.params != len(node.arguments):
            self.log_error(node, (
                f"الإجراء '{node.identifier}' يتوقع {sym.params} معامل"
                f" لكن تم تمرير {len(node.arguments)}."
            ))
                
        for arg in node.arguments:
            self.visit(arg)
        return sym.return_type if sym.return_type else None

    def visit_NumberLiteralNode(self, node: NumberLiteralNode):
        if isinstance(node.value, int):
            return INT_TYPE
        if isinstance(node.value, float):
            return FLOAT_TYPE
        self.log_error(node, f"العدد '{node.value}' غير معروف النوع.")
        return ERROR_TYPE

    def visit_StringLiteralNode(self, node: StringLiteralNode):
        return None

    def visit_VariableExprNode(self, node: VariableExprNode):
        sym = self.resolve_symbol(node.identifier, node.line)
        if sym is None:
            return ERROR_TYPE

        # ✅ FIX: Directional Safety - Actuators are WRITE-ONLY
        if isinstance(sym, ActuatorSymbol):
            self.log_error(node, f"لا يمكن القراءة من مشغّل '{node.identifier}' (المشغلات للكتابة فقط).")
            return ERROR_TYPE

        if node.index_expr:
            idx_type = self.visit(node.index_expr)
            if idx_type and idx_type not in (INT_TYPE, ERROR_TYPE):
                self.log_error(node, f"فهرس المصفوفة يجب أن يكون من نوع صحيح.")

        if hasattr(sym, 'type'):
            return sym.type
        return ERROR_TYPE

    # ─────────────────────────────────────────────────────────────────
    # التصعيد (Escalation)
    # ─────────────────────────────────────────────────────────────────

    def visit_EscalationDefNode(self, node: EscalationDefNode):
        for level in node.levels:
            self.visit(level)
        return None

    def visit_EscalationLevelNode(self, node: EscalationLevelNode):
        for field in node.fields:
            self.visit(field)
        return None

    def visit_EscalationFieldNode(self, node: EscalationFieldNode):
        if isinstance(node.value, DurationNode):
            self.visit(node.value)
        elif isinstance(node.value, ASTNode):
            self.visit(node.value)
        return None

    # ─────────────────────────────────────────────────────────────────
    # التقارير
    # ─────────────────────────────────────────────────────────────────

    def visit_ReportDefNode(self, node: ReportDefNode):
        for field in node.fields:
            self.visit(field)
        for item in node.content:
            self.visit(item)
        return None

    def visit_ReportFieldNode(self, node: ReportFieldNode):
        if isinstance(node.value, ASTNode):
            self.visit(node.value)
        return None

    def visit_ScheduleSpecNode(self, node: ScheduleSpecNode):
        return None

    def visit_ReportItemNode(self, node: ReportItemNode):
        if node.identifier:
            self.resolve_symbol(node.identifier, node.line)
        if node.duration:
            self.visit(node.duration)
        return None

    # ─────────────────────────────────────────────────────────────────
    # الانتقالات (FSM)
    # ─────────────────────────────────────────────────────────────────

    def visit_TransitionTableNode(self, node: TransitionTableNode):
        for rule in node.rules:
            self.visit(rule)
        return None

    def visit_TransitionRuleNode(self, node: TransitionRuleNode):
        for mode_name in (node.from_mode, node.to_mode):
            if mode_name not in self._defined_modes:
                self.log_error(node, f"الوضع '{mode_name}' المُستخدَم في الانتقالات غير معرّف.")
        return None

    # ─────────────────────────────────────────────────────────────────
    # الوقت
    # ─────────────────────────────────────────────────────────────────

    def visit_DurationNode(self, node: DurationNode):
        if node.value <= 0:
            self.log_error(node, f"قيمة المدة يجب أن تكون أكبر من صفر.")
        return None