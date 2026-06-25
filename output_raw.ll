; ModuleID = "mizan_program"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare void @"setup_arabic_console"()

declare void @"print_arabic"(i8* %".1")

declare void @"mizan_log"(i8* %".1")

declare void @"mizan_alert"(i32 %".1", i8* %".2")

declare void @"panic_div_zero"()

declare void @"panic_array_bounds"(i32 %".1", i32 %".2")

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

declare i32 @"mizan_health_track_disconnect"(i32 %".1", i32 %".2")

declare i32 @"mizan_health_track_stuck"(i32 %".1", double %".2", i64 %".3")

declare i32 @"mizan_health_out_of_range"(i32 %".1", double %".2", double %".3", double %".4")

declare void @"mizan_escalation_tick"()

declare void @"mizan_escalation_arm"(i32 %".1", i32 %".2", i64 %".3", i8* %".4", i8* %".5")

declare void @"mizan_report_write"(i8* %".1", i8* %".2", i8* %".3", i8* %".4")

declare void @"mizan_actuator_cmd"(i32 %".1", double %".2")

declare i32 @"mizan_actuator_cycles"(i32 %".1")

declare i32 @"mizan_actuator_state"(i32 %".1")

declare i32 @"mizan_sensor_health"(i32 %".1")

declare i32 @"mizan_schedule_check"(i32 %".1", i32 %".2", i32 %".3", i32 %".4", i32 %".5", i32 %".6")

declare i32 @"printf"(i8* %".1", ...)

declare i32 @"snprintf"(i8* %".1", i64 %".2", i8* %".3", ...)

@"s_الحرارة" = internal global double 0.0
@"s_الحرارة_conn" = internal global i32 1
@"a_مضخة_التبريد" = internal global double 0.0
@"g_حالة_التبريد" = internal global i1 0
@"__modbus_ctx" = internal global i8* null
@"__mqtt_ctx" = internal global i8* null
@"__current_mode" = internal global i32 0
@"__pending_goto" = internal global i32 -1
@"__wq_addrs" = internal global [64 x i32] [i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0]
@"__wq_values" = internal global [64 x double] [double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0, double              0x0]
@"__wq_count" = internal global i32 0
@"__rpt_buf" = internal global [2048 x i8] c"\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00"
define i32 @"main"()
{
entry:
  call void @"setup_arabic_console"()
  %".3" = bitcast [10 x i8]* @"__dev_ip_1" to i8*
  %".4" = call i8* @"mizan_modbus_connect"(i8* %".3", i32 5020)
  store i8* %".4", i8** @"__modbus_ctx"
  %".6" = bitcast [10 x i8]* @"__mq_host_2" to i8*
  %".7" = bitcast [14 x i8]* @"__mq_cid_3" to i8*
  %".8" = call i8* @"mizan_mqtt_connect"(i8* %".6", i32 1884, i8* %".7")
  store i8* %".8", i8** @"__mqtt_ctx"
  call void @"__mizan_set_mqtt_ctx"(i8* %".8")
  store i1 0, i1* @"g_حالة_التبريد"
  store i32 0, i32* @"__current_mode"
  %".13" = bitcast [55 x i8]* @"__log_4" to i8*
  call void @"mizan_log"(i8* %".13")
  store i32 1, i32* @"__pending_goto"
  br label %"scan_cycle"
scan_cycle:
  %"cycle_start" = call i64 @"mizan_now_ms"()
  %"mb" = load i8*, i8** @"__modbus_ctx"
  %"global_conn" = call i32 @"mizan_modbus_is_connected"(i8* %"mb")
  %".17" = icmp eq i32 %"global_conn", 0
  br i1 %".17", label %"safe_state_flush", label %"scan_sensors"
safe_state_flush:
  store i32 0, i32* @"__wq_count"
  store double              0x0, double* @"a_مضخة_التبريد"
  br label %"scan_sensors"
scan_sensors:
  %"raw_الحرارة" = call double @"mizan_modbus_read"(i8* %"mb", i32 8)
  store double %"raw_الحرارة", double* @"s_الحرارة"
  %"conn_الحرارة" = call i32 @"mizan_modbus_is_connected"(i8* %"mb")
  store i32 %"conn_الحرارة", i32* @"s_الحرارة_conn"
  %".24" = icmp ne i32 %"conn_الحرارة", 0
  br i1 %".24", label %"scan_sensors.if", label %"scan_sensors.endif"
scan_sensors.if:
  call void @"mizan_ring_push"(i32 0, double %"raw_الحرارة")
  br label %"scan_sensors.endif"
scan_sensors.endif:
  %"cur_mode" = load i32, i32* @"__current_mode"
  switch i32 %"cur_mode", label %"mode_default" [i32 0, label %"mode_m46458" i32 1, label %"mode_m77285"]
mode_default:
  br label %"mode_end"
mode_end:
  %"flush_n" = load i32, i32* @"__wq_count"
  %"mb_out" = load i8*, i8** @"__modbus_ctx"
  %"fi" = alloca i32
  store i32 0, i32* %"fi"
  br label %"flush_cond"
mode_m46458:
  br label %"mode_end"
mode_m77285:
  %"الحرارة" = load double, double* @"s_الحرارة"
  %"i2f" = sitofp i32 90 to double
  %"fcmp" = fcmp ogt double %"الحرارة", %"i2f"
  %"t_now" = call i64 @"mizan_now_ms"()
  %"sus_res" = alloca i1
  store i1 0, i1* %"sus_res"
  br i1 %"fcmp", label %"sus_true", label %"sus_false"
sus_true:
  %".32" = load i64, i64* @"__sustain_2561222929984"
  %".33" = icmp eq i64 %".32", -1
  br i1 %".33", label %"sus_set", label %"sus_chk"
sus_false:
  store i64 -1, i64* @"__sustain_2561222929984"
  store i1 0, i1* %"sus_res"
  br label %"sus_done"
sus_done:
  %".45" = load i1, i1* %"sus_res"
  br i1 %".45", label %"if_then", label %"if_else"
sus_set:
  store i64 %"t_now", i64* @"__sustain_2561222929984"
  br label %"sus_chk"
sus_chk:
  %".37" = load i64, i64* @"__sustain_2561222929984"
  %".38" = sub i64 %"t_now", %".37"
  %".39" = icmp sge i64 %".38", 5000
  store i1 %".39", i1* %"sus_res"
  br label %"sus_done"
if_then:
  store double 0x3ff0000000000000, double* @"a_مضخة_التبريد"
  call void @"mizan_actuator_cmd"(i32 0, double 0x3ff0000000000000)
  %"wqc" = load i32, i32* @"__wq_count"
  %".49" = icmp slt i32 %"wqc", 64
  br i1 %".49", label %"if_then.if", label %"if_then.endif"
if_else:
  store double              0x0, double* @"a_مضخة_التبريد"
  call void @"mizan_actuator_cmd"(i32 0, double              0x0)
  %"wqc.1" = load i32, i32* @"__wq_count"
  %".64" = icmp slt i32 %"wqc.1", 64
  br i1 %".64", label %"if_else.if", label %"if_else.endif"
if_end:
  br label %"mode_end"
if_then.if:
  %".51" = getelementptr inbounds [64 x i32], [64 x i32]* @"__wq_addrs", i32 0, i32 %"wqc"
  %".52" = getelementptr inbounds [64 x double], [64 x double]* @"__wq_values", i32 0, i32 %"wqc"
  store i32 34, i32* %".51"
  store double 0x3ff0000000000000, double* %".52"
  %".55" = add i32 %"wqc", 1
  store i32 %".55", i32* @"__wq_count"
  br label %"if_then.endif"
if_then.endif:
  %".58" = bitcast [68 x i8]* @"__log_5" to i8*
  call void @"mizan_log"(i8* %".58")
  store i1 1, i1* @"g_حالة_التبريد"
  br label %"if_end"
if_else.if:
  %".66" = getelementptr inbounds [64 x i32], [64 x i32]* @"__wq_addrs", i32 0, i32 %"wqc.1"
  %".67" = getelementptr inbounds [64 x double], [64 x double]* @"__wq_values", i32 0, i32 %"wqc.1"
  store i32 34, i32* %".66"
  store double              0x0, double* %".67"
  %".70" = add i32 %"wqc.1", 1
  store i32 %".70", i32* @"__wq_count"
  br label %"if_else.endif"
if_else.endif:
  store i1 0, i1* @"g_حالة_التبريد"
  br label %"if_end"
flush_cond:
  %".79" = load i32, i32* %"fi"
  %".80" = icmp slt i32 %".79", %"flush_n"
  br i1 %".80", label %"flush_body", label %"flush_end"
flush_body:
  %".82" = load i32, i32* %"fi"
  %".83" = getelementptr inbounds [64 x i32], [64 x i32]* @"__wq_addrs", i32 0, i32 %".82"
  %".84" = getelementptr inbounds [64 x double], [64 x double]* @"__wq_values", i32 0, i32 %".82"
  %".85" = load i32, i32* %".83"
  %".86" = load double, double* %".84"
  call void @"mizan_modbus_write"(i8* %"mb_out", i32 %".85", double %".86")
  %".88" = add i32 %".82", 1
  store i32 %".88", i32* %"fi"
  br label %"flush_cond"
flush_end:
  store i32 0, i32* @"__wq_count"
  call void @"mizan_escalation_tick"()
  %"pending" = load i32, i32* @"__pending_goto"
  %".93" = icmp ne i32 %"pending", -1
  br i1 %".93", label %"flush_end.if", label %"flush_end.endif"
flush_end.if:
  store i32 %"pending", i32* @"__current_mode"
  store i32 -1, i32* @"__pending_goto"
  br label %"flush_end.endif"
flush_end.endif:
  %"now" = call i64 @"mizan_now_ms"()
  %"elapsed" = sub i64 %"now", %"cycle_start"
  %"remain" = sub i64 500, %"elapsed"
  %".98" = icmp sgt i64 %"remain", 0
  br i1 %".98", label %"flush_end.endif.if", label %"flush_end.endif.endif"
flush_end.endif.if:
  call void @"mizan_sleep_ms"(i64 %"remain")
  br label %"flush_end.endif.endif"
flush_end.endif.endif:
  br label %"scan_cycle"
}

@"__dev_ip_1" = private constant [10 x i8] c"127.0.0.1\00"
@"__mq_host_2" = private constant [10 x i8] c"127.0.0.1\00"
@"__mq_cid_3" = private constant [14 x i8] c"mizan-runtime\00"
@"__log_4" = private constant [55 x i8] c"\d8\a8\d8\af\d8\a1 \d8\a7\d8\ae\d8\aa\d8\a8\d8\a7\d8\b1 \d8\a7\d9\84\d8\a7\d9\85\d8\a7\d9\86 \d8\a7\d9\84\d9\81\d9\8a\d8\b2\d9\8a\d8\a7\d8\a6\d9\8a...\00"
@"__sustain_2561222929984" = internal global i64 -1
@"__log_5" = private constant [68 x i8] c"\d8\ad\d8\b1\d8\a7\d8\b1\d8\a9 \d9\85\d8\b1\d8\aa\d9\81\d8\b9\d8\a9 \d8\a8\d8\a7\d8\b3\d8\aa\d9\85\d8\b1\d8\a7\d8\b1\d8\8c \d8\aa\d8\b4\d8\ba\d9\8a\d9\84 \d8\a7\d9\84\d9\85\d8\b6\d8\ae\d8\a9.\00"