	.file	"tmpr6iemwyw.ll"
	.section	.ltext,"axl",@progbits
	.globl	main
	.p2align	4
	.type	main,@function
main:
	movabsq	$"س", %rax
	movl	$5, (%rax)
	movabsq	$"ص", %rax
	movl	$10, (%rax)
	movabsq	$"ع", %rax
	movabsq	$4624633867356078080, %rcx
	movq	%rcx, (%rax)
	movabsq	$"مجهول", %rax
	movl	$999, (%rax)
	movabsq	$"النتيجة", %rax
	movabsq	$4621819117588971520, %rcx
	movq	%rcx, (%rax)
	xorl	%eax, %eax
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main

	.type	"س",@object
	.section	.lbss,"awl",@nobits
	.globl	"س"
	.p2align	2, 0x0
"س":
	.long	0
	.size	"س", 4

	.type	"ص",@object
	.globl	"ص"
	.p2align	2, 0x0
"ص":
	.long	0
	.size	"ص", 4

	.type	"ع",@object
	.globl	"ع"
	.p2align	3, 0x0
"ع":
	.quad	0x0000000000000000
	.size	"ع", 8

	.type	"مجهول",@object
	.globl	"مجهول"
	.p2align	2, 0x0
"مجهول":
	.long	0
	.size	"مجهول", 4

	.type	"النتيجة",@object
	.globl	"النتيجة"
	.p2align	3, 0x0
"النتيجة":
	.quad	0x0000000000000000
	.size	"النتيجة", 8

	.section	".note.GNU-stack","",@progbits
