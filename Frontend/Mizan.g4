// =====================================================================
// MIZAN GRAMMAR v1.6 (Predictive Maintenance & Enterprise SCADA)
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

deviceBlock
    : JHAZ ID LBRACE deviceField (COMMA deviceField)* COMMA? RBRACE SEMI
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
    : CUSTOM_UNITS_KW LBRACE customUnitDef (COMMA customUnitDef)* COMMA? RBRACE SEMI
    ;

// ✅ PURE CONCRETE: Only real-world units allowed!
customUnitDef : ID COLON unitExpr ;

unitExpr
    : unitExpr op=(MUL | DIV) unitTerm  # UnitMathExpr   // e.g., لتر / دقيقة
    | unitTerm                          # UnitPass       // e.g., لتر (Alias)
    ;

// ✅ SIMPLIFIED: No more baseDim! Just concrete units or parentheses.
unitTerm
    : unitType                          # UnitBase       
    | LPAREN unitExpr RPAREN            # UnitParen      
    ;

customModesBlock
    : CUSTOM_MODES_KW LBRACE (ID (COMMA ID)* COMMA?)? RBRACE SEMI
    ;

// ── Hardware Declarations (UNIFIED BLOCK SYNTAX) ──────────────────
sensorDecl
    : SENSOR_KW ID LBRACE sensorField (COMMA sensorField)* COMMA? RBRACE SEMI
    ;
sensorField
    : TYPE_KW      COLON varType
    | RANGE_KW     COLON rangeSpec
    | ADDRESS_KW   COLON REGISTER
    | HEALTH_KW    LBRACE (healthRule (COMMA healthRule)* COMMA?)? RBRACE
    ;

actuatorDecl
    : ACTUATOR_KW ID LBRACE actuatorField (COMMA actuatorField)* COMMA? RBRACE SEMI
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
    | RUN_KW        
    | MAINTENANCE_KW
    | EMERGENCY_KW
    | ID
    ;

onStartBlock : ON_START_KW LBRACE statement* RBRACE ;

ruleBlock
    : RULE_KW ID LBRACE localDecl* statement* RBRACE
    ;
localDecl       : sensorDecl | varDecl | constDecl ;

// ── Statements ────────────────────────────────────────────────────
statement
    : commandStmt
    | alertStmt
    | logStmt
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

gotoStmt      : GOTO_KW modeName SEMI ;
waitStmt      : WAIT_KW duration SEMI ;
assignStmt    : ID (LBRACKET expr RBRACKET)? ASSIGN expr SEMI ;

defaultValStmt: DEFAULT_VAL_KW COLON NUMBER SEMI ;

exprStmt      : expr SEMI ;

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
// ── Expressions (Arithmetic with Strict Precedence) ───────────────
expr
    : expr op=(MUL | DIV | MOD) expr     # MulDivExpr
    | expr op=(PLUS | MINUS) expr        # AddSubExpr
    | MINUS expr                         # UnaryMinusExpr
    | LPAREN expr RPAREN                 # ParenExpr
    | aggregateExpr                      # AggExpr
    | ID LPAREN argList? RPAREN          # ProcCallExpr
    | NUMBER                             # NumLit
    | STRING_LIT                         # StrLit
    | ID (LBRACKET expr RBRACKET)?       # VarOrArrayExpr
    | SAH                                # BoolTrueExpr    // ✅ NEW
    | KHTA                               # BoolFalseExpr   // ✅ NEW
    ;

aggregateExpr : aggFunc LPAREN ID LMDA COLON duration RPAREN ;
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
    : ESCALATION_KW ID LBRACE escalationLevel (COMMA escalationLevel)* COMMA? RBRACE SEMI
    ;
escalationLevel
    : (LEVEL_1 | LEVEL_2 | LEVEL_3 | LEVEL_N) LBRACE (escalationField (COMMA escalationField)* COMMA?)? RBRACE
    ;
escalationField
    : MESSAGE_KW    COLON STRING_LIT
    | RECEIVER_KW   COLON STRING_LIT
    | TIMEOUT_KW    COLON duration
    | ON_TIMEOUT_KW COLON escalationAction
    ;
escalationAction
    : GOTO_KW (LEVEL_1 | LEVEL_2 | LEVEL_3 | LEVEL_N)
    | ID LPAREN argList? RPAREN
    ;

// ── Native Reports ────────────────────────────────────────────────
reportDef
    : REPORT_KW ID LBRACE (reportField (COMMA reportField)* COMMA?)? reportContent RBRACE SEMI
    ;
reportField
    : SCHEDULE_KW COLON scheduleSpec
    | FORMAT_KW   COLON formatName
    | SAVE_IN_KW  COLON STRING_LIT
    | TYPE_KW     COLON IMMEDIATE_KW
    ;

// ✅ ENTERPRISE SCADA STANDARD SCHEDULING
scheduleSpec
    : EVERY_KW duration                                                # IntervalSchedule
    | DAILY_KW  AT_TIME_KW STRING_LIT                                  # DailySchedule
    | WEEKLY_KW DAY_KW STRING_LIT AT_TIME_KW STRING_LIT                # WeeklySchedule
    | MONTHLY_KW (DAY_KW NUMBER | LAST_DAY_KW) AT_TIME_KW STRING_LIT   # MonthlySchedule
    ;

formatName : JSON_FMT | CSV_FMT ;

reportContent
    : CONTENT_KW LBRACE (reportItem (COMMA reportItem)* COMMA?)? RBRACE
    ;

// ✅ PREDICTIVE MAINTENANCE & HEALTH REPORTING
reportItem
    : aggFunc LPAREN ID LMDA COLON duration RPAREN AS_TITLE_KW STRING_LIT
    | INSTANT_VAL_KW LPAREN ID RPAREN AS_TITLE_KW STRING_LIT
    | ALERT_COUNT_KW LMDA COLON duration AS_TITLE_KW STRING_LIT
    | UPTIME_KW LMDA COLON duration AS_TITLE_KW STRING_LIT
    | CURRENT_MODE_KW AS_TITLE_KW STRING_LIT
    | TIMESTAMP_KW AS_TITLE_KW STRING_LIT
    // ✅ NEW: Actuator Cycles (Predictive Maintenance)
    | CYCLE_COUNT_KW LPAREN ID RPAREN AS_TITLE_KW STRING_LIT
    // ✅ NEW: Actuator State (Current ON/OFF status)
    | ACTUATOR_STATE_KW LPAREN ID RPAREN AS_TITLE_KW STRING_LIT
    // ✅ NEW: Sensor Health (OK/FAULT status)
    | SENSOR_HEALTH_KW LPAREN ID RPAREN AS_TITLE_KW STRING_LIT
    ;

// ── Transition Table ──────────────────────────────────────────────
transitionTable
    : TRANSITIONS_KW LBRACE transitionRule* RBRACE
    ;
transitionRule : FROM_KW modeName TO_KW modeName SEMI ;

// ── Duration & Units ──────────────────────────────────────────────
duration   : NUMBER timeSuffix ;
// ✅ EXPANDED: Added WEEK_KW and MONTH_KW for interval durations
timeSuffix : SECOND_KW | MINUTE_KW | HOUR_KW | DAY_KW | WEEK_KW | MONTH_KW | MILLI_SEC_KW ;

// ✅ THE CORE UNIT SYSTEM: Categorized for the Semantic Analyzer
unitType
    // 1. Fundamental Physical Base Atoms
    : METER_U | LITER_U | CUBIC_METER_U | KG_U | GRAM_U | TON_U
    | SECOND_KW | MINUTE_KW | HOUR_KW | DAY_KW | MILLI_SEC_KW
    | CELSIUS_U | DEGREE_U | RADIAN_U
    | BAR_U | PASCAL_U
    | VOLT_U | AMPERE_U | OHM_U | WATT_U | KWATT_U | JOULE_U
    | HERTZ_U | CYCLE_U | COUNT_U
    | LUX_U | SIEMENS_U | NTU_U | PPM_U
    | BIT_U | BYTE_U
    | PERCENT_U | NO_UNIT_U
    
    // 2. "Famous Mixes" (Pre-defined composite units for SCADA/PLC convenience)
    | RPM_U | RPS_U | LPM_U | LPH_U | CMH_U | MPS_U | MPM_U 
    | BAR_S_U | CELSIUS_S_U
    
    // 3. User-defined custom units
    | ID 
    ;


// =====================================================================
// LEXER RULES (Uppercase)
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

// ── Types ───────────────────────────────────────────────────────────
BOOL_T          : 'منطقي' ;
INT_T           : 'صحيح' | 'عدد_صحيح' ;
FLOAT_T         : 'حقيقي' | 'عدد_حقيقي' ;

// ── Boolean Literals ────────────────────────────────────────────────
SAH             : 'صح' ;
KHTA            : 'خطا' ;

// ── Modes ───────────────────────────────────────────────────────────
STARTUP_KW      : 'اقلاع' ;
RUN_KW          : 'تشغيل' ;
MAINTENANCE_KW  : 'صيانة' ;
EMERGENCY_KW    : 'طوارئ' ;
MODE_KW         : 'وضع' ;
RULE_KW         : 'قاعدة' ;
ON_START_KW     : 'عند_بدء' ;

// ── Actions & Statements ────────────────────────────────────────────
CMD_KW          : 'امر' ;
ALERT_KW        : 'تنبيه' ;
LEVEL_1         : 'مستوى_1' ;
LEVEL_2         : 'مستوى_2' ;
LEVEL_3         : 'مستوى_3' ;
LEVEL_N         : 'مستوى_' [0-9]+ ;
LOG_KW          : 'سجل' ;
GOTO_KW         : 'انتقل_الى' ;
WAIT_KW         : 'انتظر' ;
IF_KW           : 'اذا' ;
ELSE_KW         : 'والا' ;
WHILE_KW        : 'طالما' ;
DEFAULT_VAL_KW  : 'قيمة_افتراضية' ;

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
ON_TIMEOUT_KW   : 'عند_انتهاء_المهلة' ;
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
DAY_KW          : 'يوم' ;
AT_TIME_KW      : 'الساعة' ;
CONTENT_KW      : 'محتوى' ;
AS_TITLE_KW     : 'بعنوان' ;
INSTANT_VAL_KW  : 'قيمة_لحظية' ;
ALERT_COUNT_KW  : 'عدد_التنبيهات' ;
UPTIME_KW       : 'وقت_التشغيل_الفعلي' ;
CURRENT_MODE_KW : 'الوضع_الحالي' ;
TIMESTAMP_KW    : 'طابع_زمني' ;
JSON_FMT        : 'json' ;
CSV_FMT         : 'csv' ;

// ✅ NEW: Predictive Maintenance & Health Report Keywords
CYCLE_COUNT_KW    : 'عدد_تشغيلات' ;
ACTUATOR_STATE_KW : 'حالة_مشغل' ;
SENSOR_HEALTH_KW  : 'حالة_صحة' ;

// ✅ NEW: Scheduling Modifiers
EVERY_KW        : 'كل' ;
MONTHLY_KW      : 'كل_شهر' ;
LAST_DAY_KW     : 'اخر_يوم' ;
WEEK_KW         : 'اسبوع' ;
MONTH_KW        : 'شهر' ;

// ── Time Units ──────────────────────────────────────────────────────
SECOND_KW       : 'ثانية' ;
MINUTE_KW       : 'دقيقة' ;
HOUR_KW         : 'ساعة' ;
MILLI_SEC_KW    : 'مللي_ثانية' ;

// ── Physical Units (Base Atoms) ─────────────────────────────────────
CELSIUS_U       : 'سيلزيوس' ;
BAR_U           : 'بار' ;
PASCAL_U        : 'باسكال' ;
VOLT_U          : 'فولت' ;
AMPERE_U        : 'امبير' ;
OHM_U           : 'أوم' ;       // ✅ Crucial for RTD sensors
PERCENT_U       : 'بالمئة' ;
METER_U         : 'متر' ;
NTU_U           : 'NTU' ;
NO_UNIT_U       : 'لا_وحدة' ;
LUX_U           : 'لوكس' ;      // ✅ Crucial for lighting
DEGREE_U        : 'درجة' ;      // ✅ Crucial for valve positioning
RADIAN_U        : 'راديان' ;
SIEMENS_U       : 'سيمنز' ;     // ✅ Crucial for water conductivity
PPM_U           : 'جزء_في_المليون' ; // ✅ Crucial for chlorine/ozone
BIT_U           : 'بت' ;
BYTE_U          : 'بايت' ;

// ✅ Fully Decoupled Base Atoms
LITER_U         : 'لتر' ;
CUBIC_METER_U   : 'متر_مكعب' ;
KG_U            : 'كيلوجرام' ;
GRAM_U          : 'جرام' ;
TON_U           : 'طن' ;
WATT_U          : 'واط' ;
KWATT_U         : 'كيلو_واط' ;
JOULE_U         : 'جول' ;
HERTZ_U         : 'هرتز' ;
COUNT_U         : 'عدد' ;
CYCLE_U         : 'دورة' ;

// ✅ "Famous Mixes" (Longest match first for safety)
LPH_U           : 'لتر_في_الساعة' ;
CMH_U           : 'متر_مكعب_في_الساعة' ;
MPS_U           : 'متر_في_الثانية' ;
MPM_U           : 'متر_في_الدقيقة' ;
RPM_U           : 'دورة_في_الدقيقة' ;
RPS_U           : 'دورة_في_الثانية' ;
LPM_U           : 'لتر_في_الدقيقة' ;
BAR_S_U         : 'بار_في_الثانية' ;
CELSIUS_S_U     : 'سيلزيوس_في_الثانية' ;

// ── Operators ───────────────────────────────────────────────────────
EQ              : '==' ;
NEQ             : '!=' ;
GTE             : '>=' ;
LTE             : '<=' ;
GT              : '>' ;
LT              : '<' ;
ASSIGN          : '=' ;
PLUS            : '+' ;
MINUS           : '-' ;
MUL             : '*' ;
DIV             : '/' ;
MOD             : '%' ;

// ── Punctuation ─────────────────────────────────────────────────────
LPAREN          : '(' ;
RPAREN          : ')' ;
LBRACE          : '{' ;
RBRACE          : '}' ;
LBRACKET        : '[' ;
RBRACKET        : ']' ;
COLON           : ':' ;
SEMI            : '؛' | ';' ;
COMMA           : '،' | ',' ;
DOTDOT          : '..' ;

// ── Literals & Identifiers ──────────────────────────────────────────
STRING_LIT      : '"' ~["\r\n]* '"' ;
fragment DIGIT  : [0-9] | [\u0660-\u0669] ;
NUMBER          : DIGIT+ ('.' DIGIT+)? ;
REGISTER        : '0x' [0-9A-Fa-f]+ ;
ID              : [\u0621-\u064A_A-Za-z] [\u0621-\u064A_A-Za-z\u0660-\u06690-9]* ;

// ── Whitespace & Comments ───────────────────────────────────────────
WS              : [ \t\r\n\u00A0\u200F\u200E]+ -> skip ;
LINE_COMMENT    : '//' ~[\r\n]* -> skip ;
BLOCK_COMMENT   : '/*' .*? '*/' -> skip ;