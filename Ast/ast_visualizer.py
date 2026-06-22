import graphviz
from Ast.nodes import *


class ASTVisualizerVisitor:
    def __init__(self):
        self.dot = graphviz.Digraph(comment='Mizan AST', format='png')
        self.dot.attr(rankdir='TB', splines='ortho', nodesep='0.5', ranksep='0.7')
        self.dot.attr('node', shape='box', style='rounded,filled', fillcolor='white',
                      fontname='Arial', fontsize='11')
        self.dot.attr('edge', fontname='Arial', fontsize='9', color='#555555')

    def render(self, root_node, output_filename='mizan_ast'):
        root_node.accept(self)
        self.dot.render(output_filename, view=False)

    def add_node_and_edge(self, parent, child, label=""):
        if child is None:
            return
        if isinstance(child, list):
            for item in child:
                self.add_node_and_edge(parent, item, label)
        elif isinstance(child, ASTNode):
            child.accept(self)
            self.dot.edge(str(id(parent)), str(id(child)), label=label)

    def visit_ProgramNode(self, node):
        self.dot.node(str(id(node)), "Program", fillcolor='#B0BEC5')
        for d in node.declarations:
            self.add_node_and_edge(node, d, "decl")

    def visit_ProgramDeclNode(self, node):
        self.dot.node(str(id(node)), f"برنامج\n{node.name}", fillcolor='#90CAF9')

    def visit_DeviceBlockNode(self, node):
        self.dot.node(str(id(node)), f"جهاز\n{node.identifier}", fillcolor='#81D4FA')
        for f in node.fields:
            self.add_node_and_edge(node, f, "حقل")

    def visit_DeviceFieldNode(self, node):
        val = node.value if not isinstance(node.value, ASTNode) else "..."
        self.dot.node(str(id(node)), f"{node.key}\n{val}", fillcolor='#E3F2FD')
        if isinstance(node.value, ASTNode):
            self.add_node_and_edge(node, node.value, "قيمة")

    def visit_CustomUnitsBlockNode(self, node):
        self.dot.node(str(id(node)), "وحدات مخصصة", fillcolor='#CE93D8')
        for u in node.units:
            self.add_node_and_edge(node, u, "وحدة")

    def visit_CustomUnitDefNode(self, node):
        self.dot.node(str(id(node)), f"وحدة: {node.identifier}", fillcolor='#E1BEE7')
        self.add_node_and_edge(node, node.dimension, "بُعد")

    def visit_DimensionExprNode(self, node):
        label = " ".join(node.elements)
        self.dot.node(str(id(node)), f"بُعد\n{label}", fillcolor='#F3E5F5')

    def visit_CustomModesBlockNode(self, node):
        self.dot.node(str(id(node)), f"أوضاع مخصصة\n{', '.join(node.modes)}", fillcolor='#CE93D8')

    def visit_SensorDeclNode(self, node):
        self.dot.node(str(id(node)), f"حساس\n{node.identifier}", fillcolor='#80DEEA')
        for f in node.fields:
            self.add_node_and_edge(node, f, "حقل")

    def visit_SensorFieldNode(self, node):
        if node.key == 'HEALTH' and isinstance(node.value, list):
            self.dot.node(str(id(node)), "صحة الحساس", fillcolor='#B2EBF2')
            for rule in node.value:
                self.add_node_and_edge(node, rule, "قاعدة")
        else:
            val = node.value if not isinstance(node.value, ASTNode) else "..."
            self.dot.node(str(id(node)), f"{node.key}\n{val}", fillcolor='#E0F7FA')
            if isinstance(node.value, ASTNode):
                self.add_node_and_edge(node, node.value, "قيمة")

    def visit_ActuatorDeclNode(self, node):
        self.dot.node(str(id(node)), f"مشغّل\n{node.identifier}", fillcolor='#80CBC4')
        for f in node.fields:
            self.add_node_and_edge(node, f, "حقل")

    def visit_ActuatorFieldNode(self, node):
        val = node.value if not isinstance(node.value, ASTNode) else "..."
        self.dot.node(str(id(node)), f"{node.key}\n{val}", fillcolor='#E0F2F1')
        if isinstance(node.value, ASTNode):
            self.add_node_and_edge(node, node.value, "قيمة")

    def visit_RangeSpecNode(self, node):
        self.dot.node(str(id(node)), f"نطاق\n[{node.min_val} .. {node.max_val}]", fillcolor='#DCEDC8')

    def visit_HealthRuleNode(self, node):
        dur = f"\nمدة: {node.duration.value} {node.duration.unit}" if node.duration else ""
        self.dot.node(str(id(node)), f"قاعدة صحة\n{node.kind}{dur}", fillcolor='#FFF9C4')
        for s in node.statements:
            self.add_node_and_edge(node, s, "جملة")

    def visit_BaseTypeNode(self, node):
        self.dot.node(str(id(node)), f"نوع\n{node.type_name}", fillcolor='#E8EAF6')

    def visit_ArrayTypeNode(self, node):
        self.dot.node(str(id(node)), f"مصفوفة[{node.size}]", fillcolor='#C5CAE9')
        self.add_node_and_edge(node, node.element_type, "نوع العنصر")

    def visit_VarDeclNode(self, node):
        self.dot.node(str(id(node)), f"متغير\n{node.identifier}", fillcolor='#C8E6C9')
        self.add_node_and_edge(node, node.var_type, "نوع")
        self.add_node_and_edge(node, node.expr, "قيمة")

    def visit_ConstDeclNode(self, node):
        self.dot.node(str(id(node)), f"ثابت\n{node.identifier}", fillcolor='#FFF9C4')
        self.add_node_and_edge(node, node.var_type, "نوع")
        self.add_node_and_edge(node, node.expr, "قيمة")

    def visit_ProcedureDefNode(self, node):
        ret = f"\nيرجع: {node.return_type}" if node.return_type else ""
        self.dot.node(str(id(node)), f"إجراء\n{node.identifier}{ret}", fillcolor='#CE93D8', fontcolor='white')
        for p in node.params:
            self.add_node_and_edge(node, p, "معامل")
        for s in node.body:
            self.add_node_and_edge(node, s, "جسم")

    def visit_ParamNode(self, node):
        self.dot.node(str(id(node)), f"معامل\n{node.identifier}", fillcolor='#E1BEE7')
        self.add_node_and_edge(node, node.var_type, "نوع")

    def visit_ModeBlockNode(self, node):
        self.dot.node(str(id(node)), f"وضع\n{node.mode_name}", fillcolor='#FFCC80')
        for s in node.on_start_statements:
            self.add_node_and_edge(node, s, "عند_بدء")
        for r in node.rules:
            self.add_node_and_edge(node, r, "قاعدة")

    def visit_RuleBlockNode(self, node):
        self.dot.node(str(id(node)), f"قاعدة\n{node.identifier}", fillcolor='#FFE082')
        for d in node.local_declarations:
            self.add_node_and_edge(node, d, "محلي")
        self.add_node_and_edge(node, node.condition, "شرط")
        for a in node.actions:
            self.add_node_and_edge(node, a, "تنفيذ")

    def visit_CommandStmtNode(self, node):
        val = node.value if isinstance(node.value, str) else "expr"
        self.dot.node(str(id(node)), f"أمر\n{node.identifier} ← {val}", fillcolor='#FFCDD2')
        if isinstance(node.value, ASTNode):
            self.add_node_and_edge(node, node.value, "قيمة")

    def visit_AlertStmtNode(self, node):
        self.dot.node(str(id(node)), f"تنبيه [{node.level}]\n\"{node.message}\"", fillcolor='#EF9A9A')

    def visit_LogStmtNode(self, node):
        self.dot.node(str(id(node)), f"سجل\n\"{node.message}\"", fillcolor='#CFD8DC')

    def visit_ExecProcStmtNode(self, node):
        self.dot.node(str(id(node)), f"نفّذ إجراء\n{node.identifier}", fillcolor='#B39DDB')
        for a in node.arguments:
            self.add_node_and_edge(node, a, "وسيط")

    def visit_GotoStmtNode(self, node):
        self.dot.node(str(id(node)), f"انتقل إلى\n{node.target_mode}", fillcolor='#FFCCBC')

    def visit_WaitStmtNode(self, node):
        self.dot.node(str(id(node)), "انتظر", fillcolor='#B2EBF2')
        self.add_node_and_edge(node, node.duration, "مدة")

    def visit_AssignStmtNode(self, node):
        self.dot.node(str(id(node)), f"إسناد\n{node.identifier}", fillcolor='#FFAB91')
        if node.index_expr:
            self.add_node_and_edge(node, node.index_expr, "فهرس")
        self.add_node_and_edge(node, node.expr, "قيمة")

    def visit_DefaultValStmtNode(self, node):
        self.dot.node(str(id(node)), f"قيمة افتراضية\n{node.value}", fillcolor='#ECEFF1')

    def visit_ExprStmtNode(self, node):
        self.dot.node(str(id(node)), "تعبير-جملة", fillcolor='#F5F5F5')
        self.add_node_and_edge(node, node.expr, "تعبير")

    def visit_IfStmtNode(self, node):
        self.dot.node(str(id(node)), "اذا", fillcolor='#FFCC80')
        self.add_node_and_edge(node, node.condition, "شرط")
        for s in node.then_branch:
            self.add_node_and_edge(node, s, "إذا_صح")
        for s in node.else_branch:
            self.add_node_and_edge(node, s, "والا")

    def visit_WhileStmtNode(self, node):
        self.dot.node(str(id(node)), "طالما", fillcolor='#FFCC80')
        self.add_node_and_edge(node, node.condition, "شرط")
        for s in node.body:
            self.add_node_and_edge(node, s, "جسم")

    def visit_ReturnStmtNode(self, node):
        self.dot.node(str(id(node)), "ارجع", fillcolor='#F8BBD0')
        if node.expr:
            self.add_node_and_edge(node, node.expr, "قيمة")

    def visit_BinaryCondNode(self, node):
        self.dot.node(str(id(node)), node.op, fillcolor='#FFF176')
        self.add_node_and_edge(node, node.left, "يسار")
        self.add_node_and_edge(node, node.right, "يمين")

    def visit_NotCondNode(self, node):
        self.dot.node(str(id(node)), "ليس", fillcolor='#FFF176')
        self.add_node_and_edge(node, node.operand, "معامل")

    def visit_CompExprNode(self, node):
        self.dot.node(str(id(node)), f"مقارنة\n{node.op}", fillcolor='#FFF9C4')
        self.add_node_and_edge(node, node.left, "يسار")
        self.add_node_and_edge(node, node.right, "يمين")

    def visit_TemporalCondNode(self, node):
        self.dot.node(str(id(node)), "عند_استمرار", fillcolor='#B3E5FC')
        self.add_node_and_edge(node, node.condition, "شرط")
        self.add_node_and_edge(node, node.duration, "لمدة")

    def visit_VotingCondNode(self, node):
        self.dot.node(str(id(node)), f"تصويت\n{node.threshold} من {node.total}", fillcolor='#DCEDC8')
        for c in node.comparisons:
            self.add_node_and_edge(node, c, "مقارنة")

    def visit_BooleanLiteralNode(self, node):
        label = "صح" if node.value else "خطأ"
        color = '#A5D6A7' if node.value else '#EF9A9A'
        self.dot.node(str(id(node)), label, fillcolor=color)

    def visit_VariableCondNode(self, node):
        self.dot.node(str(id(node)), f"شرط-متغير\n{node.identifier}", fillcolor='#FFF9C4')

    def visit_BinaryOpNode(self, node):
        self.dot.node(str(id(node)), f"عملية\n{node.op}", fillcolor='#FFFDE7')
        self.add_node_and_edge(node, node.left, "يسار")
        self.add_node_and_edge(node, node.right, "يمين")

    def visit_UnaryMinusNode(self, node):
        self.dot.node(str(id(node)), "سالب أحادي", fillcolor='#FFFDE7')
        self.add_node_and_edge(node, node.operand, "معامل")

    def visit_AggregateExprNode(self, node):
        self.dot.node(str(id(node)),
                      f"{node.function_name}\n({node.identifier})\nخلال: {node.duration.value} {node.duration.unit}",
                      fillcolor='#B2DFDB')

    def visit_ProcCallExprNode(self, node):
        self.dot.node(str(id(node)), f"استدعاء\n{node.identifier}", fillcolor='#CE93D8')
        for a in node.arguments:
            self.add_node_and_edge(node, a, "وسيط")

    def visit_NumberLiteralNode(self, node):
        self.dot.node(str(id(node)), str(node.value), fillcolor='#F5F5F5')

    def visit_StringLiteralNode(self, node):
        self.dot.node(str(id(node)), f'"{node.value}"', fillcolor='#FFF8E1')

    def visit_VariableExprNode(self, node):
        self.dot.node(str(id(node)), f"متغير\n{node.identifier}", fillcolor='#F5F5F5')
        if node.index_expr:
            self.add_node_and_edge(node, node.index_expr, "فهرس")

    def visit_EscalationDefNode(self, node):
        self.dot.node(str(id(node)), f"تصعيد\n{node.identifier}", fillcolor='#FFAB91')
        for lv in node.levels:
            self.add_node_and_edge(node, lv, "مستوى")

    def visit_EscalationLevelNode(self, node):
        self.dot.node(str(id(node)), f"مستوى\n{node.level_name}", fillcolor='#FFCCBC')
        for f in node.fields:
            self.add_node_and_edge(node, f, "حقل")

    def visit_EscalationFieldNode(self, node):
        if isinstance(node.value, ASTNode) and not isinstance(node.value, DurationNode):
            self.dot.node(str(id(node)), f"تصعيد-حقل\n{node.key}", fillcolor='#FBE9E7')
            self.add_node_and_edge(node, node.value, "إجراء")
        elif isinstance(node.value, DurationNode):
            self.dot.node(str(id(node)), f"{node.key}", fillcolor='#FBE9E7')
            self.add_node_and_edge(node, node.value, "مدة")
        else:
            self.dot.node(str(id(node)), f"{node.key}\n{node.value}", fillcolor='#FBE9E7')

    def visit_ReportDefNode(self, node):
        self.dot.node(str(id(node)), f"تقرير\n{node.identifier}", fillcolor='#F48FB1')
        for f in node.fields:
            self.add_node_and_edge(node, f, "حقل")
        for c in node.content:
            self.add_node_and_edge(node, c, "عنصر")

    def visit_ReportFieldNode(self, node):
        if isinstance(node.value, ASTNode):
            self.dot.node(str(id(node)), f"حقل-تقرير\n{node.key}", fillcolor='#FCE4EC')
            self.add_node_and_edge(node, node.value, "قيمة")
        else:
            self.dot.node(str(id(node)), f"{node.key}\n{node.value}", fillcolor='#FCE4EC')

    def visit_ScheduleSpecNode(self, node):
        day = f" {node.day}" if node.day else ""
        self.dot.node(str(id(node)), f"جدول\n{node.frequency}{day}\nالساعة {node.time}", fillcolor='#F8BBD0')

    def visit_ReportItemNode(self, node):
        func = f"{node.function_name} " if node.function_name else ""
        dur = f"\nخلال: {node.duration.value} {node.duration.unit}" if node.duration else ""
        ident = f"\n{node.identifier}" if node.identifier else ""
        self.dot.node(str(id(node)), f"{node.kind}\n{func}{ident}{dur}\n\"{node.title}\"", fillcolor='#FCE4EC')

    def visit_TransitionTableNode(self, node):
        self.dot.node(str(id(node)), "جدول الانتقالات", fillcolor='#FFD54F')
        for r in node.rules:
            self.add_node_and_edge(node, r, "قاعدة")

    def visit_TransitionRuleNode(self, node):
        self.dot.node(str(id(node)), f"انتقال\n{node.from_mode} → {node.to_mode}", fillcolor='#FFF9C4')

    def visit_DurationNode(self, node):
        self.dot.node(str(id(node)), f"{node.value} {node.unit}", fillcolor='#B2EBF2')

    def __getattr__(self, name):
        if name.startswith('visit_'):
            def _fallback(node):
                self.dot.node(str(id(node)), f"⚠ {node.__class__.__name__}",
                              fillcolor='#EF9A9A', style='rounded,filled,dashed')
            return _fallback
        raise AttributeError(name)