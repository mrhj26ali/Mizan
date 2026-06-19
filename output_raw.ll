; ModuleID = "mizan_program"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare double @"read_sensor_register"(i32 %".1")

declare void @"write_actuator_register"(i32 %".1", double %".2")

declare void @"panic_div_zero"()

@"س" = global i32 0
@"ص" = global i32 0
@"ع" = global double              0x0
@"مجهول" = global i32 0
@"النتيجة" = global double              0x0
define i32 @"main"()
{
entry:
  store i32 5, i32* @"س"
  store i32 10, i32* @"ص"
  %"س" = load i32, i32* @"س"
  %"ص" = load i32, i32* @"ص"
  %"addtmp" = add i32 %"س", %"ص"
  %"cast_to_float" = sitofp i32 %"addtmp" to double
  store double %"cast_to_float", double* @"ع"
  store i32 999, i32* @"مجهول"
  %"ص.1" = load i32, i32* @"ص"
  %"is_zero_trap" = icmp eq i32 %"ص.1", 0
  br i1 %"is_zero_trap", label %"panic_block", label %"math_block"
panic_block:
  call void @"panic_div_zero"()
  unreachable
math_block:
  %"divtmp" = sdiv i32 100, %"ص.1"
  %"cast_to_float.1" = sitofp i32 %"divtmp" to double
  store double %"cast_to_float.1", double* @"النتيجة"
  ret i32 0
}
