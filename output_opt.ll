; ModuleID = 'C:\Users\DELL\AppData\Local\Temp\tmpa2lanws2.ll'
source_filename = "C:\\Users\\DELL\\AppData\\Local\\Temp\\tmpa2lanws2.ll"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.33.0"

@"\D8\A7\D9\84\D8\B9\D9\85\D8\B1" = local_unnamed_addr global i32 0
@"\D8\A7\D9\84\D8\B3\D9\86\D8\A9_\D8\A7\D9\84\D9\82\D8\A7\D8\AF\D9\85\D8\A9" = local_unnamed_addr global i32 0
@str_0 = local_unnamed_addr constant [67 x i8] c"[\D8\B3\D8\AC\D9\84] \D8\A7\D9\87\D9\84\D8\A7 \D8\A8\D9\83 \D9\81\D9\8A \D9\84\D8\BA\D8\AA\D9\83 \D8\A7\D9\84\D8\B9\D8\B1\D8\A8\D9\8A\D8\A9 \D8\A7\D9\84\D8\AE\D8\A7\D8\B5\D8\A9!\0A\00"
@str_1 = local_unnamed_addr constant [47 x i8] c"[\D8\B3\D8\AC\D9\84] \D8\AA\D9\85 \D8\AD\D8\B3\D8\A7\D8\A8 \D8\A7\D9\84\D8\B9\D9\85\D8\B1 \D8\A8\D9\86\D8\AC\D8\A7\D8\AD.\0A\00"
@str = private unnamed_addr constant [66 x i8] c"[\D8\B3\D8\AC\D9\84] \D8\A7\D9\87\D9\84\D8\A7 \D8\A8\D9\83 \D9\81\D9\8A \D9\84\D8\BA\D8\AA\D9\83 \D8\A7\D9\84\D8\B9\D8\B1\D8\A8\D9\8A\D8\A9 \D8\A7\D9\84\D8\AE\D8\A7\D8\B5\D8\A9!\00", align 1
@str.1 = private unnamed_addr constant [46 x i8] c"[\D8\B3\D8\AC\D9\84] \D8\AA\D9\85 \D8\AD\D8\B3\D8\A7\D8\A8 \D8\A7\D9\84\D8\B9\D9\85\D8\B1 \D8\A8\D9\86\D8\AC\D8\A7\D8\AD.\00", align 1

declare void @setup_arabic_console() local_unnamed_addr

; Function Attrs: nofree nounwind
define void @"\D8\AA\D8\B4\D8\BA\D9\8A\D9\84_\D8\A7\D9\84\D9\86\D8\B8\D8\A7\D9\85"() local_unnamed_addr #0 {
entry:
  %"\D8\A7\D9\84\D8\B9\D9\85\D8\B1" = load i32, ptr @"\D8\A7\D9\84\D8\B9\D9\85\D8\B1", align 4
  %addtmp = add i32 %"\D8\A7\D9\84\D8\B9\D9\85\D8\B1", 1
  store i32 %addtmp, ptr @"\D8\A7\D9\84\D8\B3\D9\86\D8\A9_\D8\A7\D9\84\D9\82\D8\A7\D8\AF\D9\85\D8\A9", align 4
  %puts = tail call i32 @puts(ptr nonnull dereferenceable(1) @str)
  %puts1 = tail call i32 @puts(ptr nonnull dereferenceable(1) @str.1)
  ret void
}

define noundef i32 @main() local_unnamed_addr {
entry:
  tail call void @setup_arabic_console()
  store i32 25, ptr @"\D8\A7\D9\84\D8\B9\D9\85\D8\B1", align 4
  store i32 26, ptr @"\D8\A7\D9\84\D8\B3\D9\86\D8\A9_\D8\A7\D9\84\D9\82\D8\A7\D8\AF\D9\85\D8\A9", align 4
  %puts.i = tail call i32 @puts(ptr nonnull dereferenceable(1) @str)
  %puts1.i = tail call i32 @puts(ptr nonnull dereferenceable(1) @str.1)
  ret i32 0
}

; Function Attrs: nofree nounwind
declare noundef i32 @puts(ptr nocapture noundef readonly) local_unnamed_addr #0

attributes #0 = { nofree nounwind }
