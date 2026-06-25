	.file	"<string>"
	.section	.rodata.cst8,"aM",@progbits,8
	.p2align	3, 0x0
.LCPI0_0:
	.quad	0x4020000000000000
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
	subq	$104, %rsp
	movaps	%xmm8, 80(%rsp)
	movapd	%xmm7, 64(%rsp)
	movaps	%xmm6, 48(%rsp)
	.cfi_def_cfa_offset 176
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
	movabsq	$mizan_now_ms, %rdi
	movabsq	$mizan_modbus_is_connected, %rsi
	movabsq	$__wq_count, %r15
	movabsq	$.LCPI0_0, %rax
	movsd	(%rax), %xmm8
	movabsq	$.LCPI0_1, %rax
	movsd	(%rax), %xmm6
	movabsq	$mizan_modbus_write, %r14
	.p2align	4
.LBB0_1:
	callq	*%rdi
	movq	%rax, %r13
	movabsq	$__modbus_ctx, %rax
	movq	(%rax), %rbp
	movq	%rbp, %rcx
	callq	*%rsi
	testl	%eax, %eax
	jne	.LBB0_3
	movl	$0, (%r15)
.LBB0_3:
	movq	%rbp, %rcx
	movl	$2, %edx
	movabsq	$mizan_modbus_read, %rax
	callq	*%rax
	movapd	%xmm0, %xmm7
	movabsq	$"s_الضغط", %rax
	movsd	%xmm0, (%rax)
	movq	%rbp, %rcx
	callq	*%rsi
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
	movabsq	$"s_الضغط", %rax
	movsd	(%rax), %xmm0
	ucomisd	%xmm8, %xmm0
	jbe	.LBB0_22
	xorl	%ecx, %ecx
	movapd	%xmm6, %xmm1
	movabsq	$mizan_actuator_cmd, %rax
	callq	*%rax
	movslq	(%r15), %rax
	cmpq	$64, %rax
	jge	.LBB0_21
	movabsq	$__wq_addrs, %rcx
	movl	$36, (%rcx,%rax,4)
	movabsq	$__wq_values, %rcx
	movabsq	$4607182418800017408, %rdx
	movq	%rdx, (%rcx,%rax,8)
	incl	%eax
	movl	%eax, (%r15)
.LBB0_21:
	movl	$1, %ecx
	movabsq	$.L__alert_5, %rdx
	movabsq	$mizan_alert, %rax
	callq	*%rax
.LBB0_6:
	movl	(%r15), %esi
	testl	%esi, %esi
	jg	.LBB0_8
	jmp	.LBB0_10
	.p2align	4
.LBB0_22:
	xorpd	%xmm1, %xmm1
	xorl	%ecx, %ecx
	movabsq	$mizan_actuator_cmd, %rax
	callq	*%rax
	movslq	(%r15), %rsi
	cmpq	$64, %rsi
	jge	.LBB0_8
	movabsq	$__wq_addrs, %rax
	movl	$36, (%rax,%rsi,4)
	movabsq	$__wq_values, %rax
	movq	$0, (%rax,%rsi,8)
	incl	%esi
	movl	%esi, (%r15)
	testl	%esi, %esi
	jle	.LBB0_10
	.p2align	4
.LBB0_8:
	movabsq	$__modbus_ctx, %rax
	movq	(%rax), %rbp
	xorl	%ebx, %ebx
	movabsq	$__wq_addrs, %r15
	movabsq	$__wq_values, %r12
	.p2align	4
.LBB0_9:
	movl	(%r15), %edx
	movsd	(%r12), %xmm2
	movq	%rbp, %rcx
	callq	*%r14
	incl	%ebx
	addq	$8, %r12
	addq	$4, %r15
	cmpl	%esi, %ebx
	jb	.LBB0_9
.LBB0_10:
	movabsq	$__wq_count, %r15
	movl	$0, (%r15)
	movabsq	$mizan_escalation_tick, %rax
	callq	*%rax
	callq	*%rdi
	movq	%rax, %rbp
	movabsq	$__rpt_timer_0, %rax
	movq	(%rax), %rax
	cmpq	$-1, %rax
	je	.LBB0_11
	cmpq	%rax, %rbp
	jl	.LBB0_14
.LBB0_13:
	xorl	%ecx, %ecx
	movabsq	$mizan_actuator_cycles, %rax
	callq	*%rax
	movl	%eax, %esi
	xorl	%ecx, %ecx
	movabsq	$mizan_actuator_state, %rax
	callq	*%rax
	movl	%eax, %ebx
	xorl	%ecx, %ecx
	movabsq	$mizan_sensor_health, %rax
	callq	*%rax
	movl	%eax, 40(%rsp)
	movl	%ebx, 32(%rsp)
	movl	$2048, %edx
	movabsq	$__rpt_buf, %rbx
	movq	%rbx, %rcx
	movabsq	$.L__rpt_fmt_6, %r8
	movl	%esi, %r9d
	movabsq	$snprintf, %rax
	callq	*%rax
	movabsq	$.L__rpt_id_7, %rcx
	movabsq	$.L__rpt_fmtarg_8, %rdx
	movabsq	$.L__rpt_dir_9, %r8
	movq	%rbx, %r9
	movabsq	$mizan_report_write, %rax
	callq	*%rax
	addq	$5000, %rbp
	movabsq	$__rpt_timer_0, %rax
	movq	%rbp, (%rax)
.LBB0_14:
	movabsq	$__pending_goto, %rax
	cmpb	$1, (%rax)
	movabsq	$mizan_modbus_is_connected, %rsi
	jne	.LBB0_16
	movabsq	$__current_mode, %rax
	movb	$1, (%rax)
	movabsq	$__pending_goto, %rax
	movb	$0, (%rax)
.LBB0_16:
	callq	*%rdi
	subq	%rax, %r13
	addq	$500, %r13
	testq	%r13, %r13
	jle	.LBB0_1
	movq	%r13, %rcx
	movabsq	$mizan_sleep_ms, %rax
	callq	*%rax
	jmp	.LBB0_1
	.p2align	4
.LBB0_11:
	leaq	5000(%rbp), %rcx
	movabsq	$__rpt_timer_0, %rdx
	movq	%rcx, (%rdx)
	cmpq	%rax, %rbp
	jge	.LBB0_13
	jmp	.LBB0_14
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc

	.type	"s_الضغط",@object
	.section	.lbss,"awl",@nobits
	.p2align	3, 0x0
"s_الضغط":
	.quad	0x0000000000000000
	.size	"s_الضغط", 8

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

	.type	__rpt_buf,@object
	.p2align	4, 0x0
__rpt_buf:
	.zero	2048
	.size	__rpt_buf, 2048

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
	.asciz	"\330\250\330\257\330\241 \331\206\330\270\330\247\331\205 \330\247\331\204\330\252\331\202\330\247\330\261\331\212\330\261..."
	.size	.L__log_4, 36

	.type	.L__alert_5,@object
	.p2align	4, 0x0
.L__alert_5:
	.asciz	"[\330\252\331\206\330\250\331\212\331\207 \331\205\330\263\330\252\331\210\331\211_1] \330\247\331\204\330\266\330\272\330\267 \331\205\330\261\330\252\331\201\330\271 \330\254\330\257\330\247!"
	.size	.L__alert_5, 56

	.type	__rpt_timer_0,@object
	.section	.ldata,"awl",@progbits
	.p2align	3, 0x0
__rpt_timer_0:
	.quad	-1
	.size	__rpt_timer_0, 8

	.type	.L__rpt_fmt_6,@object
	.section	.lrodata,"al",@progbits
	.p2align	4, 0x0
.L__rpt_fmt_6:
	.asciz	"{\"\330\257\331\210\330\261\330\247\330\252_\330\247\331\204\331\205\330\266\330\256\330\251\":%d,\"\330\255\330\247\331\204\330\251_\330\247\331\204\331\205\330\266\330\256\330\251\":%d,\"\330\263\331\204\330\247\331\205\330\251_\330\247\331\204\330\255\330\263\330\247\330\263\":%d}"
	.size	.L__rpt_fmt_6, 87

	.type	.L__rpt_id_7,@object
	.p2align	4, 0x0
.L__rpt_id_7:
	.asciz	"\330\252\331\202\330\261\331\212\330\261_\330\247\331\204\330\265\331\212\330\247\331\206\330\251"
	.size	.L__rpt_id_7, 26

	.type	.L__rpt_fmtarg_8,@object
.L__rpt_fmtarg_8:
	.asciz	"json"
	.size	.L__rpt_fmtarg_8, 5

	.type	.L__rpt_dir_9,@object
.L__rpt_dir_9:
	.asciz	"./reports/cbm"
	.size	.L__rpt_dir_9, 14

	.section	".note.GNU-stack","",@progbits
