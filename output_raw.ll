; ModuleID = "mizan_program"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare void @"setup_arabic_console"()

declare void @"print_arabic"(i8* %".1")

declare void @"mizan_log"(i8* %".1")

declare void @"mizan_alert"(i32 %".1", i8* %".2")

declare void @"panic_div_zero"()

declare i8* @"mizan_modbus_connect"(i8* %".1", i32 %".2")

declare double @"mizan_modbus_read"(i8* %".1", i32 %".2")

declare void @"mizan_modbus_write"(i8* %".1", i32 %".2", double %".3")

declare i32 @"mizan_modbus_is_connected"(i8* %".1")

declare i8* @"mizan_mqtt_connect"(i8* %".1", i32 %".2", i8* %".3")

declare void @"mizan_mqtt_publish"(i8* %".1", i8* %".2", i8* %".3")

declare void @"__mizan_set_mqtt_ctx"(i8* %".1")

declare i64 @"mizan_now_ms"()

declare void @"mizan_sleep_ms"(i64 %".1")

declare void @"mizan_ring_push"(i32 %".1", double %".2")

declare double @"mizan_ring_avg"(i32 %".1", i64 %".2")

declare double @"mizan_ring_max"(i32 %".1", i64 %".2")

declare double @"mizan_ring_min"(i32 %".1", i64 %".2")

declare double @"mizan_ring_sum"(i32 %".1", i64 %".2")

declare double @"mizan_ring_rate"(i32 %".1", i64 %".2")

declare double @"mizan_ring_last"(i32 %".1")

declare i64 @"mizan_health_track_stuck"(i32 %".1", double %".2", i64 %".3")

declare i32 @"mizan_health_out_of_range"(double %".1", double %".2", double %".3")

declare void @"mizan_escalation_tick"()

declare void @"mizan_escalation_arm"(i32 %".1", i32 %".2", i64 %".3", i8* %".4", i8* %".5")

declare void @"mizan_report_write"(i8* %".1", i8* %".2", i8* %".3", i8* %".4")

declare i32 @"printf"(i8* %".1", ...)

declare i32 @"snprintf"(i8* %".1", i64 %".2", i8* %".3", ...)

@"s_درجة_الحرارة" = internal global double 0.0
@"s_درجة_الحرارة_conn" = internal global i32 1
@"s_الضغط" = internal global double 0.0
@"s_الضغط_conn" = internal global i32 1
@"a_صمام_التبريد" = internal global double 0.0
@"a_منبه_الانذار" = internal global double 0.0
@"g_عداد_التنبيهات" = internal global i32 0
@"__modbus_ctx" = internal global i8* null
@"__mqtt_ctx" = internal global i8* null
@"__current_mode" = internal global i32 0
@"__pending_goto" = internal global i32 -1
@"__wq_addrs" = internal global [64 x i32] [i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0]
@"__wq_values" = internal global [64 x double] [double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0]
@"__wq_count" = internal global i32 0
@"__rpt_buf" = internal global [2048 x i8] c"\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00"
define void @"proc_تسجيل_تنبيه"()
{
entry:
  %"عداد_التنبيهات" = load i32, i32* @"g_عداد_التنبيهات"
  %"add" = add i32 %"عداد_التنبيهات", 1
  store i32 %"add", i32* @"g_عداد_التنبيهات"
  %".3" = bitcast [45 x i8]* @"__log_1" to i8*
  call void @"mizan_log"(i8* %".3")
  ret void
}

@"__log_1" = private constant [45 x i8] c"[\d8\b3\d8\ac\d9\84] \d8\aa\d9\85 \d8\aa\d8\b3\d8\ac\d9\8a\d9\84 \d8\aa\d9\86\d8\a8\d9\8a\d9\87 \d8\ac\d8\af\d9\8a\d8\af\00"
define i32 @"main"()
{
entry:
  call void @"setup_arabic_console"()
  %".3" = bitcast [10 x i8]* @"__dev_ip_2" to i8*
  %".4" = call i8* @"mizan_modbus_connect"(i8* %".3", i32 5020)
  store i8* %".4", i8** @"__modbus_ctx"
  %".6" = bitcast [10 x i8]* @"__mq_host_3" to i8*
  %".7" = bitcast [14 x i8]* @"__mq_cid_4" to i8*
  %".8" = call i8* @"mizan_mqtt_connect"(i8* %".6", i32 1883, i8* %".7")
  store i8* %".8", i8** @"__mqtt_ctx"
  call void @"__mizan_set_mqtt_ctx"(i8* %".8")
  store i32 0, i32* @"g_عداد_التنبيهات"
  store i32 0, i32* @"__current_mode"
  %".13" = bitcast [49 x i8]* @"__log_5" to i8*
  call void @"mizan_log"(i8* %".13")
  store double              0x0, double* @"a_صمام_التبريد"
  %"wqc" = load i32, i32* @"__wq_count"
  %".16" = icmp slt i32 %"wqc", 64
  br i1 %".16", label %"entry.if", label %"entry.endif"
entry.if:
  %".18" = getelementptr inbounds [64 x i32], [64 x i32]* @"__wq_addrs", i32 0, i32 %"wqc"
  %".19" = getelementptr inbounds [64 x double], [64 x double]* @"__wq_values", i32 0, i32 %"wqc"
  store i32 32, i32* %".18"
  store double              0x0, double* %".19"
  %".22" = add i32 %"wqc", 1
  store i32 %".22", i32* @"__wq_count"
  br label %"entry.endif"
entry.endif:
  store double              0x0, double* @"a_منبه_الانذار"
  %"wqc.1" = load i32, i32* @"__wq_count"
  %".26" = icmp slt i32 %"wqc.1", 64
  br i1 %".26", label %"entry.endif.if", label %"entry.endif.endif"
entry.endif.if:
  %".28" = getelementptr inbounds [64 x i32], [64 x i32]* @"__wq_addrs", i32 0, i32 %"wqc.1"
  %".29" = getelementptr inbounds [64 x double], [64 x double]* @"__wq_values", i32 0, i32 %"wqc.1"
  store i32 34, i32* %".28"
  store double              0x0, double* %".29"
  %".32" = add i32 %"wqc.1", 1
  store i32 %".32", i32* @"__wq_count"
  br label %"entry.endif.endif"
entry.endif.endif:
  store i32 1, i32* @"__pending_goto"
  br label %"scan_cycle"
scan_cycle:
  %"cycle_start" = call i64 @"mizan_now_ms"()
  %"mb" = load i8*, i8** @"__modbus_ctx"
  %"raw_درجة_الحرارة" = call double @"mizan_modbus_read"(i8* %"mb", i32 8)
  store double %"raw_درجة_الحرارة", double* @"s_درجة_الحرارة"
  call void @"mizan_ring_push"(i32 0, double %"raw_درجة_الحرارة")
  %"conn_درجة_الحرارة" = call i32 @"mizan_modbus_is_connected"(i8* %"mb")
  store i32 %"conn_درجة_الحرارة", i32* @"s_درجة_الحرارة_conn"
  %".40" = icmp eq i32 %"conn_درجة_الحرارة", 0
  br i1 %".40", label %"scan_cycle.if", label %"scan_cycle.endif"
scan_cycle.if:
  %".42" = bitcast [61 x i8]* @"__alert_6" to i8*
  call void @"mizan_alert"(i32 2, i8* %".42")
  br label %"scan_cycle.endif"
scan_cycle.endif:
  %"stuck_ms" = call i64 @"mizan_health_track_stuck"(i32 0, double %"raw_درجة_الحرارة", i64 30000)
  %".45" = icmp sge i64 %"stuck_ms", 30000
  br i1 %".45", label %"scan_cycle.endif.if", label %"scan_cycle.endif.endif"
scan_cycle.endif.if:
  %".47" = bitcast [79 x i8]* @"__alert_7" to i8*
  call void @"mizan_alert"(i32 1, i8* %".47")
  br label %"scan_cycle.endif.endif"
scan_cycle.endif.endif:
  %"raw_الضغط" = call double @"mizan_modbus_read"(i8* %"mb", i32 2)
  store double %"raw_الضغط", double* @"s_الضغط"
  call void @"mizan_ring_push"(i32 1, double %"raw_الضغط")
  %"conn_الضغط" = call i32 @"mizan_modbus_is_connected"(i8* %"mb")
  store i32 %"conn_الضغط", i32* @"s_الضغط_conn"
  %"cur_mode" = load i32, i32* @"__current_mode"
  switch i32 %"cur_mode", label %"mode_default" [i32 0, label %"mode_m81440" i32 1, label %"mode_m92691" i32 2, label %"mode_m89999"]
mode_default:
  br label %"mode_end"
mode_end:
  %"flush_n" = load i32, i32* @"__wq_count"
  %"mb_out" = load i8*, i8** @"__modbus_ctx"
  %"fi" = alloca i32
  store i32 0, i32* %"fi"
  br label %"flush_cond"
mode_m81440:
  br label %"mode_end"
mode_m92691:
  %"درجة_الحرارة" = load double, double* @"s_درجة_الحرارة"
  %"fcmp" = fcmp ogt double %"درجة_الحرارة", 0x4055400000000000
  br i1 %"fcmp", label %"rule_m35350_then", label %"rule_m35350_end"
rule_m35350_then:
  store double 0x3ff0000000000000, double* @"a_صمام_التبريد"
  %"wqc.2" = load i32, i32* @"__wq_count"
  %".57" = icmp slt i32 %"wqc.2", 64
  br i1 %".57", label %"rule_m35350_then.if", label %"rule_m35350_then.endif"
rule_m35350_end:
  %"درجة_الحرارة.1" = load double, double* @"s_درجة_الحرارة"
  %"fcmp.1" = fcmp olt double %"درجة_الحرارة.1", 0x4051800000000000
  br i1 %"fcmp.1", label %"rule_m51337_then", label %"rule_m51337_end"
rule_m35350_then.if:
  %".59" = getelementptr inbounds [64 x i32], [64 x i32]* @"__wq_addrs", i32 0, i32 %"wqc.2"
  %".60" = getelementptr inbounds [64 x double], [64 x double]* @"__wq_values", i32 0, i32 %"wqc.2"
  store i32 32, i32* %".59"
  store double 0x3ff0000000000000, double* %".60"
  %".63" = add i32 %"wqc.2", 1
  store i32 %".63", i32* @"__wq_count"
  br label %"rule_m35350_then.endif"
rule_m35350_then.endif:
  %".66" = bitcast [52 x i8]* @"__alert_8" to i8*
  call void @"mizan_alert"(i32 1, i8* %".66")
  call void @"proc_تسجيل_تنبيه"()
  br label %"rule_m35350_end"
rule_m51337_then:
  store double              0x0, double* @"a_صمام_التبريد"
  %"wqc.3" = load i32, i32* @"__wq_count"
  %".72" = icmp slt i32 %"wqc.3", 64
  br i1 %".72", label %"rule_m51337_then.if", label %"rule_m51337_then.endif"
rule_m51337_end:
  %"درجة_الحرارة.2" = load double, double* @"s_درجة_الحرارة"
  %"fcmp.2" = fcmp ogt double %"درجة_الحرارة.2", 0x405e000000000000
  br i1 %"fcmp.2", label %"or_end", label %"or_rhs"
rule_m51337_then.if:
  %".74" = getelementptr inbounds [64 x i32], [64 x i32]* @"__wq_addrs", i32 0, i32 %"wqc.3"
  %".75" = getelementptr inbounds [64 x double], [64 x double]* @"__wq_values", i32 0, i32 %"wqc.3"
  store i32 32, i32* %".74"
  store double              0x0, double* %".75"
  %".78" = add i32 %"wqc.3", 1
  store i32 %".78", i32* @"__wq_count"
  br label %"rule_m51337_then.endif"
rule_m51337_then.endif:
  br label %"rule_m51337_end"
or_rhs:
  %"الضغط" = load double, double* @"s_الضغط"
  %"fcmp.3" = fcmp ogt double %"الضغط", 0x4022000000000000
  br label %"or_end"
or_end:
  %"or_res" = phi  i1 [1, %"rule_m51337_end"], [%"fcmp.3", %"or_rhs"]
  br i1 %"or_res", label %"rule_m310_then", label %"rule_m310_end"
rule_m310_then:
  store double 0x3ff0000000000000, double* @"a_منبه_الانذار"
  %"wqc.4" = load i32, i32* @"__wq_count"
  %".86" = icmp slt i32 %"wqc.4", 64
  br i1 %".86", label %"rule_m310_then.if", label %"rule_m310_then.endif"
rule_m310_end:
  %"درجة_الحرارة.3" = load double, double* @"s_درجة_الحرارة"
  %"fcmp.4" = fcmp ogt double %"درجة_الحرارة.3", 0x4056800000000000
  %"t_now" = call i64 @"mizan_now_ms"()
  %"sus_res" = alloca i1
  store i1 0, i1* %"sus_res"
  br i1 %"fcmp.4", label %"sus_true", label %"sus_false"
rule_m310_then.if:
  %".88" = getelementptr inbounds [64 x i32], [64 x i32]* @"__wq_addrs", i32 0, i32 %"wqc.4"
  %".89" = getelementptr inbounds [64 x double], [64 x double]* @"__wq_values", i32 0, i32 %"wqc.4"
  store i32 34, i32* %".88"
  store double 0x3ff0000000000000, double* %".89"
  %".92" = add i32 %"wqc.4", 1
  store i32 %".92", i32* @"__wq_count"
  br label %"rule_m310_then.endif"
rule_m310_then.endif:
  %".95" = bitcast [92 x i8]* @"__alert_9" to i8*
  call void @"mizan_alert"(i32 3, i8* %".95")
  store i32 2, i32* @"__pending_goto"
  br label %"rule_m310_end"
sus_true:
  %".101" = load i64, i64* @"__sustain_1305777795296"
  %".102" = icmp eq i64 %".101", -1
  br i1 %".102", label %"sus_set", label %"sus_chk"
sus_false:
  store i64 -1, i64* @"__sustain_1305777795296"
  store i1 0, i1* %"sus_res"
  br label %"sus_done"
sus_done:
  %".114" = load i1, i1* %"sus_res"
  br i1 %".114", label %"rule_m57492_then", label %"rule_m57492_end"
sus_set:
  store i64 %"t_now", i64* @"__sustain_1305777795296"
  br label %"sus_chk"
sus_chk:
  %".106" = load i64, i64* @"__sustain_1305777795296"
  %".107" = sub i64 %"t_now", %".106"
  %".108" = icmp sge i64 %".107", 10000
  store i1 %".108", i1* %"sus_res"
  br label %"sus_done"
rule_m57492_then:
  %".116" = bitcast [90 x i8]* @"__alert_10" to i8*
  call void @"mizan_alert"(i32 2, i8* %".116")
  br label %"rule_m57492_end"
rule_m57492_end:
  br label %"mode_end"
mode_m89999:
  br i1 1, label %"rule_m97217_then", label %"rule_m97217_end"
rule_m97217_then:
  br label %"rule_m97217_end"
rule_m97217_end:
  br label %"mode_end"
flush_cond:
  %".126" = load i32, i32* %"fi"
  %".127" = icmp slt i32 %".126", %"flush_n"
  br i1 %".127", label %"flush_body", label %"flush_end"
flush_body:
  %".129" = load i32, i32* %"fi"
  %".130" = getelementptr inbounds [64 x i32], [64 x i32]* @"__wq_addrs", i32 0, i32 %".129"
  %".131" = getelementptr inbounds [64 x double], [64 x double]* @"__wq_values", i32 0, i32 %".129"
  %".132" = load i32, i32* %".130"
  %".133" = load double, double* %".131"
  call void @"mizan_modbus_write"(i8* %"mb_out", i32 %".132", double %".133")
  %".135" = add i32 %".129", 1
  store i32 %".135", i32* %"fi"
  br label %"flush_cond"
flush_end:
  store i32 0, i32* @"__wq_count"
  call void @"mizan_escalation_tick"()
  %".140" = bitcast [2048 x i8]* @"__rpt_buf" to i8*
  %"agg" = call double @"mizan_ring_avg"(i32 0, i64 86400000)
  %"agg.1" = call double @"mizan_ring_max"(i32 1, i64 86400000)
  %".141" = load i32, i32* @"__current_mode"
  %"i2f" = sitofp i32 %".141" to double
  %".142" = bitcast [70 x i8]* @"__rpt_fmt_11" to i8*
  %".143" = call i32 (i8*, i64, i8*, ...) @"snprintf"(i8* %".140", i64 2048, i8* %".142", double %"agg", double %"agg.1", double %"i2f")
  %".144" = bitcast [24 x i8]* @"__rpt_id_12" to i8*
  %".145" = bitcast [5 x i8]* @"__rpt_fmtarg_13" to i8*
  %".146" = bitcast [16 x i8]* @"__rpt_dir_14" to i8*
  call void @"mizan_report_write"(i8* %".144", i8* %".145", i8* %".146", i8* %".140")
  %"pending" = load i32, i32* @"__pending_goto"
  %".148" = icmp ne i32 %"pending", -1
  br i1 %".148", label %"flush_end.if", label %"flush_end.endif"
flush_end.if:
  store i32 %"pending", i32* @"__current_mode"
  store i32 -1, i32* @"__pending_goto"
  br label %"flush_end.endif"
flush_end.endif:
  %"now" = call i64 @"mizan_now_ms"()
  %"elapsed" = sub i64 %"now", %"cycle_start"
  %"remain" = sub i64 1000, %"elapsed"
  %".153" = icmp sgt i64 %"remain", 0
  br i1 %".153", label %"flush_end.endif.if", label %"flush_end.endif.endif"
flush_end.endif.if:
  call void @"mizan_sleep_ms"(i64 %"remain")
  br label %"flush_end.endif.endif"
flush_end.endif.endif:
  br label %"scan_cycle"
}

@"__dev_ip_2" = private constant [10 x i8] c"127.0.0.1\00"
@"__mq_host_3" = private constant [10 x i8] c"127.0.0.1\00"
@"__mq_cid_4" = private constant [14 x i8] c"mizan-runtime\00"
@"__log_5" = private constant [49 x i8] c"[\d8\b3\d8\ac\d9\84] \d8\a8\d8\af\d8\a1 \d8\aa\d8\b4\d8\ba\d9\8a\d9\84 \d9\86\d8\b8\d8\a7\d9\85 \d8\a7\d9\84\d8\aa\d8\ad\d9\83\d9\85\00"
@"__alert_6" = private constant [61 x i8] c"[\d8\aa\d9\86\d8\a8\d9\8a\d9\87 \d9\85\d8\b3\d8\aa\d9\88\d9\89_2] \d8\a7\d9\86\d9\82\d8\b7\d8\b9 \d8\ad\d8\b3\d8\a7\d8\b3 \d8\a7\d9\84\d8\ad\d8\b1\d8\a7\d8\b1\d8\a9\00"
@"__alert_7" = private constant [79 x i8] c"[\d8\aa\d9\86\d8\a8\d9\8a\d9\87 \d9\85\d8\b3\d8\aa\d9\88\d9\89_1] \d8\ad\d8\b3\d8\a7\d8\b3 \d8\a7\d9\84\d8\ad\d8\b1\d8\a7\d8\b1\d8\a9 \d9\8a\d8\b9\d8\b7\d9\8a \d9\82\d9\8a\d9\85\d8\a9 \d8\ab\d8\a7\d8\a8\d8\aa\d8\a9\00"
@"__alert_8" = private constant [52 x i8] c"[\d8\aa\d9\86\d8\a8\d9\8a\d9\87 \d9\85\d8\b3\d8\aa\d9\88\d9\89_1] \d8\aa\d9\81\d8\b9\d9\8a\d9\84 \d8\a7\d9\84\d8\aa\d8\a8\d8\b1\d9\8a\d8\af\00"
@"__alert_9" = private constant [92 x i8] c"[\d8\aa\d9\86\d8\a8\d9\8a\d9\87 \d9\85\d8\b3\d8\aa\d9\88\d9\89_3] \d8\ad\d8\a7\d9\84\d8\a9 \d8\b7\d9\88\d8\a7\d8\b1\d8\a6: \d8\ad\d8\b1\d8\a7\d8\b1\d8\a9 \d8\a7\d9\88 \d8\b6\d8\ba\d8\b7 \d8\ae\d8\a7\d8\b1\d8\ac \d8\a7\d9\84\d8\ad\d8\af\d9\88\d8\af\00"
@"__sustain_1305777795296" = internal global i64 -1
@"__alert_10" = private constant [90 x i8] c"[\d8\aa\d9\86\d8\a8\d9\8a\d9\87 \d9\85\d8\b3\d8\aa\d9\88\d9\89_2] \d8\a7\d9\84\d8\ad\d8\b1\d8\a7\d8\b1\d8\a9 \d9\85\d8\b1\d8\aa\d9\81\d8\b9\d8\a9 \d9\84\d9\85\d8\af\d8\a9 10 \d8\ab\d9\88\d8\a7\d9\86 \d9\85\d8\aa\d9\88\d8\a7\d8\b5\d9\84\d8\a9\00"
@"__rpt_fmt_11" = private constant [70 x i8] c"{\22\d9\85\d8\aa\d9\88\d8\b3\d8\b7 \d8\a7\d9\84\d8\ad\d8\b1\d8\a7\d8\b1\d8\a9\22:%f,\22\d8\a7\d8\b9\d9\84\d9\89 \d8\b6\d8\ba\d8\b7\22:%f,\22\d8\a7\d9\84\d9\88\d8\b6\d8\b9\22:%f}\00"
@"__rpt_id_12" = private constant [24 x i8] c"\d8\aa\d9\82\d8\b1\d9\8a\d8\b1_\d8\a7\d9\84\d9\8a\d9\88\d9\85\d9\8a\00"
@"__rpt_fmtarg_13" = private constant [5 x i8] c"json\00"
@"__rpt_dir_14" = private constant [16 x i8] c"./mizan_reports\00"