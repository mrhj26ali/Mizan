# Generated from Mizan.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MizanParser import MizanParser
else:
    from MizanParser import MizanParser

# This class defines a complete generic visitor for a parse tree produced by MizanParser.

class MizanVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MizanParser#program.
    def visitProgram(self, ctx:MizanParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#topLevelDecl.
    def visitTopLevelDecl(self, ctx:MizanParser.TopLevelDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#programDecl.
    def visitProgramDecl(self, ctx:MizanParser.ProgramDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#deviceBlock.
    def visitDeviceBlock(self, ctx:MizanParser.DeviceBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#deviceField.
    def visitDeviceField(self, ctx:MizanParser.DeviceFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#customUnitsBlock.
    def visitCustomUnitsBlock(self, ctx:MizanParser.CustomUnitsBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#customUnitDef.
    def visitCustomUnitDef(self, ctx:MizanParser.CustomUnitDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#UnitPass.
    def visitUnitPass(self, ctx:MizanParser.UnitPassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#UnitMathExpr.
    def visitUnitMathExpr(self, ctx:MizanParser.UnitMathExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#UnitBase.
    def visitUnitBase(self, ctx:MizanParser.UnitBaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#UnitParen.
    def visitUnitParen(self, ctx:MizanParser.UnitParenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#customModesBlock.
    def visitCustomModesBlock(self, ctx:MizanParser.CustomModesBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#sensorDecl.
    def visitSensorDecl(self, ctx:MizanParser.SensorDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#sensorField.
    def visitSensorField(self, ctx:MizanParser.SensorFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#actuatorDecl.
    def visitActuatorDecl(self, ctx:MizanParser.ActuatorDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#actuatorField.
    def visitActuatorField(self, ctx:MizanParser.ActuatorFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#varDecl.
    def visitVarDecl(self, ctx:MizanParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#constDecl.
    def visitConstDecl(self, ctx:MizanParser.ConstDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#varType.
    def visitVarType(self, ctx:MizanParser.VarTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#rangeSpec.
    def visitRangeSpec(self, ctx:MizanParser.RangeSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#procedureDef.
    def visitProcedureDef(self, ctx:MizanParser.ProcedureDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#paramList.
    def visitParamList(self, ctx:MizanParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#param.
    def visitParam(self, ctx:MizanParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#modeBlock.
    def visitModeBlock(self, ctx:MizanParser.ModeBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#modeName.
    def visitModeName(self, ctx:MizanParser.ModeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#onStartBlock.
    def visitOnStartBlock(self, ctx:MizanParser.OnStartBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#ruleBlock.
    def visitRuleBlock(self, ctx:MizanParser.RuleBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#localDecl.
    def visitLocalDecl(self, ctx:MizanParser.LocalDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#statement.
    def visitStatement(self, ctx:MizanParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#commandStmt.
    def visitCommandStmt(self, ctx:MizanParser.CommandStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#actuatorValue.
    def visitActuatorValue(self, ctx:MizanParser.ActuatorValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#alertStmt.
    def visitAlertStmt(self, ctx:MizanParser.AlertStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#alertLevel.
    def visitAlertLevel(self, ctx:MizanParser.AlertLevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#logStmt.
    def visitLogStmt(self, ctx:MizanParser.LogStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#gotoStmt.
    def visitGotoStmt(self, ctx:MizanParser.GotoStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#waitStmt.
    def visitWaitStmt(self, ctx:MizanParser.WaitStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#assignStmt.
    def visitAssignStmt(self, ctx:MizanParser.AssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#defaultValStmt.
    def visitDefaultValStmt(self, ctx:MizanParser.DefaultValStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#exprStmt.
    def visitExprStmt(self, ctx:MizanParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#ifStmt.
    def visitIfStmt(self, ctx:MizanParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#whileStmt.
    def visitWhileStmt(self, ctx:MizanParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#returnStmt.
    def visitReturnStmt(self, ctx:MizanParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#OrExpr.
    def visitOrExpr(self, ctx:MizanParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#OrPass.
    def visitOrPass(self, ctx:MizanParser.OrPassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#AndExpr.
    def visitAndExpr(self, ctx:MizanParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#AndPass.
    def visitAndPass(self, ctx:MizanParser.AndPassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#NotExpr.
    def visitNotExpr(self, ctx:MizanParser.NotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#PrimaryPass.
    def visitPrimaryPass(self, ctx:MizanParser.PrimaryPassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#ParenCond.
    def visitParenCond(self, ctx:MizanParser.ParenCondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#CompExpr.
    def visitCompExpr(self, ctx:MizanParser.CompExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#TemporalExpr.
    def visitTemporalExpr(self, ctx:MizanParser.TemporalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#VotingExpr.
    def visitVotingExpr(self, ctx:MizanParser.VotingExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#TrueLit.
    def visitTrueLit(self, ctx:MizanParser.TrueLitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#FalseLit.
    def visitFalseLit(self, ctx:MizanParser.FalseLitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#BoolVar.
    def visitBoolVar(self, ctx:MizanParser.BoolVarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#comparisonList.
    def visitComparisonList(self, ctx:MizanParser.ComparisonListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#comparison.
    def visitComparison(self, ctx:MizanParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#compOp.
    def visitCompOp(self, ctx:MizanParser.CompOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#BoolTrueExpr.
    def visitBoolTrueExpr(self, ctx:MizanParser.BoolTrueExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#AggExpr.
    def visitAggExpr(self, ctx:MizanParser.AggExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#VarOrArrayExpr.
    def visitVarOrArrayExpr(self, ctx:MizanParser.VarOrArrayExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#MulDivExpr.
    def visitMulDivExpr(self, ctx:MizanParser.MulDivExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#BoolFalseExpr.
    def visitBoolFalseExpr(self, ctx:MizanParser.BoolFalseExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#ProcCallExpr.
    def visitProcCallExpr(self, ctx:MizanParser.ProcCallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#ParenExpr.
    def visitParenExpr(self, ctx:MizanParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#NumLit.
    def visitNumLit(self, ctx:MizanParser.NumLitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#AddSubExpr.
    def visitAddSubExpr(self, ctx:MizanParser.AddSubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#UnaryMinusExpr.
    def visitUnaryMinusExpr(self, ctx:MizanParser.UnaryMinusExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#StrLit.
    def visitStrLit(self, ctx:MizanParser.StrLitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#aggregateExpr.
    def visitAggregateExpr(self, ctx:MizanParser.AggregateExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#aggFunc.
    def visitAggFunc(self, ctx:MizanParser.AggFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#argList.
    def visitArgList(self, ctx:MizanParser.ArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#healthRule.
    def visitHealthRule(self, ctx:MizanParser.HealthRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#escalationDef.
    def visitEscalationDef(self, ctx:MizanParser.EscalationDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#escalationLevel.
    def visitEscalationLevel(self, ctx:MizanParser.EscalationLevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#escalationField.
    def visitEscalationField(self, ctx:MizanParser.EscalationFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#escalationAction.
    def visitEscalationAction(self, ctx:MizanParser.EscalationActionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#reportDef.
    def visitReportDef(self, ctx:MizanParser.ReportDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#reportField.
    def visitReportField(self, ctx:MizanParser.ReportFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#IntervalSchedule.
    def visitIntervalSchedule(self, ctx:MizanParser.IntervalScheduleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#DailySchedule.
    def visitDailySchedule(self, ctx:MizanParser.DailyScheduleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#WeeklySchedule.
    def visitWeeklySchedule(self, ctx:MizanParser.WeeklyScheduleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#MonthlySchedule.
    def visitMonthlySchedule(self, ctx:MizanParser.MonthlyScheduleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#formatName.
    def visitFormatName(self, ctx:MizanParser.FormatNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#reportContent.
    def visitReportContent(self, ctx:MizanParser.ReportContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#reportItem.
    def visitReportItem(self, ctx:MizanParser.ReportItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#transitionTable.
    def visitTransitionTable(self, ctx:MizanParser.TransitionTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#transitionRule.
    def visitTransitionRule(self, ctx:MizanParser.TransitionRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#duration.
    def visitDuration(self, ctx:MizanParser.DurationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#timeSuffix.
    def visitTimeSuffix(self, ctx:MizanParser.TimeSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MizanParser#unitType.
    def visitUnitType(self, ctx:MizanParser.UnitTypeContext):
        return self.visitChildren(ctx)



del MizanParser