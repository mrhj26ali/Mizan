; ModuleID = "mizan_program"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define i32 @"main"()
{
entry:
  %"درجة_الحرارة" = alloca double
  store double 0x4039000000000000, double* %"درجة_الحرارة"
  %"عداد_الدورات" = alloca i32
  store i32 0, i32* %"عداد_الدورات"
  %"الحد_الاقصى" = alloca double
  store double 0x4054000000000000, double* %"الحد_الاقصى"
  ret i32 0
}

define void @"مراقبة_المصنع"()
{
entry:
  br label %"while.cond"
while.cond:
  %"عداد_الدورات" = load i32, i32* %"عداد_الدورات"
  %"cmptmp" = icmp slt i32 %"عداد_الدورات", 5
  br i1 %"cmptmp", label %"while.body", label %"while.end"
while.body:
  %"درجة_الحرارة" = load double, double* %"درجة_الحرارة"
  %"addtmp" = fadd double %"درجة_الحرارة", 0x402e000000000000
  store double %"addtmp", double* %"درجة_الحرارة"
  %"عداد_الدورات.1" = load i32, i32* %"عداد_الدورات"
  %"addtmp.1" = add i32 %"عداد_الدورات.1", 1
  store i32 %"addtmp.1", i32* %"عداد_الدورات"
  %".6" = bitcast [61 x i8]* @"str_1" to i8*
  %"printf_call" = call i32 (i8*, ...) @"printf"(i8* %".6")
  %"درجة_الحرارة.1" = load double, double* %"درجة_الحرارة"
  %"الحد_الاقصى" = load double, double* %"الحد_الاقصى"
  %"cmptmp.1" = fcmp ogt double %"درجة_الحرارة.1", %"الحد_الاقصى"
  br i1 %"cmptmp.1", label %"then", label %"else"
while.end:
  ret void
then:
  %".8" = bitcast [92 x i8]* @"str_2" to i8*
  %"printf_call.1" = call i32 (i8*, ...) @"printf"(i8* %".8")
  %".9" = bitcast [66 x i8]* @"str_3" to i8*
  %"printf_call.2" = call i32 (i8*, ...) @"printf"(i8* %".9")
  br label %"ifmerge"
ifmerge:
  br label %"while.cond"
else:
  %".11" = bitcast [57 x i8]* @"str_4" to i8*
  %"printf_call.3" = call i32 (i8*, ...) @"printf"(i8* %".11")
  br label %"ifmerge"
}

@"str_1" = constant [61 x i8] c"[\d8\b3\d8\ac\d9\84] \d8\a7\d9\84\d8\af\d9\88\d8\b1\d8\a9 \d8\a7\d9\84\d8\ad\d8\a7\d9\84\d9\8a\d8\a9: \d9\81\d8\ad\d8\b5 \d8\a7\d9\84\d8\ad\d8\b1\d8\a7\d8\b1\d8\a9\0a\00"
@"str_2" = constant [92 x i8] c"[\d8\aa\d9\86\d8\a8\d9\8a\d9\87 \d9\85\d8\b3\d8\aa\d9\88\d9\89_1] \d8\aa\d8\ad\d8\b0\d9\8a\d8\b1: \d8\a7\d9\84\d8\ad\d8\b1\d8\a7\d8\b1\d8\a9 \d8\aa\d8\ac\d8\a7\d9\88\d8\b2\d8\aa \d8\a7\d9\84\d8\ad\d8\af \d8\a7\d9\84\d9\85\d8\b3\d9\85\d9\88\d8\ad!\0a\00"
@"str_3" = constant [66 x i8] c"[\d8\a3\d9\85\d8\b1] \d8\a5\d8\b1\d8\b3\d8\a7\d9\84 \d8\a5\d9\84\d9\89 '\d9\85\d9\86\d8\a8\d9\87_\d8\a7\d9\84\d9\86\d8\b8\d8\a7\d9\85' -> \d8\aa\d8\b4\d8\ba\d9\8a\d9\84\0a\00"
@"str_4" = constant [57 x i8] c"[\d8\b3\d8\ac\d9\84] \d8\a7\d9\84\d8\ad\d8\b1\d8\a7\d8\b1\d8\a9 \d8\b6\d9\85\d9\86 \d8\a7\d9\84\d9\86\d8\b7\d8\a7\d9\82 \d8\a7\d9\84\d8\a7\d9\85\d9\86.\0a\00"