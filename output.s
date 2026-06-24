	.file	"<string>"
	.section	.ltext,"axl",@progbits
	.globl	"proc_حساب_السرعة"
	.p2align	4
	.type	"proc_حساب_السرعة",@function
"proc_حساب_السرعة":
	.cfi_startproc
	subq	$56, %rsp
	movapd	%xmm6, 32(%rsp)
	.cfi_def_cfa_offset 64
	.cfi_offset %xmm6, -32
	xorpd	%xmm6, %xmm6
	ucomisd	%xmm1, %xmm6
	jae	.LBB0_1
	divsd	%xmm1, %xmm0
	movapd	%xmm0, %xmm6
	jmp	.LBB0_2
.LBB0_1:
	movabsq	$.L__log_1, %rcx
	movabsq	$mizan_log, %rax
	callq	*%rax
.LBB0_2:
	movapd	%xmm6, %xmm0
	movaps	32(%rsp), %xmm6
	addq	$56, %rsp
	retq
.Lfunc_end0:
	.size	"proc_حساب_السرعة", .Lfunc_end0-"proc_حساب_السرعة"
	.cfi_endproc

	.globl	main
	.p2align	4
	.type	main,@function
main:
	.cfi_startproc
	pushq	%r14
	.cfi_def_cfa_offset 16
	pushq	%rsi
	.cfi_def_cfa_offset 24
	pushq	%rdi
	.cfi_def_cfa_offset 32
	pushq	%rbx
	.cfi_def_cfa_offset 40
	subq	$40, %rsp
	.cfi_def_cfa_offset 80
	.cfi_offset %rbx, -40
	.cfi_offset %rdi, -32
	.cfi_offset %rsi, -24
	.cfi_offset %r14, -16
	movabsq	$setup_arabic_console, %rax
	callq	*%rax
	movabsq	$.L__dev_ip_2, %rcx
	movabsq	$mizan_modbus_connect, %rax
	movl	$5020, %edx
	callq	*%rax
	movabsq	$__modbus_ctx, %rcx
	movq	%rax, (%rcx)
	movabsq	$.L__mq_host_3, %rcx
	movabsq	$.L__mq_cid_4, %r8
	movabsq	$mizan_mqtt_connect, %rax
	movl	$1884, %edx
	callq	*%rax
	movabsq	$__mqtt_ctx, %rcx
	movq	%rax, (%rcx)
	movabsq	$__mizan_set_mqtt_ctx, %rdx
	movq	%rax, %rcx
	callq	*%rdx
	movabsq	$"g_عداد", %rdi
	movl	$0, (%rdi)
	movabsq	$.L__log_5, %rcx
	movabsq	$mizan_log, %rbx
	callq	*%rbx
	movabsq	$.L__alert_6, %rdx
	movabsq	$mizan_alert, %rax
	movl	$1, %ecx
	callq	*%rax
	cmpl	$1, (%rdi)
	jg	.LBB1_3
	movabsq	$.L__log_8, %rsi
	.p2align	4
.LBB1_2:
	movq	%rsi, %rcx
	callq	*%rbx
	movl	(%rdi), %eax
	incl	%eax
	movl	%eax, (%rdi)
	cmpl	$2, %eax
	jl	.LBB1_2
.LBB1_3:
	movabsq	$mizan_now_ms, %rdi
	movabsq	$mizan_escalation_tick, %rbx
	movabsq	$mizan_sleep_ms, %r14
	.p2align	4
.LBB1_4:
	callq	*%rdi
	movq	%rax, %rsi
	callq	*%rbx
	callq	*%rdi
	subq	%rax, %rsi
	addq	$1000, %rsi
	testq	%rsi, %rsi
	jle	.LBB1_4
	movq	%rsi, %rcx
	callq	*%r14
	jmp	.LBB1_4
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc

	.type	"g_عداد",@object
	.section	.lbss,"awl",@nobits
	.p2align	2, 0x0
"g_عداد":
	.long	0
	.size	"g_عداد", 4

	.type	__modbus_ctx,@object
	.p2align	3, 0x0
__modbus_ctx:
	.quad	0
	.size	__modbus_ctx, 8

	.type	__mqtt_ctx,@object
	.p2align	3, 0x0
__mqtt_ctx:
	.quad	0
	.size	__mqtt_ctx, 8

	.type	.L__log_1,@object
	.section	.lrodata,"al",@progbits
	.p2align	4, 0x0
.L__log_1:
	.asciz	"\330\256\330\267\330\247: \330\247\331\204\330\262\331\205\331\206 \331\212\330\254\330\250 \330\247\331\206 \331\212\331\203\331\210\331\206 \330\247\331\203\330\250\330\261 \331\205\331\206 \330\265\331\201\330\261"
	.size	.L__log_1, 61

	.type	.L__dev_ip_2,@object
.L__dev_ip_2:
	.asciz	"127.0.0.1"
	.size	.L__dev_ip_2, 10

	.type	.L__mq_host_3,@object
.L__mq_host_3:
	.asciz	"127.0.0.1"
	.size	.L__mq_host_3, 10

	.type	.L__mq_cid_4,@object
.L__mq_cid_4:
	.asciz	"mizan-runtime"
	.size	.L__mq_cid_4, 14

	.type	.L__log_5,@object
	.p2align	4, 0x0
.L__log_5:
	.asciz	"\330\250\330\257\330\241 \330\247\330\256\330\252\330\250\330\247\330\261 \330\247\331\204\331\210\330\255\330\257\330\247\330\252"
	.size	.L__log_5, 35

	.type	.L__alert_6,@object
	.p2align	4, 0x0
.L__alert_6:
	.asciz	"[\330\252\331\206\330\250\331\212\331\207 \331\205\330\263\330\252\331\210\331\211_1] \330\247\331\204\330\263\330\261\330\271\330\251 \330\271\330\247\331\204\331\212\330\251"
	.size	.L__alert_6, 50

	.type	.L__log_8,@object
	.p2align	4, 0x0
.L__log_8:
	.asciz	"\330\257\331\210\330\261\330\251 \330\255\330\263\330\247\330\250\331\212\330\251"
	.size	.L__log_8, 22

	.section	".note.GNU-stack","",@progbits
