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
@"g_حالة_النظام" = internal global i32 0
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
  store i32 0, i32* @"g_حالة_النظام"
  store i32 0, i32* @"__current_mode"
  %".13" = bitcast [34 x i8]* @"__log_4" to i8*
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
  br label %"scan_sensors"
scan_sensors:
  %"raw_الحرارة" = call double @"mizan_modbus_read"(i8* %"mb", i32 8)
  store double %"raw_الحرارة", double* @"s_الحرارة"
  %"conn_الحرارة" = call i32 @"mizan_modbus_is_connected"(i8* %"mb")
  store i32 %"conn_الحرارة", i32* @"s_الحرارة_conn"
  %".23" = icmp ne i32 %"conn_الحرارة", 0
  br i1 %".23", label %"scan_sensors.if", label %"scan_sensors.endif"
scan_sensors.if:
  call void @"mizan_ring_push"(i32 0, double %"raw_الحرارة")
  br label %"scan_sensors.endif"
scan_sensors.endif:
  %"disc_edge" = call i32 @"mizan_health_track_disconnect"(i32 0, i32 %"conn_الحرارة")
  %".27" = icmp ne i32 %"disc_edge", 0
  br i1 %".27", label %"scan_sensors.endif.if", label %"scan_sensors.endif.endif"
scan_sensors.endif.if:
  %".29" = bitcast [53 x i8]* @"__alert_5" to i8*
  call void @"mizan_alert"(i32 3, i8* %".29")
  br label %"scan_sensors.endif.endif"
scan_sensors.endif.endif:
  %"oor_edge" = call i32 @"mizan_health_out_of_range"(i32 0, double %"raw_الحرارة", double              0x0, double 0x4062c00000000000)
  %".32" = icmp ne i32 %"oor_edge", 0
  br i1 %".32", label %"scan_sensors.endif.endif.if", label %"scan_sensors.endif.endif.endif"
scan_sensors.endif.endif.if:
  %".34" = bitcast [75 x i8]* @"__alert_6" to i8*
  call void @"mizan_alert"(i32 2, i8* %".34")
  br label %"scan_sensors.endif.endif.endif"
scan_sensors.endif.endif.endif:
  %"cur_mode" = load i32, i32* @"__current_mode"
  switch i32 %"cur_mode", label %"mode_default" [i32 0, label %"mode_m8564" i32 1, label %"mode_m99874"]
mode_default:
  br label %"mode_end"
mode_end:
  %"flush_n" = load i32, i32* @"__wq_count"
  %"mb_out" = load i8*, i8** @"__modbus_ctx"
  %"fi" = alloca i32
  store i32 0, i32* %"fi"
  br label %"flush_cond"
mode_m8564:
  br label %"mode_end"
mode_m99874:
  %"الحرارة" = load double, double* @"s_الحرارة"
  %"fcmp" = fcmp ogt double %"الحرارة", 0x4049000000000000
  br i1 %"fcmp", label %"if_then", label %"if_else"
if_then:
  %".40" = bitcast [23 x i8]* @"__log_7" to i8*
  call void @"mizan_log"(i8* %".40")
  store i32 1, i32* @"g_حالة_النظام"
  br label %"if_end"
if_else:
  store i32 0, i32* @"g_حالة_النظام"
  br label %"if_end"
if_end:
  br label %"mode_end"
flush_cond:
  %".50" = load i32, i32* %"fi"
  %".51" = icmp slt i32 %".50", %"flush_n"
  br i1 %".51", label %"flush_body", label %"flush_end"
flush_body:
  %".53" = load i32, i32* %"fi"
  %".54" = getelementptr inbounds [64 x i32], [64 x i32]* @"__wq_addrs", i32 0, i32 %".53"
  %".55" = getelementptr inbounds [64 x double], [64 x double]* @"__wq_values", i32 0, i32 %".53"
  %".56" = load i32, i32* %".54"
  %".57" = load double, double* %".55"
  call void @"mizan_modbus_write"(i8* %"mb_out", i32 %".56", double %".57")
  %".59" = add i32 %".53", 1
  store i32 %".59", i32* %"fi"
  br label %"flush_cond"
flush_end:
  store i32 0, i32* @"__wq_count"
  call void @"mizan_escalation_tick"()
  %"pending" = load i32, i32* @"__pending_goto"
  %".64" = icmp ne i32 %"pending", -1
  br i1 %".64", label %"flush_end.if", label %"flush_end.endif"
flush_end.if:
  store i32 %"pending", i32* @"__current_mode"
  store i32 -1, i32* @"__pending_goto"
  br label %"flush_end.endif"
flush_end.endif:
  %"now" = call i64 @"mizan_now_ms"()
  %"elapsed" = sub i64 %"now", %"cycle_start"
  %"remain" = sub i64 500, %"elapsed"
  %".69" = icmp sgt i64 %"remain", 0
  br i1 %".69", label %"flush_end.endif.if", label %"flush_end.endif.endif"
flush_end.endif.if:
  call void @"mizan_sleep_ms"(i64 %"remain")
  br label %"flush_end.endif.endif"
flush_end.endif.endif:
  br label %"scan_cycle"
}

@"__dev_ip_1" = private constant [10 x i8] c"127.0.0.1\00"
@"__mq_host_2" = private constant [10 x i8] c"127.0.0.1\00"
@"__mq_cid_3" = private constant [14 x i8] c"mizan-runtime\00"
@"__log_4" = private constant [34 x i8] c"\d8\a8\d8\af\d8\a1 \d9\85\d8\b1\d8\a7\d9\82\d8\a8\d8\a9 \d8\a7\d9\84\d8\b5\d8\ad\d8\a9...\00"
@"__alert_5" = private constant [53 x i8] c"[\d8\aa\d9\86\d8\a8\d9\8a\d9\87 \d9\85\d8\b3\d8\aa\d9\88\d9\89_3] \d9\81\d9\82\d8\af\d8\a7\d9\86 \d8\a7\d9\84\d8\a7\d8\aa\d8\b5\d8\a7\d9\84!\00"
@"__alert_6" = private constant [75 x i8] c"[\d8\aa\d9\86\d8\a8\d9\8a\d9\87 \d9\85\d8\b3\d8\aa\d9\88\d9\89_2] \d8\a7\d9\84\d9\82\d8\b1\d8\a7\d8\a1\d8\a9 \d8\ae\d8\a7\d8\b1\d8\ac \d8\a7\d9\84\d9\86\d8\b7\d8\a7\d9\82 \d8\a7\d9\84\d8\a7\d9\85\d9\86!\00"
@"__log_7" = private constant [23 x i8] c"\d8\a7\d9\84\d9\86\d8\b8\d8\a7\d9\85 \d9\8a\d8\b9\d9\85\d9\84.\00"