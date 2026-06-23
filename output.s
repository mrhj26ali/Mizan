	.file	"<string>"
	.section	.ltext,"axl",@progbits
	.globl	"proc_الرئيسي"
	.p2align	4
	.type	"proc_الرئيسي",@function
"proc_الرئيسي":
	.cfi_startproc
	pushq	%rsi
	.cfi_def_cfa_offset 16
	subq	$32, %rsp
	.cfi_def_cfa_offset 48
	.cfi_offset %rsi, -16
	movabsq	$.L__log_1, %rcx
	movabsq	$mizan_log, %rsi
	callq	*%rsi
	movabsq	$.L__log_2, %rcx
	movq	%rsi, %rax
	addq	$32, %rsp
	popq	%rsi
	rex64 jmpq	*%rax
.Lfunc_end0:
	.size	"proc_الرئيسي", .Lfunc_end0-"proc_الرئيسي"
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
	movabsq	$.L__dev_ip_3, %rcx
	movabsq	$mizan_modbus_connect, %rax
	movl	$5020, %edx
	callq	*%rax
	movabsq	$__modbus_ctx, %rcx
	movq	%rax, (%rcx)
	movabsq	$.L__mq_host_4, %rcx
	movabsq	$.L__mq_cid_5, %r8
	movabsq	$mizan_mqtt_connect, %rax
	movl	$1884, %edx
	callq	*%rax
	movabsq	$__mqtt_ctx, %rcx
	movq	%rax, (%rcx)
	movabsq	$__mizan_set_mqtt_ctx, %rdx
	movq	%rax, %rcx
	callq	*%rdx
	movabsq	$.L__log_1, %rcx
	movabsq	$mizan_log, %rsi
	callq	*%rsi
	movabsq	$.L__log_2, %rcx
	callq	*%rsi
	movabsq	$mizan_now_ms, %rdi
	movabsq	$mizan_escalation_tick, %rbx
	movabsq	$mizan_sleep_ms, %r14
	.p2align	4
.LBB1_1:
	callq	*%rdi
	movq	%rax, %rsi
	callq	*%rbx
	callq	*%rdi
	subq	%rax, %rsi
	addq	$1000, %rsi
	testq	%rsi, %rsi
	jle	.LBB1_1
	movq	%rsi, %rcx
	callq	*%r14
	jmp	.LBB1_1
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc

	.type	__modbus_ctx,@object
	.section	.lbss,"awl",@nobits
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
	.asciz	"[\330\263\330\254\331\204] \331\205\330\261\330\255\330\250\330\247 \330\250\330\247\331\204\330\271\330\247\331\204\331\205 \331\205\331\206 \331\204\330\272\330\251 \331\205\331\212\330\262\330\247\331\206"
	.size	.L__log_1, 58

	.type	.L__log_2,@object
	.p2align	4, 0x0
.L__log_2:
	.asciz	"[\330\263\330\254\331\204] \331\207\330\260\331\207 \331\204\330\272\330\251 \330\250\330\261\331\205\330\254\330\251 \330\271\330\261\330\250\331\212\330\251 \331\205\330\254\331\205\330\271\330\251"
	.size	.L__log_2, 56

	.type	.L__dev_ip_3,@object
.L__dev_ip_3:
	.asciz	"127.0.0.1"
	.size	.L__dev_ip_3, 10

	.type	.L__mq_host_4,@object
.L__mq_host_4:
	.asciz	"127.0.0.1"
	.size	.L__mq_host_4, 10

	.type	.L__mq_cid_5,@object
.L__mq_cid_5:
	.asciz	"mizan-runtime"
	.size	.L__mq_cid_5, 14

	.section	".note.GNU-stack","",@progbits
