; ModuleID = "mizan_program"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare double @"read_sensor_register"(i32 %".1")

declare void @"write_actuator_register"(i32 %".1", double %".2")

@"درجة_الحرارة" = global double              0x0
@"عداد_الدورات" = global i32 0
@"الحد_الاقصى" = constant double              0x0
define void @"مراقبة_المصنع"()
{
entry:
  ret void
}

define i32 @"main"()
{
entry:
  store double 0x4039000000000000, double* @"درجة_الحرارة"
  store i32 0, i32* @"عداد_الدورات"
  store double 0x4054000000000000, double* @"الحد_الاقصى"
  ret i32 0
}
