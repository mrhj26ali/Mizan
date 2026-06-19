; ModuleID = 'C:\Users\DELL\AppData\Local\Temp\tmpr6iemwyw.ll'
source_filename = "C:\\Users\\DELL\\AppData\\Local\\Temp\\tmpr6iemwyw.ll"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.33.0"

@"\D8\B3" = local_unnamed_addr global i32 0
@"\D8\B5" = local_unnamed_addr global i32 0
@"\D8\B9" = local_unnamed_addr global double 0.000000e+00
@"\D9\85\D8\AC\D9\87\D9\88\D9\84" = local_unnamed_addr global i32 0
@"\D8\A7\D9\84\D9\86\D8\AA\D9\8A\D8\AC\D8\A9" = local_unnamed_addr global double 0.000000e+00

; Function Attrs: mustprogress nofree norecurse nosync nounwind willreturn memory(write, argmem: none, inaccessiblemem: none)
define noundef i32 @main() local_unnamed_addr #0 {
entry:
  store i32 5, ptr @"\D8\B3", align 4
  store i32 10, ptr @"\D8\B5", align 4
  store double 1.500000e+01, ptr @"\D8\B9", align 8
  store i32 999, ptr @"\D9\85\D8\AC\D9\87\D9\88\D9\84", align 4
  store double 1.000000e+01, ptr @"\D8\A7\D9\84\D9\86\D8\AA\D9\8A\D8\AC\D8\A9", align 8
  ret i32 0
}

attributes #0 = { mustprogress nofree norecurse nosync nounwind willreturn memory(write, argmem: none, inaccessiblemem: none) }
