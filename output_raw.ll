; ModuleID = "mizan_program"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare double @"read_sensor_register"(i32 %".1")

declare void @"write_actuator_register"(i32 %".1", double %".2")

declare void @"panic_div_zero"()

declare void @"setup_arabic_console"()

declare void @"print_arabic"(i8* %".1")

@"العمر" = global i32 0
@"السنة_القادمة" = global i32 0
define void @"تشغيل_النظام"()
{
entry:
  %"العمر" = load i32, i32* @"العمر"
  %"addtmp" = add i32 %"العمر", 1
  store i32 %"addtmp", i32* @"السنة_القادمة"
  %".3" = bitcast [39 x i8]* @"str_0" to i8*
  call void @"print_arabic"(i8* %".3")
  %".5" = bitcast [2 x i8]* @"str_1" to i8*
  %".6" = call i32 (i8*, ...) @"printf"(i8* %".5")
  %".7" = bitcast [53 x i8]* @"str_2" to i8*
  call void @"print_arabic"(i8* %".7")
  %".9" = bitcast [2 x i8]* @"str_3" to i8*
  %".10" = call i32 (i8*, ...) @"printf"(i8* %".9")
  %".11" = bitcast [59 x i8]* @"str_4" to i8*
  call void @"print_arabic"(i8* %".11")
  %".13" = bitcast [2 x i8]* @"str_5" to i8*
  %".14" = call i32 (i8*, ...) @"printf"(i8* %".13")
  %".15" = bitcast [53 x i8]* @"str_6" to i8*
  call void @"print_arabic"(i8* %".15")
  %".17" = bitcast [2 x i8]* @"str_7" to i8*
  %".18" = call i32 (i8*, ...) @"printf"(i8* %".17")
  %".19" = bitcast [46 x i8]* @"str_8" to i8*
  call void @"print_arabic"(i8* %".19")
  %".21" = bitcast [2 x i8]* @"str_9" to i8*
  %".22" = call i32 (i8*, ...) @"printf"(i8* %".21")
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

@"str_0" = constant [39 x i8] c"[\d8\b3\d8\ac\d9\84] \d9\83\d8\aa\d8\a7\d8\a8\d8\8c \d8\a8\d8\a7\d8\a8\d8\a7\d8\8c \d9\82\d9\84\d9\85.\00"
@"str_1" = constant [2 x i8] c"\0a\00"
@"str_2" = constant [53 x i8] c"[\d8\b3\d8\ac\d9\84] \d9\82\d8\a7\d9\84: \d8\a7\d9\84\d8\a7\d8\b3\d9\84\d8\a7\d9\85\d8\8c \d8\a7\d9\84\d9\84\d9\87\d8\8c \d9\84\d8\a7\d9\86.\00"
@"str_3" = constant [2 x i8] c"\0a\00"
@"str_4" = constant [59 x i8] c"[\d8\b3\d8\ac\d9\84] \d8\a7\d9\84\d8\ad\d8\b1\d8\a7\d8\b1\d8\a9 \d8\a7\d9\84\d9\8a\d9\88\d9\85 25 \d8\af\d8\b1\d8\ac\d8\a9 \d9\85\d8\a6\d9\88\d9\8a\d8\a9.\00"
@"str_5" = constant [2 x i8] c"\0a\00"
@"str_6" = constant [53 x i8] c"[\d8\b3\d8\ac\d9\84] \d8\a7\d9\84\d8\a7\d8\b5\d8\af\d8\a7\d8\b1 v1.0 \d9\85\d9\86 \d9\84\d8\ba\d8\a9 \d9\85\d9\8a\d8\b2\d8\a7\d9\86.\00"
@"str_7" = constant [2 x i8] c"\0a\00"
@"str_8" = constant [46 x i8] c"[\d8\b3\d8\ac\d9\84] \d8\aa\d9\85 \d8\ad\d8\b3\d8\a7\d8\a8 \d8\a7\d9\84\d8\b9\d9\85\d8\b1 \d8\a8\d9\86\d8\ac\d8\a7\d8\ad.\00"
@"str_9" = constant [2 x i8] c"\0a\00"