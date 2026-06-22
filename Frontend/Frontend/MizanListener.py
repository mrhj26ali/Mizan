# Generated from Frontend/Mizan.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MizanParser import MizanParser
else:
    from MizanParser import MizanParser

# This class defines a complete listener for a parse tree produced by MizanParser.
class MizanListener(ParseTreeListener):

    # Enter a parse tree produced by MizanParser#program.
    def enterProgram(self, ctx:MizanParser.ProgramContext):
        pass

    # Exit a parse tree produced by MizanParser#program.
    def exitProgram(self, ctx:MizanParser.ProgramContext):
        pass


    # Enter a parse tree produced by MizanParser#topLevelDecl.
    def enterTopLevelDecl(self, ctx:MizanParser.TopLevelDeclContext):
        pass

    # Exit a parse tree produced by MizanParser#topLevelDecl.
    def exitTopLevelDecl(self, ctx:MizanParser.TopLevelDeclContext):
        pass


    # Enter a parse tree produced by MizanParser#programDecl.
    def enterProgramDecl(self, ctx:MizanParser.ProgramDeclContext):
        pass

    # Exit a parse tree produced by MizanParser#programDecl.
    def exitProgramDecl(self, ctx:MizanParser.ProgramDeclContext):
        pass


    # Enter a parse tree produced by MizanParser#deviceBlock.
    def enterDeviceBlock(self, ctx:MizanParser.DeviceBlockContext):
        pass

    # Exit a parse tree produced by MizanParser#deviceBlock.
    def exitDeviceBlock(self, ctx:MizanParser.DeviceBlockContext):
        pass


    # Enter a parse tree produced by MizanParser#deviceField.
    def enterDeviceField(self, ctx:MizanParser.DeviceFieldContext):
        pass

    # Exit a parse tree produced by MizanParser#deviceField.
    def exitDeviceField(self, ctx:MizanParser.DeviceFieldContext):
        pass


    # Enter a parse tree produced by MizanParser#customUnitsBlock.
    def enterCustomUnitsBlock(self, ctx:MizanParser.CustomUnitsBlockContext):
        pass

    # Exit a parse tree produced by MizanParser#customUnitsBlock.
    def exitCustomUnitsBlock(self, ctx:MizanParser.CustomUnitsBlockContext):
        pass


    # Enter a parse tree produced by MizanParser#customUnitDef.
    def enterCustomUnitDef(self, ctx:MizanParser.CustomUnitDefContext):
        pass

    # Exit a parse tree produced by MizanParser#customUnitDef.
    def exitCustomUnitDef(self, ctx:MizanParser.CustomUnitDefContext):
        pass


    # Enter a parse tree produced by MizanParser#dimensionExpr.
    def enterDimensionExpr(self, ctx:MizanParser.DimensionExprContext):
        pass

    # Exit a parse tree produced by MizanParser#dimensionExpr.
    def exitDimensionExpr(self, ctx:MizanParser.DimensionExprContext):
        pass


    # Enter a parse tree produced by MizanParser#baseDim.
    def enterBaseDim(self, ctx:MizanParser.BaseDimContext):
        pass

    # Exit a parse tree produced by MizanParser#baseDim.
    def exitBaseDim(self, ctx:MizanParser.BaseDimContext):
        pass


    # Enter a parse tree produced by MizanParser#customModesBlock.
    def enterCustomModesBlock(self, ctx:MizanParser.CustomModesBlockContext):
        pass

    # Exit a parse tree produced by MizanParser#customModesBlock.
    def exitCustomModesBlock(self, ctx:MizanParser.CustomModesBlockContext):
        pass


    # Enter a parse tree produced by MizanParser#sensorDecl.
    def enterSensorDecl(self, ctx:MizanParser.SensorDeclContext):
        pass

    # Exit a parse tree produced by MizanParser#sensorDecl.
    def exitSensorDecl(self, ctx:MizanParser.SensorDeclContext):
        pass


    # Enter a parse tree produced by MizanParser#sensorField.
    def enterSensorField(self, ctx:MizanParser.SensorFieldContext):
        pass

    # Exit a parse tree produced by MizanParser#sensorField.
    def exitSensorField(self, ctx:MizanParser.SensorFieldContext):
        pass


    # Enter a parse tree produced by MizanParser#actuatorDecl.
    def enterActuatorDecl(self, ctx:MizanParser.ActuatorDeclContext):
        pass

    # Exit a parse tree produced by MizanParser#actuatorDecl.
    def exitActuatorDecl(self, ctx:MizanParser.ActuatorDeclContext):
        pass


    # Enter a parse tree produced by MizanParser#actuatorField.
    def enterActuatorField(self, ctx:MizanParser.ActuatorFieldContext):
        pass

    # Exit a parse tree produced by MizanParser#actuatorField.
    def exitActuatorField(self, ctx:MizanParser.ActuatorFieldContext):
        pass


    # Enter a parse tree produced by MizanParser#varDecl.
    def enterVarDecl(self, ctx:MizanParser.VarDeclContext):
        pass

    # Exit a parse tree produced by MizanParser#varDecl.
    def exitVarDecl(self, ctx:MizanParser.VarDeclContext):
        pass


    # Enter a parse tree produced by MizanParser#constDecl.
    def enterConstDecl(self, ctx:MizanParser.ConstDeclContext):
        pass

    # Exit a parse tree produced by MizanParser#constDecl.
    def exitConstDecl(self, ctx:MizanParser.ConstDeclContext):
        pass


    # Enter a parse tree produced by MizanParser#varType.
    def enterVarType(self, ctx:MizanParser.VarTypeContext):
        pass

    # Exit a parse tree produced by MizanParser#varType.
    def exitVarType(self, ctx:MizanParser.VarTypeContext):
        pass


    # Enter a parse tree produced by MizanParser#rangeSpec.
    def enterRangeSpec(self, ctx:MizanParser.RangeSpecContext):
        pass

    # Exit a parse tree produced by MizanParser#rangeSpec.
    def exitRangeSpec(self, ctx:MizanParser.RangeSpecContext):
        pass


    # Enter a parse tree produced by MizanParser#procedureDef.
    def enterProcedureDef(self, ctx:MizanParser.ProcedureDefContext):
        pass

    # Exit a parse tree produced by MizanParser#procedureDef.
    def exitProcedureDef(self, ctx:MizanParser.ProcedureDefContext):
        pass


    # Enter a parse tree produced by MizanParser#paramList.
    def enterParamList(self, ctx:MizanParser.ParamListContext):
        pass

    # Exit a parse tree produced by MizanParser#paramList.
    def exitParamList(self, ctx:MizanParser.ParamListContext):
        pass


    # Enter a parse tree produced by MizanParser#param.
    def enterParam(self, ctx:MizanParser.ParamContext):
        pass

    # Exit a parse tree produced by MizanParser#param.
    def exitParam(self, ctx:MizanParser.ParamContext):
        pass


    # Enter a parse tree produced by MizanParser#modeBlock.
    def enterModeBlock(self, ctx:MizanParser.ModeBlockContext):
        pass

    # Exit a parse tree produced by MizanParser#modeBlock.
    def exitModeBlock(self, ctx:MizanParser.ModeBlockContext):
        pass


    # Enter a parse tree produced by MizanParser#modeName.
    def enterModeName(self, ctx:MizanParser.ModeNameContext):
        pass

    # Exit a parse tree produced by MizanParser#modeName.
    def exitModeName(self, ctx:MizanParser.ModeNameContext):
        pass


    # Enter a parse tree produced by MizanParser#onStartBlock.
    def enterOnStartBlock(self, ctx:MizanParser.OnStartBlockContext):
        pass

    # Exit a parse tree produced by MizanParser#onStartBlock.
    def exitOnStartBlock(self, ctx:MizanParser.OnStartBlockContext):
        pass


    # Enter a parse tree produced by MizanParser#ruleBlock.
    def enterRuleBlock(self, ctx:MizanParser.RuleBlockContext):
        pass

    # Exit a parse tree produced by MizanParser#ruleBlock.
    def exitRuleBlock(self, ctx:MizanParser.RuleBlockContext):
        pass


    # Enter a parse tree produced by MizanParser#localDecl.
    def enterLocalDecl(self, ctx:MizanParser.LocalDeclContext):
        pass

    # Exit a parse tree produced by MizanParser#localDecl.
    def exitLocalDecl(self, ctx:MizanParser.LocalDeclContext):
        pass


    # Enter a parse tree produced by MizanParser#conditionClause.
    def enterConditionClause(self, ctx:MizanParser.ConditionClauseContext):
        pass

    # Exit a parse tree produced by MizanParser#conditionClause.
    def exitConditionClause(self, ctx:MizanParser.ConditionClauseContext):
        pass


    # Enter a parse tree produced by MizanParser#actionClause.
    def enterActionClause(self, ctx:MizanParser.ActionClauseContext):
        pass

    # Exit a parse tree produced by MizanParser#actionClause.
    def exitActionClause(self, ctx:MizanParser.ActionClauseContext):
        pass


    # Enter a parse tree produced by MizanParser#statement.
    def enterStatement(self, ctx:MizanParser.StatementContext):
        pass

    # Exit a parse tree produced by MizanParser#statement.
    def exitStatement(self, ctx:MizanParser.StatementContext):
        pass


    # Enter a parse tree produced by MizanParser#commandStmt.
    def enterCommandStmt(self, ctx:MizanParser.CommandStmtContext):
        pass

    # Exit a parse tree produced by MizanParser#commandStmt.
    def exitCommandStmt(self, ctx:MizanParser.CommandStmtContext):
        pass


    # Enter a parse tree produced by MizanParser#actuatorValue.
    def enterActuatorValue(self, ctx:MizanParser.ActuatorValueContext):
        pass

    # Exit a parse tree produced by MizanParser#actuatorValue.
    def exitActuatorValue(self, ctx:MizanParser.ActuatorValueContext):
        pass


    # Enter a parse tree produced by MizanParser#alertStmt.
    def enterAlertStmt(self, ctx:MizanParser.AlertStmtContext):
        pass

    # Exit a parse tree produced by MizanParser#alertStmt.
    def exitAlertStmt(self, ctx:MizanParser.AlertStmtContext):
        pass


    # Enter a parse tree produced by MizanParser#alertLevel.
    def enterAlertLevel(self, ctx:MizanParser.AlertLevelContext):
        pass

    # Exit a parse tree produced by MizanParser#alertLevel.
    def exitAlertLevel(self, ctx:MizanParser.AlertLevelContext):
        pass


    # Enter a parse tree produced by MizanParser#logStmt.
    def enterLogStmt(self, ctx:MizanParser.LogStmtContext):
        pass

    # Exit a parse tree produced by MizanParser#logStmt.
    def exitLogStmt(self, ctx:MizanParser.LogStmtContext):
        pass


    # Enter a parse tree produced by MizanParser#execProcStmt.
    def enterExecProcStmt(self, ctx:MizanParser.ExecProcStmtContext):
        pass

    # Exit a parse tree produced by MizanParser#execProcStmt.
    def exitExecProcStmt(self, ctx:MizanParser.ExecProcStmtContext):
        pass


    # Enter a parse tree produced by MizanParser#gotoStmt.
    def enterGotoStmt(self, ctx:MizanParser.GotoStmtContext):
        pass

    # Exit a parse tree produced by MizanParser#gotoStmt.
    def exitGotoStmt(self, ctx:MizanParser.GotoStmtContext):
        pass


    # Enter a parse tree produced by MizanParser#waitStmt.
    def enterWaitStmt(self, ctx:MizanParser.WaitStmtContext):
        pass

    # Exit a parse tree produced by MizanParser#waitStmt.
    def exitWaitStmt(self, ctx:MizanParser.WaitStmtContext):
        pass


    # Enter a parse tree produced by MizanParser#assignStmt.
    def enterAssignStmt(self, ctx:MizanParser.AssignStmtContext):
        pass

    # Exit a parse tree produced by MizanParser#assignStmt.
    def exitAssignStmt(self, ctx:MizanParser.AssignStmtContext):
        pass


    # Enter a parse tree produced by MizanParser#defaultValStmt.
    def enterDefaultValStmt(self, ctx:MizanParser.DefaultValStmtContext):
        pass

    # Exit a parse tree produced by MizanParser#defaultValStmt.
    def exitDefaultValStmt(self, ctx:MizanParser.DefaultValStmtContext):
        pass


    # Enter a parse tree produced by MizanParser#exprStmt.
    def enterExprStmt(self, ctx:MizanParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by MizanParser#exprStmt.
    def exitExprStmt(self, ctx:MizanParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by MizanParser#ifStmt.
    def enterIfStmt(self, ctx:MizanParser.IfStmtContext):
        pass

    # Exit a parse tree produced by MizanParser#ifStmt.
    def exitIfStmt(self, ctx:MizanParser.IfStmtContext):
        pass


    # Enter a parse tree produced by MizanParser#whileStmt.
    def enterWhileStmt(self, ctx:MizanParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by MizanParser#whileStmt.
    def exitWhileStmt(self, ctx:MizanParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by MizanParser#returnStmt.
    def enterReturnStmt(self, ctx:MizanParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by MizanParser#returnStmt.
    def exitReturnStmt(self, ctx:MizanParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by MizanParser#OrExpr.
    def enterOrExpr(self, ctx:MizanParser.OrExprContext):
        pass

    # Exit a parse tree produced by MizanParser#OrExpr.
    def exitOrExpr(self, ctx:MizanParser.OrExprContext):
        pass


    # Enter a parse tree produced by MizanParser#OrPass.
    def enterOrPass(self, ctx:MizanParser.OrPassContext):
        pass

    # Exit a parse tree produced by MizanParser#OrPass.
    def exitOrPass(self, ctx:MizanParser.OrPassContext):
        pass


    # Enter a parse tree produced by MizanParser#AndExpr.
    def enterAndExpr(self, ctx:MizanParser.AndExprContext):
        pass

    # Exit a parse tree produced by MizanParser#AndExpr.
    def exitAndExpr(self, ctx:MizanParser.AndExprContext):
        pass


    # Enter a parse tree produced by MizanParser#AndPass.
    def enterAndPass(self, ctx:MizanParser.AndPassContext):
        pass

    # Exit a parse tree produced by MizanParser#AndPass.
    def exitAndPass(self, ctx:MizanParser.AndPassContext):
        pass


    # Enter a parse tree produced by MizanParser#NotExpr.
    def enterNotExpr(self, ctx:MizanParser.NotExprContext):
        pass

    # Exit a parse tree produced by MizanParser#NotExpr.
    def exitNotExpr(self, ctx:MizanParser.NotExprContext):
        pass


    # Enter a parse tree produced by MizanParser#PrimaryPass.
    def enterPrimaryPass(self, ctx:MizanParser.PrimaryPassContext):
        pass

    # Exit a parse tree produced by MizanParser#PrimaryPass.
    def exitPrimaryPass(self, ctx:MizanParser.PrimaryPassContext):
        pass


    # Enter a parse tree produced by MizanParser#ParenCond.
    def enterParenCond(self, ctx:MizanParser.ParenCondContext):
        pass

    # Exit a parse tree produced by MizanParser#ParenCond.
    def exitParenCond(self, ctx:MizanParser.ParenCondContext):
        pass


    # Enter a parse tree produced by MizanParser#CompExpr.
    def enterCompExpr(self, ctx:MizanParser.CompExprContext):
        pass

    # Exit a parse tree produced by MizanParser#CompExpr.
    def exitCompExpr(self, ctx:MizanParser.CompExprContext):
        pass


    # Enter a parse tree produced by MizanParser#TemporalExpr.
    def enterTemporalExpr(self, ctx:MizanParser.TemporalExprContext):
        pass

    # Exit a parse tree produced by MizanParser#TemporalExpr.
    def exitTemporalExpr(self, ctx:MizanParser.TemporalExprContext):
        pass


    # Enter a parse tree produced by MizanParser#VotingExpr.
    def enterVotingExpr(self, ctx:MizanParser.VotingExprContext):
        pass

    # Exit a parse tree produced by MizanParser#VotingExpr.
    def exitVotingExpr(self, ctx:MizanParser.VotingExprContext):
        pass


    # Enter a parse tree produced by MizanParser#TrueLit.
    def enterTrueLit(self, ctx:MizanParser.TrueLitContext):
        pass

    # Exit a parse tree produced by MizanParser#TrueLit.
    def exitTrueLit(self, ctx:MizanParser.TrueLitContext):
        pass


    # Enter a parse tree produced by MizanParser#FalseLit.
    def enterFalseLit(self, ctx:MizanParser.FalseLitContext):
        pass

    # Exit a parse tree produced by MizanParser#FalseLit.
    def exitFalseLit(self, ctx:MizanParser.FalseLitContext):
        pass


    # Enter a parse tree produced by MizanParser#BoolVar.
    def enterBoolVar(self, ctx:MizanParser.BoolVarContext):
        pass

    # Exit a parse tree produced by MizanParser#BoolVar.
    def exitBoolVar(self, ctx:MizanParser.BoolVarContext):
        pass


    # Enter a parse tree produced by MizanParser#comparisonList.
    def enterComparisonList(self, ctx:MizanParser.ComparisonListContext):
        pass

    # Exit a parse tree produced by MizanParser#comparisonList.
    def exitComparisonList(self, ctx:MizanParser.ComparisonListContext):
        pass


    # Enter a parse tree produced by MizanParser#comparison.
    def enterComparison(self, ctx:MizanParser.ComparisonContext):
        pass

    # Exit a parse tree produced by MizanParser#comparison.
    def exitComparison(self, ctx:MizanParser.ComparisonContext):
        pass


    # Enter a parse tree produced by MizanParser#compOp.
    def enterCompOp(self, ctx:MizanParser.CompOpContext):
        pass

    # Exit a parse tree produced by MizanParser#compOp.
    def exitCompOp(self, ctx:MizanParser.CompOpContext):
        pass


    # Enter a parse tree produced by MizanParser#AggExpr.
    def enterAggExpr(self, ctx:MizanParser.AggExprContext):
        pass

    # Exit a parse tree produced by MizanParser#AggExpr.
    def exitAggExpr(self, ctx:MizanParser.AggExprContext):
        pass


    # Enter a parse tree produced by MizanParser#VarOrArrayExpr.
    def enterVarOrArrayExpr(self, ctx:MizanParser.VarOrArrayExprContext):
        pass

    # Exit a parse tree produced by MizanParser#VarOrArrayExpr.
    def exitVarOrArrayExpr(self, ctx:MizanParser.VarOrArrayExprContext):
        pass


    # Enter a parse tree produced by MizanParser#MulDivExpr.
    def enterMulDivExpr(self, ctx:MizanParser.MulDivExprContext):
        pass

    # Exit a parse tree produced by MizanParser#MulDivExpr.
    def exitMulDivExpr(self, ctx:MizanParser.MulDivExprContext):
        pass


    # Enter a parse tree produced by MizanParser#ProcCallExpr.
    def enterProcCallExpr(self, ctx:MizanParser.ProcCallExprContext):
        pass

    # Exit a parse tree produced by MizanParser#ProcCallExpr.
    def exitProcCallExpr(self, ctx:MizanParser.ProcCallExprContext):
        pass


    # Enter a parse tree produced by MizanParser#ParenExpr.
    def enterParenExpr(self, ctx:MizanParser.ParenExprContext):
        pass

    # Exit a parse tree produced by MizanParser#ParenExpr.
    def exitParenExpr(self, ctx:MizanParser.ParenExprContext):
        pass


    # Enter a parse tree produced by MizanParser#NumLit.
    def enterNumLit(self, ctx:MizanParser.NumLitContext):
        pass

    # Exit a parse tree produced by MizanParser#NumLit.
    def exitNumLit(self, ctx:MizanParser.NumLitContext):
        pass


    # Enter a parse tree produced by MizanParser#AddSubExpr.
    def enterAddSubExpr(self, ctx:MizanParser.AddSubExprContext):
        pass

    # Exit a parse tree produced by MizanParser#AddSubExpr.
    def exitAddSubExpr(self, ctx:MizanParser.AddSubExprContext):
        pass


    # Enter a parse tree produced by MizanParser#UnaryMinusExpr.
    def enterUnaryMinusExpr(self, ctx:MizanParser.UnaryMinusExprContext):
        pass

    # Exit a parse tree produced by MizanParser#UnaryMinusExpr.
    def exitUnaryMinusExpr(self, ctx:MizanParser.UnaryMinusExprContext):
        pass


    # Enter a parse tree produced by MizanParser#StrLit.
    def enterStrLit(self, ctx:MizanParser.StrLitContext):
        pass

    # Exit a parse tree produced by MizanParser#StrLit.
    def exitStrLit(self, ctx:MizanParser.StrLitContext):
        pass


    # Enter a parse tree produced by MizanParser#aggregateExpr.
    def enterAggregateExpr(self, ctx:MizanParser.AggregateExprContext):
        pass

    # Exit a parse tree produced by MizanParser#aggregateExpr.
    def exitAggregateExpr(self, ctx:MizanParser.AggregateExprContext):
        pass


    # Enter a parse tree produced by MizanParser#aggFunc.
    def enterAggFunc(self, ctx:MizanParser.AggFuncContext):
        pass

    # Exit a parse tree produced by MizanParser#aggFunc.
    def exitAggFunc(self, ctx:MizanParser.AggFuncContext):
        pass


    # Enter a parse tree produced by MizanParser#argList.
    def enterArgList(self, ctx:MizanParser.ArgListContext):
        pass

    # Exit a parse tree produced by MizanParser#argList.
    def exitArgList(self, ctx:MizanParser.ArgListContext):
        pass


    # Enter a parse tree produced by MizanParser#healthRule.
    def enterHealthRule(self, ctx:MizanParser.HealthRuleContext):
        pass

    # Exit a parse tree produced by MizanParser#healthRule.
    def exitHealthRule(self, ctx:MizanParser.HealthRuleContext):
        pass


    # Enter a parse tree produced by MizanParser#escalationDef.
    def enterEscalationDef(self, ctx:MizanParser.EscalationDefContext):
        pass

    # Exit a parse tree produced by MizanParser#escalationDef.
    def exitEscalationDef(self, ctx:MizanParser.EscalationDefContext):
        pass


    # Enter a parse tree produced by MizanParser#escalationLevel.
    def enterEscalationLevel(self, ctx:MizanParser.EscalationLevelContext):
        pass

    # Exit a parse tree produced by MizanParser#escalationLevel.
    def exitEscalationLevel(self, ctx:MizanParser.EscalationLevelContext):
        pass


    # Enter a parse tree produced by MizanParser#escalationField.
    def enterEscalationField(self, ctx:MizanParser.EscalationFieldContext):
        pass

    # Exit a parse tree produced by MizanParser#escalationField.
    def exitEscalationField(self, ctx:MizanParser.EscalationFieldContext):
        pass


    # Enter a parse tree produced by MizanParser#escalationAction.
    def enterEscalationAction(self, ctx:MizanParser.EscalationActionContext):
        pass

    # Exit a parse tree produced by MizanParser#escalationAction.
    def exitEscalationAction(self, ctx:MizanParser.EscalationActionContext):
        pass


    # Enter a parse tree produced by MizanParser#reportDef.
    def enterReportDef(self, ctx:MizanParser.ReportDefContext):
        pass

    # Exit a parse tree produced by MizanParser#reportDef.
    def exitReportDef(self, ctx:MizanParser.ReportDefContext):
        pass


    # Enter a parse tree produced by MizanParser#reportField.
    def enterReportField(self, ctx:MizanParser.ReportFieldContext):
        pass

    # Exit a parse tree produced by MizanParser#reportField.
    def exitReportField(self, ctx:MizanParser.ReportFieldContext):
        pass


    # Enter a parse tree produced by MizanParser#scheduleSpec.
    def enterScheduleSpec(self, ctx:MizanParser.ScheduleSpecContext):
        pass

    # Exit a parse tree produced by MizanParser#scheduleSpec.
    def exitScheduleSpec(self, ctx:MizanParser.ScheduleSpecContext):
        pass


    # Enter a parse tree produced by MizanParser#formatName.
    def enterFormatName(self, ctx:MizanParser.FormatNameContext):
        pass

    # Exit a parse tree produced by MizanParser#formatName.
    def exitFormatName(self, ctx:MizanParser.FormatNameContext):
        pass


    # Enter a parse tree produced by MizanParser#reportContent.
    def enterReportContent(self, ctx:MizanParser.ReportContentContext):
        pass

    # Exit a parse tree produced by MizanParser#reportContent.
    def exitReportContent(self, ctx:MizanParser.ReportContentContext):
        pass


    # Enter a parse tree produced by MizanParser#reportItem.
    def enterReportItem(self, ctx:MizanParser.ReportItemContext):
        pass

    # Exit a parse tree produced by MizanParser#reportItem.
    def exitReportItem(self, ctx:MizanParser.ReportItemContext):
        pass


    # Enter a parse tree produced by MizanParser#transitionTable.
    def enterTransitionTable(self, ctx:MizanParser.TransitionTableContext):
        pass

    # Exit a parse tree produced by MizanParser#transitionTable.
    def exitTransitionTable(self, ctx:MizanParser.TransitionTableContext):
        pass


    # Enter a parse tree produced by MizanParser#transitionRule.
    def enterTransitionRule(self, ctx:MizanParser.TransitionRuleContext):
        pass

    # Exit a parse tree produced by MizanParser#transitionRule.
    def exitTransitionRule(self, ctx:MizanParser.TransitionRuleContext):
        pass


    # Enter a parse tree produced by MizanParser#duration.
    def enterDuration(self, ctx:MizanParser.DurationContext):
        pass

    # Exit a parse tree produced by MizanParser#duration.
    def exitDuration(self, ctx:MizanParser.DurationContext):
        pass


    # Enter a parse tree produced by MizanParser#timeSuffix.
    def enterTimeSuffix(self, ctx:MizanParser.TimeSuffixContext):
        pass

    # Exit a parse tree produced by MizanParser#timeSuffix.
    def exitTimeSuffix(self, ctx:MizanParser.TimeSuffixContext):
        pass


    # Enter a parse tree produced by MizanParser#unitType.
    def enterUnitType(self, ctx:MizanParser.UnitTypeContext):
        pass

    # Exit a parse tree produced by MizanParser#unitType.
    def exitUnitType(self, ctx:MizanParser.UnitTypeContext):
        pass


    # Enter a parse tree produced by MizanParser#fieldSep.
    def enterFieldSep(self, ctx:MizanParser.FieldSepContext):
        pass

    # Exit a parse tree produced by MizanParser#fieldSep.
    def exitFieldSep(self, ctx:MizanParser.FieldSepContext):
        pass



del MizanParser