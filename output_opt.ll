; ModuleID = '<string>'
source_filename = "<string>"
target triple = "x86_64-pc-windows-msvc"

@"s_\D8\A7\D9\84\D8\B6\D8\BA\D8\B7" = internal unnamed_addr global double 0.000000e+00
@__modbus_ctx = internal unnamed_addr global ptr null
@__mqtt_ctx = internal unnamed_addr global ptr null
@__current_mode = internal unnamed_addr global i1 false
@__pending_goto = internal unnamed_addr global i1 false
@__wq_addrs = internal unnamed_addr global [64 x i32] zeroinitializer
@__wq_values = internal unnamed_addr global [64 x double] zeroinitializer
@__wq_count = internal unnamed_addr global i32 0
@__rpt_buf = internal global [2048 x i8] zeroinitializer
@__dev_ip_1 = private constant [10 x i8] c"127.0.0.1\00"
@__mq_host_2 = private constant [10 x i8] c"127.0.0.1\00"
@__mq_cid_3 = private constant [14 x i8] c"mizan-runtime\00"
@__log_4 = private constant [36 x i8] c"\D8\A8\D8\AF\D8\A1 \D9\86\D8\B8\D8\A7\D9\85 \D8\A7\D9\84\D8\AA\D9\82\D8\A7\D8\B1\D9\8A\D8\B1...\00"
@__alert_5 = private constant [56 x i8] c"[\D8\AA\D9\86\D8\A8\D9\8A\D9\87 \D9\85\D8\B3\D8\AA\D9\88\D9\89_1] \D8\A7\D9\84\D8\B6\D8\BA\D8\B7 \D9\85\D8\B1\D8\AA\D9\81\D8\B9 \D8\AC\D8\AF\D8\A7!\00"
@__rpt_timer_0 = internal unnamed_addr global i64 -1
@__rpt_fmt_6 = private constant [87 x i8] c"{\22\D8\AF\D9\88\D8\B1\D8\A7\D8\AA_\D8\A7\D9\84\D9\85\D8\B6\D8\AE\D8\A9\22:%d,\22\D8\AD\D8\A7\D9\84\D8\A9_\D8\A7\D9\84\D9\85\D8\B6\D8\AE\D8\A9\22:%d,\22\D8\B3\D9\84\D8\A7\D9\85\D8\A9_\D8\A7\D9\84\D8\AD\D8\B3\D8\A7\D8\B3\22:%d}\00"
@__rpt_id_7 = private constant [26 x i8] c"\D8\AA\D9\82\D8\B1\D9\8A\D8\B1_\D8\A7\D9\84\D8\B5\D9\8A\D8\A7\D9\86\D8\A9\00"
@__rpt_fmtarg_8 = private constant [5 x i8] c"json\00"
@__rpt_dir_9 = private constant [14 x i8] c"./reports/cbm\00"

declare void @setup_arabic_console() local_unnamed_addr

declare void @mizan_log(ptr) local_unnamed_addr

declare void @mizan_alert(i32, ptr) local_unnamed_addr

declare ptr @mizan_modbus_connect(ptr, i32) local_unnamed_addr

declare double @mizan_modbus_read(ptr, i32) local_unnamed_addr

declare void @mizan_modbus_write(ptr, i32, double) local_unnamed_addr

declare i32 @mizan_modbus_is_connected(ptr) local_unnamed_addr

declare ptr @mizan_mqtt_connect(ptr, i32, ptr) local_unnamed_addr

declare void @__mizan_set_mqtt_ctx(ptr) local_unnamed_addr

declare i64 @mizan_now_ms() local_unnamed_addr

declare void @mizan_sleep_ms(i64) local_unnamed_addr

declare void @mizan_ring_push(i32, double) local_unnamed_addr

declare void @mizan_escalation_tick() local_unnamed_addr

declare void @mizan_report_write(ptr, ptr, ptr, ptr) local_unnamed_addr

declare void @mizan_actuator_cmd(i32, double) local_unnamed_addr

declare i32 @mizan_actuator_cycles(i32) local_unnamed_addr

declare i32 @mizan_actuator_state(i32) local_unnamed_addr

declare i32 @mizan_sensor_health(i32) local_unnamed_addr

; Function Attrs: nofree nounwind
declare noundef i32 @snprintf(ptr noalias nocapture noundef writeonly, i64 noundef, ptr nocapture noundef readonly, ...) local_unnamed_addr #0

; Function Attrs: noreturn
define noundef i32 @main() local_unnamed_addr #1 {
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
  %.17 = icmp eq i32 %global_conn, 0
  br i1 %.17, label %safe_state_flush, label %scan_sensors

safe_state_flush:                                 ; preds = %scan_cycle
  store i32 0, ptr @__wq_count, align 4
  br label %scan_sensors

scan_sensors:                                     ; preds = %safe_state_flush, %scan_cycle
  %"raw_\D8\A7\D9\84\D8\B6\D8\BA\D8\B7" = tail call double @mizan_modbus_read(ptr %mb, i32 2)
  store double %"raw_\D8\A7\D9\84\D8\B6\D8\BA\D8\B7", ptr @"s_\D8\A7\D9\84\D8\B6\D8\BA\D8\B7", align 8
  %"conn_\D8\A7\D9\84\D8\B6\D8\BA\D8\B7" = tail call i32 @mizan_modbus_is_connected(ptr %mb)
  %.24.not = icmp eq i32 %"conn_\D8\A7\D9\84\D8\B6\D8\BA\D8\B7", 0
  br i1 %.24.not, label %scan_sensors.endif, label %scan_sensors.if

scan_sensors.if:                                  ; preds = %scan_sensors
  tail call void @mizan_ring_push(i32 0, double %"raw_\D8\A7\D9\84\D8\B6\D8\BA\D8\B7")
  br label %scan_sensors.endif

scan_sensors.endif:                               ; preds = %scan_sensors.if, %scan_sensors
  %cur_mode.b = load i1, ptr @__current_mode, align 1
  br i1 %cur_mode.b, label %mode_m36121, label %mode_endthread-pre-split

mode_endthread-pre-split:                         ; preds = %scan_sensors.endif, %if_then.endif
  %flush_n.pr = load i32, ptr @__wq_count, align 4
  br label %mode_end

mode_end:                                         ; preds = %mode_endthread-pre-split, %if_else.if
  %flush_n = phi i32 [ %flush_n.pr, %mode_endthread-pre-split ], [ %.54, %if_else.if ]
  %.641 = icmp sgt i32 %flush_n, 0
  br i1 %.641, label %flush_body.preheader, label %flush_end

flush_body.preheader:                             ; preds = %if_else, %mode_end
  %flush_n6 = phi i32 [ %flush_n, %mode_end ], [ %wqc.1, %if_else ]
  %mb_out7 = load ptr, ptr @__modbus_ctx, align 8
  br label %flush_body

mode_m36121:                                      ; preds = %scan_sensors.endif
  %"\D8\A7\D9\84\D8\B6\D8\BA\D8\B7" = load double, ptr @"s_\D8\A7\D9\84\D8\B6\D8\BA\D8\B7", align 8
  %fcmp = fcmp ogt double %"\D8\A7\D9\84\D8\B6\D8\BA\D8\B7", 8.000000e+00
  br i1 %fcmp, label %if_then, label %if_else

if_then:                                          ; preds = %mode_m36121
  tail call void @mizan_actuator_cmd(i32 0, double 1.000000e+00)
  %wqc = load i32, ptr @__wq_count, align 4
  %.33 = icmp slt i32 %wqc, 64
  br i1 %.33, label %if_then.if, label %if_then.endif

if_else:                                          ; preds = %mode_m36121
  tail call void @mizan_actuator_cmd(i32 0, double 0.000000e+00)
  %wqc.1 = load i32, ptr @__wq_count, align 4
  %.48 = icmp slt i32 %wqc.1, 64
  br i1 %.48, label %if_else.if, label %flush_body.preheader

if_then.if:                                       ; preds = %if_then
  %0 = sext i32 %wqc to i64
  %.35 = getelementptr inbounds [64 x i32], ptr @__wq_addrs, i64 0, i64 %0
  %.36 = getelementptr inbounds [64 x double], ptr @__wq_values, i64 0, i64 %0
  store i32 36, ptr %.35, align 4
  store double 1.000000e+00, ptr %.36, align 8
  %.39 = add nsw i32 %wqc, 1
  store i32 %.39, ptr @__wq_count, align 4
  br label %if_then.endif

if_then.endif:                                    ; preds = %if_then.if, %if_then
  tail call void @mizan_alert(i32 1, ptr nonnull @__alert_5)
  br label %mode_endthread-pre-split

if_else.if:                                       ; preds = %if_else
  %1 = sext i32 %wqc.1 to i64
  %.50 = getelementptr inbounds [64 x i32], ptr @__wq_addrs, i64 0, i64 %1
  %.51 = getelementptr inbounds [64 x double], ptr @__wq_values, i64 0, i64 %1
  store i32 36, ptr %.50, align 4
  store double 0.000000e+00, ptr %.51, align 8
  %.54 = add nsw i32 %wqc.1, 1
  store i32 %.54, ptr @__wq_count, align 4
  br label %mode_end

flush_body:                                       ; preds = %flush_body.preheader, %flush_body
  %storemerge2 = phi i32 [ %.72, %flush_body ], [ 0, %flush_body.preheader ]
  %2 = zext nneg i32 %storemerge2 to i64
  %.67 = getelementptr inbounds nuw [64 x i32], ptr @__wq_addrs, i64 0, i64 %2
  %.68 = getelementptr inbounds nuw [64 x double], ptr @__wq_values, i64 0, i64 %2
  %.69 = load i32, ptr %.67, align 4
  %.70 = load double, ptr %.68, align 8
  tail call void @mizan_modbus_write(ptr %mb_out7, i32 %.69, double %.70)
  %.72 = add nuw nsw i32 %storemerge2, 1
  %.64 = icmp samesign ult i32 %.72, %flush_n6
  br i1 %.64, label %flush_body, label %flush_end

flush_end:                                        ; preds = %flush_body, %mode_end
  store i32 0, ptr @__wq_count, align 4
  tail call void @mizan_escalation_tick()
  %rpt_now = tail call i64 @mizan_now_ms()
  %next_fire = load i64, ptr @__rpt_timer_0, align 8
  %.77 = icmp eq i64 %next_fire, -1
  br i1 %.77, label %flush_end.if, label %flush_end.endif

flush_end.if:                                     ; preds = %flush_end
  %.79 = add i64 %rpt_now, 5000
  store i64 %.79, ptr @__rpt_timer_0, align 8
  br label %flush_end.endif

flush_end.endif:                                  ; preds = %flush_end.if, %flush_end
  %.82.not = icmp slt i64 %rpt_now, %next_fire
  br i1 %.82.not, label %flush_end.endif.endif, label %flush_end.endif.if

flush_end.endif.if:                               ; preds = %flush_end.endif
  %.85 = tail call i32 @mizan_actuator_cycles(i32 0)
  %.86 = tail call i32 @mizan_actuator_state(i32 0)
  %.87 = tail call i32 @mizan_sensor_health(i32 0)
  %.89 = tail call i32 (ptr, i64, ptr, ...) @snprintf(ptr nonnull dereferenceable(1) @__rpt_buf, i64 2048, ptr nonnull @__rpt_fmt_6, i32 %.85, i32 %.86, i32 %.87)
  tail call void @mizan_report_write(ptr nonnull @__rpt_id_7, ptr nonnull @__rpt_fmtarg_8, ptr nonnull @__rpt_dir_9, ptr nonnull @__rpt_buf)
  %.94 = add i64 %rpt_now, 5000
  store i64 %.94, ptr @__rpt_timer_0, align 8
  br label %flush_end.endif.endif

flush_end.endif.endif:                            ; preds = %flush_end.endif.if, %flush_end.endif
  %pending.b = load i1, ptr @__pending_goto, align 1
  br i1 %pending.b, label %flush_end.endif.endif.if, label %flush_end.endif.endif.endif

flush_end.endif.endif.if:                         ; preds = %flush_end.endif.endif
  store i1 true, ptr @__current_mode, align 1
  store i1 false, ptr @__pending_goto, align 1
  br label %flush_end.endif.endif.endif

flush_end.endif.endif.endif:                      ; preds = %flush_end.endif.endif.if, %flush_end.endif.endif
  %now = tail call i64 @mizan_now_ms()
  %elapsed.neg = sub i64 %cycle_start, %now
  %remain = add i64 %elapsed.neg, 500
  %.102 = icmp sgt i64 %remain, 0
  br i1 %.102, label %flush_end.endif.endif.endif.if, label %scan_cycle.backedge

flush_end.endif.endif.endif.if:                   ; preds = %flush_end.endif.endif.endif
  tail call void @mizan_sleep_ms(i64 %remain)
  br label %scan_cycle.backedge

scan_cycle.backedge:                              ; preds = %flush_end.endif.endif.endif.if, %flush_end.endif.endif.endif
  br label %scan_cycle
}

attributes #0 = { nofree nounwind }
attributes #1 = { noreturn }
