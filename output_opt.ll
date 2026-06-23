; ModuleID = '<string>'
source_filename = "<string>"
target triple = "x86_64-pc-windows-msvc"

@__modbus_ctx = internal unnamed_addr global ptr null
@__mqtt_ctx = internal unnamed_addr global ptr null
@__log_1 = private constant [58 x i8] c"[\D8\B3\D8\AC\D9\84] \D9\85\D8\B1\D8\AD\D8\A8\D8\A7 \D8\A8\D8\A7\D9\84\D8\B9\D8\A7\D9\84\D9\85 \D9\85\D9\86 \D9\84\D8\BA\D8\A9 \D9\85\D9\8A\D8\B2\D8\A7\D9\86\00"
@__log_2 = private constant [56 x i8] c"[\D8\B3\D8\AC\D9\84] \D9\87\D8\B0\D9\87 \D9\84\D8\BA\D8\A9 \D8\A8\D8\B1\D9\85\D8\AC\D8\A9 \D8\B9\D8\B1\D8\A8\D9\8A\D8\A9 \D9\85\D8\AC\D9\85\D8\B9\D8\A9\00"
@__dev_ip_3 = private constant [10 x i8] c"127.0.0.1\00"
@__mq_host_4 = private constant [10 x i8] c"127.0.0.1\00"
@__mq_cid_5 = private constant [14 x i8] c"mizan-runtime\00"

declare void @setup_arabic_console() local_unnamed_addr

declare void @mizan_log(ptr) local_unnamed_addr

declare ptr @mizan_modbus_connect(ptr, i32) local_unnamed_addr

declare ptr @mizan_mqtt_connect(ptr, i32, ptr) local_unnamed_addr

declare void @__mizan_set_mqtt_ctx(ptr) local_unnamed_addr

declare i64 @mizan_now_ms() local_unnamed_addr

declare void @mizan_sleep_ms(i64) local_unnamed_addr

declare void @mizan_escalation_tick() local_unnamed_addr

define void @"proc_\D8\A7\D9\84\D8\B1\D8\A6\D9\8A\D8\B3\D9\8A"() local_unnamed_addr {
entry:
  tail call void @mizan_log(ptr nonnull @__log_1)
  tail call void @mizan_log(ptr nonnull @__log_2)
  ret void
}

; Function Attrs: noreturn
define noundef i32 @main() local_unnamed_addr #0 {
entry:
  tail call void @setup_arabic_console()
  %.4 = tail call ptr @mizan_modbus_connect(ptr nonnull @__dev_ip_3, i32 5020)
  store ptr %.4, ptr @__modbus_ctx, align 8
  %.8 = tail call ptr @mizan_mqtt_connect(ptr nonnull @__mq_host_4, i32 1884, ptr nonnull @__mq_cid_5)
  store ptr %.8, ptr @__mqtt_ctx, align 8
  tail call void @__mizan_set_mqtt_ctx(ptr %.8)
  tail call void @mizan_log(ptr nonnull @__log_1)
  tail call void @mizan_log(ptr nonnull @__log_2)
  br label %scan_cycle

scan_cycle:                                       ; preds = %scan_cycle.backedge, %entry
  %cycle_start = tail call i64 @mizan_now_ms()
  tail call void @mizan_escalation_tick()
  %now = tail call i64 @mizan_now_ms()
  %elapsed.neg = sub i64 %cycle_start, %now
  %remain = add i64 %elapsed.neg, 1000
  %.38 = icmp sgt i64 %remain, 0
  br i1 %.38, label %flush_end.endif.if, label %scan_cycle.backedge

flush_end.endif.if:                               ; preds = %scan_cycle
  tail call void @mizan_sleep_ms(i64 %remain)
  br label %scan_cycle.backedge

scan_cycle.backedge:                              ; preds = %flush_end.endif.if, %scan_cycle
  br label %scan_cycle
}

attributes #0 = { noreturn }
