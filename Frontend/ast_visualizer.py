import graphviz
from Mizan.Ast.nodes import *

class ASTVisualizerVisitor:
    def __init__(self):
        self.dot = graphviz.Digraph(comment='Mizan AST', format='png')
        self.dot.attr('node', shape='box', style='rounded,filled', fillcolor='white', fontname='Arial')

    def render(self, root_node, output_filename='mizan_ast'):
        root_node.accept(self)
        self.dot.render(output_filename, view=True)

    def add_node_and_edge(self, parent, child, label=""):
        if child:
            if isinstance(child, list):
                for item in child:
                    self.add_node_and_edge(parent, item, label)
            else:
                child.accept(self)
                self.dot.edge(str(id(parent)), str(id(child)), label=label)

    # ── الهيكل الأساسي ──
    def visit_ProgramNode(self, node):
        self.dot.node(str(id(node)), "Program", fillcolor='gray')
        for d in node.declarations: self.add_node_and_edge(node, d, "decl")

    def visit_ProgramDeclNode(self, node):
        self.dot.node(str(id(node)), f"Prog: {node.name}", fillcolor='lightblue')

    # ── الأجهزة والحساسات والمشغلات ──
    def visit_DeviceBlockNode(self, node):
        self.dot.node(str(id(node)), f"Device: {node.identifier}", fillcolor='skyblue')
        for f in node.fields: self.add_node_and_edge(node, f, "field")

    def visit_SensorDeclNode(self, node):
        self.dot.node(str(id(node)), f"Sensor: {node.identifier}", fillcolor='skyblue')
        for f in node.fields: self.add_node_and_edge(node, f, "field")
        
    def visit_ActuatorDeclNode(self, node):
        self.dot.node(str(id(node)), f"Actuator: {node.identifier}", fillcolor='skyblue')
        for f in node.fields: self.add_node_and_edge(node, f, "field")

    def visit_DeviceFieldNode(self, node):
        self.dot.node(str(id(node)), f"{node.key}: {node.value}", fillcolor='white')

    # ── الإجراءات والدوال ──
    def visit_ProcedureDefNode(self, node):
        self.dot.node(str(id(node)), f"Procedure: {node.identifier}", fillcolor='purple', fontcolor='white')
        for p in node.params: self.add_node_and_edge(node, p, "param")
        for s in node.body: self.add_node_and_edge(node, s, "body")

    def visit_ParamNode(self, node):
        self.dot.node(str(id(node)), f"Param: {node.identifier}", fillcolor='lavender')
        self.add_node_and_edge(node, node.var_type, "type")

    # ── المتغيرات والأنواع ──
    def visit_VarDeclNode(self, node):
        self.dot.node(str(id(node)), f"Var: {node.identifier}", fillcolor='lightgreen')
        self.add_node_and_edge(node, node.var_type, "type")
        self.add_node_and_edge(node, node.expr, "expr")

    def visit_ConstDeclNode(self, node):
        self.dot.node(str(id(node)), f"Const: {node.identifier}", fillcolor='yellow')
        self.add_node_and_edge(node, node.expr, "value")

    def visit_BaseTypeNode(self, node):
        self.dot.node(str(id(node)), f"Type: {node.type_name}", fillcolor='lavender')

    # ── التحكم (If, While) ──
    def visit_IfStmtNode(self, node):
        self.dot.node(str(id(node)), "If", fillcolor='orange')
        self.add_node_and_edge(node, node.condition, "cond")
        for s in node.then_branch: self.add_node_and_edge(node, s, "then")
        for s in node.else_branch: self.add_node_and_edge(node, s, "else")

    def visit_WhileStmtNode(self, node):
        self.dot.node(str(id(node)), "While", fillcolor='orange')
        self.add_node_and_edge(node, node.condition, "cond")
        for s in node.body: self.add_node_and_edge(node, s, "body")

    # ── التقارير والتصعيد والتحولات ──
    def visit_ReportDefNode(self, node):
        self.dot.node(str(id(node)), f"Report: {node.identifier}", fillcolor='pink')
        for c in node.content: self.add_node_and_edge(node, c, "item")

    def visit_EscalationDefNode(self, node):
        self.dot.node(str(id(node)), f"Escalation: {node.identifier}", fillcolor='salmon')
        for l in node.levels: self.add_node_and_edge(node, l, "level")

    def visit_TransitionTableNode(self, node):
        self.dot.node(str(id(node)), "Transitions", fillcolor='gold')
        for r in node.rules: self.add_node_and_edge(node, r, "rule")

    # ── التعابير والعمليات ──
    def visit_BinaryOpNode(self, node):
        self.dot.node(str(id(node)), f"Op: {node.op}", fillcolor='lightyellow')
        self.add_node_and_edge(node, node.left, "left")
        self.add_node_and_edge(node, node.right, "right")

    def visit_CompExprNode(self, node):
        self.dot.node(str(id(node)), f"Comp: {node.op}", fillcolor='lightyellow')
        self.add_node_and_edge(node, node.left, "left")
        self.add_node_and_edge(node, node.right, "right")

    def visit_NumberLiteralNode(self, node):
        self.dot.node(str(id(node)), str(node.value), fillcolor='white')

    def visit_DurationNode(self, node):
        self.dot.node(str(id(node)), f"{node.value} {node.unit}", fillcolor='cyan')

    def visit_VariableExprNode(self, node):
        self.dot.node(str(id(node)), f"ID: {node.identifier}", fillcolor='white')

    def __getattr__(self, name):
        return lambda node: self.dot.node(str(id(node)), f"{node.__class__.__name__}", fillcolor='red')
    
    # ── تحديث دالة الـ AssignStmt لتطابق الـ Grammar ──
    def visit_AssignStmtNode(self, node):
        label = f"Assign: {node.identifier}"
        self.dot.node(str(id(node)), label, fillcolor='salmon')
        
        # في الـ Grammar: ID (LBRACKET expr RBRACKET)? ASSIGN expr SEMI
        # إذا وجد index_expr (مصفوفة)
        if node.index_expr:
            self.add_node_and_edge(node, node.index_expr, "index")
        
        # التعبير الذي سيتم إسناده (الجزء بعد علامة =)
        if node.expr:
            self.add_node_and_edge(node, node.expr, "expr")

    # إضافة دعم لـ ProcCallExprNode (مهم جداً للـ ExecProcStmt)
    def visit_ProcCallExprNode(self, node):
        self.dot.node(str(id(node)), f"Call: {node.identifier}", fillcolor='plum')
        for arg in node.arguments:
            self.add_node_and_edge(node, arg, "arg")

    # إضافة دعم لـ ExecProcStmtNode
    def visit_ExecProcStmtNode(self, node):
        self.dot.node(str(id(node)), f"Exec: {node.identifier}", fillcolor='orchid')
        for arg in node.arguments:
            self.add_node_and_edge(node, arg, "arg")

    # ── إضافات لضمان اكتمال التغطية ──
    def visit_AlertStmtNode(self, node):
        self.dot.node(str(id(node)), f"Alert: {node.level}", fillcolor='red', fontcolor='white')
        self.dot.node(str(id(node) + 1), node.message, shape='note')
        self.dot.edge(str(id(node)), str(id(node) + 1))

    def visit_LogStmtNode(self, node):
        self.dot.node(str(id(node)), f"Log: {node.message}", fillcolor='lightgrey')

    def visit_GotoStmtNode(self, node):
        self.dot.node(str(id(node)), f"Goto: {node.target}", fillcolor='khaki')

    def visit_WaitStmtNode(self, node):
        self.dot.node(str(id(node)), "Wait", fillcolor='cyan')
        self.add_node_and_edge(node, node.duration, "time")