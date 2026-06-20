; ModuleID = 'C:\Users\DELL\AppData\Local\Temp\tmplpne8ziq.ll'
source_filename = "C:\\Users\\DELL\\AppData\\Local\\Temp\\tmplpne8ziq.ll"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.33.0"

@"\D8\A7\D9\84\D8\B9\D9\85\D8\B1" = local_unnamed_addr global i32 0
@"\D8\A7\D9\84\D8\B3\D9\86\D8\A9_\D8\A7\D9\84\D9\82\D8\A7\D8\AF\D9\85\D8\A9" = local_unnamed_addr global i32 0
@str_0 = constant [39 x i8] c"[\D8\B3\D8\AC\D9\84] \D9\83\D8\AA\D8\A7\D8\A8\D8\8C \D8\A8\D8\A7\D8\A8\D8\A7\D8\8C \D9\82\D9\84\D9\85.\00"
@str_1 = local_unnamed_addr constant [2 x i8] c"\0A\00"
@str_2 = constant [53 x i8] c"[\D8\B3\D8\AC\D9\84] \D9\82\D8\A7\D9\84: \D8\A7\D9\84\D8\A7\D8\B3\D9\84\D8\A7\D9\85\D8\8C \D8\A7\D9\84\D9\84\D9\87\D8\8C \D9\84\D8\A7\D9\86.\00"
@str_3 = local_unnamed_addr constant [2 x i8] c"\0A\00"
@str_4 = constant [59 x i8] c"[\D8\B3\D8\AC\D9\84] \D8\A7\D9\84\D8\AD\D8\B1\D8\A7\D8\B1\D8\A9 \D8\A7\D9\84\D9\8A\D9\88\D9\85 25 \D8\AF\D8\B1\D8\AC\D8\A9 \D9\85\D8\A6\D9\88\D9\8A\D8\A9.\00"
@str_5 = local_unnamed_addr constant [2 x i8] c"\0A\00"
@str_6 = constant [53 x i8] c"[\D8\B3\D8\AC\D9\84] \D8\A7\D9\84\D8\A7\D8\B5\D8\AF\D8\A7\D8\B1 v1.0 \D9\85\D9\86 \D9\84\D8\BA\D8\A9 \D9\85\D9\8A\D8\B2\D8\A7\D9\86.\00"
@str_7 = local_unnamed_addr constant [2 x i8] c"\0A\00"
@str_8 = constant [46 x i8] c"[\D8\B3\D8\AC\D9\84] \D8\AA\D9\85 \D8\AD\D8\B3\D8\A7\D8\A8 \D8\A7\D9\84\D8\B9\D9\85\D8\B1 \D8\A8\D9\86\D8\AC\D8\A7\D8\AD.\00"
@str_9 = local_unnamed_addr constant [2 x i8] c"\0A\00"

declare void @setup_arabic_console() local_unnamed_addr

declare void @print_arabic(ptr) local_unnamed_addr

define void @"\D8\AA\D8\B4\D8\BA\D9\8A\D9\84_\D8\A7\D9\84\D9\86\D8\B8\D8\A7\D9\85"() local_unnamed_addr {
entry:
  %"\D8\A7\D9\84\D8\B9\D9\85\D8\B1" = load i32, ptr @"\D8\A7\D9\84\D8\B9\D9\85\D8\B1", align 4
  %addtmp = add i32 %"\D8\A7\D9\84\D8\B9\D9\85\D8\B1", 1
  store i32 %addtmp, ptr @"\D8\A7\D9\84\D8\B3\D9\86\D8\A9_\D8\A7\D9\84\D9\82\D8\A7\D8\AF\D9\85\D8\A9", align 4
  tail call void @print_arabic(ptr nonnull @str_0)
  %putchar = tail call i32 @putchar(i32 10)
  tail call void @print_arabic(ptr nonnull @str_2)
  %putchar1 = tail call i32 @putchar(i32 10)
  tail call void @print_arabic(ptr nonnull @str_4)
  %putchar2 = tail call i32 @putchar(i32 10)
  tail call void @print_arabic(ptr nonnull @str_6)
  %putchar3 = tail call i32 @putchar(i32 10)
  tail call void @print_arabic(ptr nonnull @str_8)
  %putchar4 = tail call i32 @putchar(i32 10)
  ret void
}

define noundef i32 @main() local_unnamed_addr {
entry:
  tail call void @setup_arabic_console()
  store i32 25, ptr @"\D8\A7\D9\84\D8\B9\D9\85\D8\B1", align 4
  store i32 26, ptr @"\D8\A7\D9\84\D8\B3\D9\86\D8\A9_\D8\A7\D9\84\D9\82\D8\A7\D8\AF\D9\85\D8\A9", align 4
  tail call void @print_arabic(ptr nonnull @str_0)
  %putchar.i = tail call i32 @putchar(i32 10)
  tail call void @print_arabic(ptr nonnull @str_2)
  %putchar1.i = tail call i32 @putchar(i32 10)
  tail call void @print_arabic(ptr nonnull @str_4)
  %putchar2.i = tail call i32 @putchar(i32 10)
  tail call void @print_arabic(ptr nonnull @str_6)
  %putchar3.i = tail call i32 @putchar(i32 10)
  tail call void @print_arabic(ptr nonnull @str_8)
  %putchar4.i = tail call i32 @putchar(i32 10)
  ret i32 0
}

; Function Attrs: nofree nounwind
declare noundef i32 @putchar(i32 noundef) local_unnamed_addr #0

attributes #0 = { nofree nounwind }
