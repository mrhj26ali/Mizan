; ModuleID = '<string>'
source_filename = "<string>"
target triple = "x86_64-pc-windows-msvc"

@"s_\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9" = internal unnamed_addr global double 0.000000e+00
@__modbus_ctx = internal unnamed_addr global ptr null
@__mqtt_ctx = internal unnamed_addr global ptr null
@__current_mode = internal unnamed_addr global i1 false
@__pending_goto = internal unnamed_addr global i1 false
@__wq_addrs = internal unnamed_addr global [64 x i32] zeroinitializer
@__wq_values = internal unnamed_addr global [64 x double] zeroinitializer
@__wq_count = internal unnamed_addr global i32 0
@__dev_ip_1 = private constant [10 x i8] c"127.0.0.1\00"
@__mq_host_2 = private constant [10 x i8] c"127.0.0.1\00"
@__mq_cid_3 = private constant [14 x i8] c"mizan-runtime\00"
@__log_4 = private constant [55 x i8] c"\D8\A8\D8\AF\D8\A1 \D8\A7\D8\AE\D8\AA\D8\A8\D8\A7\D8\B1 \D8\A7\D9\84\D8\A7\D9\85\D8\A7\D9\86 \D8\A7\D9\84\D9\81\D9\8A\D8\B2\D9\8A\D8\A7\D8\A6\D9\8A...\00"
@__sustain_2561222929984 = internal unnamed_addr global i64 -1
@__log_5 = private constant [68 x i8] c"\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9 \D9\85\D8\B1\D8\AA\D9\81\D8\B9\D8\A9 \D8\A8\D8\A7\D8\B3\D8\AA\D9\85\D8\B1\D8\A7\D8\B1\D8\8C \D8\AA\D8\B4\D8\BA\D9\8A\D9\84 \D8\A7\D9\84\D9\85\D8\B6\D8\AE\D8\A9.\00"

declare void @setup_arabic_console() local_unnamed_addr

declare void @mizan_log(ptr) local_unnamed_addr

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

declare void @mizan_actuator_cmd(i32, double) local_unnamed_addr

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
  %.17 = icmp eq i32 %global_conn, 0
  br i1 %.17, label %safe_state_flush, label %scan_sensors

safe_state_flush:                                 ; preds = %scan_cycle
  store i32 0, ptr @__wq_count, align 4
  br label %scan_sensors

scan_sensors:                                     ; preds = %safe_state_flush, %scan_cycle
  %"raw_\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9" = tail call double @mizan_modbus_read(ptr %mb, i32 8)
  store double %"raw_\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9", ptr @"s_\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9", align 8
  %"conn_\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9" = tail call i32 @mizan_modbus_is_connected(ptr %mb)
  %.24.not = icmp eq i32 %"conn_\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9", 0
  br i1 %.24.not, label %scan_sensors.endif, label %scan_sensors.if

scan_sensors.if:                                  ; preds = %scan_sensors
  tail call void @mizan_ring_push(i32 0, double %"raw_\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9")
  br label %scan_sensors.endif

scan_sensors.endif:                               ; preds = %scan_sensors.if, %scan_sensors
  %cur_mode.b = load i1, ptr @__current_mode, align 1
  br i1 %cur_mode.b, label %mode_m77285, label %mode_endthread-pre-split

mode_endthread-pre-split:                         ; preds = %scan_sensors.endif, %if_then.endif
  %flush_n.pr = load i32, ptr @__wq_count, align 4
  br label %mode_end

mode_end:                                         ; preds = %mode_endthread-pre-split, %if_else.if
  %flush_n = phi i32 [ %flush_n.pr, %mode_endthread-pre-split ], [ %.70, %if_else.if ]
  %.802 = icmp sgt i32 %flush_n, 0
  br i1 %.802, label %flush_body.preheader, label %flush_end

flush_body.preheader:                             ; preds = %if_else, %mode_end
  %flush_n8 = phi i32 [ %flush_n, %mode_end ], [ %wqc.1, %if_else ]
  %mb_out9 = load ptr, ptr @__modbus_ctx, align 8
  br label %flush_body

mode_m77285:                                      ; preds = %scan_sensors.endif
  %"\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9" = load double, ptr @"s_\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9", align 8
  %fcmp = fcmp ogt double %"\D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9", 9.000000e+01
  %t_now = tail call i64 @mizan_now_ms()
  br i1 %fcmp, label %sus_true, label %sus_false

sus_true:                                         ; preds = %mode_m77285
  %.32 = load i64, ptr @__sustain_2561222929984, align 8
  %.33 = icmp eq i64 %.32, -1
  br i1 %.33, label %sus_set, label %sus_chk

sus_false:                                        ; preds = %mode_m77285
  store i64 -1, ptr @__sustain_2561222929984, align 8
  br label %if_else

sus_set:                                          ; preds = %sus_true
  store i64 %t_now, ptr @__sustain_2561222929984, align 8
  br label %sus_chk

sus_chk:                                          ; preds = %sus_set, %sus_true
  %.37 = phi i64 [ %t_now, %sus_set ], [ %.32, %sus_true ]
  %.38 = sub i64 %t_now, %.37
  %.39 = icmp sgt i64 %.38, 4999
  br i1 %.39, label %if_then, label %if_else

if_then:                                          ; preds = %sus_chk
  tail call void @mizan_actuator_cmd(i32 0, double 1.000000e+00)
  %wqc = load i32, ptr @__wq_count, align 4
  %.49 = icmp slt i32 %wqc, 64
  br i1 %.49, label %if_then.if, label %if_then.endif

if_else:                                          ; preds = %sus_false, %sus_chk
  tail call void @mizan_actuator_cmd(i32 0, double 0.000000e+00)
  %wqc.1 = load i32, ptr @__wq_count, align 4
  %.64 = icmp slt i32 %wqc.1, 64
  br i1 %.64, label %if_else.if, label %flush_body.preheader

if_then.if:                                       ; preds = %if_then
  %0 = sext i32 %wqc to i64
  %.51 = getelementptr inbounds [64 x i32], ptr @__wq_addrs, i64 0, i64 %0
  %.52 = getelementptr inbounds [64 x double], ptr @__wq_values, i64 0, i64 %0
  store i32 34, ptr %.51, align 4
  store double 1.000000e+00, ptr %.52, align 8
  %.55 = add nsw i32 %wqc, 1
  store i32 %.55, ptr @__wq_count, align 4
  br label %if_then.endif

if_then.endif:                                    ; preds = %if_then.if, %if_then
  tail call void @mizan_log(ptr nonnull @__log_5)
  br label %mode_endthread-pre-split

if_else.if:                                       ; preds = %if_else
  %1 = sext i32 %wqc.1 to i64
  %.66 = getelementptr inbounds [64 x i32], ptr @__wq_addrs, i64 0, i64 %1
  %.67 = getelementptr inbounds [64 x double], ptr @__wq_values, i64 0, i64 %1
  store i32 34, ptr %.66, align 4
  store double 0.000000e+00, ptr %.67, align 8
  %.70 = add nsw i32 %wqc.1, 1
  store i32 %.70, ptr @__wq_count, align 4
  br label %mode_end

flush_body:                                       ; preds = %flush_body.preheader, %flush_body
  %storemerge13 = phi i32 [ %.88, %flush_body ], [ 0, %flush_body.preheader ]
  %2 = zext nneg i32 %storemerge13 to i64
  %.83 = getelementptr inbounds nuw [64 x i32], ptr @__wq_addrs, i64 0, i64 %2
  %.84 = getelementptr inbounds nuw [64 x double], ptr @__wq_values, i64 0, i64 %2
  %.85 = load i32, ptr %.83, align 4
  %.86 = load double, ptr %.84, align 8
  tail call void @mizan_modbus_write(ptr %mb_out9, i32 %.85, double %.86)
  %.88 = add nuw nsw i32 %storemerge13, 1
  %.80 = icmp samesign ult i32 %.88, %flush_n8
  br i1 %.80, label %flush_body, label %flush_end

flush_end:                                        ; preds = %flush_body, %mode_end
  store i32 0, ptr @__wq_count, align 4
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
  %.98 = icmp sgt i64 %remain, 0
  br i1 %.98, label %flush_end.endif.if, label %scan_cycle.backedge

flush_end.endif.if:                               ; preds = %flush_end.endif
  tail call void @mizan_sleep_ms(i64 %remain)
  br label %scan_cycle.backedge

scan_cycle.backedge:                              ; preds = %flush_end.endif.if, %flush_end.endif
  br label %scan_cycle
}

attributes #0 = { noreturn }
