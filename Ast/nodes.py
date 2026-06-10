from dataclasses import dataclass
from typing import List, Optional, Union
from abc import ABC, abstractmethod

from Mizan.Ast.ast_visitor import ASTVisitor

# =====================================================================
# BASE AST NODE & VISITOR INTERFACE
# =====================================================================

@dataclass(kw_only=True)
class ASTNode(ABC):
    line: int = 0
    column: int = 0

    @abstractmethod
    def accept(self, visitor):
        method_name = f'visit_{self.__class__.__name__}'
        visitor_method = getattr(visitor, method_name)
        return visitor_method(self)



# =====================================================================
# STRUCTURAL & CONFIGURATION NODES
# =====================================================================

@dataclass
class ProgramNode(ASTNode):
    declarations: List[ASTNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_ProgramNode(self)

@dataclass
class ProgramDeclNode(ASTNode):
    name: str

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_ProgramDeclNode(self)

@dataclass
class DurationNode(ASTNode):
    value: float
    unit: str  # SECOND_KW, MINUTE_KW, HOUR_KW, DAY_KW, MILLI_SEC_KW

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_DurationNode(self)

@dataclass
class DeviceFieldNode(ASTNode):
    key: str  # 'TYPE', 'OS', 'PROTOCOL', 'IP', 'PORT', 'SERIAL_PORT', 'SCAN_CYCLE'
    value: Union[str, float, DurationNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_DeviceFieldNode(self)

@dataclass
class DeviceBlockNode(ASTNode):
    identifier: str
    fields: List[DeviceFieldNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_DeviceBlockNode(self)

@dataclass
class DimensionExprNode(ASTNode):
    elements: List[str]  # Ordered sequence of operators and base units (e.g., ['MASS', 'DIV', 'VOLUME'])

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_DimensionExprNode(self)

@dataclass
class CustomUnitDefNode(ASTNode):
    identifier: str
    dimension: DimensionExprNode

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_CustomUnitDefNode(self)

@dataclass
class CustomUnitsBlockNode(ASTNode):
    units: List[CustomUnitDefNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_CustomUnitsBlockNode(self)

@dataclass
class CustomModesBlockNode(ASTNode):
    modes: List[str]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_CustomModesBlockNode(self)


# =====================================================================
# TYPE SYSTEMS & HARDWARE DECLARATIONS
# =====================================================================

@dataclass
class BaseTypeNode(ASTNode):
    type_name: str  # 'BOOL', 'INT', 'FLOAT', or custom unit ID

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_BaseTypeNode(self)

@dataclass
class ArrayTypeNode(ASTNode):
    element_type: ASTNode
    size: int

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_ArrayTypeNode(self)

@dataclass
class RangeSpecNode(ASTNode):
    min_val: float
    max_val: float

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_RangeSpecNode(self)

@dataclass
class HealthRuleNode(ASTNode):
    kind: str  # 'DISCONNECT', 'STUCK', 'OUT_OF_RANGE'
    duration: Optional[DurationNode]
    statements: List[ASTNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_HealthRuleNode(self)

@dataclass
class SensorFieldNode(ASTNode):
    key: str  # 'TYPE', 'RANGE', 'ADDRESS', 'HEALTH'
    value: Union[ASTNode, str, List[HealthRuleNode]]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_SensorFieldNode(self)

@dataclass
class SensorDeclNode(ASTNode):
    identifier: str
    fields: List[SensorFieldNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_SensorDeclNode(self)

@dataclass
class ActuatorFieldNode(ASTNode):
    key: str  # 'TYPE', 'RANGE', 'ADDRESS'
    value: Union[ASTNode, str]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_ActuatorFieldNode(self)

@dataclass
class ActuatorDeclNode(ASTNode):
    identifier: str
    fields: List[ActuatorFieldNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_ActuatorDeclNode(self)


# =====================================================================
# CORE VARIABLES & PROCEDURE DECLARATIONS
# =====================================================================

@dataclass
class VarDeclNode(ASTNode):
    identifier: str
    var_type: ASTNode
    expr: ASTNode

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_VarDeclNode(self)

@dataclass
class ConstDeclNode(ASTNode):
    identifier: str
    var_type: ASTNode
    expr: ASTNode

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_ConstDeclNode(self)

@dataclass
class ParamNode(ASTNode):
    identifier: str
    var_type: ASTNode

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_ParamNode(self)

@dataclass
class ProcedureDefNode(ASTNode):
    identifier: str
    params: List[ParamNode]
    return_type: Optional[ASTNode]
    body: List[ASTNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_ProcedureDefNode(self)


# =====================================================================
# OPERATING MODES & SAFETY RULES (IEC 62443)
# =====================================================================

@dataclass
class RuleBlockNode(ASTNode):
    identifier: str
    local_declarations: List[ASTNode]
    condition: ASTNode
    actions: List[ASTNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_RuleBlockNode(self)

@dataclass
class ModeBlockNode(ASTNode):
    mode_name: str  # 'STARTUP', 'RUN', 'MAINTENANCE', 'EMERGENCY', or custom ID
    on_start_statements: List[ASTNode]
    rules: List[RuleBlockNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_ModeBlockNode(self)


# =====================================================================
# STATEMENTS
# =====================================================================

@dataclass
class CommandStmtNode(ASTNode):
    identifier: str
    value: Union[str, ASTNode]  # State constant string or raw expression payload

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_CommandStmtNode(self)

@dataclass
class AlertStmtNode(ASTNode):
    level: str  # 'LEVEL_1', 'LEVEL_2', 'LEVEL_3', or 'LEVEL_N'
    message: str

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_AlertStmtNode(self)

@dataclass
class LogStmtNode(ASTNode):
    message: str

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_LogStmtNode(self)

@dataclass
class ExecProcStmtNode(ASTNode):
    identifier: str
    arguments: List[ASTNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_ExecProcStmtNode(self)

@dataclass
class GotoStmtNode(ASTNode):
    target_mode: str

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_GotoStmtNode(self)

@dataclass
class WaitStmtNode(ASTNode):
    duration: DurationNode

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_WaitStmtNode(self)

@dataclass
class AssignStmtNode(ASTNode):
    identifier: str
    index_expr: Optional[ASTNode]
    expr: ASTNode

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_AssignStmtNode(self)

@dataclass
class DefaultValStmtNode(ASTNode):
    value: float

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_DefaultValStmtNode(self)

@dataclass
class ExprStmtNode(ASTNode):
    expr: ASTNode

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_ExprStmtNode(self)

@dataclass
class IfStmtNode(ASTNode):
    condition: ASTNode
    then_branch: List[ASTNode]
    else_branch: List[ASTNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_IfStmtNode(self)

@dataclass
class WhileStmtNode(ASTNode):
    condition: ASTNode
    body: List[ASTNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_WhileStmtNode(self)

@dataclass
class ReturnStmtNode(ASTNode):
    expr: Optional[ASTNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_ReturnStmtNode(self)


# =====================================================================
# CONDITIONS & BOOLEAN EXPRESSIONS
# =====================================================================

@dataclass
class BinaryCondNode(ASTNode):
    left: ASTNode
    op: str  # 'AND', 'OR'
    right: ASTNode

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_BinaryCondNode(self)

@dataclass
class NotCondNode(ASTNode):
    operand: ASTNode

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_NotCondNode(self)

@dataclass
class CompExprNode(ASTNode):
    left: ASTNode
    op: str  # 'GT', 'LT', 'GTE', 'LTE', 'EQ', 'NEQ'
    right: ASTNode

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_CompExprNode(self)

@dataclass
class TemporalCondNode(ASTNode):
    condition: ASTNode
    duration: DurationNode

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_TemporalCondNode(self)

@dataclass
class VotingCondNode(ASTNode):
    threshold: int
    total: int
    comparisons: List[CompExprNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_VotingCondNode(self)

@dataclass
class BooleanLiteralNode(ASTNode):
    value: bool

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_BooleanLiteralNode(self)

@dataclass
class VariableCondNode(ASTNode):
    identifier: str

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_VariableCondNode(self)


# =====================================================================
# ARITHMETIC EXPRESSIONS
# =====================================================================

@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    op: str  # 'MUL', 'DIV', 'MOD', 'PLUS', 'MINUS'
    right: ASTNode

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_BinaryOpNode(self)

@dataclass
class UnaryMinusNode(ASTNode):
    operand: ASTNode

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_UnaryMinusNode(self)

@dataclass
class AggregateExprNode(ASTNode):
    function_name: str  # 'AVG', 'MAX', 'MIN', 'SUM', 'RATE', 'LAST'
    identifier: str
    duration: DurationNode

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_AggregateExprNode(self)

@dataclass
class ProcCallExprNode(ASTNode):
    identifier: str
    arguments: List[ASTNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_ProcCallExprNode(self)

@dataclass
class NumberLiteralNode(ASTNode):
    value: float

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_NumberLiteralNode(self)

@dataclass
class StringLiteralNode(ASTNode):
    value: str

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_StringLiteralNode(self)

@dataclass
class VariableExprNode(ASTNode):
    identifier: str
    index_expr: Optional[ASTNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_VariableExprNode(self)


# =====================================================================
# ESCALATION MANAGEMENT (ISA-18.2)
# =====================================================================

@dataclass
class EscalationFieldNode(ASTNode):
    key: str  # 'MESSAGE', 'RECEIVER', 'TIMEOUT', 'IF_NO_RESP'
    value: Union[str, DurationNode, ASTNode]  # Value can be raw text, duration or action stmt node

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_EscalationFieldNode(self)

@dataclass
class EscalationLevelNode(ASTNode):
    level_name: str  # 'LEVEL_1', 'LEVEL_2', 'LEVEL_3', 'LEVEL_N'
    fields: List[EscalationFieldNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_EscalationLevelNode(self)

@dataclass
class EscalationDefNode(ASTNode):
    identifier: str
    levels: List[EscalationLevelNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_EscalationDefNode(self)


# =====================================================================
# INDUSTRIAL DATA REPORTING SUBSYSTEM
# =====================================================================

@dataclass
class ScheduleSpecNode(ASTNode):
    frequency: str  # 'DAILY', 'WEEKLY'
    day: Optional[str]
    time: str

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_ScheduleSpecNode(self)

@dataclass
class ReportFieldNode(ASTNode):
    key: str  # 'SCHEDULE', 'FORMAT', 'SAVE_IN', 'TYPE'
    value: Union[ScheduleSpecNode, str]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_ReportFieldNode(self)

@dataclass
class ReportItemNode(ASTNode):
    kind: str  # 'AGGREGATE', 'INSTANT', 'ALERT_COUNT', 'UPTIME', 'CURRENT_MODE', 'TIMESTAMP'
    title: str
    identifier: Optional[str]
    duration: Optional[DurationNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_ReportItemNode(self)

@dataclass
class ReportDefNode(ASTNode):
    identifier: str
    fields: List[ReportFieldNode]
    content: List[ReportItemNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_ReportDefNode(self)


# =====================================================================
# FINITE STATE TRANSITIONS (FSM)
# =====================================================================

@dataclass
class TransitionRuleNode(ASTNode):
    from_mode: str
    to_mode: str

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_TransitionRuleNode(self)

@dataclass
class TransitionTableNode(ASTNode):
    rules: List[TransitionRuleNode]

    def accept(self, visitor: ASTVisitor):
        return visitor.visit_TransitionTableNode(self)