// =====================================================================
// MIZAN GRAMMAR v1.0 (Final Locked Baseline + Enhancements)
// Arabic-native compiled DSL for industrial process monitoring
// Target: Native ELF via LLVM (llvmlite)
// =====================================================================
grammar Mizan;

// =====================================================================
// PARSER RULES (Lowercase)
// =====================================================================

program
    : topLevelDecl* EOF
    ;

topLevelDecl
    : programDecl
    | deviceBlock
    | customUnitsBlock
    | customModesBlock
    | sensorDecl
    | actuatorDecl
    | varDecl
    | constDecl
    | procedureDef
    | modeBlock
    | escalationDef
    | reportDef
    | transitionTable
    ;

// ── Program & Device Configuration ────────────────────────────────
programDecl : BARNMJ ID SEMI ;

// Unified Block Syntax for Device
deviceBlock
    : JHAZ ID LBRACE deviceField (fieldSep deviceField)* RBRACE SEMI
    ;

deviceField
    : TYPE_KW        COLON STRING_LIT
    | OS_KW          COLON STRING_LIT
    | PROTOCOL_KW    COLON STRING_LIT
    | IP_KW          COLON STRING_LIT
    | PORT_KW        COLON NUMBER
    | SERIAL_PORT_KW COLON STRING_LIT
    | SCAN_CYCLE_KW  COLON duration
    ;

// ── Custom Units & Modes ──────────────────────────────────────────
customUnitsBlock
    : CUSTOM_UNITS_KW LBRACE customUnitDef (fieldSep customUnitDef)* RBRACE SEMI
    ;
customUnitDef : ID COLON dimensionExpr ;
dimensionExpr : baseDim ((DIV | MUL) baseDim)* ;
baseDim
    : MASS_KW | VOLUME_KW | TIME_DIM_KW | LENGTH_KW | TEMP_DIM_KW
    | CURRENT_DIM_KW | VOLTAGE_DIM_KW | PRESSURE_DIM_KW | COUNT_DIM_KW | ENERGY_KW
    ;

customModesBlock
    : CUSTOM_MODES_KW LBRACE (ID SEMI)* RBRACE SEMI
    ;

// ── Hardware Declarations (UNIFIED BLOCK SYNTAX) ──────────────────
sensorDecl
    : SENSOR_KW ID LBRACE sensorField (fieldSep sensorField)* RBRACE SEMI
    ;
sensorField
    : TYPE_KW      COLON varType
    | RANGE_KW     COLON rangeSpec
    | ADDRESS_KW   COLON REGISTER
    | HEALTH_KW    LBRACE healthRule (fieldSep healthRule)* RBRACE
    ;

actuatorDecl
    : ACTUATOR_KW ID LBRACE actuatorField (fieldSep actuatorField)* RBRACE SEMI
    ;
actuatorField
    : TYPE_KW    COLON varType
    | RANGE_KW   COLON rangeSpec
    | ADDRESS_KW COLON REGISTER
    ;

// ── Internal Variables & Constants ────────────────────────────────
varDecl   : VAR_KW   ID COLON varType ASSIGN expr SEMI ;
constDecl : CONST_KW ID COLON varType ASSIGN expr SEMI ;

varType
    : BOOL_T
    | INT_T
    | FLOAT_T
    | unitType
    | varType LBRACKET NUMBER RBRACKET // Static array support
    ;

rangeSpec : LBRACKET NUMBER DOTDOT NUMBER RBRACKET ;

// ── Procedures (Reusable Logic) ───────────────────────────────────
procedureDef
    : PROC_KW ID LPAREN paramList? RPAREN (RETURNS_KW varType)? LBRACE statement* RBRACE
    ;
paramList : param (COMMA param)* ;
param     : ID COLON varType ;

// ── Operating Modes & Rules (IEC 62443 Safety) ────────────────────
modeBlock
    : MODE_KW modeName LBRACE onStartBlock? ruleBlock* RBRACE
    ;
modeName
    : STARTUP_KW
    | RUN_KW        // CONFLICT RESOLVED: Context distinguishes from actuatorValue
    | MAINTENANCE_KW
    | EMERGENCY_KW
    | ID
    ;

onStartBlock : ON_START_KW LBRACE statement* RBRACE ;

ruleBlock
    : RULE_KW ID LBRACE localDecl* conditionClause actionClause RBRACE
    ;
localDecl       : sensorDecl | varDecl | constDecl ;
conditionClause : CONDITION_KW COLON condition SEMI ;
actionClause    : EXECUTE_KW LBRACE statement* RBRACE ;

// ── Statements ────────────────────────────────────────────────────
statement
    : commandStmt
    | alertStmt
    | logStmt
    | execProcStmt
    | gotoStmt
    | waitStmt
    | assignStmt
    | ifStmt
    | whileStmt
    | returnStmt
    | defaultValStmt
    | exprStmt
    ;

commandStmt   : CMD_KW ID COLON actuatorValue SEMI ;
actuatorValue : RUN_KW | OFF_KW | OPEN_KW | CLOSED_KW | ACTIVE_KW | INACTIVE_KW | expr ;

alertStmt     : ALERT_KW alertLevel STRING_LIT SEMI ;
alertLevel    : LEVEL_1 | LEVEL_2 | LEVEL_3 ;

logStmt       : LOG_KW STRING_LIT SEMI ;
execProcStmt  : EXEC_KW PROC_KW ID LPAREN argList? RPAREN SEMI ;
gotoStmt      : GOTO_KW modeName SEMI ;
waitStmt      : WAIT_KW duration SEMI ;
assignStmt    : ID (LBRACKET expr RBRACKET)? ASSIGN expr SEMI ;
defaultValStmt: DEFAULT_VAL_KW COLON NUMBER SEMI ;
exprStmt      : expr SEMI ;

// MANDATORY BRACES: Eliminates Dangling Else ambiguity entirely.
ifStmt
    : IF_KW LPAREN condition RPAREN LBRACE statement* RBRACE 
      (ELSE_KW LBRACE statement* RBRACE)?
    ;

whileStmt
    : WHILE_KW LPAREN condition RPAREN LBRACE statement* RBRACE
    ;

returnStmt : RETURN_KW expr? SEMI ;

// ── Conditions (Boolean Logic with Strict Precedence) ─────────────
condition
    : condition AO orOperand             # OrExpr
    | orOperand                          # OrPass
    ;

orOperand
    : orOperand WA andOperand            # AndExpr
    | andOperand                         # AndPass
    ;

andOperand
    : LIS andOperand                     # NotExpr
    | primaryCondition                   # PrimaryPass
    ;

primaryCondition
    : LPAREN condition RPAREN            # ParenCond
    | expr compOp expr                   # CompExpr
    | WHILE_CONT_KW LPAREN condition LMDA COLON duration RPAREN # TemporalExpr
    | VOTE_KW LPAREN NUMBER FROM_KW NUMBER COLON comparisonList RPAREN # VotingExpr
    | SAH                                # TrueLit
    | KHTA                               # FalseLit
    | ID                                 # BoolVar
    ;

comparisonList : comparison (COMMA comparison)* ;
comparison     : expr compOp expr ;
compOp         : GT | LT | GTE | LTE | EQ | NEQ ;

// ── Expressions (Arithmetic with Strict Precedence) ───────────────
expr
    : expr op=(MUL | DIV | MOD) expr     # MulDivExpr
    | expr op=(PLUS | MINUS) expr        # AddSubExpr
    | MINUS expr                         # UnaryMinusExpr
    | LPAREN expr RPAREN                 # ParenExpr
    | aggregateExpr                      # AggExpr
    | EXEC_KW PROC_KW ID LPAREN argList? RPAREN # ProcCallExpr
    | NUMBER                             # NumLit
    | STRING_LIT                         # StrLit
    | ID (LBRACKET expr RBRACKET)?       # VarOrArrayExpr
    ;

aggregateExpr : aggFunc LPAREN ID DURING_KW COLON duration RPAREN ;
aggFunc       : AVG_KW | MAX_KW | MIN_KW | SUM_KW | RATE_KW | LAST_KW ;
argList       : expr (COMMA expr)* ;

// ── Sensor Health Rules (Enhancement) ─────────────────────────────
healthRule
    : ON_DISCONNECT_KW LBRACE statement* RBRACE
    | ON_STUCK_KW LPAREN DURATION_KW COLON duration RPAREN LBRACE statement* RBRACE
    | ON_OUT_RANGE_KW LBRACE statement* RBRACE
    ;

// ── Escalation Chains (ISA-18.2) ──────────────────────────────────
escalationDef
    : ESCALATION_KW ID LBRACE escalationLevel+ RBRACE
    ;
escalationLevel
    : (LEVEL_1 | LEVEL_2 | LEVEL_3 | LEVEL_N) LBRACE escalationField* RBRACE
    ;
escalationField
    : MESSAGE_KW    COLON STRING_LIT SEMI
    | RECEIVER_KW   COLON STRING_LIT SEMI
    | TIMEOUT_KW    COLON duration SEMI
    | IF_NO_RESP_KW COLON escalationAction
    ;
escalationAction
    : GOTO_KW (LEVEL_1 | LEVEL_2 | LEVEL_3 | LEVEL_N) SEMI
    | EXEC_PROC_KW ID LPAREN argList? RPAREN SEMI
    ;

// ── Native Reports ────────────────────────────────────────────────
reportDef
    : REPORT_KW ID LBRACE reportField* reportContent RBRACE
    ;
reportField
    : SCHEDULE_KW COLON scheduleSpec SEMI
    | FORMAT_KW   COLON formatName SEMI
    | SAVE_IN_KW  COLON STRING_LIT SEMI
    | TYPE_KW     COLON IMMEDIATE_KW SEMI
    ;
scheduleSpec
    : DAILY_KW  AT_TIME_KW STRING_LIT
    | WEEKLY_KW DAY_KW STRING_LIT AT_TIME_KW STRING_LIT // DAY_KW resolved by context
    ;
formatName : JSON_FMT | CSV_FMT ;

reportContent
    : CONTENT_KW LBRACE reportItem* RBRACE
    ;
reportItem
    : aggFunc LPAREN ID DURING_KW COLON duration RPAREN AS_TITLE_KW STRING_LIT SEMI
    | INSTANT_VAL_KW LPAREN ID RPAREN AS_TITLE_KW STRING_LIT SEMI
    | ALERT_COUNT_KW DURING_KW COLON duration AS_TITLE_KW STRING_LIT SEMI
    | UPTIME_KW DURING_KW COLON duration AS_TITLE_KW STRING_LIT SEMI
    | CURRENT_MODE_KW AS_TITLE_KW STRING_LIT SEMI
    | TIMESTAMP_KW AS_TITLE_KW STRING_LIT SEMI
    ;

// ── Transition Table ──────────────────────────────────────────────
transitionTable
    : TRANSITIONS_KW LBRACE transitionRule* RBRACE
    ;
transitionRule : FROM_KW modeName TO_KW modeName SEMI ;

// ── Duration & Units ──────────────────────────────────────────────
duration   : NUMBER timeSuffix ;
timeSuffix : SECOND_KW | MINUTE_KW | HOUR_KW | DAY_KW | MILLI_SEC_KW ;

unitType
    : CELSIUS_U | BAR_U | PASCAL_U | VOLT_U | AMPERE_U
    | RPM_U | LPM_U | PERCENT_U | METER_U | NTU_U | NO_UNIT_U
    | BAR_S_U | CELSIUS_S_U
    | ID // Custom units
    ;

// Flexible separator for block fields (accepts ;, ؛, ,, or ،)
fieldSep : SEMI | COMMA ;


// =====================================================================
// LEXER RULES (Uppercase)
// ORDER IS CRITICAL: Multi-char operators first, then keywords, then ID.
// =====================================================================

// ── Structure & Configuration ───────────────────────────────────────
BARNMJ          : 'برنامج' ;
JHAZ            : 'جهاز' ;
CUSTOM_UNITS_KW : 'وحدات_مخصصة' ;
CUSTOM_MODES_KW : 'اوضاع_مخصصة' ;
TYPE_KW         : 'نوع' ;
OS_KW           : 'نظام' ;
PROTOCOL_KW     : 'بروتوكول' ;
IP_KW           : 'عنوان_ip' ;
PORT_KW         : 'منفذ' ;
SERIAL_PORT_KW  : 'منفذ_تسلسلي' ;
SCAN_CYCLE_KW   : 'دورة_مسح' ;
RANGE_KW        : 'نطاق' ;
ADDRESS_KW      : 'عنوان' ;

// ── Declarations ────────────────────────────────────────────────────
SENSOR_KW       : 'حساس' ;
ACTUATOR_KW     : 'مشغل' ;
VAR_KW          : 'متغير' ;
CONST_KW        : 'ثابت' ;
PROC_KW         : 'اجراء' ;
RETURNS_KW      : 'يرجع' ;
RETURN_KW       : 'ارجع' ;

// ── Types (Using the | operator for clean aliases) ──────────────────
BOOL_T          : 'منطقي' ;
INT_T           : 'صحيح' | 'عدد_صحيح' ;       // ALIASES: One token, two valid strings
FLOAT_T         : 'حقيقي' | 'عدد_حقيقي' ;     // ALIASES: One token, two valid strings

// ── Boolean Literals ────────────────────────────────────────────────
SAH             : 'صح' ;
KHTA            : 'خطا' ;

// ── Modes ───────────────────────────────────────────────────────────
STARTUP_KW      : 'اقلاع' ;
RUN_KW          : 'تشغيل' ;       // CONFLICT RESOLVED: Context (modeName vs actuatorValue)
MAINTENANCE_KW  : 'صيانة' ;
EMERGENCY_KW    : 'طوارئ' ;
MODE_KW         : 'وضع' ;
RULE_KW         : 'قاعدة' ;
CONDITION_KW    : 'شرط' ;
EXECUTE_KW      : 'تنفيذ' ;
ON_START_KW     : 'عند_بدء' ;

// ── Actions & Statements ────────────────────────────────────────────
CMD_KW          : 'امر' ;
ALERT_KW        : 'تنبيه' ;
LEVEL_1         : 'مستوى_1' ;     // MUST be before LEVEL_N
LEVEL_2         : 'مستوى_2' ;
LEVEL_3         : 'مستوى_3' ;
LEVEL_N         : 'مستوى_' [0-9]+ ;
LOG_KW          : 'سجل_حادثة' ;
EXEC_KW         : 'نفذ' ;
GOTO_KW         : 'انتقل_الى' ;
WAIT_KW         : 'انتظر' ;
IF_KW           : 'اذا' ;
ELSE_KW         : 'والا' ;
WHILE_KW        : 'طالما' ;
DEFAULT_VAL_KW  : 'استخدم_قيمة_افتراضية' ;

// ── Actuator Values ─────────────────────────────────────────────────
OFF_KW          : 'ايقاف' ;
OPEN_KW         : 'مفتوح' ;
CLOSED_KW       : 'مغلق' ;
ACTIVE_KW       : 'نشط' ;
INACTIVE_KW     : 'غير_نشط' ;

// ── Logical Operators ───────────────────────────────────────────────
WA              : 'و' ;
AO              : 'او' ;
LIS             : 'ليس' ;

// ── Temporal, Voting, Aggregates ────────────────────────────────────
WHILE_CONT_KW   : 'عند_استمرار' ;
LMDA            : 'لمدة' ;
VOTE_KW         : 'تصويت' ;
FROM_KW         : 'من' ;
AVG_KW          : 'متوسط' ;
MAX_KW          : 'اقصى' ;
MIN_KW          : 'ادنى' ;
SUM_KW          : 'مجموع' ;
RATE_KW         : 'معدل_التغيير' ;
LAST_KW         : 'اخر' ;
DURING_KW       : 'خلال' ;

// ── Sensor Health ───────────────────────────────────────────────────
HEALTH_KW       : 'صحة' ;
ON_DISCONNECT_KW: 'عند_انقطاع_الاتصال' ;
ON_STUCK_KW     : 'عند_قيمة_ثابتة' ;
ON_OUT_RANGE_KW : 'عند_خروج_عن_النطاق' ;
DURATION_KW     : 'مدة' ;

// ── Escalation ──────────────────────────────────────────────────────
ESCALATION_KW   : 'تصعيد' ;
MESSAGE_KW      : 'رسالة' ;
RECEIVER_KW     : 'مستلم' ;
TIMEOUT_KW      : 'مهلة' ;
IF_NO_RESP_KW   : 'اذا_لم_يستجب_خلال_المهلة' ;
EXEC_PROC_KW    : 'نفذ_اجراء' ;
TRANSITIONS_KW  : 'انتقالات' ;
TO_KW           : 'الى' ;

// ── Reports ─────────────────────────────────────────────────────────
REPORT_KW       : 'تقرير' ;
SCHEDULE_KW     : 'جدول' ;
FORMAT_KW       : 'تنسيق' ;
SAVE_IN_KW      : 'حفظ_في' ;
IMMEDIATE_KW    : 'فوري' ;
DAILY_KW        : 'كل_يوم' ;
WEEKLY_KW       : 'كل_اسبوع' ;
DAY_KW          : 'يوم' ;          // CONFLICT RESOLVED: Context (timeSuffix vs scheduleSpec)
AT_TIME_KW      : 'الساعة' ;
CONTENT_KW      : 'محتوى' ;
AS_TITLE_KW     : 'بعنوان' ;
INSTANT_VAL_KW  : 'قيمة_لحظية' ;
ALERT_COUNT_KW  : 'عدد_التنبيهات_خلال' ;
UPTIME_KW       : 'وقت_التشغيل_الفعلي' ;
CURRENT_MODE_KW : 'الوضع_الحالي' ;
TIMESTAMP_KW    : 'طابع_زمني' ;
JSON_FMT        : 'json' ;
CSV_FMT         : 'csv' ;

// ── Base Dimensions ─────────────────────────────────────────────────
MASS_KW         : 'كتلة' ;
VOLUME_KW       : 'حجم' ;
TIME_DIM_KW     : 'زمن' ;
LENGTH_KW       : 'طول' ;
TEMP_DIM_KW     : 'درجة_حرارة' ;
CURRENT_DIM_KW  : 'تيار' ;
VOLTAGE_DIM_KW  : 'جهد' ;
PRESSURE_DIM_KW : 'ضغط' ;
COUNT_DIM_KW    : 'عدد' ;
ENERGY_KW       : 'طاقة' ;

// ── Time Units ──────────────────────────────────────────────────────
SECOND_KW       : 'ثانية' ;
MINUTE_KW       : 'دقيقة' ;
HOUR_KW         : 'ساعة' ;
MILLI_SEC_KW    : 'مللي_ثانية' ;

// ── Physical Units ──────────────────────────────────────────────────
CELSIUS_U       : 'سيلزيوس' ;
BAR_U           : 'بار' ;
PASCAL_U        : 'باسكال' ;
VOLT_U          : 'فولت' ;
AMPERE_U        : 'امبير' ;
RPM_U           : 'دورة_في_الدقيقة' ;
LPM_U           : 'لتر_في_الدقيقة' ;
PERCENT_U       : 'بالمئة' ;
METER_U         : 'متر' ;
NTU_U           : 'NTU' ;
NO_UNIT_U       : 'لا_وحدة' ;
BAR_S_U         : 'بار_في_الثانية' ;
CELSIUS_S_U     : 'سيلزيوس_في_الثانية' ;

// ── Operators (STRICT ORDER: Multi-char before Single-char) ─────────
EQ              : '==' ;     // BEFORE ASSIGN
NEQ             : '!=' ;
GTE             : '>=' ;     // BEFORE GT
LTE             : '<=' ;     // BEFORE LT
GT              : '>' ;
LT              : '<' ;
ASSIGN          : '=' ;
PLUS            : '+' ;
MINUS           : '-' ;
MUL             : '*' ;
DIV             : '/' ;
MOD             : '%' ;

// ── Punctuation (FLEXIBILITY: Arabic and English interchangeable) ───
LPAREN          : '(' ;
RPAREN          : ')' ;
LBRACE          : '{' ;
RBRACE          : '}' ;
LBRACKET        : '[' ;
RBRACKET        : ']' ;
COLON           : ':' ;
SEMI            : '؛' | ';' ;      // Arabic OR English semicolon (Statement terminator)
COMMA           : '،' | ',' ;      // Arabic OR English comma (List separator)
DOTDOT          : '..' ;

// ── Literals & Identifiers ──────────────────────────────────────────
STRING_LIT      : '"' ~["\r\n]* '"' ;
fragment DIGIT  : [0-9] | [\u0660-\u0669] ;
NUMBER          : DIGIT+ ('.' DIGIT+)? ;
REGISTER        : '0x' [0-9A-Fa-f]+ ;

// ID MUST BE LAST. It catches anything not matched by the keywords above.
ID              : [\u0621-\u064A_A-Za-z] [\u0621-\u064A_A-Za-z\u0660-\u06690-9]* ;

// ── Whitespace & Comments ───────────────────────────────────────────
WS              : [ \t\r\n\u00A0\u200F\u200E]+ -> skip ;
LINE_COMMENT    : '//' ~[\r\n]* -> skip ;
BLOCK_COMMENT   : '/*' .*? '*/' -> skip ;