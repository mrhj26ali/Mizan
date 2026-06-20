; ModuleID = "mizan_program"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare double @"read_sensor_register"(i32 %".1")

declare void @"write_actuator_register"(i32 %".1", double %".2")

declare void @"panic_div_zero"()

declare void @"setup_arabic_console"()

@"العمر" = global i32 0
@"السنة_القادمة" = global i32 0
define void @"تشغيل_النظام"()
{
entry:
  %"العمر" = load i32, i32* @"العمر"
  %"addtmp" = add i32 %"العمر", 1
  store i32 %"addtmp", i32* @"السنة_القادمة"
  %".3" = bitcast [67 x i8]* @"str_0" to i8*
  %".4" = call i32 (i8*, ...) @"printf"(i8* %".3")
  %".5" = bitcast [47 x i8]* @"str_1" to i8*
  %".6" = call i32 (i8*, ...) @"printf"(i8* %".5")
  ret void
}

define i32 @"main"()
{
entry:
  call void @"setup_arabic_console"()
  store i32 25, i32* @"العمر"
  store i32 0, i32* @"السنة_القادمة"
  call void @"تشغيل_النظام"()
  ret i32 0
}

@"str_0" = constant [67 x i8] c"[\d8\b3\d8\ac\d9\84] \d8\a7\d9\87\d9\84\d8\a7 \d8\a8\d9\83 \d9\81\d9\8a \d9\84\d8\ba\d8\aa\d9\83 \d8\a7\d9\84\d8\b9\d8\b1\d8\a8\d9\8a\d8\a9 \d8\a7\d9\84\d8\ae\d8\a7\d8\b5\d8\a9!\0a\00"
@"str_1" = constant [47 x i8] c"[\d8\b3\d8\ac\d9\84] \d8\aa\d9\85 \d8\ad\d8\b3\d8\a7\d8\a8 \d8\a7\d9\84\d8\b9\d9\85\d8\b1 \d8\a8\d9\86\d8\ac\d8\a7\d8\ad.\0a\00"