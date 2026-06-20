	.file	"tmplpne8ziq.ll"
	.section	.ltext,"axl",@progbits
	.globl	"تشغيل_النظام"
	.p2align	4
	.type	"تشغيل_النظام",@function
"تشغيل_النظام":
	.cfi_startproc
	pushq	%rsi
	.cfi_def_cfa_offset 16
	pushq	%rdi
	.cfi_def_cfa_offset 24
	subq	$40, %rsp
	.cfi_def_cfa_offset 64
	.cfi_offset %rdi, -24
	.cfi_offset %rsi, -16
	movabsq	$"العمر", %rax
	movl	(%rax), %eax
	incl	%eax
	movabsq	$"السنة_القادمة", %rcx
	movl	%eax, (%rcx)
	movabsq	$str_0, %rcx
	movabsq	$print_arabic, %rsi
	callq	*%rsi
	movabsq	$putchar, %rdi
	movl	$10, %ecx
	callq	*%rdi
	movabsq	$str_2, %rcx
	callq	*%rsi
	movl	$10, %ecx
	callq	*%rdi
	movabsq	$str_4, %rcx
	callq	*%rsi
	movl	$10, %ecx
	callq	*%rdi
	movabsq	$str_6, %rcx
	callq	*%rsi
	movl	$10, %ecx
	callq	*%rdi
	movabsq	$str_8, %rcx
	callq	*%rsi
	movl	$10, %ecx
	movq	%rdi, %rax
	addq	$40, %rsp
	popq	%rdi
	popq	%rsi
	rex64 jmpq	*%rax
.Lfunc_end0:
	.size	"تشغيل_النظام", .Lfunc_end0-"تشغيل_النظام"
	.cfi_endproc

	.globl	main
	.p2align	4
	.type	main,@function
main:
	.cfi_startproc
	pushq	%rsi
	.cfi_def_cfa_offset 16
	pushq	%rdi
	.cfi_def_cfa_offset 24
	subq	$40, %rsp
	.cfi_def_cfa_offset 64
	.cfi_offset %rdi, -24
	.cfi_offset %rsi, -16
	movabsq	$setup_arabic_console, %rax
	callq	*%rax
	movabsq	$"العمر", %rax
	movl	$25, (%rax)
	movabsq	$"السنة_القادمة", %rax
	movl	$26, (%rax)
	movabsq	$str_0, %rcx
	movabsq	$print_arabic, %rsi
	callq	*%rsi
	movabsq	$putchar, %rdi
	movl	$10, %ecx
	callq	*%rdi
	movabsq	$str_2, %rcx
	callq	*%rsi
	movl	$10, %ecx
	callq	*%rdi
	movabsq	$str_4, %rcx
	callq	*%rsi
	movl	$10, %ecx
	callq	*%rdi
	movabsq	$str_6, %rcx
	callq	*%rsi
	movl	$10, %ecx
	callq	*%rdi
	movabsq	$str_8, %rcx
	callq	*%rsi
	movl	$10, %ecx
	callq	*%rdi
	xorl	%eax, %eax
	addq	$40, %rsp
	popq	%rdi
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
	.asciz	"[\330\263\330\254\331\204] \331\203\330\252\330\247\330\250\330\214 \330\250\330\247\330\250\330\247\330\214 \331\202\331\204\331\205."
	.size	str_0, 39

	.type	str_1,@object
	.globl	str_1
str_1:
	.asciz	"\n"
	.size	str_1, 2

	.type	str_2,@object
	.globl	str_2
	.p2align	4, 0x0
str_2:
	.asciz	"[\330\263\330\254\331\204] \331\202\330\247\331\204: \330\247\331\204\330\247\330\263\331\204\330\247\331\205\330\214 \330\247\331\204\331\204\331\207\330\214 \331\204\330\247\331\206."
	.size	str_2, 53

	.type	str_3,@object
	.globl	str_3
str_3:
	.asciz	"\n"
	.size	str_3, 2

	.type	str_4,@object
	.globl	str_4
	.p2align	4, 0x0
str_4:
	.asciz	"[\330\263\330\254\331\204] \330\247\331\204\330\255\330\261\330\247\330\261\330\251 \330\247\331\204\331\212\331\210\331\205 25 \330\257\330\261\330\254\330\251 \331\205\330\246\331\210\331\212\330\251."
	.size	str_4, 59

	.type	str_5,@object
	.globl	str_5
str_5:
	.asciz	"\n"
	.size	str_5, 2

	.type	str_6,@object
	.globl	str_6
	.p2align	4, 0x0
str_6:
	.asciz	"[\330\263\330\254\331\204] \330\247\331\204\330\247\330\265\330\257\330\247\330\261 v1.0 \331\205\331\206 \331\204\330\272\330\251 \331\205\331\212\330\262\330\247\331\206."
	.size	str_6, 53

	.type	str_7,@object
	.globl	str_7
str_7:
	.asciz	"\n"
	.size	str_7, 2

	.type	str_8,@object
	.globl	str_8
	.p2align	4, 0x0
str_8:
	.asciz	"[\330\263\330\254\331\204] \330\252\331\205 \330\255\330\263\330\247\330\250 \330\247\331\204\330\271\331\205\330\261 \330\250\331\206\330\254\330\247\330\255."
	.size	str_8, 46

	.type	str_9,@object
	.globl	str_9
str_9:
	.asciz	"\n"
	.size	str_9, 2

	.section	".note.GNU-stack","",@progbits
