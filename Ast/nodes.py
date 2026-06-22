from dataclasses import dataclass, field
from typing import List, Optional, Union
from abc import ABC, abstractmethod

from Ast.ast_visitor import ASTVisitor


@dataclass(kw_only=True)
class ASTNode(ABC):
    line: int = 0
    column: int = 0

    @abstractmethod
    def accept(self, visitor):
        method_name = f'visit_{self.__class__.__name__}'
        visitor_method = getattr(visitor, method_name)
        return visitor_method(self)


# ── Structural & configuration nodes ──────────────────────────────

@dataclass
class ProgramNode(ASTNode):
    declarations: List[ASTNode]
    def accept(self, visitor): return visitor.visit_ProgramNode(self)

@dataclass
class ProgramDeclNode(ASTNode):
    name: str
    def accept(self, visitor): return visitor.visit_ProgramDeclNode(self)

@dataclass
class DurationNode(ASTNode):
    value: float
    unit: str
    def accept(self, visitor): return visitor.visit_DurationNode(self)
    def to_seconds(self) -> float:
        factors = {'مللي_ثانية': 0.001, 'ثانية': 1.0, 'دقيقة': 60.0, 'ساعة': 3600.0, 'يوم': 86400.0}
        return self.value * factors.get(self.unit, 1.0)

@dataclass
class DeviceFieldNode(ASTNode):
    key: str
    value: Union[str, float, DurationNode]
    def accept(self, visitor): return visitor.visit_DeviceFieldNode(self)

@dataclass
class DeviceBlockNode(ASTNode):
    identifier: str
    fields: List[DeviceFieldNode]
    def accept(self, visitor): return visitor.visit_DeviceBlockNode(self)

@dataclass
class DimensionExprNode(ASTNode):
    elements: List[str]
    def accept(self, visitor): return visitor.visit_DimensionExprNode(self)

@dataclass
class CustomUnitDefNode(ASTNode):
    identifier: str
    dimension: DimensionExprNode
    def accept(self, visitor): return visitor.visit_CustomUnitDefNode(self)

@dataclass
class CustomUnitsBlockNode(ASTNode):
    units: List[CustomUnitDefNode]
    def accept(self, visitor): return visitor.visit_CustomUnitsBlockNode(self)

@dataclass
class CustomModesBlockNode(ASTNode):
    modes: List[str]
    def accept(self, visitor): return visitor.visit_CustomModesBlockNode(self)


# ── Type system & hardware declarations ───────────────────────────

@dataclass
class BaseTypeNode(ASTNode):
    type_name: str
    def accept(self, visitor): return visitor.visit_BaseTypeNode(self)
    def __str__(self): return self.type_name

@dataclass
class ArrayTypeNode(ASTNode):
    element_type: ASTNode
    size: int
    def accept(self, visitor): return visitor.visit_ArrayTypeNode(self)

@dataclass
class RangeSpecNode(ASTNode):
    min_val: float
    max_val: float
    def accept(self, visitor): return visitor.visit_RangeSpecNode(self)

@dataclass
class HealthRuleNode(ASTNode):
    kind: str  # 'DISCONNECT' | 'STUCK' | 'OUT_OF_RANGE'
    duration: Optional[DurationNode]
    statements: List[ASTNode]
    def accept(self, visitor): return visitor.visit_HealthRuleNode(self)

@dataclass
class SensorFieldNode(ASTNode):
    key: str
    value: Union[ASTNode, str, List[HealthRuleNode]]
    def accept(self, visitor): return visitor.visit_SensorFieldNode(self)

@dataclass
class SensorDeclNode(ASTNode):
    identifier: str
    fields: List[SensorFieldNode]
    def accept(self, visitor): return visitor.visit_SensorDeclNode(self)

@dataclass
class ActuatorFieldNode(ASTNode):
    key: str
    value: Union[ASTNode, str]
    def accept(self, visitor): return visitor.visit_ActuatorFieldNode(self)

@dataclass
class ActuatorDeclNode(ASTNode):
    identifier: str
    fields: List[ActuatorFieldNode]
    def accept(self, visitor): return visitor.visit_ActuatorDeclNode(self)


# ── Core variables & procedure declarations ───────────────────────

@dataclass
class VarDeclNode(ASTNode):
    identifier: str
    var_type: ASTNode
    expr: ASTNode
    def accept(self, visitor): return visitor.visit_VarDeclNode(self)

@dataclass
class ConstDeclNode(ASTNode):
    identifier: str
    var_type: ASTNode
    expr: ASTNode
    def accept(self, visitor): return visitor.visit_ConstDeclNode(self)

@dataclass
class ParamNode(ASTNode):
    identifier: str
    var_type: ASTNode
    def accept(self, visitor): return visitor.visit_ParamNode(self)

@dataclass
class ProcedureDefNode(ASTNode):
    identifier: str
    params: List[ParamNode]
    return_type: Optional[ASTNode]
    body: List[ASTNode]
    def accept(self, visitor): return visitor.visit_ProcedureDefNode(self)


# ── Operating modes & safety rules (IEC 62443) ────────────────────

@dataclass
class RuleBlockNode(ASTNode):
    identifier: str
    local_declarations: List[ASTNode]
    condition: ASTNode
    actions: List[ASTNode]
    def accept(self, visitor): return visitor.visit_RuleBlockNode(self)

@dataclass
class ModeBlockNode(ASTNode):
    mode_name: str
    on_start_statements: List[ASTNode]
    rules: List[RuleBlockNode]
    def accept(self, visitor): return visitor.visit_ModeBlockNode(self)


# ── Statements ──────────────────────────────────────────────────

@dataclass
class CommandStmtNode(ASTNode):
    identifier: str
    value: Union[str, ASTNode]
    def accept(self, visitor): return visitor.visit_CommandStmtNode(self)

@dataclass
class AlertStmtNode(ASTNode):
    level: str
    message: str
    def accept(self, visitor): return visitor.visit_AlertStmtNode(self)

@dataclass
class LogStmtNode(ASTNode):
    message: str
    def accept(self, visitor): return visitor.visit_LogStmtNode(self)

@dataclass
class ExecProcStmtNode(ASTNode):
    identifier: str
    arguments: List[ASTNode]
    def accept(self, visitor): return visitor.visit_ExecProcStmtNode(self)

@dataclass
class GotoStmtNode(ASTNode):
    target_mode: str
    def accept(self, visitor): return visitor.visit_GotoStmtNode(self)

@dataclass
class WaitStmtNode(ASTNode):
    duration: DurationNode
    def accept(self, visitor): return visitor.visit_WaitStmtNode(self)

@dataclass
class AssignStmtNode(ASTNode):
    identifier: str
    index_expr: Optional[ASTNode]
    expr: ASTNode
    def accept(self, visitor): return visitor.visit_AssignStmtNode(self)

@dataclass
class DefaultValStmtNode(ASTNode):
    value: float
    def accept(self, visitor): return visitor.visit_DefaultValStmtNode(self)

@dataclass
class ExprStmtNode(ASTNode):
    expr: ASTNode
    def accept(self, visitor): return visitor.visit_ExprStmtNode(self)

@dataclass
class IfStmtNode(ASTNode):
    condition: ASTNode
    then_branch: List[ASTNode]
    else_branch: List[ASTNode]
    def accept(self, visitor): return visitor.visit_IfStmtNode(self)

@dataclass
class WhileStmtNode(ASTNode):
    condition: ASTNode
    body: List[ASTNode]
    def accept(self, visitor): return visitor.visit_WhileStmtNode(self)

@dataclass
class ReturnStmtNode(ASTNode):
    expr: Optional[ASTNode]
    def accept(self, visitor): return visitor.visit_ReturnStmtNode(self)


# ── Conditions & boolean expressions ──────────────────────────────

@dataclass
class BinaryCondNode(ASTNode):
    left: ASTNode
    op: str  # 'AND' | 'OR'
    right: ASTNode
    def accept(self, visitor): return visitor.visit_BinaryCondNode(self)

@dataclass
class NotCondNode(ASTNode):
    operand: ASTNode
    def accept(self, visitor): return visitor.visit_NotCondNode(self)

@dataclass
class CompExprNode(ASTNode):
    left: ASTNode
    op: str
    right: ASTNode
    def accept(self, visitor): return visitor.visit_CompExprNode(self)

@dataclass
class TemporalCondNode(ASTNode):
    condition: ASTNode
    duration: DurationNode
    def accept(self, visitor): return visitor.visit_TemporalCondNode(self)

@dataclass
class VotingCondNode(ASTNode):
    threshold: int
    total: int
    comparisons: List[CompExprNode]
    def accept(self, visitor): return visitor.visit_VotingCondNode(self)

@dataclass
class BooleanLiteralNode(ASTNode):
    value: bool
    def accept(self, visitor): return visitor.visit_BooleanLiteralNode(self)

@dataclass
class VariableCondNode(ASTNode):
    identifier: str
    def accept(self, visitor): return visitor.visit_VariableCondNode(self)


# ── Arithmetic expressions ─────────────────────────────────────────

@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    op: str
    right: ASTNode
    def accept(self, visitor): return visitor.visit_BinaryOpNode(self)

@dataclass
class UnaryMinusNode(ASTNode):
    operand: ASTNode
    def accept(self, visitor): return visitor.visit_UnaryMinusNode(self)

@dataclass
class AggregateExprNode(ASTNode):
    function_name: str
    identifier: str
    duration: DurationNode
    def accept(self, visitor): return visitor.visit_AggregateExprNode(self)

@dataclass
class ProcCallExprNode(ASTNode):
    identifier: str
    arguments: List[ASTNode]
    def accept(self, visitor): return visitor.visit_ProcCallExprNode(self)

@dataclass
class NumberLiteralNode(ASTNode):
    value: float
    def accept(self, visitor): return visitor.visit_NumberLiteralNode(self)

@dataclass
class StringLiteralNode(ASTNode):
    value: str
    def accept(self, visitor): return visitor.visit_StringLiteralNode(self)

@dataclass
class VariableExprNode(ASTNode):
    identifier: str
    index_expr: Optional[ASTNode]
    def accept(self, visitor): return visitor.visit_VariableExprNode(self)


# ── Escalation management (ISA-18.2) ──────────────────────────────

@dataclass
class EscalationFieldNode(ASTNode):
    key: str
    value: Union[str, DurationNode, ASTNode]
    def accept(self, visitor): return visitor.visit_EscalationFieldNode(self)

@dataclass
class EscalationLevelNode(ASTNode):
    level_name: str
    fields: List[EscalationFieldNode]
    def accept(self, visitor): return visitor.visit_EscalationLevelNode(self)

@dataclass
class EscalationDefNode(ASTNode):
    identifier: str
    levels: List[EscalationLevelNode]
    def accept(self, visitor): return visitor.visit_EscalationDefNode(self)


# ── Industrial data reporting subsystem ────────────────────────────

@dataclass
class ScheduleSpecNode(ASTNode):
    frequency: str
    day: Optional[str]
    time: str
    def accept(self, visitor): return visitor.visit_ScheduleSpecNode(self)

@dataclass
class ReportFieldNode(ASTNode):
    key: str
    value: Union[ScheduleSpecNode, str]
    def accept(self, visitor): return visitor.visit_ReportFieldNode(self)

@dataclass
class ReportItemNode(ASTNode):
    kind: str
    title: str
    identifier: Optional[str]
    duration: Optional[DurationNode]
    function_name: Optional[str] = None
    def accept(self, visitor): return visitor.visit_ReportItemNode(self)

@dataclass
class ReportDefNode(ASTNode):
    identifier: str
    fields: List[ReportFieldNode]
    content: List[ReportItemNode]
    def accept(self, visitor): return visitor.visit_ReportDefNode(self)


# ── Finite state transitions (FSM) ─────────────────────────────────

@dataclass
class TransitionRuleNode(ASTNode):
    from_mode: str
    to_mode: str
    def accept(self, visitor): return visitor.visit_TransitionRuleNode(self)

@dataclass
class TransitionTableNode(ASTNode):
    rules: List[TransitionRuleNode]
    def accept(self, visitor): return visitor.visit_TransitionTableNode(self)