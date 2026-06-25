	.file	"<string>"
	.section	.rodata.cst8,"aM",@progbits,8
	.p2align	3, 0x0
.LCPI0_0:
	.quad	0x4056800000000000
.LCPI0_1:
	.quad	0x3ff0000000000000
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
	movabsq	$__current_mode, %rax
	movb	$0, (%rax)
	movabsq	$.L__log_4, %rcx
	movabsq	$mizan_log, %rax
	callq	*%rax
	movabsq	$__pending_goto, %rax
	movb	$1, (%rax)
	movabsq	$mizan_now_ms, %r14
	movabsq	$mizan_modbus_is_connected, %r15
	movabsq	$__wq_count, %rsi
	movabsq	$.LCPI0_0, %rax
	movsd	(%rax), %xmm8
	movabsq	$.LCPI0_1, %rax
	movsd	(%rax), %xmm6
	movabsq	$mizan_modbus_write, %r13
	.p2align	4
.LBB0_1:
	callq	*%r14
	movq	%rax, %rdi
	movabsq	$__modbus_ctx, %rax
	movq	(%rax), %rbx
	movq	%rbx, %rcx
	callq	*%r15
	testl	%eax, %eax
	jne	.LBB0_3
	movl	$0, (%rsi)
.LBB0_3:
	movq	%rbx, %rcx
	movl	$8, %edx
	movabsq	$mizan_modbus_read, %rax
	callq	*%rax
	movapd	%xmm0, %xmm7
	movabsq	$"s_الحرارة", %rax
	movsd	%xmm0, (%rax)
	movq	%rbx, %rcx
	callq	*%r15
	testl	%eax, %eax
	je	.LBB0_5
	xorl	%ecx, %ecx
	movapd	%xmm7, %xmm1
	movabsq	$mizan_ring_push, %rax
	callq	*%rax
.LBB0_5:
	movabsq	$__current_mode, %rax
	cmpb	$0, (%rax)
	je	.LBB0_6
	movabsq	$"s_الحرارة", %rax
	movsd	(%rax), %xmm7
	callq	*%r14
	ucomisd	%xmm8, %xmm7
	jbe	.LBB0_21
	movabsq	$__sustain_2561222929984, %rcx
	movq	(%rcx), %rcx
	cmpq	$-1, %rcx
	jne	.LBB0_17
	movabsq	$__sustain_2561222929984, %rcx
	movq	%rax, (%rcx)
	movq	%rax, %rcx
.LBB0_17:
	subq	%rcx, %rax
	cmpq	$5000, %rax
	jl	.LBB0_22
	xorl	%ecx, %ecx
	movapd	%xmm6, %xmm1
	movabsq	$mizan_actuator_cmd, %rax
	callq	*%rax
	movslq	(%rsi), %rax
	cmpq	$64, %rax
	jge	.LBB0_20
	movabsq	$__wq_addrs, %rcx
	movl	$34, (%rcx,%rax,4)
	movabsq	$__wq_values, %rcx
	movabsq	$4607182418800017408, %rdx
	movq	%rdx, (%rcx,%rax,8)
	incl	%eax
	movl	%eax, (%rsi)
.LBB0_20:
	movabsq	$.L__log_5, %rcx
	movabsq	$mizan_log, %rax
	callq	*%rax
	.p2align	4
.LBB0_6:
	movl	(%rsi), %r14d
	testl	%r14d, %r14d
	jg	.LBB0_8
	jmp	.LBB0_10
	.p2align	4
.LBB0_21:
	movabsq	$__sustain_2561222929984, %rax
	movq	$-1, (%rax)
.LBB0_22:
	xorpd	%xmm1, %xmm1
	xorl	%ecx, %ecx
	movabsq	$mizan_actuator_cmd, %rax
	callq	*%rax
	movslq	(%rsi), %r14
	cmpq	$64, %r14
	jge	.LBB0_8
	movabsq	$__wq_addrs, %rax
	movl	$34, (%rax,%r14,4)
	movabsq	$__wq_values, %rax
	movq	$0, (%rax,%r14,8)
	incl	%r14d
	movl	%r14d, (%rsi)
	testl	%r14d, %r14d
	jle	.LBB0_10
	.p2align	4
.LBB0_8:
	movabsq	$__modbus_ctx, %rax
	movq	(%rax), %rbx
	xorl	%r15d, %r15d
	movabsq	$__wq_addrs, %r12
	movabsq	$__wq_values, %rbp
	.p2align	4
.LBB0_9:
	movl	(%r12), %edx
	movsd	(%rbp), %xmm2
	movq	%rbx, %rcx
	callq	*%r13
	incl	%r15d
	addq	$8, %rbp
	addq	$4, %r12
	cmpl	%r14d, %r15d
	jb	.LBB0_9
.LBB0_10:
	movl	$0, (%rsi)
	movabsq	$mizan_escalation_tick, %rax
	callq	*%rax
	movabsq	$__pending_goto, %rax
	cmpb	$1, (%rax)
	jne	.LBB0_12
	movabsq	$__current_mode, %rax
	movb	$1, (%rax)
	movabsq	$__pending_goto, %rax
	movb	$0, (%rax)
.LBB0_12:
	movabsq	$mizan_now_ms, %r14
	callq	*%r14
	subq	%rax, %rdi
	addq	$500, %rdi
	testq	%rdi, %rdi
	movabsq	$mizan_modbus_is_connected, %r15
	jle	.LBB0_1
	movq	%rdi, %rcx
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

	.type	__wq_addrs,@object
	.p2align	4, 0x0
__wq_addrs:
	.zero	256
	.size	__wq_addrs, 256

	.type	__wq_values,@object
	.p2align	4, 0x0
__wq_values:
	.zero	512
	.size	__wq_values, 512

	.type	__wq_count,@object
	.p2align	2, 0x0
__wq_count:
	.long	0
	.size	__wq_count, 4

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
	.asciz	"\330\250\330\257\330\241 \330\247\330\256\330\252\330\250\330\247\330\261 \330\247\331\204\330\247\331\205\330\247\331\206 \330\247\331\204\331\201\331\212\330\262\331\212\330\247\330\246\331\212..."
	.size	.L__log_4, 55

	.type	__sustain_2561222929984,@object
	.section	.ldata,"awl",@progbits
	.p2align	3, 0x0
__sustain_2561222929984:
	.quad	-1
	.size	__sustain_2561222929984, 8

	.type	.L__log_5,@object
	.section	.lrodata,"al",@progbits
	.p2align	4, 0x0
.L__log_5:
	.asciz	"\330\255\330\261\330\247\330\261\330\251 \331\205\330\261\330\252\331\201\330\271\330\251 \330\250\330\247\330\263\330\252\331\205\330\261\330\247\330\261\330\214 \330\252\330\264\330\272\331\212\331\204 \330\247\331\204\331\205\330\266\330\256\330\251."
	.size	.L__log_5, 68

	.section	".note.GNU-stack","",@progbits
