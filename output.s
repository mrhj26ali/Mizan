	.file	"<string>"
	.section	.rodata.cst8,"aM",@progbits,8
	.p2align	3, 0x0
.LCPI0_0:
	.quad	0x4062c00000000000
.LCPI0_1:
	.quad	0x4049000000000000
	.section	.ltext,"axl",@progbits
	.globl	main
	.p2align	4
	.type	main,@function
main:
	.cfi_startproc
	pushq	%r15
	.cfi_def_cfa_offset 16
	pushq	%r14
	.cfi_def_cfa_offset 24
	pushq	%r13
	.cfi_def_cfa_offset 32
	pushq	%r12
	.cfi_def_cfa_offset 40
	pushq	%rsi
	.cfi_def_cfa_offset 48
	pushq	%rdi
	.cfi_def_cfa_offset 56
	pushq	%rbp
	.cfi_def_cfa_offset 64
	pushq	%rbx
	.cfi_def_cfa_offset 72
	subq	$88, %rsp
	movaps	%xmm8, 64(%rsp)
	movapd	%xmm7, 48(%rsp)
	movaps	%xmm6, 32(%rsp)
	.cfi_def_cfa_offset 160
	.cfi_offset %rbx, -72
	.cfi_offset %rbp, -64
	.cfi_offset %rdi, -56
	.cfi_offset %rsi, -48
	.cfi_offset %r12, -40
	.cfi_offset %r13, -32
	.cfi_offset %r14, -24
	.cfi_offset %r15, -16
	.cfi_offset %xmm6, -128
	.cfi_offset %xmm7, -112
	.cfi_offset %xmm8, -96
	movabsq	$setup_arabic_console, %rax
	callq	*%rax
	movabsq	$.L__dev_ip_1, %rcx
	movabsq	$mizan_modbus_connect, %rax
	movl	$5020, %edx
	callq	*%rax
	movabsq	$__modbus_ctx, %rcx
	movq	%rax, (%rcx)
	movabsq	$.L__mq_host_2, %rcx
	movabsq	$.L__mq_cid_3, %r8
	movabsq	$mizan_mqtt_connect, %rax
	movl	$1884, %edx
	callq	*%rax
	movabsq	$__mqtt_ctx, %rcx
	movq	%rax, (%rcx)
	movabsq	$__mizan_set_mqtt_ctx, %rdx
	movq	%rax, %rcx
	callq	*%rdx
	movabsq	$__current_mode, %r13
	movb	$0, (%r13)
	movabsq	$.L__log_4, %rcx
	movabsq	$mizan_log, %rax
	callq	*%rax
	movabsq	$__pending_goto, %rsi
	movb	$1, (%rsi)
	movabsq	$mizan_now_ms, %rdi
	movabsq	$mizan_modbus_is_connected, %rbx
	movabsq	$"s_الحرارة", %r12
	movabsq	$.LCPI0_0, %rax
	movsd	(%rax), %xmm6
	movabsq	$.LCPI0_1, %rax
	movsd	(%rax), %xmm8
	.p2align	4
.LBB0_1:
	callq	*%rdi
	movq	%rax, %r14
	movabsq	$__modbus_ctx, %rax
	movq	(%rax), %r15
	movq	%r15, %rcx
	callq	*%rbx
	movq	%r15, %rcx
	movl	$8, %edx
	movabsq	$mizan_modbus_read, %rax
	callq	*%rax
	movapd	%xmm0, %xmm7
	movsd	%xmm0, (%r12)
	movq	%r15, %rcx
	callq	*%rbx
	movl	%eax, %ebp
	testl	%eax, %eax
	je	.LBB0_3
	xorl	%ecx, %ecx
	movapd	%xmm7, %xmm1
	movabsq	$mizan_ring_push, %rax
	callq	*%rax
.LBB0_3:
	xorl	%ecx, %ecx
	movl	%ebp, %edx
	movabsq	$mizan_health_track_disconnect, %rax
	callq	*%rax
	testl	%eax, %eax
	je	.LBB0_5
	movl	$3, %ecx
	movabsq	$.L__alert_5, %rdx
	movabsq	$mizan_alert, %rax
	callq	*%rax
.LBB0_5:
	xorps	%xmm2, %xmm2
	xorl	%ecx, %ecx
	movapd	%xmm7, %xmm1
	movaps	%xmm6, %xmm3
	movabsq	$mizan_health_out_of_range, %rax
	callq	*%rax
	testl	%eax, %eax
	je	.LBB0_7
	movl	$2, %ecx
	movabsq	$.L__alert_6, %rdx
	movabsq	$mizan_alert, %rax
	callq	*%rax
.LBB0_7:
	cmpb	$1, (%r13)
	jne	.LBB0_10
	movsd	(%r12), %xmm0
	ucomisd	%xmm8, %xmm0
	jbe	.LBB0_10
	movabsq	$.L__log_7, %rcx
	movabsq	$mizan_log, %rax
	callq	*%rax
.LBB0_10:
	movabsq	$mizan_escalation_tick, %rax
	callq	*%rax
	cmpb	$1, (%rsi)
	jne	.LBB0_12
	movb	$1, (%r13)
	movb	$0, (%rsi)
.LBB0_12:
	callq	*%rdi
	subq	%rax, %r14
	addq	$500, %r14
	testq	%r14, %r14
	jle	.LBB0_1
	movq	%r14, %rcx
	movabsq	$mizan_sleep_ms, %rax
	callq	*%rax
	jmp	.LBB0_1
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc

	.type	"s_الحرارة",@object
	.section	.lbss,"awl",@nobits
	.p2align	3, 0x0
"s_الحرارة":
	.quad	0x0000000000000000
	.size	"s_الحرارة", 8

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

	.type	__current_mode,@object
__current_mode:
	.byte	0
	.size	__current_mode, 1

	.type	__pending_goto,@object
__pending_goto:
	.byte	0
	.size	__pending_goto, 1

	.type	.L__dev_ip_1,@object
	.section	.lrodata,"al",@progbits
.L__dev_ip_1:
	.asciz	"127.0.0.1"
	.size	.L__dev_ip_1, 10

	.type	.L__mq_host_2,@object
.L__mq_host_2:
	.asciz	"127.0.0.1"
	.size	.L__mq_host_2, 10

	.type	.L__mq_cid_3,@object
.L__mq_cid_3:
	.asciz	"mizan-runtime"
	.size	.L__mq_cid_3, 14

	.type	.L__log_4,@object
	.p2align	4, 0x0
.L__log_4:
	.asciz	"\330\250\330\257\330\241 \331\205\330\261\330\247\331\202\330\250\330\251 \330\247\331\204\330\265\330\255\330\251..."
	.size	.L__log_4, 34

	.type	.L__alert_5,@object
	.p2align	4, 0x0
.L__alert_5:
	.asciz	"[\330\252\331\206\330\250\331\212\331\207 \331\205\330\263\330\252\331\210\331\211_3] \331\201\331\202\330\257\330\247\331\206 \330\247\331\204\330\247\330\252\330\265\330\247\331\204!"
	.size	.L__alert_5, 53

	.type	.L__alert_6,@object
	.p2align	4, 0x0
.L__alert_6:
	.asciz	"[\330\252\331\206\330\250\331\212\331\207 \331\205\330\263\330\252\331\210\331\211_2] \330\247\331\204\331\202\330\261\330\247\330\241\330\251 \330\256\330\247\330\261\330\254 \330\247\331\204\331\206\330\267\330\247\331\202 \330\247\331\204\330\247\331\205\331\206!"
	.size	.L__alert_6, 75

	.type	.L__log_7,@object
	.p2align	4, 0x0
.L__log_7:
	.asciz	"\330\247\331\204\331\206\330\270\330\247\331\205 \331\212\330\271\331\205\331\204."
	.size	.L__log_7, 23

	.section	".note.GNU-stack","",@progbits
