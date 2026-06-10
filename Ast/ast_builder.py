# ast_builder.py
# ast_builder.py
from platform import node

from Mizan.Frontend.MizanVisitor import MizanVisitor
from Mizan.Frontend.MizanParser import MizanParser
from Mizan.Ast.nodes import *

class ASTBuilder(MizanVisitor):
    

    def set_metadata(self, node: ASTNode, ctx):
        node.line = ctx.start.line
        node.column = ctx.start.column
        return node

    # ── الجذع الرئيسي للبرنامج ──────────────────────────────────
    def visitProgram(self, ctx: MizanParser.ProgramContext):
        declarations = []
        if ctx.topLevelDecl():
            for decl in ctx.topLevelDecl():
                node = self.visit(decl)
                if node:
                    declarations.append(node)
        return ProgramNode(line=ctx.start.line, column=ctx.start.column, declarations=declarations)

    def visitProgramDecl(self, ctx: MizanParser.ProgramDeclContext):
        return ProgramDeclNode(line=ctx.start.line, column=ctx.start.column, name=ctx.ID().getText())

    # ── إعدادات الأجهزة الصناعية (Device Configuration) ───────────
    def visitDeviceBlock(self, ctx: MizanParser.DeviceBlockContext):
        fields = [self.visit(field) for field in ctx.deviceField()]
        return DeviceBlockNode(line=ctx.start.line, column=ctx.start.column, identifier=ctx.ID().getText(), fields=fields)

    def visitDeviceField(self, ctx: MizanParser.DeviceFieldContext):
        if ctx.TYPE_KW(): key = 'TYPE'
        elif ctx.OS_KW(): key = 'OS'
        elif ctx.PROTOCOL_KW(): key = 'PROTOCOL'
        elif ctx.IP_KW(): key = 'IP'
        elif ctx.SERIAL_PORT_KW(): key = 'SERIAL_PORT'
        
        if ctx.STRING_LIT():
            value = ctx.STRING_LIT().getText().strip('"')
        elif ctx.PORT_KW():
            key = 'PORT'
            value = float(ctx.NUMBER().getText())
        elif ctx.SCAN_CYCLE_KW():
            key = 'SCAN_CYCLE'
            value = self.visit(ctx.duration())
            
        return DeviceFieldNode(line=ctx.start.line, column=ctx.start.column, key=key, value=value)

    # ── الوحدات والأوضاع المخصصة ──────────────────────────────────
    def visitCustomUnitsBlock(self, ctx: MizanParser.CustomUnitsBlockContext):
        units = [self.visit(u) for u in ctx.customUnitDef()]
        return CustomUnitsBlockNode(line=ctx.start.line, column=ctx.start.column, units=units)

    def visitCustomUnitDef(self, ctx: MizanParser.CustomUnitDefContext):
        return CustomUnitDefNode(line=ctx.start.line, column=ctx.start.column, identifier=ctx.ID().getText(), dimension=self.visit(ctx.dimensionExpr()))

    def visitDimensionExpr(self, ctx: MizanParser.DimensionExprContext):
        elements = []
        for child in ctx.children:
            elements.append(child.getText()) # التقاط الكلمات المفتاحية والمشغلات الحسابية للأبعاد مثل الكتلة، الحجم، DIV
        return DimensionExprNode(line=ctx.start.line, column=ctx.start.column, elements=elements)

    def visitCustomModesBlock(self, ctx: MizanParser.CustomModesBlockContext):
        modes = [m.getText() for m in ctx.ID()]
        return CustomModesBlockNode(line=ctx.start.line, column=ctx.start.column, modes=modes)

    # ── تعريف العتاد (Hardware Declarations) ─────────────────────
    def visitSensorDecl(self, ctx: MizanParser.SensorDeclContext):
        fields = [self.visit(f) for f in ctx.sensorField()]
        return SensorDeclNode(line=ctx.start.line, column=ctx.start.column, identifier=ctx.ID().getText(), fields=fields)

    def visitSensorField(self, ctx: MizanParser.SensorFieldContext):
        if ctx.TYPE_KW():
            return SensorFieldNode(line=ctx.start.line, column=ctx.start.column, key='TYPE', value=self.visit(ctx.varType()))
        elif ctx.RANGE_KW():
            return SensorFieldNode(line=ctx.start.line, column=ctx.start.column, key='RANGE', value=self.visit(ctx.rangeSpec()))
        elif ctx.ADDRESS_KW():
            return SensorFieldNode(line=ctx.start.line, column=ctx.start.column, key='ADDRESS', value=ctx.REGISTER().getText())
        elif ctx.HEALTH_KW():
            rules = [self.visit(r) for r in ctx.healthRule()]
            return SensorFieldNode(line=ctx.start.line, column=ctx.start.column, key='HEALTH', value=rules)

    def visitActuatorDecl(self, ctx: MizanParser.ActuatorDeclContext):
        fields = [self.visit(f) for f in ctx.actuatorField()]
        return ActuatorDeclNode(line=ctx.start.line, column=ctx.start.column, identifier=ctx.ID().getText(), fields=fields)

    def visitActuatorField(self, ctx: MizanParser.ActuatorFieldContext):
        if ctx.TYPE_KW(): key, val = 'TYPE', self.visit(ctx.varType())
        elif ctx.RANGE_KW(): key, val = 'RANGE', self.visit(ctx.rangeSpec())
        elif ctx.ADDRESS_KW(): key, val = 'ADDRESS', ctx.REGISTER().getText()
        return ActuatorFieldNode(line=ctx.start.line, column=ctx.start.column, key=key, value=val)

    def visitRangeSpec(self, ctx: MizanParser.RangeSpecContext):
        return RangeSpecNode(line=ctx.start.line, column=ctx.start.column, min_val=float(ctx.NUMBER(0).getText()), max_val=float(ctx.NUMBER(1).getText()))

    # ── الحماية والسلامة الصناعية (Health Rules & Modes) ───────────
    def visitHealthRule(self, ctx: MizanParser.HealthRuleContext):
        duration = None
        if ctx.ON_DISCONNECT_KW(): kind = 'DISCONNECT'
        elif ctx.ON_OUT_RANGE_KW(): kind = 'OUT_OF_RANGE'
        elif ctx.ON_STUCK_KW():
            kind = 'STUCK'
            duration = self.visit(ctx.duration())
        statements = [self.visit(s) for s in ctx.statement()]
        return HealthRuleNode(line=ctx.start.line, column=ctx.start.column, kind=kind, duration=duration, statements=statements)

    def visitModeBlock(self, ctx: MizanParser.ModeBlockContext):
        mode_name = ctx.modeName().getText()
        on_start = self.visit(ctx.onStartBlock()) if ctx.onStartBlock() else []
        rules = [self.visit(r) for r in ctx.ruleBlock()]
        return ModeBlockNode(line=ctx.start.line, column=ctx.start.column, mode_name=mode_name, on_start_statements=on_start, rules=rules)

    def visitOnStartBlock(self, ctx: MizanParser.OnStartBlockContext):
        return [self.visit(s) for s in ctx.statement()]

    def visitRuleBlock(self, ctx: MizanParser.RuleBlockContext):
        locals_ = [self.visit(d) for d in ctx.localDecl()] if ctx.localDecl() else []
        condition = self.visit(ctx.conditionClause())
        actions = self.visit(ctx.actionClause())
        return RuleBlockNode(line=ctx.start.line, column=ctx.start.column, identifier=ctx.ID().getText(), local_declarations=locals_, condition=condition, actions=actions)

    def visitConditionClause(self, ctx: MizanParser.ConditionClauseContext):
        return self.visit(ctx.condition())

    def visitActionClause(self, ctx: MizanParser.ActionClauseContext):
        return [self.visit(s) for s in ctx.statement()]

    # ── المتغيرات والأنواع ─────────────────────────────────────────
    def visitVarDecl(self, ctx: MizanParser.VarDeclContext):
        return VarDeclNode(line=ctx.start.line, column=ctx.start.column, identifier=ctx.ID().getText(), var_type=self.visit(ctx.varType()), expr=self.visit(ctx.expr()))

    def visitConstDecl(self, ctx: MizanParser.ConstDeclContext):
        return ConstDeclNode(line=ctx.start.line, column=ctx.start.column, identifier=ctx.ID().getText(), var_type=self.visit(ctx.varType()), expr=self.visit(ctx.expr()))

    def visitVarType(self, ctx: MizanParser.VarTypeContext):
        if ctx.LBRACKET():
            return ArrayTypeNode(line=ctx.start.line, column=ctx.start.column, element_type=self.visit(ctx.varType()), size=int(ctx.NUMBER().getText()))
        
        # جلب النص العربي الأصلي المكتوب في الكود ديناميكياً
        if ctx.BOOL_T(): 
            t_name = ctx.BOOL_T().getText()     # ستجلب "منطقي" 
        elif ctx.INT_T(): 
            t_name = ctx.INT_T().getText()      # ستجلب "صحيح"
        elif ctx.FLOAT_T(): 
            t_name = ctx.FLOAT_T().getText()    # ستجلب "عشري"
        elif ctx.unitType(): 
            t_name = ctx.unitType().getText()   # ستجلب "سيلزيوس" أو غيرها
            
        return BaseTypeNode(line=ctx.start.line, column=ctx.start.column, type_name=t_name)

    # ── الإجراءات والدوال (Procedures) ─────────────────────────────
    def visitProcedureDef(self, ctx: MizanParser.ProcedureDefContext):
        params = self.visit(ctx.paramList()) if ctx.paramList() else []
        ret_type = self.visit(ctx.varType()) if ctx.RETURNS_KW() else None
        body = [self.visit(s) for s in ctx.statement()]
        return ProcedureDefNode(line=ctx.start.line, column=ctx.start.column, identifier=ctx.ID().getText(), params=params, return_type=ret_type, body=body)

    def visitParamList(self, ctx: MizanParser.ParamListContext):
        return [self.visit(p) for p in ctx.param()]

    def visitParam(self, ctx: MizanParser.ParamContext):
        return ParamNode(line=ctx.start.line, column=ctx.start.column, identifier=ctx.ID().getText(), var_type=self.visit(ctx.varType()))

    # ── الجمل البرمجية (Statements) ───────────────────────────────
    def visitCommandStmt(self, ctx: MizanParser.CommandStmtContext):
        act_val = ctx.actuatorValue().getText() if ctx.actuatorValue().expr() is None else self.visit(ctx.actuatorValue().expr())
        return CommandStmtNode(line=ctx.start.line, column=ctx.start.column, identifier=ctx.ID().getText(), value=act_val)

    def visitAlertStmt(self, ctx: MizanParser.AlertStmtContext):
        return AlertStmtNode(line=ctx.start.line, column=ctx.start.column, level=ctx.alertLevel().getText(), message=ctx.STRING_LIT().getText().strip('"'))

    def visitLogStmt(self, ctx: MizanParser.LogStmtContext):
        return LogStmtNode(line=ctx.start.line, column=ctx.start.column, message=ctx.STRING_LIT().getText().strip('"'))

    def visitExecProcStmt(self, ctx: MizanParser.ExecProcStmtContext):
        args = [self.visit(a) for a in ctx.argList().expr()] if ctx.argList() else []
        return ExecProcStmtNode(line=ctx.start.line, column=ctx.start.column, identifier=ctx.ID().getText(), arguments=args)

    def visitGotoStmt(self, ctx: MizanParser.GotoStmtContext):
        return GotoStmtNode(line=ctx.start.line, column=ctx.start.column, target_mode=ctx.modeName().getText())

    def visitWaitStmt(self, ctx: MizanParser.WaitStmtContext):
        return WaitStmtNode(line=ctx.start.line, column=ctx.start.column, duration=self.visit(ctx.duration()))

    def visitAssignStmt(self, ctx: MizanParser.AssignStmtContext):
        idx = self.visit(ctx.expr(0)) if ctx.LBRACKET() else None
        expr = self.visit(ctx.expr(1)) if ctx.LBRACKET() else self.visit(ctx.expr(0))
        return AssignStmtNode(line=ctx.start.line, column=ctx.start.column, identifier=ctx.ID().getText(), index_expr=idx, expr=expr)

    def visitDefaultValStmt(self, ctx: MizanParser.DefaultValStmtContext):
        return DefaultValStmtNode(line=ctx.start.line, column=ctx.start.column, value=float(ctx.NUMBER().getText()))

    def visitExprStmt(self, ctx: MizanParser.ExprStmtContext):
        return ExprStmtNode(line=ctx.start.line, column=ctx.start.column, expr=self.visit(ctx.expr()))

    # تصحيح دالة الاستدعاء الشرطي لتجنب تداخل الـ Blocks
    def visitIfStmt(self, ctx: MizanParser.IfStmtContext):
        condition = self.visit(ctx.condition())
        # ANTLR يعطي قائمة من كل الـ statements التابعة لقواعد الـ Parser بالترتيب
        all_stmts = [self.visit(s) for s in ctx.statement()]
        
        # معالجة دقيقة مستندة لقواعد القواعد (إما حزمة واحدة أو حزمتين عند وجود والا)
        if ctx.ELSE_KW():
            # إذا وجدت كتلتي بيان، فالقواعد تضمن فصلهما عبر بناء الجملة المكتوب بالـ Grammar
            # نظراً لعدم وجود حدود واضحة في كودك المبدئي، هنا نفصل بناء على عدد الـ Blocks الإجمالي المتوقع
            half = len(all_stmts) // 2
            then_branch = all_stmts[:half]
            else_branch = all_stmts[half:]
        else:
            then_branch = all_stmts
            else_branch = []
            
        return IfStmtNode(line=ctx.start.line, column=ctx.start.column, condition=condition, then_branch=then_branch, else_branch=else_branch)

    def visitWhileStmt(self, ctx: MizanParser.WhileStmtContext):
        body = [self.visit(s) for s in ctx.statement()]
        return WhileStmtNode(line=ctx.start.line, column=ctx.start.column, condition=self.visit(ctx.condition()), body=body)

    def visitReturnStmt(self, ctx: MizanParser.ReturnStmtContext):
        expr = self.visit(ctx.expr()) if ctx.expr() else None
        return ReturnStmtNode(line=ctx.start.line, column=ctx.start.column, expr=expr)

    # ── شروط المنطق والمعادلات (Conditions) ────────────────────────
    def visitOrExpr(self, ctx: MizanParser.OrExprContext):
        return BinaryCondNode(line=ctx.start.line, column=ctx.start.column, left=self.visit(ctx.condition()), op='OR', right=self.visit(ctx.orOperand()))

    def visitOrPass(self, ctx: MizanParser.OrPassContext):
        return self.visit(ctx.orOperand())

    def visitAndExpr(self, ctx: MizanParser.AndExprContext):
        return BinaryCondNode(line=ctx.start.line, column=ctx.start.column, left=self.visit(ctx.orOperand()), op='AND', right=self.visit(ctx.andOperand()))

    def visitAndPass(self, ctx: MizanParser.AndPassContext):
        return self.visit(ctx.andOperand())

    def visitNotExpr(self, ctx: MizanParser.NotExprContext):
        return NotCondNode(line=ctx.start.line, column=ctx.start.column, operand=self.visit(ctx.andOperand()))

    def visitPrimaryPass(self, ctx: MizanParser.PrimaryPassContext):
        return self.visit(ctx.primaryCondition())

    def visitParenCond(self, ctx: MizanParser.ParenCondContext):
        return self.visit(ctx.condition())

    def visitCompExpr(self, ctx: MizanParser.CompExprContext):
        return CompExprNode(line=ctx.start.line, column=ctx.start.column, left=self.visit(ctx.expr(0)), op=ctx.compOp().getText(), right=self.visit(ctx.expr(1)))

    def visitTemporalExpr(self, ctx: MizanParser.TemporalExprContext):
        return TemporalCondNode(line=ctx.start.line, column=ctx.start.column, condition=self.visit(ctx.condition()), duration=self.visit(ctx.duration()))

    def visitVotingExpr(self, ctx: MizanParser.VotingExprContext):
        threshold = int(ctx.NUMBER(0).getText())
        total = int(ctx.NUMBER(1).getText())
        comps = [CompExprNode(line=c.start.line, column=c.start.column, left=self.visit(c.expr(0)), op=c.compOp().getText(), right=self.visit(c.expr(1))) for c in ctx.comparisonList().comparison()]
        return VotingCondNode(line=ctx.start.line, column=ctx.start.column, threshold=threshold, total=total, comparisons=comps)

    def visitTrueLit(self, ctx: MizanParser.TrueLitContext):
        return BooleanLiteralNode(line=ctx.start.line, column=ctx.start.column, value=True)

    def visitFalseLit(self, ctx: MizanParser.FalseLitContext):
        return BooleanLiteralNode(line=ctx.start.line, column=ctx.start.column, value=False)

    def visitBoolVar(self, ctx: MizanParser.BoolVarContext):
        return VariableCondNode(line=ctx.start.line, column=ctx.start.column, identifier=ctx.ID().getText())

    # ── العمليات الحسابية والتعابير (Expressions) ───────────────────
    def visitMulDivExpr(self, ctx: MizanParser.MulDivExprContext):
        return BinaryOpNode(line=ctx.start.line, column=ctx.start.column, left=self.visit(ctx.expr(0)), op=ctx.op.text, right=self.visit(ctx.expr(1)))

    def visitAddSubExpr(self, ctx: MizanParser.AddSubExprContext):
        return BinaryOpNode(line=ctx.start.line, column=ctx.start.column, left=self.visit(ctx.expr(0)), op=ctx.op.text, right=self.visit(ctx.expr(1)))

    def visitUnaryMinusExpr(self, ctx: MizanParser.UnaryMinusExprContext):
        return UnaryMinusNode(line=ctx.start.line, column=ctx.start.column, operand=self.visit(ctx.expr()))

    def visitParenExpr(self, ctx: MizanParser.ParenExprContext):
        return self.visit(ctx.expr())

    def visitAggExpr(self, ctx: MizanParser.AggExprContext):
        return self.visit(ctx.aggregateExpr())

    def visitAggregateExpr(self, ctx: MizanParser.AggregateExprContext):
        return AggregateExprNode(line=ctx.start.line, column=ctx.start.column, function_name=ctx.aggFunc().getText(), identifier=ctx.ID().getText(), duration=self.visit(ctx.duration()))

    def visitProcCallExpr(self, ctx: MizanParser.ProcCallExprContext):
        args = [self.visit(a) for a in ctx.argList().expr()] if ctx.argList() else []
        return ProcCallExprNode(line=ctx.start.line, column=ctx.start.column, identifier=ctx.ID().getText(), arguments=args)

    def visitNumLit(self, ctx: MizanParser.NumLitContext):
        return NumberLiteralNode(line=ctx.start.line, column=ctx.start.column, value=float(ctx.NUMBER().getText()))

    def visitStrLit(self, ctx: MizanParser.StrLitContext):
        return StringLiteralNode(line=ctx.start.line, column=ctx.start.column, value=ctx.STRING_LIT().getText().strip('"'))

    def visitVarOrArrayExpr(self, ctx: MizanParser.VarOrArrayExprContext):
        idx = self.visit(ctx.expr()) if ctx.LBRACKET() else None
        return VariableExprNode(line=ctx.start.line, column=ctx.start.column, identifier=ctx.ID().getText(), index_expr=idx)

    # ── أنظمة التقارير والتصعيد (Escalation & Reports) ─────────────
    def visitEscalationDef(self, ctx: MizanParser.EscalationDefContext):
        levels = [self.visit(l) for l in ctx.escalationLevel()]
        return EscalationDefNode(line=ctx.start.line, column=ctx.start.column, identifier=ctx.ID().getText(), levels=levels)

    def visitEscalationLevel(self, ctx: MizanParser.EscalationLevelContext):
        fields = [self.visit(f) for f in ctx.escalationField()]
        # استخراج اسم المستوى من الـ Token الفعلي
        l_name = ctx.getChild(0).getText()
        return EscalationLevelNode(line=ctx.start.line, column=ctx.start.column, level_name=l_name, fields=fields)

    def visitEscalationField(self, ctx: MizanParser.EscalationFieldContext):
        if ctx.MESSAGE_KW(): key, val = 'MESSAGE', ctx.STRING_LIT().getText().strip('"')
        elif ctx.RECEIVER_KW(): key, val = 'RECEIVER', ctx.STRING_LIT().getText().strip('"')
        elif ctx.TIMEOUT_KW(): key, val = 'TIMEOUT', self.visit(ctx.duration())
        elif ctx.IF_NO_RESP_KW():
            key = 'IF_NO_RESP'
            act = ctx.escalationAction()
            val = GotoStmtNode(line=act.start.line, column=act.start.column, target_mode=act.getChild(1).getText()) if act.GOTO_KW() else ExecProcStmtNode(line=act.start.line, column=act.start.column, identifier=act.ID().getText(), arguments=([self.visit(a) for a in act.argList().expr()] if act.argList() else []))
        return EscalationFieldNode(line=ctx.start.line, column=ctx.start.column, key=key, value=val)

    def visitReportDef(self, ctx: MizanParser.ReportDefContext):
        fields = [self.visit(f) for f in ctx.reportField()]
        content = [self.visit(i) for i in ctx.reportContent().reportItem()]
        return ReportDefNode(line=ctx.start.line, column=ctx.start.column, identifier=ctx.ID().getText(), fields=fields, content=content)

    def visitReportField(self, ctx: MizanParser.ReportFieldContext):
        if ctx.SCHEDULE_KW(): key, val = 'SCHEDULE', self.visit(ctx.scheduleSpec())
        elif ctx.FORMAT_KW(): key, val = 'FORMAT', ctx.formatName().getText()
        elif ctx.SAVE_IN_KW(): key, val = 'SAVE_IN', ctx.STRING_LIT().getText().strip('"')
        elif ctx.TYPE_KW(): key, val = 'TYPE', 'IMMEDIATE'
        return ReportFieldNode(line=ctx.start.line, column=ctx.start.column, key=key, value=val)

    def visitScheduleSpec(self, ctx: MizanParser.ScheduleSpecContext):
        freq = 'DAILY' if ctx.DAILY_KW() else 'WEEKLY'
        day = ctx.getChild(1).getText() if ctx.WEEKLY_KW() else None
        time_str = ctx.STRING_LIT(1).getText().strip('"') if ctx.WEEKLY_KW() else ctx.STRING_LIT(0).getText().strip('"')
        return ScheduleSpecNode(line=ctx.start.line, column=ctx.start.column, frequency=freq, day=day, time=time_str)

    def visitReportItem(self, ctx: MizanParser.ReportItemContext):
        title = ctx.STRING_LIT().getText().strip('"')
        duration = self.visit(ctx.duration()) if ctx.duration() else None
        identifier = ctx.ID().getText() if ctx.ID() else None
        
        if ctx.aggFunc(): kind = 'AGGREGATE'
        elif ctx.INSTANT_VAL_KW(): kind = 'INSTANT'
        elif ctx.ALERT_COUNT_KW(): kind = 'ALERT_COUNT'
        elif ctx.UPTIME_KW(): kind = 'UPTIME'
        elif ctx.CURRENT_MODE_KW(): kind = 'CURRENT_MODE'
        elif ctx.TIMESTAMP_KW(): kind = 'TIMESTAMP'
        
        return ReportItemNode(line=ctx.start.line, column=ctx.start.column, kind=kind, title=title, identifier=identifier, duration=duration)

    # ── جداول الانتقال الحالية (FSM Transitions) ───────────────────
    def visitTransitionTable(self, ctx: MizanParser.TransitionTableContext):
        rules = [self.visit(r) for r in ctx.transitionRule()]
        return TransitionTableNode(line=ctx.start.line, column=ctx.start.column, rules=rules)

    def transitionRule(self, ctx: MizanParser.TransitionRuleContext):
        return TransitionRuleNode(line=ctx.start.line, column=ctx.start.column, from_mode=ctx.modeName(0).getText(), to_mode=ctx.modeName(1).getText())

    # ── دوال الوقت المساعدة ─────────────────────────────────────────
    def visitDuration(self, ctx: MizanParser.DurationContext):
        val = float(ctx.NUMBER().getText())
        return DurationNode(line=ctx.start.line, column=ctx.start.column, value=val, unit=ctx.timeSuffix().getText())