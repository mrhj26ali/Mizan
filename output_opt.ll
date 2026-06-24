; ModuleID = '<string>'
source_filename = "<string>"
target triple = "x86_64-pc-windows-msvc"

@"g_\D8\B9\D8\AF\D8\A7\D8\AF" = internal unnamed_addr global i32 0
@__modbus_ctx = internal unnamed_addr global ptr null
@__mqtt_ctx = internal unnamed_addr global ptr null
@__log_1 = private constant [61 x i8] c"\D8\AE\D8\B7\D8\A7: \D8\A7\D9\84\D8\B2\D9\85\D9\86 \D9\8A\D8\AC\D8\A8 \D8\A7\D9\86 \D9\8A\D9\83\D9\88\D9\86 \D8\A7\D9\83\D8\A8\D8\B1 \D9\85\D9\86 \D8\B5\D9\81\D8\B1\00"
@__dev_ip_2 = private constant [10 x i8] c"127.0.0.1\00"
@__mq_host_3 = private constant [10 x i8] c"127.0.0.1\00"
@__mq_cid_4 = private constant [14 x i8] c"mizan-runtime\00"
@__log_5 = private constant [35 x i8] c"\D8\A8\D8\AF\D8\A1 \D8\A7\D8\AE\D8\AA\D8\A8\D8\A7\D8\B1 \D8\A7\D9\84\D9\88\D8\AD\D8\AF\D8\A7\D8\AA\00"
@__alert_6 = private constant [50 x i8] c"[\D8\AA\D9\86\D8\A8\D9\8A\D9\87 \D9\85\D8\B3\D8\AA\D9\88\D9\89_1] \D8\A7\D9\84\D8\B3\D8\B1\D8\B9\D8\A9 \D8\B9\D8\A7\D9\84\D9\8A\D8\A9\00"
@__log_8 = private constant [22 x i8] c"\D8\AF\D9\88\D8\B1\D8\A9 \D8\AD\D8\B3\D8\A7\D8\A8\D9\8A\D8\A9\00"

declare void @setup_arabic_console() local_unnamed_addr

declare void @mizan_log(ptr) local_unnamed_addr

declare void @mizan_alert(i32, ptr) local_unnamed_addr

declare ptr @mizan_modbus_connect(ptr, i32) local_unnamed_addr

declare ptr @mizan_mqtt_connect(ptr, i32, ptr) local_unnamed_addr

declare void @__mizan_set_mqtt_ctx(ptr) local_unnamed_addr

declare i64 @mizan_now_ms() local_unnamed_addr

declare void @mizan_sleep_ms(i64) local_unnamed_addr

declare void @mizan_escalation_tick() local_unnamed_addr

define double @"proc_\D8\AD\D8\B3\D8\A7\D8\A8_\D8\A7\D9\84\D8\B3\D8\B1\D8\B9\D8\A9"(double %"\D8\A7\D9\84\D9\85\D8\B3\D8\A7\D9\81\D8\A9", double %"\D8\A7\D9\84\D8\B2\D9\85\D9\86") local_unnamed_addr {
entry:
  %fcmp = fcmp ugt double %"\D8\A7\D9\84\D8\B2\D9\85\D9\86", 0.000000e+00
  br i1 %fcmp, label %if_end, label %if_then

common.ret:                                       ; preds = %if_end, %if_then
  %common.ret.op = phi double [ 0.000000e+00, %if_then ], [ %fdiv, %if_end ]
  ret double %common.ret.op

if_then:                                          ; preds = %entry
  tail call void @mizan_log(ptr nonnull @__log_1)
  br label %common.ret

if_end:                                           ; preds = %entry
  %fdiv = fdiv double %"\D8\A7\D9\84\D9\85\D8\B3\D8\A7\D9\81\D8\A9", %"\D8\A7\D9\84\D8\B2\D9\85\D9\86"
  br label %common.ret
}

; Function Attrs: noreturn
define noundef i32 @main() local_unnamed_addr #0 {
if_end:
  tail call void @setup_arabic_console()
  %.4 = tail call ptr @mizan_modbus_connect(ptr nonnull @__dev_ip_2, i32 5020)
  store ptr %.4, ptr @__modbus_ctx, align 8
  %.8 = tail call ptr @mizan_mqtt_connect(ptr nonnull @__mq_host_3, i32 1884, ptr nonnull @__mq_cid_4)
  store ptr %.8, ptr @__mqtt_ctx, align 8
  tail call void @__mizan_set_mqtt_ctx(ptr %.8)
  store i32 0, ptr @"g_\D8\B9\D8\AF\D8\A7\D8\AF", align 4
  tail call void @mizan_log(ptr nonnull @__log_5)
  tail call void @mizan_alert(i32 1, ptr nonnull @__alert_6)
  %"\D8\B9\D8\AF\D8\A7\D8\AF.pr" = load i32, ptr @"g_\D8\B9\D8\AF\D8\A7\D8\AF", align 4
  %icmp1 = icmp slt i32 %"\D8\B9\D8\AF\D8\A7\D8\AF.pr", 2
  br i1 %icmp1, label %while_body, label %scan_cycle.preheader

while_body:                                       ; preds = %if_end, %while_body
  tail call void @mizan_log(ptr nonnull @__log_8)
  %"\D8\B9\D8\AF\D8\A7\D8\AF.1" = load i32, ptr @"g_\D8\B9\D8\AF\D8\A7\D8\AF", align 4
  %add = add i32 %"\D8\B9\D8\AF\D8\A7\D8\AF.1", 1
  store i32 %add, ptr @"g_\D8\B9\D8\AF\D8\A7\D8\AF", align 4
  %icmp = icmp slt i32 %add, 2
  br i1 %icmp, label %while_body, label %scan_cycle.preheader

scan_cycle.preheader:                             ; preds = %while_body, %if_end
  br label %scan_cycle

scan_cycle:                                       ; preds = %scan_cycle.backedge, %scan_cycle.preheader
  %cycle_start = tail call i64 @mizan_now_ms()
  tail call void @mizan_escalation_tick()
  %now = tail call i64 @mizan_now_ms()
  %elapsed.neg = sub i64 %cycle_start, %now
  %remain = add i64 %elapsed.neg, 1000
  %.57 = icmp sgt i64 %remain, 0
  br i1 %.57, label %flush_end.endif.if, label %scan_cycle.backedge

flush_end.endif.if:                               ; preds = %scan_cycle
  tail call void @mizan_sleep_ms(i64 %remain)
  br label %scan_cycle.backedge

scan_cycle.backedge:                              ; preds = %flush_end.endif.if, %scan_cycle
  br label %scan_cycle
}

attributes #0 = { noreturn }
