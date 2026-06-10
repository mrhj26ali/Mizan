// Generated from c:/Users/DELL/Desktop/Projects/Mizan/Frontend/Mizan.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link MizanParser}.
 */
public interface MizanListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link MizanParser#program}.
	 * @param ctx the parse tree
	 */
	void enterProgram(MizanParser.ProgramContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#program}.
	 * @param ctx the parse tree
	 */
	void exitProgram(MizanParser.ProgramContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#topLevelDecl}.
	 * @param ctx the parse tree
	 */
	void enterTopLevelDecl(MizanParser.TopLevelDeclContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#topLevelDecl}.
	 * @param ctx the parse tree
	 */
	void exitTopLevelDecl(MizanParser.TopLevelDeclContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#programDecl}.
	 * @param ctx the parse tree
	 */
	void enterProgramDecl(MizanParser.ProgramDeclContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#programDecl}.
	 * @param ctx the parse tree
	 */
	void exitProgramDecl(MizanParser.ProgramDeclContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#deviceBlock}.
	 * @param ctx the parse tree
	 */
	void enterDeviceBlock(MizanParser.DeviceBlockContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#deviceBlock}.
	 * @param ctx the parse tree
	 */
	void exitDeviceBlock(MizanParser.DeviceBlockContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#deviceField}.
	 * @param ctx the parse tree
	 */
	void enterDeviceField(MizanParser.DeviceFieldContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#deviceField}.
	 * @param ctx the parse tree
	 */
	void exitDeviceField(MizanParser.DeviceFieldContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#customUnitsBlock}.
	 * @param ctx the parse tree
	 */
	void enterCustomUnitsBlock(MizanParser.CustomUnitsBlockContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#customUnitsBlock}.
	 * @param ctx the parse tree
	 */
	void exitCustomUnitsBlock(MizanParser.CustomUnitsBlockContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#customUnitDef}.
	 * @param ctx the parse tree
	 */
	void enterCustomUnitDef(MizanParser.CustomUnitDefContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#customUnitDef}.
	 * @param ctx the parse tree
	 */
	void exitCustomUnitDef(MizanParser.CustomUnitDefContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#dimensionExpr}.
	 * @param ctx the parse tree
	 */
	void enterDimensionExpr(MizanParser.DimensionExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#dimensionExpr}.
	 * @param ctx the parse tree
	 */
	void exitDimensionExpr(MizanParser.DimensionExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#baseDim}.
	 * @param ctx the parse tree
	 */
	void enterBaseDim(MizanParser.BaseDimContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#baseDim}.
	 * @param ctx the parse tree
	 */
	void exitBaseDim(MizanParser.BaseDimContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#customModesBlock}.
	 * @param ctx the parse tree
	 */
	void enterCustomModesBlock(MizanParser.CustomModesBlockContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#customModesBlock}.
	 * @param ctx the parse tree
	 */
	void exitCustomModesBlock(MizanParser.CustomModesBlockContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#sensorDecl}.
	 * @param ctx the parse tree
	 */
	void enterSensorDecl(MizanParser.SensorDeclContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#sensorDecl}.
	 * @param ctx the parse tree
	 */
	void exitSensorDecl(MizanParser.SensorDeclContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#sensorField}.
	 * @param ctx the parse tree
	 */
	void enterSensorField(MizanParser.SensorFieldContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#sensorField}.
	 * @param ctx the parse tree
	 */
	void exitSensorField(MizanParser.SensorFieldContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#actuatorDecl}.
	 * @param ctx the parse tree
	 */
	void enterActuatorDecl(MizanParser.ActuatorDeclContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#actuatorDecl}.
	 * @param ctx the parse tree
	 */
	void exitActuatorDecl(MizanParser.ActuatorDeclContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#actuatorField}.
	 * @param ctx the parse tree
	 */
	void enterActuatorField(MizanParser.ActuatorFieldContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#actuatorField}.
	 * @param ctx the parse tree
	 */
	void exitActuatorField(MizanParser.ActuatorFieldContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#varDecl}.
	 * @param ctx the parse tree
	 */
	void enterVarDecl(MizanParser.VarDeclContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#varDecl}.
	 * @param ctx the parse tree
	 */
	void exitVarDecl(MizanParser.VarDeclContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#constDecl}.
	 * @param ctx the parse tree
	 */
	void enterConstDecl(MizanParser.ConstDeclContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#constDecl}.
	 * @param ctx the parse tree
	 */
	void exitConstDecl(MizanParser.ConstDeclContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#varType}.
	 * @param ctx the parse tree
	 */
	void enterVarType(MizanParser.VarTypeContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#varType}.
	 * @param ctx the parse tree
	 */
	void exitVarType(MizanParser.VarTypeContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#rangeSpec}.
	 * @param ctx the parse tree
	 */
	void enterRangeSpec(MizanParser.RangeSpecContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#rangeSpec}.
	 * @param ctx the parse tree
	 */
	void exitRangeSpec(MizanParser.RangeSpecContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#procedureDef}.
	 * @param ctx the parse tree
	 */
	void enterProcedureDef(MizanParser.ProcedureDefContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#procedureDef}.
	 * @param ctx the parse tree
	 */
	void exitProcedureDef(MizanParser.ProcedureDefContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#paramList}.
	 * @param ctx the parse tree
	 */
	void enterParamList(MizanParser.ParamListContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#paramList}.
	 * @param ctx the parse tree
	 */
	void exitParamList(MizanParser.ParamListContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#param}.
	 * @param ctx the parse tree
	 */
	void enterParam(MizanParser.ParamContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#param}.
	 * @param ctx the parse tree
	 */
	void exitParam(MizanParser.ParamContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#modeBlock}.
	 * @param ctx the parse tree
	 */
	void enterModeBlock(MizanParser.ModeBlockContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#modeBlock}.
	 * @param ctx the parse tree
	 */
	void exitModeBlock(MizanParser.ModeBlockContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#modeName}.
	 * @param ctx the parse tree
	 */
	void enterModeName(MizanParser.ModeNameContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#modeName}.
	 * @param ctx the parse tree
	 */
	void exitModeName(MizanParser.ModeNameContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#onStartBlock}.
	 * @param ctx the parse tree
	 */
	void enterOnStartBlock(MizanParser.OnStartBlockContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#onStartBlock}.
	 * @param ctx the parse tree
	 */
	void exitOnStartBlock(MizanParser.OnStartBlockContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#ruleBlock}.
	 * @param ctx the parse tree
	 */
	void enterRuleBlock(MizanParser.RuleBlockContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#ruleBlock}.
	 * @param ctx the parse tree
	 */
	void exitRuleBlock(MizanParser.RuleBlockContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#localDecl}.
	 * @param ctx the parse tree
	 */
	void enterLocalDecl(MizanParser.LocalDeclContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#localDecl}.
	 * @param ctx the parse tree
	 */
	void exitLocalDecl(MizanParser.LocalDeclContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#conditionClause}.
	 * @param ctx the parse tree
	 */
	void enterConditionClause(MizanParser.ConditionClauseContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#conditionClause}.
	 * @param ctx the parse tree
	 */
	void exitConditionClause(MizanParser.ConditionClauseContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#actionClause}.
	 * @param ctx the parse tree
	 */
	void enterActionClause(MizanParser.ActionClauseContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#actionClause}.
	 * @param ctx the parse tree
	 */
	void exitActionClause(MizanParser.ActionClauseContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterStatement(MizanParser.StatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitStatement(MizanParser.StatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#commandStmt}.
	 * @param ctx the parse tree
	 */
	void enterCommandStmt(MizanParser.CommandStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#commandStmt}.
	 * @param ctx the parse tree
	 */
	void exitCommandStmt(MizanParser.CommandStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#actuatorValue}.
	 * @param ctx the parse tree
	 */
	void enterActuatorValue(MizanParser.ActuatorValueContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#actuatorValue}.
	 * @param ctx the parse tree
	 */
	void exitActuatorValue(MizanParser.ActuatorValueContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#alertStmt}.
	 * @param ctx the parse tree
	 */
	void enterAlertStmt(MizanParser.AlertStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#alertStmt}.
	 * @param ctx the parse tree
	 */
	void exitAlertStmt(MizanParser.AlertStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#alertLevel}.
	 * @param ctx the parse tree
	 */
	void enterAlertLevel(MizanParser.AlertLevelContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#alertLevel}.
	 * @param ctx the parse tree
	 */
	void exitAlertLevel(MizanParser.AlertLevelContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#logStmt}.
	 * @param ctx the parse tree
	 */
	void enterLogStmt(MizanParser.LogStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#logStmt}.
	 * @param ctx the parse tree
	 */
	void exitLogStmt(MizanParser.LogStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#execProcStmt}.
	 * @param ctx the parse tree
	 */
	void enterExecProcStmt(MizanParser.ExecProcStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#execProcStmt}.
	 * @param ctx the parse tree
	 */
	void exitExecProcStmt(MizanParser.ExecProcStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#gotoStmt}.
	 * @param ctx the parse tree
	 */
	void enterGotoStmt(MizanParser.GotoStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#gotoStmt}.
	 * @param ctx the parse tree
	 */
	void exitGotoStmt(MizanParser.GotoStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#waitStmt}.
	 * @param ctx the parse tree
	 */
	void enterWaitStmt(MizanParser.WaitStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#waitStmt}.
	 * @param ctx the parse tree
	 */
	void exitWaitStmt(MizanParser.WaitStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#assignStmt}.
	 * @param ctx the parse tree
	 */
	void enterAssignStmt(MizanParser.AssignStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#assignStmt}.
	 * @param ctx the parse tree
	 */
	void exitAssignStmt(MizanParser.AssignStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#defaultValStmt}.
	 * @param ctx the parse tree
	 */
	void enterDefaultValStmt(MizanParser.DefaultValStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#defaultValStmt}.
	 * @param ctx the parse tree
	 */
	void exitDefaultValStmt(MizanParser.DefaultValStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#exprStmt}.
	 * @param ctx the parse tree
	 */
	void enterExprStmt(MizanParser.ExprStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#exprStmt}.
	 * @param ctx the parse tree
	 */
	void exitExprStmt(MizanParser.ExprStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#ifStmt}.
	 * @param ctx the parse tree
	 */
	void enterIfStmt(MizanParser.IfStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#ifStmt}.
	 * @param ctx the parse tree
	 */
	void exitIfStmt(MizanParser.IfStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#whileStmt}.
	 * @param ctx the parse tree
	 */
	void enterWhileStmt(MizanParser.WhileStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#whileStmt}.
	 * @param ctx the parse tree
	 */
	void exitWhileStmt(MizanParser.WhileStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#returnStmt}.
	 * @param ctx the parse tree
	 */
	void enterReturnStmt(MizanParser.ReturnStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#returnStmt}.
	 * @param ctx the parse tree
	 */
	void exitReturnStmt(MizanParser.ReturnStmtContext ctx);
	/**
	 * Enter a parse tree produced by the {@code OrExpr}
	 * labeled alternative in {@link MizanParser#condition}.
	 * @param ctx the parse tree
	 */
	void enterOrExpr(MizanParser.OrExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code OrExpr}
	 * labeled alternative in {@link MizanParser#condition}.
	 * @param ctx the parse tree
	 */
	void exitOrExpr(MizanParser.OrExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code OrPass}
	 * labeled alternative in {@link MizanParser#condition}.
	 * @param ctx the parse tree
	 */
	void enterOrPass(MizanParser.OrPassContext ctx);
	/**
	 * Exit a parse tree produced by the {@code OrPass}
	 * labeled alternative in {@link MizanParser#condition}.
	 * @param ctx the parse tree
	 */
	void exitOrPass(MizanParser.OrPassContext ctx);
	/**
	 * Enter a parse tree produced by the {@code AndExpr}
	 * labeled alternative in {@link MizanParser#orOperand}.
	 * @param ctx the parse tree
	 */
	void enterAndExpr(MizanParser.AndExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code AndExpr}
	 * labeled alternative in {@link MizanParser#orOperand}.
	 * @param ctx the parse tree
	 */
	void exitAndExpr(MizanParser.AndExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code AndPass}
	 * labeled alternative in {@link MizanParser#orOperand}.
	 * @param ctx the parse tree
	 */
	void enterAndPass(MizanParser.AndPassContext ctx);
	/**
	 * Exit a parse tree produced by the {@code AndPass}
	 * labeled alternative in {@link MizanParser#orOperand}.
	 * @param ctx the parse tree
	 */
	void exitAndPass(MizanParser.AndPassContext ctx);
	/**
	 * Enter a parse tree produced by the {@code NotExpr}
	 * labeled alternative in {@link MizanParser#andOperand}.
	 * @param ctx the parse tree
	 */
	void enterNotExpr(MizanParser.NotExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code NotExpr}
	 * labeled alternative in {@link MizanParser#andOperand}.
	 * @param ctx the parse tree
	 */
	void exitNotExpr(MizanParser.NotExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code PrimaryPass}
	 * labeled alternative in {@link MizanParser#andOperand}.
	 * @param ctx the parse tree
	 */
	void enterPrimaryPass(MizanParser.PrimaryPassContext ctx);
	/**
	 * Exit a parse tree produced by the {@code PrimaryPass}
	 * labeled alternative in {@link MizanParser#andOperand}.
	 * @param ctx the parse tree
	 */
	void exitPrimaryPass(MizanParser.PrimaryPassContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ParenCond}
	 * labeled alternative in {@link MizanParser#primaryCondition}.
	 * @param ctx the parse tree
	 */
	void enterParenCond(MizanParser.ParenCondContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ParenCond}
	 * labeled alternative in {@link MizanParser#primaryCondition}.
	 * @param ctx the parse tree
	 */
	void exitParenCond(MizanParser.ParenCondContext ctx);
	/**
	 * Enter a parse tree produced by the {@code CompExpr}
	 * labeled alternative in {@link MizanParser#primaryCondition}.
	 * @param ctx the parse tree
	 */
	void enterCompExpr(MizanParser.CompExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code CompExpr}
	 * labeled alternative in {@link MizanParser#primaryCondition}.
	 * @param ctx the parse tree
	 */
	void exitCompExpr(MizanParser.CompExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code TemporalExpr}
	 * labeled alternative in {@link MizanParser#primaryCondition}.
	 * @param ctx the parse tree
	 */
	void enterTemporalExpr(MizanParser.TemporalExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code TemporalExpr}
	 * labeled alternative in {@link MizanParser#primaryCondition}.
	 * @param ctx the parse tree
	 */
	void exitTemporalExpr(MizanParser.TemporalExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code VotingExpr}
	 * labeled alternative in {@link MizanParser#primaryCondition}.
	 * @param ctx the parse tree
	 */
	void enterVotingExpr(MizanParser.VotingExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code VotingExpr}
	 * labeled alternative in {@link MizanParser#primaryCondition}.
	 * @param ctx the parse tree
	 */
	void exitVotingExpr(MizanParser.VotingExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code TrueLit}
	 * labeled alternative in {@link MizanParser#primaryCondition}.
	 * @param ctx the parse tree
	 */
	void enterTrueLit(MizanParser.TrueLitContext ctx);
	/**
	 * Exit a parse tree produced by the {@code TrueLit}
	 * labeled alternative in {@link MizanParser#primaryCondition}.
	 * @param ctx the parse tree
	 */
	void exitTrueLit(MizanParser.TrueLitContext ctx);
	/**
	 * Enter a parse tree produced by the {@code FalseLit}
	 * labeled alternative in {@link MizanParser#primaryCondition}.
	 * @param ctx the parse tree
	 */
	void enterFalseLit(MizanParser.FalseLitContext ctx);
	/**
	 * Exit a parse tree produced by the {@code FalseLit}
	 * labeled alternative in {@link MizanParser#primaryCondition}.
	 * @param ctx the parse tree
	 */
	void exitFalseLit(MizanParser.FalseLitContext ctx);
	/**
	 * Enter a parse tree produced by the {@code BoolVar}
	 * labeled alternative in {@link MizanParser#primaryCondition}.
	 * @param ctx the parse tree
	 */
	void enterBoolVar(MizanParser.BoolVarContext ctx);
	/**
	 * Exit a parse tree produced by the {@code BoolVar}
	 * labeled alternative in {@link MizanParser#primaryCondition}.
	 * @param ctx the parse tree
	 */
	void exitBoolVar(MizanParser.BoolVarContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#comparisonList}.
	 * @param ctx the parse tree
	 */
	void enterComparisonList(MizanParser.ComparisonListContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#comparisonList}.
	 * @param ctx the parse tree
	 */
	void exitComparisonList(MizanParser.ComparisonListContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#comparison}.
	 * @param ctx the parse tree
	 */
	void enterComparison(MizanParser.ComparisonContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#comparison}.
	 * @param ctx the parse tree
	 */
	void exitComparison(MizanParser.ComparisonContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#compOp}.
	 * @param ctx the parse tree
	 */
	void enterCompOp(MizanParser.CompOpContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#compOp}.
	 * @param ctx the parse tree
	 */
	void exitCompOp(MizanParser.CompOpContext ctx);
	/**
	 * Enter a parse tree produced by the {@code AggExpr}
	 * labeled alternative in {@link MizanParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterAggExpr(MizanParser.AggExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code AggExpr}
	 * labeled alternative in {@link MizanParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitAggExpr(MizanParser.AggExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code VarOrArrayExpr}
	 * labeled alternative in {@link MizanParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterVarOrArrayExpr(MizanParser.VarOrArrayExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code VarOrArrayExpr}
	 * labeled alternative in {@link MizanParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitVarOrArrayExpr(MizanParser.VarOrArrayExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code MulDivExpr}
	 * labeled alternative in {@link MizanParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterMulDivExpr(MizanParser.MulDivExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code MulDivExpr}
	 * labeled alternative in {@link MizanParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitMulDivExpr(MizanParser.MulDivExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ProcCallExpr}
	 * labeled alternative in {@link MizanParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterProcCallExpr(MizanParser.ProcCallExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ProcCallExpr}
	 * labeled alternative in {@link MizanParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitProcCallExpr(MizanParser.ProcCallExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ParenExpr}
	 * labeled alternative in {@link MizanParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterParenExpr(MizanParser.ParenExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ParenExpr}
	 * labeled alternative in {@link MizanParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitParenExpr(MizanParser.ParenExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code NumLit}
	 * labeled alternative in {@link MizanParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterNumLit(MizanParser.NumLitContext ctx);
	/**
	 * Exit a parse tree produced by the {@code NumLit}
	 * labeled alternative in {@link MizanParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitNumLit(MizanParser.NumLitContext ctx);
	/**
	 * Enter a parse tree produced by the {@code AddSubExpr}
	 * labeled alternative in {@link MizanParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterAddSubExpr(MizanParser.AddSubExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code AddSubExpr}
	 * labeled alternative in {@link MizanParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitAddSubExpr(MizanParser.AddSubExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code UnaryMinusExpr}
	 * labeled alternative in {@link MizanParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterUnaryMinusExpr(MizanParser.UnaryMinusExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code UnaryMinusExpr}
	 * labeled alternative in {@link MizanParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitUnaryMinusExpr(MizanParser.UnaryMinusExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code StrLit}
	 * labeled alternative in {@link MizanParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterStrLit(MizanParser.StrLitContext ctx);
	/**
	 * Exit a parse tree produced by the {@code StrLit}
	 * labeled alternative in {@link MizanParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitStrLit(MizanParser.StrLitContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#aggregateExpr}.
	 * @param ctx the parse tree
	 */
	void enterAggregateExpr(MizanParser.AggregateExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#aggregateExpr}.
	 * @param ctx the parse tree
	 */
	void exitAggregateExpr(MizanParser.AggregateExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#aggFunc}.
	 * @param ctx the parse tree
	 */
	void enterAggFunc(MizanParser.AggFuncContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#aggFunc}.
	 * @param ctx the parse tree
	 */
	void exitAggFunc(MizanParser.AggFuncContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#argList}.
	 * @param ctx the parse tree
	 */
	void enterArgList(MizanParser.ArgListContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#argList}.
	 * @param ctx the parse tree
	 */
	void exitArgList(MizanParser.ArgListContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#healthRule}.
	 * @param ctx the parse tree
	 */
	void enterHealthRule(MizanParser.HealthRuleContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#healthRule}.
	 * @param ctx the parse tree
	 */
	void exitHealthRule(MizanParser.HealthRuleContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#escalationDef}.
	 * @param ctx the parse tree
	 */
	void enterEscalationDef(MizanParser.EscalationDefContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#escalationDef}.
	 * @param ctx the parse tree
	 */
	void exitEscalationDef(MizanParser.EscalationDefContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#escalationLevel}.
	 * @param ctx the parse tree
	 */
	void enterEscalationLevel(MizanParser.EscalationLevelContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#escalationLevel}.
	 * @param ctx the parse tree
	 */
	void exitEscalationLevel(MizanParser.EscalationLevelContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#escalationField}.
	 * @param ctx the parse tree
	 */
	void enterEscalationField(MizanParser.EscalationFieldContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#escalationField}.
	 * @param ctx the parse tree
	 */
	void exitEscalationField(MizanParser.EscalationFieldContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#escalationAction}.
	 * @param ctx the parse tree
	 */
	void enterEscalationAction(MizanParser.EscalationActionContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#escalationAction}.
	 * @param ctx the parse tree
	 */
	void exitEscalationAction(MizanParser.EscalationActionContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#reportDef}.
	 * @param ctx the parse tree
	 */
	void enterReportDef(MizanParser.ReportDefContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#reportDef}.
	 * @param ctx the parse tree
	 */
	void exitReportDef(MizanParser.ReportDefContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#reportField}.
	 * @param ctx the parse tree
	 */
	void enterReportField(MizanParser.ReportFieldContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#reportField}.
	 * @param ctx the parse tree
	 */
	void exitReportField(MizanParser.ReportFieldContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#scheduleSpec}.
	 * @param ctx the parse tree
	 */
	void enterScheduleSpec(MizanParser.ScheduleSpecContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#scheduleSpec}.
	 * @param ctx the parse tree
	 */
	void exitScheduleSpec(MizanParser.ScheduleSpecContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#formatName}.
	 * @param ctx the parse tree
	 */
	void enterFormatName(MizanParser.FormatNameContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#formatName}.
	 * @param ctx the parse tree
	 */
	void exitFormatName(MizanParser.FormatNameContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#reportContent}.
	 * @param ctx the parse tree
	 */
	void enterReportContent(MizanParser.ReportContentContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#reportContent}.
	 * @param ctx the parse tree
	 */
	void exitReportContent(MizanParser.ReportContentContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#reportItem}.
	 * @param ctx the parse tree
	 */
	void enterReportItem(MizanParser.ReportItemContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#reportItem}.
	 * @param ctx the parse tree
	 */
	void exitReportItem(MizanParser.ReportItemContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#transitionTable}.
	 * @param ctx the parse tree
	 */
	void enterTransitionTable(MizanParser.TransitionTableContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#transitionTable}.
	 * @param ctx the parse tree
	 */
	void exitTransitionTable(MizanParser.TransitionTableContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#transitionRule}.
	 * @param ctx the parse tree
	 */
	void enterTransitionRule(MizanParser.TransitionRuleContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#transitionRule}.
	 * @param ctx the parse tree
	 */
	void exitTransitionRule(MizanParser.TransitionRuleContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#duration}.
	 * @param ctx the parse tree
	 */
	void enterDuration(MizanParser.DurationContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#duration}.
	 * @param ctx the parse tree
	 */
	void exitDuration(MizanParser.DurationContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#timeSuffix}.
	 * @param ctx the parse tree
	 */
	void enterTimeSuffix(MizanParser.TimeSuffixContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#timeSuffix}.
	 * @param ctx the parse tree
	 */
	void exitTimeSuffix(MizanParser.TimeSuffixContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#unitType}.
	 * @param ctx the parse tree
	 */
	void enterUnitType(MizanParser.UnitTypeContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#unitType}.
	 * @param ctx the parse tree
	 */
	void exitUnitType(MizanParser.UnitTypeContext ctx);
	/**
	 * Enter a parse tree produced by {@link MizanParser#fieldSep}.
	 * @param ctx the parse tree
	 */
	void enterFieldSep(MizanParser.FieldSepContext ctx);
	/**
	 * Exit a parse tree produced by {@link MizanParser#fieldSep}.
	 * @param ctx the parse tree
	 */
	void exitFieldSep(MizanParser.FieldSepContext ctx);
}