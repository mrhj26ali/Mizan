; ModuleID = '<string>'
source_filename = "<string>"
target triple = "x86_64-pc-windows-msvc"

@"s_\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9" = internal unnamed_addr global double 0.000000e+00
@__modbus_ctx = internal unnamed_addr global ptr null
@__mqtt_ctx = internal unnamed_addr global ptr null
@__current_mode = internal unnamed_addr global i1 false
@__pending_goto = internal unnamed_addr global i1 false
@__dev_ip_1 = private constant [10 x i8] c"127.0.0.1\00"
@__mq_host_2 = private constant [10 x i8] c"127.0.0.1\00"
@__mq_cid_3 = private constant [14 x i8] c"mizan-runtime\00"
@__log_4 = private constant [34 x i8] c"\D8\A8\D8\AF\D8\A1 \D9\85\D8\B1\D8\A7\D9\82\D8\A8\D8\A9 \D8\A7\D9\84\D8\B5\D8\AD\D8\A9...\00"
@__alert_5 = private constant [53 x i8] c"[\D8\AA\D9\86\D8\A8\D9\8A\D9\87 \D9\85\D8\B3\D8\AA\D9\88\D9\89_3] \D9\81\D9\82\D8\AF\D8\A7\D9\86 \D8\A7\D9\84\D8\A7\D8\AA\D8\B5\D8\A7\D9\84!\00"
@__alert_6 = private constant [75 x i8] c"[\D8\AA\D9\86\D8\A8\D9\8A\D9\87 \D9\85\D8\B3\D8\AA\D9\88\D9\89_2] \D8\A7\D9\84\D9\82\D8\B1\D8\A7\D8\A1\D8\A9 \D8\AE\D8\A7\D8\B1\D8\AC \D8\A7\D9\84\D9\86\D8\B7\D8\A7\D9\82 \D8\A7\D9\84\D8\A7\D9\85\D9\86!\00"
@__log_7 = private constant [23 x i8] c"\D8\A7\D9\84\D9\86\D8\B8\D8\A7\D9\85 \D9\8A\D8\B9\D9\85\D9\84.\00"

declare void @setup_arabic_console() local_unnamed_addr

declare void @mizan_log(ptr) local_unnamed_addr

declare void @mizan_alert(i32, ptr) local_unnamed_addr

declare ptr @mizan_modbus_connect(ptr, i32) local_unnamed_addr

declare double @mizan_modbus_read(ptr, i32) local_unnamed_addr

declare i32 @mizan_modbus_is_connected(ptr) local_unnamed_addr

declare ptr @mizan_mqtt_connect(ptr, i32, ptr) local_unnamed_addr

declare void @__mizan_set_mqtt_ctx(ptr) local_unnamed_addr

declare i64 @mizan_now_ms() local_unnamed_addr

declare void @mizan_sleep_ms(i64) local_unnamed_addr

declare void @mizan_ring_push(i32, double) local_unnamed_addr

declare i32 @mizan_health_track_disconnect(i32, i32) local_unnamed_addr

declare i32 @mizan_health_out_of_range(i32, double, double, double) local_unnamed_addr

declare void @mizan_escalation_tick() local_unnamed_addr

; Function Attrs: noreturn
define noundef i32 @main() local_unnamed_addr #0 {
entry:
  tail call void @setup_arabic_console()
  %.4 = tail call ptr @mizan_modbus_connect(ptr nonnull @__dev_ip_1, i32 5020)
  store ptr %.4, ptr @__modbus_ctx, align 8
  %.8 = tail call ptr @mizan_mqtt_connect(ptr nonnull @__mq_host_2, i32 1884, ptr nonnull @__mq_cid_3)
  store ptr %.8, ptr @__mqtt_ctx, align 8
  tail call void @__mizan_set_mqtt_ctx(ptr %.8)
  store i1 false, ptr @__current_mode, align 1
  tail call void @mizan_log(ptr nonnull @__log_4)
  store i1 true, ptr @__pending_goto, align 1
  br label %scan_cycle

scan_cycle:                                       ; preds = %scan_cycle.backedge, %entry
  %cycle_start = tail call i64 @mizan_now_ms()
  %mb = load ptr, ptr @__modbus_ctx, align 8
  %global_conn = tail call i32 @mizan_modbus_is_connected(ptr %mb)
  %"raw_\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9" = tail call double @mizan_modbus_read(ptr %mb, i32 8)
  store double %"raw_\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9", ptr @"s_\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9", align 8
  %"conn_\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9" = tail call i32 @mizan_modbus_is_connected(ptr %mb)
  %.23.not = icmp eq i32 %"conn_\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9", 0
  br i1 %.23.not, label %scan_sensors.endif, label %scan_sensors.if

scan_sensors.if:                                  ; preds = %scan_cycle
  tail call void @mizan_ring_push(i32 0, double %"raw_\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9")
  br label %scan_sensors.endif

scan_sensors.endif:                               ; preds = %scan_sensors.if, %scan_cycle
  %disc_edge = tail call i32 @mizan_health_track_disconnect(i32 0, i32 %"conn_\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9")
  %.27.not = icmp eq i32 %disc_edge, 0
  br i1 %.27.not, label %scan_sensors.endif.endif, label %scan_sensors.endif.if

scan_sensors.endif.if:                            ; preds = %scan_sensors.endif
  tail call void @mizan_alert(i32 3, ptr nonnull @__alert_5)
  br label %scan_sensors.endif.endif

scan_sensors.endif.endif:                         ; preds = %scan_sensors.endif.if, %scan_sensors.endif
  %oor_edge = tail call i32 @mizan_health_out_of_range(i32 0, double %"raw_\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9", double 0.000000e+00, double 1.500000e+02)
  %.32.not = icmp eq i32 %oor_edge, 0
  br i1 %.32.not, label %scan_sensors.endif.endif.endif, label %scan_sensors.endif.endif.if

scan_sensors.endif.endif.if:                      ; preds = %scan_sensors.endif.endif
  tail call void @mizan_alert(i32 2, ptr nonnull @__alert_6)
  br label %scan_sensors.endif.endif.endif

scan_sensors.endif.endif.endif:                   ; preds = %scan_sensors.endif.endif.if, %scan_sensors.endif.endif
  %cur_mode.b = load i1, ptr @__current_mode, align 1
  %"\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9" = load double, ptr @"s_\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9", align 8
  %fcmp = fcmp ogt double %"\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9", 5.000000e+01
  %or.cond = select i1 %cur_mode.b, i1 %fcmp, i1 false
  br i1 %or.cond, label %if_then, label %flush_end

if_then:                                          ; preds = %scan_sensors.endif.endif.endif
  tail call void @mizan_log(ptr nonnull @__log_7)
  br label %flush_end

flush_end:                                        ; preds = %if_then, %scan_sensors.endif.endif.endif
  tail call void @mizan_escalation_tick()
  %pending.b = load i1, ptr @__pending_goto, align 1
  br i1 %pending.b, label %flush_end.if, label %flush_end.endif

flush_end.if:                                     ; preds = %flush_end
  store i1 true, ptr @__current_mode, align 1
  store i1 false, ptr @__pending_goto, align 1
  br label %flush_end.endif

flush_end.endif:                                  ; preds = %flush_end.if, %flush_end
  %now = tail call i64 @mizan_now_ms()
  %elapsed.neg = sub i64 %cycle_start, %now
  %remain = add i64 %elapsed.neg, 500
  %.69 = icmp sgt i64 %remain, 0
  br i1 %.69, label %flush_end.endif.if, label %scan_cycle.backedge

flush_end.endif.if:                               ; preds = %flush_end.endif
  tail call void @mizan_sleep_ms(i64 %remain)
  br label %scan_cycle.backedge

scan_cycle.backedge:                              ; preds = %flush_end.endif.if, %flush_end.endif
  br label %scan_cycle
}

attributes #0 = { noreturn }
