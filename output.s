	.file	"tmpa2lanws2.ll"
	.section	.ltext,"axl",@progbits
	.globl	"تشغيل_النظام"
	.p2align	4
	.type	"تشغيل_النظام",@function
"تشغيل_النظام":
	pushq	%rsi
	subq	$32, %rsp
	movabsq	$"العمر", %rax
	movl	(%rax), %eax
	incl	%eax
	movabsq	$"السنة_القادمة", %rcx
	movl	%eax, (%rcx)
	movabsq	$.Lstr, %rcx
	movabsq	$puts, %rsi
	callq	*%rsi
	movabsq	$.Lstr.1, %rcx
	movq	%rsi, %rax
	addq	$32, %rsp
	popq	%rsi
	rex64 jmpq	*%rax
.Lfunc_end0:
	.size	"تشغيل_النظام", .Lfunc_end0-"تشغيل_النظام"

	.globl	main
	.p2align	4
	.type	main,@function
main:
	.cfi_startproc
	pushq	%rsi
	.cfi_def_cfa_offset 16
	subq	$32, %rsp
	.cfi_def_cfa_offset 48
	.cfi_offset %rsi, -16
	movabsq	$setup_arabic_console, %rax
	callq	*%rax
	movabsq	$"العمر", %rax
	movl	$25, (%rax)
	movabsq	$"السنة_القادمة", %rax
	movl	$26, (%rax)
	movabsq	$.Lstr, %rcx
	movabsq	$puts, %rsi
	callq	*%rsi
	movabsq	$.Lstr.1, %rcx
	callq	*%rsi
	xorl	%eax, %eax
	addq	$32, %rsp
	popq	%rsi
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc

	.type	"العمر",@object
	.section	.lbss,"awl",@nobits
	.globl	"العمر"
	.p2align	2, 0x0
"العمر":
	.long	0
	.size	"العمر", 4

	.type	"السنة_القادمة",@object
	.globl	"السنة_القادمة"
	.p2align	2, 0x0
"السنة_القادمة":
	.long	0
	.size	"السنة_القادمة", 4

	.type	str_0,@object
	.section	.lrodata,"al",@progbits
	.globl	str_0
	.p2align	4, 0x0
str_0:
	.asciz	"[\330\263\330\254\331\204] \330\247\331\207\331\204\330\247 \330\250\331\203 \331\201\331\212 \331\204\330\272\330\252\331\203 \330\247\331\204\330\271\330\261\330\250\331\212\330\251 \330\247\331\204\330\256\330\247\330\265\330\251!\n"
	.size	str_0, 67

	.type	str_1,@object
	.globl	str_1
	.p2align	4, 0x0
str_1:
	.asciz	"[\330\263\330\254\331\204] \330\252\331\205 \330\255\330\263\330\247\330\250 \330\247\331\204\330\271\331\205\330\261 \330\250\331\206\330\254\330\247\330\255.\n"
	.size	str_1, 47

	.type	.Lstr,@object
	.section	.lrodata.str1.1,"aMSl",@progbits,1
.Lstr:
	.asciz	"[\330\263\330\254\331\204] \330\247\331\207\331\204\330\247 \330\250\331\203 \331\201\331\212 \331\204\330\272\330\252\331\203 \330\247\331\204\330\271\330\261\330\250\331\212\330\251 \330\247\331\204\330\256\330\247\330\265\330\251!"
	.size	.Lstr, 66

	.type	.Lstr.1,@object
.Lstr.1:
	.asciz	"[\330\263\330\254\331\204] \330\252\331\205 \330\255\330\263\330\247\330\250 \330\247\331\204\330\271\331\205\330\261 \330\250\331\206\330\254\330\247\330\255."
	.size	.Lstr.1, 46

	.section	".note.GNU-stack","",@progbits
