	.file	"<string>"
	.section	.ltext,"axl",@progbits
	.globl	"proc_تسجيل_تنبيه"
	.p2align	4
	.type	"proc_تسجيل_تنبيه",@function
"proc_تسجيل_تنبيه":
	.cfi_startproc
	movabsq	$"g_عداد_التنبيهات", %rax
	incl	(%rax)
	movabsq	$.L__log_1, %rcx
	movabsq	$mizan_log, %rax
	rex64 jmpq	*%rax
.Lfunc_end0:
	.size	"proc_تسجيل_تنبيه", .Lfunc_end0-"proc_تسجيل_تنبيه"
	.cfi_endproc

	.section	.rodata.cst8,"aM",@progbits,8
	.p2align	3, 0x0
.LCPI1_0:
	.quad	0x4055400000000000
.LCPI1_1:
	.quad	0x4051800000000000
.LCPI1_2:
	.quad	0x405e000000000000
.LCPI1_3:
	.quad	0x4022000000000000
.LCPI1_4:
	.quad	0x4056800000000000
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
	subq	$168, %rsp
	movaps	%xmm11, 144(%rsp)
	movaps	%xmm10, 128(%rsp)
	movaps	%xmm9, 112(%rsp)
	movaps	%xmm8, 96(%rsp)
	movaps	%xmm7, 80(%rsp)
	movapd	%xmm6, 64(%rsp)
	.cfi_def_cfa_offset 240
	.cfi_offset %rbx, -72
	.cfi_offset %rbp, -64
	.cfi_offset %rdi, -56
	.cfi_offset %rsi, -48
	.cfi_offset %r12, -40
	.cfi_offset %r13, -32
	.cfi_offset %r14, -24
	.cfi_offset %r15, -16
	.cfi_offset %xmm6, -176
	.cfi_offset %xmm7, -160
	.cfi_offset %xmm8, -144
	.cfi_offset %xmm9, -128
	.cfi_offset %xmm10, -112
	.cfi_offset %xmm11, -96
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
	movl	$1883, %edx
	callq	*%rax
	movabsq	$__mqtt_ctx, %rcx
	movq	%rax, (%rcx)
	movabsq	$__mizan_set_mqtt_ctx, %rdx
	movq	%rax, %rcx
	callq	*%rdx
	movabsq	$"g_عداد_التنبيهات", %rax
	movl	$0, (%rax)
	movabsq	$__current_mode, %rbx
	movl	$0, (%rbx)
	movabsq	$.L__log_5, %rcx
	movabsq	$mizan_log, %rax
	callq	*%rax
	movabsq	$__wq_count, %r14
	movslq	(%r14), %rax
	cmpq	$63, %rax
	jg	.LBB1_3
	movabsq	$__wq_addrs, %rcx
	movabsq	$__wq_values, %rdx
	movl	$32, (%rcx,%rax,4)
	movq	$0, (%rdx,%rax,8)
	leal	1(%rax), %ecx
	movl	%ecx, (%r14)
	cmpl	$63, %eax
	je	.LBB1_3
	movabsq	$__wq_addrs+4, %rcx
	movl	$34, (%rcx,%rax,4)
	movabsq	$__wq_values+8, %rcx
	movq	$0, (%rcx,%rax,8)
	addl	$2, %eax
	movl	%eax, (%r14)
.LBB1_3:
	movabsq	$__pending_goto, %r15
	movl	$1, (%r15)
	movabsq	$mizan_now_ms, %r12
	movabsq	$mizan_modbus_read, %r13
	movabsq	$"s_درجة_الحرارة", %rbp
	movabsq	$.LCPI1_0, %rax
	movsd	(%rax), %xmm7
	movabsq	$.LCPI1_1, %rax
	movsd	(%rax), %xmm8
	movabsq	$.LCPI1_2, %rax
	movsd	(%rax), %xmm9
	movabsq	$.LCPI1_4, %rax
	movsd	(%rax), %xmm10
	movabsq	$.LCPI1_3, %rax
	movsd	(%rax), %xmm11
	movabsq	$mizan_modbus_write, %rdi
	.p2align	4
.LBB1_4:
	callq	*%r12
	movq	%rax, 56(%rsp)
	movabsq	$__modbus_ctx, %rax
	movq	(%rax), %rsi
	movq	%rsi, %rcx
	movl	$8, %edx
	callq	*%r13
	movapd	%xmm0, %xmm6
	movsd	%xmm0, (%rbp)
	xorl	%ecx, %ecx
	movapd	%xmm0, %xmm1
	movabsq	$mizan_ring_push, %rax
	callq	*%rax
	movq	%rsi, %rcx
	movabsq	$mizan_modbus_is_connected, %rax
	callq	*%rax
	testl	%eax, %eax
	jne	.LBB1_6
	movl	$2, %ecx
	movabsq	$.L__alert_6, %rdx
	movabsq	$mizan_alert, %rax
	callq	*%rax
.LBB1_6:
	movl	$30000, %r8d
	xorl	%ecx, %ecx
	movapd	%xmm6, %xmm1
	movabsq	$mizan_health_track_stuck, %rax
	callq	*%rax
	cmpq	$30000, %rax
	jl	.LBB1_8
	movl	$1, %ecx
	movabsq	$.L__alert_7, %rdx
	movabsq	$mizan_alert, %rax
	callq	*%rax
.LBB1_8:
	movq	%rsi, %rcx
	movl	$2, %edx
	callq	*%r13
	movabsq	$"s_الضغط", %rax
	movsd	%xmm0, (%rax)
	movl	$1, %ecx
	movapd	%xmm0, %xmm1
	movabsq	$mizan_ring_push, %rax
	callq	*%rax
	movq	%rsi, %rcx
	movabsq	$mizan_modbus_is_connected, %rax
	callq	*%rax
	cmpl	$1, (%rbx)
	jne	.LBB1_9
	movsd	(%rbp), %xmm6
	ucomisd	%xmm7, %xmm6
	jbe	.LBB1_20
	movslq	(%r14), %rax
	cmpq	$64, %rax
	jge	.LBB1_19
	movabsq	$__wq_addrs, %rcx
	movl	$32, (%rcx,%rax,4)
	movabsq	$__wq_values, %rcx
	movabsq	$4607182418800017408, %rdx
	movq	%rdx, (%rcx,%rax,8)
	incl	%eax
	movl	%eax, (%r14)
.LBB1_19:
	movl	$1, %ecx
	movabsq	$.L__alert_8, %rdx
	movabsq	$mizan_alert, %rax
	callq	*%rax
	movabsq	$"g_عداد_التنبيهات", %rax
	incl	(%rax)
	movabsq	$.L__log_1, %rcx
	movabsq	$mizan_log, %rax
	callq	*%rax
	movsd	(%rbp), %xmm6
.LBB1_20:
	ucomisd	%xmm6, %xmm8
	jbe	.LBB1_22
	movslq	(%r14), %rax
	cmpq	$64, %rax
	jge	.LBB1_22
	movabsq	$__wq_addrs, %rcx
	movl	$32, (%rcx,%rax,4)
	movabsq	$__wq_values, %rcx
	movq	$0, (%rcx,%rax,8)
	incl	%eax
	movl	%eax, (%r14)
.LBB1_22:
	ucomisd	%xmm9, %xmm6
	ja	.LBB1_24
	movabsq	$"s_الضغط", %rax
	movsd	(%rax), %xmm0
	ucomisd	%xmm11, %xmm0
	jbe	.LBB1_27
.LBB1_24:
	movslq	(%r14), %rax
	cmpq	$64, %rax
	jge	.LBB1_26
	movabsq	$__wq_addrs, %rcx
	movl	$34, (%rcx,%rax,4)
	movabsq	$__wq_values, %rcx
	movabsq	$4607182418800017408, %rdx
	movq	%rdx, (%rcx,%rax,8)
	incl	%eax
	movl	%eax, (%r14)
.LBB1_26:
	movl	$3, %ecx
	movabsq	$.L__alert_9, %rdx
	movabsq	$mizan_alert, %rax
	callq	*%rax
	movl	$2, (%r15)
	movsd	(%rbp), %xmm6
.LBB1_27:
	callq	*%r12
	ucomisd	%xmm10, %xmm6
	jbe	.LBB1_33
	movabsq	$__sustain_1305777795296, %rcx
	movq	(%rcx), %rcx
	cmpq	$-1, %rcx
	jne	.LBB1_30
	movabsq	$__sustain_1305777795296, %rcx
	movq	%rax, (%rcx)
	movq	%rax, %rcx
.LBB1_30:
	subq	%rcx, %rax
	cmpq	$10000, %rax
	jl	.LBB1_9
	movl	$2, %ecx
	movabsq	$.L__alert_10, %rdx
	movabsq	$mizan_alert, %rax
	callq	*%rax
	jmp	.LBB1_9
	.p2align	4
.LBB1_33:
	movabsq	$__sustain_1305777795296, %rax
	movq	$-1, (%rax)
.LBB1_9:
	movq	%rbx, %r12
	movq	%r14, %r15
	movl	(%r14), %ebx
	testl	%ebx, %ebx
	jle	.LBB1_12
	movabsq	$__modbus_ctx, %rax
	movq	(%rax), %rsi
	xorl	%r13d, %r13d
	movabsq	$__wq_addrs, %rbp
	movabsq	$__wq_values, %r14
	.p2align	4
.LBB1_11:
	movl	(%rbp), %edx
	movsd	(%r14), %xmm2
	movq	%rsi, %rcx
	callq	*%rdi
	incl	%r13d
	addq	$8, %r14
	addq	$4, %rbp
	cmpl	%ebx, %r13d
	jl	.LBB1_11
.LBB1_12:
	movq	%r15, %r14
	movl	$0, (%r15)
	movabsq	$mizan_escalation_tick, %rax
	callq	*%rax
	movl	$86400000, %edx
	xorl	%ecx, %ecx
	movabsq	$mizan_ring_avg, %rax
	callq	*%rax
	movapd	%xmm0, %xmm6
	movl	$86400000, %edx
	movl	$1, %ecx
	movabsq	$mizan_ring_max, %rax
	callq	*%rax
	movq	%r12, %rbx
	xorps	%xmm1, %xmm1
	cvtsi2sdl	(%r12), %xmm1
	movsd	%xmm1, 40(%rsp)
	movsd	%xmm0, 32(%rsp)
	movl	$2048, %edx
	movabsq	$__rpt_buf, %rsi
	movq	%rsi, %rcx
	movabsq	$.L__rpt_fmt_11, %r8
	movapd	%xmm6, %xmm3
	movq	%xmm6, %r9
	movabsq	$snprintf, %rax
	callq	*%rax
	movabsq	$.L__rpt_id_12, %rcx
	movabsq	$.L__rpt_fmtarg_13, %rdx
	movabsq	$.L__rpt_dir_14, %r8
	movq	%rsi, %r9
	movabsq	$mizan_report_write, %rax
	callq	*%rax
	movabsq	$__pending_goto, %r15
	movl	(%r15), %eax
	cmpl	$-1, %eax
	je	.LBB1_14
	movl	%eax, (%rbx)
	movl	$-1, (%r15)
.LBB1_14:
	movabsq	$mizan_now_ms, %r12
	callq	*%r12
	movq	56(%rsp), %rcx
	subq	%rax, %rcx
	addq	$1000, %rcx
	testq	%rcx, %rcx
	movabsq	$mizan_modbus_read, %r13
	movabsq	$"s_درجة_الحرارة", %rbp
	jle	.LBB1_4
	movabsq	$mizan_sleep_ms, %rax
	callq	*%rax
	jmp	.LBB1_4
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc

	.type	"s_درجة_الحرارة",@object
	.section	.lbss,"awl",@nobits
	.p2align	3, 0x0
"s_درجة_الحرارة":
	.quad	0x0000000000000000
	.size	"s_درجة_الحرارة", 8

	.type	"s_الضغط",@object
	.p2align	3, 0x0
"s_الضغط":
	.quad	0x0000000000000000
	.size	"s_الضغط", 8

	.type	"g_عداد_التنبيهات",@object
	.p2align	2, 0x0
"g_عداد_التنبيهات":
	.long	0
	.size	"g_عداد_التنبيهات", 4

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
	.p2align	2, 0x0
__current_mode:
	.long	0
	.size	__current_mode, 4

	.type	__pending_goto,@object
	.section	.ldata,"awl",@progbits
	.p2align	2, 0x0
__pending_goto:
	.long	4294967295
	.size	__pending_goto, 4

	.type	__wq_addrs,@object
	.section	.lbss,"awl",@nobits
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

	.type	.L__log_1,@object
	.section	.lrodata,"al",@progbits
	.p2align	4, 0x0
.L__log_1:
	.asciz	"[\330\263\330\254\331\204] \330\252\331\205 \330\252\330\263\330\254\331\212\331\204 \330\252\331\206\330\250\331\212\331\207 \330\254\330\257\331\212\330\257"
	.size	.L__log_1, 45

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
	.asciz	"[\330\263\330\254\331\204] \330\250\330\257\330\241 \330\252\330\264\330\272\331\212\331\204 \331\206\330\270\330\247\331\205 \330\247\331\204\330\252\330\255\331\203\331\205"
	.size	.L__log_5, 49

	.type	.L__alert_6,@object
	.p2align	4, 0x0
.L__alert_6:
	.asciz	"[\330\252\331\206\330\250\331\212\331\207 \331\205\330\263\330\252\331\210\331\211_2] \330\247\331\206\331\202\330\267\330\271 \330\255\330\263\330\247\330\263 \330\247\331\204\330\255\330\261\330\247\330\261\330\251"
	.size	.L__alert_6, 61

	.type	.L__alert_7,@object
	.p2align	4, 0x0
.L__alert_7:
	.asciz	"[\330\252\331\206\330\250\331\212\331\207 \331\205\330\263\330\252\331\210\331\211_1] \330\255\330\263\330\247\330\263 \330\247\331\204\330\255\330\261\330\247\330\261\330\251 \331\212\330\271\330\267\331\212 \331\202\331\212\331\205\330\251 \330\253\330\247\330\250\330\252\330\251"
	.size	.L__alert_7, 79

	.type	.L__alert_8,@object
	.p2align	4, 0x0
.L__alert_8:
	.asciz	"[\330\252\331\206\330\250\331\212\331\207 \331\205\330\263\330\252\331\210\331\211_1] \330\252\331\201\330\271\331\212\331\204 \330\247\331\204\330\252\330\250\330\261\331\212\330\257"
	.size	.L__alert_8, 52

	.type	.L__alert_9,@object
	.p2align	4, 0x0
.L__alert_9:
	.asciz	"[\330\252\331\206\330\250\331\212\331\207 \331\205\330\263\330\252\331\210\331\211_3] \330\255\330\247\331\204\330\251 \330\267\331\210\330\247\330\261\330\246: \330\255\330\261\330\247\330\261\330\251 \330\247\331\210 \330\266\330\272\330\267 \330\256\330\247\330\261\330\254 \330\247\331\204\330\255\330\257\331\210\330\257"
	.size	.L__alert_9, 92

	.type	__sustain_1305777795296,@object
	.section	.ldata,"awl",@progbits
	.p2align	3, 0x0
__sustain_1305777795296:
	.quad	-1
	.size	__sustain_1305777795296, 8

	.type	.L__alert_10,@object
	.section	.lrodata,"al",@progbits
	.p2align	4, 0x0
.L__alert_10:
	.asciz	"[\330\252\331\206\330\250\331\212\331\207 \331\205\330\263\330\252\331\210\331\211_2] \330\247\331\204\330\255\330\261\330\247\330\261\330\251 \331\205\330\261\330\252\331\201\330\271\330\251 \331\204\331\205\330\257\330\251 10 \330\253\331\210\330\247\331\206 \331\205\330\252\331\210\330\247\330\265\331\204\330\251"
	.size	.L__alert_10, 90

	.type	.L__rpt_fmt_11,@object
	.p2align	4, 0x0
.L__rpt_fmt_11:
	.asciz	"{\"\331\205\330\252\331\210\330\263\330\267 \330\247\331\204\330\255\330\261\330\247\330\261\330\251\":%f,\"\330\247\330\271\331\204\331\211 \330\266\330\272\330\267\":%f,\"\330\247\331\204\331\210\330\266\330\271\":%f}"
	.size	.L__rpt_fmt_11, 70

	.type	.L__rpt_id_12,@object
	.p2align	4, 0x0
.L__rpt_id_12:
	.asciz	"\330\252\331\202\330\261\331\212\330\261_\330\247\331\204\331\212\331\210\331\205\331\212"
	.size	.L__rpt_id_12, 24

	.type	.L__rpt_fmtarg_13,@object
.L__rpt_fmtarg_13:
	.asciz	"json"
	.size	.L__rpt_fmtarg_13, 5

	.type	.L__rpt_dir_14,@object
.L__rpt_dir_14:
	.asciz	"./mizan_reports"
	.size	.L__rpt_dir_14, 16

	.section	".note.GNU-stack","",@progbits
