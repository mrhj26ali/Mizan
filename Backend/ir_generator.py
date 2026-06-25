import llvmlite.ir as ir
import llvmlite.binding as llvm
from Ast.nodes import *
from semantic.symbols import SensorSymbol, ActuatorSymbol, ProcedureSymbol

class IRGenerator:
    def __init__(self, semantic_symbols=None, scan_cycle_ms=1000,
                 device_ip="127.0.0.1", device_port=5020,
                 mqtt_host="127.0.0.1", mqtt_port=1883,
                 data_dir="./mizan_reports", target_triple=None):
        self.module = ir.Module(name="mizan_program")
        self.module.triple = target_triple if target_triple else llvm.get_default_triple()
        self.i1     = ir.IntType(1)
        self.i8     = ir.IntType(8)
        self.i32    = ir.IntType(32)
        self.i64    = ir.IntType(64)
        self.double = ir.DoubleType()
        self.void   = ir.VoidType()
        self.i8ptr  = ir.PointerType(ir.IntType(8))
        self.builder: ir.IRBuilder = None
        self.function: ir.Function = None
        self._str_counter = 0
        self._loop_stack = []
        self._locals = {}
        self.mizan_symbols = semantic_symbols or {}
        self.global_syms = {}
        self.procedures  = {}
        self.proc_defs   = {}
        self.modes       = {}
        self.mode_order  = []
        self.mode_ids    = {}
        self.esc_defs    = {}
        self.esc_ids     = {}
        self.report_defs = []
        self.scan_cycle_ms = scan_cycle_ms
        self.device_ip     = device_ip
        self.device_port   = device_port
        self.mqtt_host     = mqtt_host
        self.mqtt_port     = mqtt_port
        self.data_dir      = data_dir
        self._next_sensor_id = 0
        self._next_actuator_id = 0
        self.g_modbus_ctx      = None
        self.g_mqtt_ctx        = None
        self.g_current_mode    = None
        self.g_pending_goto    = None
        self.g_wq_addrs        = None
        self.g_wq_values       = None
        self.g_wq_count        = None
        self.g_rpt_buf         = None  
        self.MAX_QUEUE         = 64
        self._declare_runtime_functions()

    def _decl(self, name, ret, args, var_arg=False):
        fnty = ir.FunctionType(ret, args, var_arg=var_arg)
        fn = ir.Function(self.module, fnty, name=name)
        setattr(self, f"_rt_{name.replace('.','_')}", fn)
        return fn

    def _declare_runtime_functions(self):
        v   = self.void;   i8p = self.i8ptr
        i32 = self.i32;    i64 = self.i64
        dbl = self.double; i1  = self.i1
        
        self._decl("setup_arabic_console", v,   [])
        self._decl("print_arabic",          v,   [i8p])
        self._decl("mizan_log",             v,   [i8p])
        self._decl("mizan_alert",           v,   [i32, i8p])
        self._decl("panic_div_zero",        v,   [])
        self._decl("panic_array_bounds",    v,   [i32, i32]) # ✅ NEW: Bounds checking panic
        
        self._decl("mizan_modbus_connect",       i8p, [i8p, i32])
        self._decl("mizan_modbus_read",          dbl, [i8p, i32])
        self._decl("mizan_modbus_write",         v,   [i8p, i32, dbl])
        self._decl("mizan_modbus_is_connected",  i32, [i8p])
        
        self._decl("mizan_mqtt_connect",  i8p, [i8p, i32, i8p])
        self._decl("mizan_mqtt_publish",  v,   [i8p, i8p, i8p])
        self._decl("__mizan_set_mqtt_ctx", v,  [i8p])
        
        self._decl("mizan_now_ms",   i64, [])
        self._decl("mizan_sleep_ms", v,   [i64])
        
        self._decl("mizan_ring_push", v,   [i32, dbl])
        self._decl("mizan_ring_avg",  dbl, [i32, i64])
        self._decl("mizan_ring_max",  dbl, [i32, i64])
        self._decl("mizan_ring_min",  dbl, [i32, i64])
        self._decl("mizan_ring_sum",  dbl, [i32, i64])
        self._decl("mizan_ring_rate", dbl, [i32, i64])
        self._decl("mizan_ring_last", dbl, [i32])
        
        # ✅ UPDATED: Edge-triggered health functions
        self._decl("mizan_health_track_disconnect", i32, [i32, i32])
        self._decl("mizan_health_track_stuck",      i32, [i32, dbl, i64]) # Changed return to i32
        self._decl("mizan_health_out_of_range",     i32, [i32, dbl, dbl, dbl]) # Added sid
        
        self._decl("mizan_escalation_tick", v,   [])
        self._decl("mizan_escalation_arm",  v,   [i32, i32, i64, i8p, i8p])
        self._decl("mizan_report_write", v, [i8p, i8p, i8p, i8p])
        
        # ✅ Predictive Maintenance & Scheduling Runtime Functions
        self._decl("mizan_actuator_cmd", v, [i32, dbl])
        self._decl("mizan_actuator_cycles", i32, [i32])
        self._decl("mizan_actuator_state", i32, [i32])
        self._decl("mizan_sensor_health", i32, [i32])
        self._decl("mizan_schedule_check", i32, [i32, i32, i32, i32, i32, i32])
        
        printf_ty   = ir.FunctionType(i32, [i8p], var_arg=True)
        snprintf_ty = ir.FunctionType(i32, [i8p, i64, i8p], var_arg=True)
        self._rt_printf   = ir.Function(self.module, printf_ty,   name="printf")
        self._rt_snprintf = ir.Function(self.module, snprintf_ty, name="snprintf")

    def _str_const(self, text: str, prefix="s") -> ir.Value:
        self._str_counter += 1
        encoded = (text + '\0').encode('utf-8')
        arr_ty  = ir.ArrayType(self.i8, len(encoded))
        name    = f"__{prefix}_{self._str_counter}"
        gv      = ir.GlobalVariable(self.module, arr_ty, name=name)
        gv.linkage = 'private'
        gv.global_constant = True
        gv.initializer = ir.Constant(arr_ty, bytearray(encoded))
        return self.builder.bitcast(gv, self.i8ptr)

    def _ast_type_to_llvm(self, type_node) -> ir.Type:
        if isinstance(type_node, ArrayTypeNode):
            return ir.ArrayType(self._ast_type_to_llvm(type_node.element_type), type_node.size)
        if isinstance(type_node, BaseTypeNode):
            n = type_node.type_name
            if n in ('حقيقي', 'عدد_حقيقي'): return self.double
            if n in ('صحيح',  'عدد_صحيح'):   return self.i32
            if n == 'منطقي':                  return self.i1
            return self.double # All units are doubles at runtime

    def _cast(self, val: ir.Value, target: ir.Type) -> ir.Value:
        if val.type == target: return val
        if isinstance(target, ir.DoubleType) and isinstance(val.type, ir.IntType):
            return self.builder.sitofp(val, self.double, "i2f")
        if isinstance(target, ir.IntType) and isinstance(val.type, ir.DoubleType):
            return self.builder.fptosi(val, target, "f2i")
        if isinstance(target, ir.IntType) and isinstance(val.type, ir.IntType):
            if target.width > val.type.width: return self.builder.sext(val, target, "sext")
            if target.width < val.type.width: return self.builder.trunc(val, target, "trunc")
        return val

    def _as_i1(self, val: ir.Value) -> ir.Value:
        if val.type == self.i1: return val
        if isinstance(val.type, ir.DoubleType):
            return self.builder.fcmp_ordered('!=', val, ir.Constant(self.double, 0.0))
        return self.builder.icmp_signed('!=', val, ir.Constant(val.type, 0))

    def _lookup(self, name: str) -> dict:
        if name in self._locals: return self._locals[name]
        return self.global_syms.get(name)

    def _load_var(self, name: str) -> ir.Value:
        info = self._lookup(name)
        if info is None: return ir.Constant(self.double, 0.0)
        return self.builder.load(info['gv'], name)

    def _safe_name(self, arabic: str) -> str:
        return "m" + str(abs(hash(arabic)) % 100000)

    def generate(self, ast_root: ProgramNode) -> str:
        print("🏭 بدء توليد كود LLVM IR...")
        self._pass1_collect(ast_root)
        self._pass2_declare_globals(ast_root)
        self._declare_scan_cycle_globals()
        self._pass3_declare_proc_signatures()
        self._pass4_emit_proc_bodies()
        self._emit_main(ast_root)
        print("✅ تم توليد كود LLVM IR بنجاح!")
        return str(self.module)

    def _pass1_collect(self, program: ProgramNode):
        for decl in program.declarations:
            if isinstance(decl, ModeBlockNode):
                self.modes[decl.mode_name] = decl; self.mode_order.append(decl.mode_name)
            elif isinstance(decl, ProcedureDefNode): self.proc_defs[decl.identifier] = decl
            elif isinstance(decl, EscalationDefNode): self.esc_defs[decl.identifier] = decl
            elif isinstance(decl, ReportDefNode): self.report_defs.append(decl)
            elif isinstance(decl, DeviceBlockNode): self._consume_device_block(decl)
        for i, name in enumerate(self.mode_order): self.mode_ids[name] = i
        for i, name in enumerate(self.esc_defs.keys()): self.esc_ids[name] = i

    def _consume_device_block(self, node: DeviceBlockNode):
        for f in node.fields:
            if f.key == 'IP': self.device_ip = f.value
            elif f.key == 'PORT': self.device_port = int(f.value)
            elif f.key == 'SCAN_CYCLE' and isinstance(f.value, DurationNode):
                self.scan_cycle_ms = int(f.value.to_seconds() * 1000)

    def _pass2_declare_globals(self, program: ProgramNode):
        for decl in program.declarations:
            if isinstance(decl, VarDeclNode): self._decl_global_var(decl)
            elif isinstance(decl, ConstDeclNode): self._decl_global_const(decl)
            elif isinstance(decl, SensorDeclNode): self._decl_sensor(decl)
            elif isinstance(decl, ActuatorDeclNode): self._decl_actuator(decl)

    def _make_global(self, name: str, llvm_type: ir.Type, linkage='internal') -> ir.GlobalVariable:
        gv = ir.GlobalVariable(self.module, llvm_type, name=name)
        gv.linkage = linkage
        gv.initializer = ir.Constant(llvm_type, None)
        return gv

    def _decl_global_var(self, node: VarDeclNode):
        lt = self._ast_type_to_llvm(node.var_type)
        gv = self._make_global(f"g_{node.identifier}", lt)
        is_arr = isinstance(node.var_type, ArrayTypeNode)
        self.global_syms[node.identifier] = {'gv': gv, 'type': lt, 'kind': 'var', 'is_array': is_arr, 'array_size': node.var_type.size if is_arr else 0, 'init_expr': node.expr}

    def _decl_global_const(self, node: ConstDeclNode):
        lt = self._ast_type_to_llvm(node.var_type)
        gv = self._make_global(f"c_{node.identifier}", lt)
        self.global_syms[node.identifier] = {'gv': gv, 'type': lt, 'kind': 'const', 'is_array': False, 'init_expr': node.expr}

    def _decl_sensor(self, node: SensorDeclNode):
        address, health, rng = 0, [], None
        for f in node.fields:
            if f.key == 'ADDRESS':
                raw = f.value; address = int(raw, 16) if isinstance(raw, str) and raw.startswith('0x') else int(raw)
            elif f.key == 'HEALTH': health = f.value
            elif f.key == 'RANGE' and isinstance(f.value, RangeSpecNode): rng = (f.value.min_val, f.value.max_val)
        gv = self._make_global(f"s_{node.identifier}", self.double)
        conn_gv = self._make_global(f"s_{node.identifier}_conn", self.i32)
        conn_gv.initializer = ir.Constant(self.i32, 1)
        sid = self._next_sensor_id; self._next_sensor_id += 1
        self.global_syms[node.identifier] = {'gv': gv, 'type': self.double, 'kind': 'sensor', 'is_array': False, 'address': address, 'sensor_id': sid, 'conn_gv': conn_gv, 'health': health, 'range': rng}

    def _decl_actuator(self, node: ActuatorDeclNode):
        address = 0
        for f in node.fields:
            if f.key == 'ADDRESS':
                raw = f.value; address = int(raw, 16) if isinstance(raw, str) and raw.startswith('0x') else int(raw)
        gv = self._make_global(f"a_{node.identifier}", self.double)
        aid = self._next_actuator_id; self._next_actuator_id += 1
        self.global_syms[node.identifier] = {'gv': gv, 'type': self.double, 'kind': 'actuator', 'is_array': False, 'address': address, 'actuator_id': aid}

    def _declare_scan_cycle_globals(self):
        def mk(name, lt, init_val=None):
            gv = ir.GlobalVariable(self.module, lt, name=name)
            gv.linkage = 'internal'
            gv.initializer = ir.Constant(lt, init_val if init_val is not None else 0)
            return gv
        self.g_modbus_ctx   = mk("__modbus_ctx",   self.i8ptr, None)
        self.g_modbus_ctx.initializer = ir.Constant(self.i8ptr, None)
        self.g_mqtt_ctx     = mk("__mqtt_ctx",     self.i8ptr, None)
        self.g_mqtt_ctx.initializer = ir.Constant(self.i8ptr, None)
        self.g_current_mode = mk("__current_mode", self.i32,   0)
        self.g_pending_goto = mk("__pending_goto",  self.i32,   -1)
        addr_arr = ir.ArrayType(self.i32,    self.MAX_QUEUE)
        val_arr  = ir.ArrayType(self.double, self.MAX_QUEUE)
        self.g_wq_addrs  = mk("__wq_addrs",  addr_arr)
        self.g_wq_values = mk("__wq_values", val_arr)
        self.g_wq_count  = mk("__wq_count",  self.i32, 0)
        self.g_wq_addrs.initializer  = ir.Constant(addr_arr, [ir.Constant(self.i32, 0)]    * self.MAX_QUEUE)
        self.g_wq_values.initializer = ir.Constant(val_arr,  [ir.Constant(self.double, 0.0)] * self.MAX_QUEUE)
        rpt_buf_ty = ir.ArrayType(self.i8, 2048)
        self.g_rpt_buf = ir.GlobalVariable(self.module, rpt_buf_ty, name="__rpt_buf")
        self.g_rpt_buf.linkage = 'internal'
        self.g_rpt_buf.initializer = ir.Constant(rpt_buf_ty, bytearray(2048))

    def _pass3_declare_proc_signatures(self):
        for name, node in self.proc_defs.items():
            param_types = [self._ast_type_to_llvm(p.var_type) for p in node.params]
            ret_type    = self._ast_type_to_llvm(node.return_type) if node.return_type else self.void
            fnty = ir.FunctionType(ret_type, param_types)
            fn   = ir.Function(self.module, fnty, name=f"proc_{name}")
            for arg, p in zip(fn.args, node.params): arg.name = p.identifier
            self.procedures[name] = fn

    def _pass4_emit_proc_bodies(self):
        for name, node in self.proc_defs.items():
            fn = self.procedures[name]
            old_fn, old_bld, old_loc = self.function, self.builder, self._locals
            self.function = fn
            entry = fn.append_basic_block('entry')
            self.builder = ir.IRBuilder(entry)
            self._locals  = {}
            for arg, p in zip(fn.args, node.params):
                slot = self.builder.alloca(arg.type, name=f"{p.identifier}_slot")
                self.builder.store(arg, slot)
                self._locals[p.identifier] = {'gv': slot, 'type': arg.type, 'kind': 'local'}
            for stmt in node.body:
                self._emit_stmt(stmt)
                if isinstance(stmt, ReturnStmtNode): break
            if not self.builder.block.is_terminated:
                rt = fn.function_type.return_type
                if isinstance(rt, ir.VoidType): self.builder.ret_void()
                else: self.builder.ret(ir.Constant(rt, 0))
            self.function, self.builder, self._locals = old_fn, old_bld, old_loc

    def _emit_main(self, program: ProgramNode):
        fn_ty = ir.FunctionType(self.i32, [])
        self.function = ir.Function(self.module, fn_ty, name="main")
        entry = self.function.append_basic_block('entry')
        self.builder = ir.IRBuilder(entry)
        self._locals  = {}
        self.builder.call(self._rt_setup_arabic_console, [])
        ip_str  = self._str_const(self.device_ip,  "dev_ip")
        mb_ctx  = self.builder.call(self._rt_mizan_modbus_connect, [ip_str, ir.Constant(self.i32, self.device_port)])
        self.builder.store(mb_ctx, self.g_modbus_ctx)
        mq_host = self._str_const(self.mqtt_host, "mq_host")
        mq_cid  = self._str_const("mizan-runtime", "mq_cid")
        mq_ctx  = self.builder.call(self._rt_mizan_mqtt_connect, [mq_host, ir.Constant(self.i32, self.mqtt_port), mq_cid])
        self.builder.store(mq_ctx, self.g_mqtt_ctx)
        self.builder.call(self._rt___mizan_set_mqtt_ctx, [mq_ctx])
        for name, info in self.global_syms.items():
            if info['kind'] in ('var', 'const') and info.get('init_expr') is not None:
                val = self._emit_expr(info['init_expr'])
                self.builder.store(self._cast(val, info['type']), info['gv'])
        startup_id = self.mode_ids.get('اقلاع', self.mode_ids.get(self.mode_order[0], 0) if self.mode_order else 0)
        self.builder.store(ir.Constant(self.i32, startup_id), self.g_current_mode)
        startup_node = self.modes.get('اقلاع')
        if startup_node and startup_node.on_start_statements:
            for stmt in startup_node.on_start_statements: self._emit_stmt(stmt)
        scan_block = self.function.append_basic_block('scan_cycle')
        self.builder.branch(scan_block)
        self.builder.position_at_end(scan_block)
        cycle_start = self.builder.call(self._rt_mizan_now_ms, [], "cycle_start")
        self._emit_input_scan()
        self._emit_logic_solve()
        self._emit_output_scan()
        self.builder.call(self._rt_mizan_escalation_tick, [])
        self._emit_reports_tick()
        self._emit_mode_switch()
        self._emit_cycle_sleep(cycle_start)
        self.builder.branch(scan_block)

    # ✅ UPGRADED: Watchdog Safe State on Disconnect
    def _emit_input_scan(self):
        mb = self.builder.load(self.g_modbus_ctx, "mb")
        
        global_conn = self.builder.call(self._rt_mizan_modbus_is_connected, [mb], "global_conn")
        is_disconnected = self.builder.icmp_signed('==', global_conn, ir.Constant(self.i32, 0))
        
        flush_bb = self.function.append_basic_block("safe_state_flush")
        cont_bb = self.function.append_basic_block("scan_sensors")
        self.builder.cbranch(is_disconnected, flush_bb, cont_bb)
        
        self.builder.position_at_end(flush_bb)
        self.builder.store(ir.Constant(self.i32, 0), self.g_wq_count) # Flush queue
        for name, info in self.global_syms.items():
            if info['kind'] == 'actuator':
                self.builder.store(ir.Constant(self.double, 0.0), info['gv']) # Force Safe State
        self.builder.branch(cont_bb)
        
        self.builder.position_at_end(cont_bb)
        
        for name, info in self.global_syms.items():
            if info['kind'] != 'sensor': continue
            addr  = ir.Constant(self.i32, info['address'])
            sid   = ir.Constant(self.i32, info['sensor_id'])
            raw   = self.builder.call(self._rt_mizan_modbus_read, [mb, addr], f"raw_{name}")
            self.builder.store(raw, info['gv'])
            
            conn_raw = self.builder.call(self._rt_mizan_modbus_is_connected, [mb], f"conn_{name}")
            self.builder.store(conn_raw, info['conn_gv'])
            
            is_conn = self.builder.icmp_signed('!=', conn_raw, ir.Constant(self.i32, 0))
            with self.builder.if_then(is_conn):
                self.builder.call(self._rt_mizan_ring_push, [sid, raw])
                
            self._emit_health_rules(name, info, raw, conn_raw)

    # ✅ UPGRADED: Edge-Triggered Health Rules (ISA-18.2)
    def _emit_health_rules(self, sensor_name: str, info: dict, raw: ir.Value, conn: ir.Value):
        sid = ir.Constant(self.i32, info['sensor_id'])
        for rule in info['health']:
            if rule.kind == 'DISCONNECT':
                is_disc_edge = self.builder.call(self._rt_mizan_health_track_disconnect, [sid, conn], "disc_edge")
                with self.builder.if_then(self.builder.icmp_signed('!=', is_disc_edge, ir.Constant(self.i32, 0))):
                    for s in rule.statements: self._emit_stmt(s)
            elif rule.kind == 'STUCK':
                thr_ms = int(rule.duration.to_seconds() * 1000) if rule.duration else 60000
                stuck_edge = self.builder.call(self._rt_mizan_health_track_stuck, [sid, raw, ir.Constant(self.i64, thr_ms)], "stuck_edge")
                with self.builder.if_then(self.builder.icmp_signed('!=', stuck_edge, ir.Constant(self.i32, 0))):
                    for s in rule.statements: self._emit_stmt(s)
            elif rule.kind == 'OUT_OF_RANGE':
                rng = info.get('range') or (-1e18, 1e18)
                oor_edge = self.builder.call(self._rt_mizan_health_out_of_range, [sid, raw, ir.Constant(self.double, rng[0]), ir.Constant(self.double, rng[1])], "oor_edge")
                with self.builder.if_then(self.builder.icmp_signed('!=', oor_edge, ir.Constant(self.i32, 0))):
                    for s in rule.statements: self._emit_stmt(s)

    def _emit_logic_solve(self):
        cur_mode = self.builder.load(self.g_current_mode, "cur_mode")
        default_bb = self.function.append_basic_block('mode_default')
        end_bb     = self.function.append_basic_block('mode_end')
        sw = self.builder.switch(cur_mode, default_bb)
        for mode_name in self.mode_order:
            node    = self.modes[mode_name]
            mode_id = self.mode_ids[mode_name]
            bb      = self.function.append_basic_block(f"mode_{self._safe_name(mode_name)}")
            sw.add_case(ir.Constant(self.i32, mode_id), bb)
            self.builder.position_at_end(bb)
            self._current_mode_name = mode_name
            for rule in node.rules: self._emit_rule(rule)
            if not self.builder.block.is_terminated: self.builder.branch(end_bb)
        self.builder.position_at_end(default_bb)
        if not self.builder.block.is_terminated: self.builder.branch(end_bb)
        self.builder.position_at_end(end_bb)

    def _emit_rule(self, rule: RuleBlockNode):
        saved_locals = dict(self._locals)
        for local in rule.local_declarations: self._emit_local_decl(local)
        for stmt in rule.statements: self._emit_stmt(stmt)
        self._locals = saved_locals

    def _emit_local_decl(self, node):
        if isinstance(node, (VarDeclNode, ConstDeclNode)):
            lt   = self._ast_type_to_llvm(node.var_type)
            slot = self.builder.alloca(lt, name=f"loc_{node.identifier}")
            if node.expr: self.builder.store(self._cast(self._emit_expr(node.expr), lt), slot)
            self._locals[node.identifier] = {'gv': slot, 'type': lt, 'kind': 'local'}

    def _queue_write(self, address: int, value: ir.Value):
        count   = self.builder.load(self.g_wq_count, "wqc")
        in_bnd  = self.builder.icmp_signed('<', count, ir.Constant(self.i32, self.MAX_QUEUE))
        with self.builder.if_then(in_bnd):
            aslot = self.builder.gep(self.g_wq_addrs, [ir.Constant(self.i32, 0), count], inbounds=True)
            vslot = self.builder.gep(self.g_wq_values, [ir.Constant(self.i32, 0), count], inbounds=True)
            self.builder.store(ir.Constant(self.i32, address), aslot)
            self.builder.store(value, vslot)
            self.builder.store(self.builder.add(count, ir.Constant(self.i32, 1)), self.g_wq_count)

    def _emit_output_scan(self):
        count  = self.builder.load(self.g_wq_count, "flush_n")
        mb     = self.builder.load(self.g_modbus_ctx, "mb_out")
        idx    = self.builder.alloca(self.i32, name="fi")
        self.builder.store(ir.Constant(self.i32, 0), idx)
        cond_bb = self.function.append_basic_block('flush_cond')
        body_bb = self.function.append_basic_block('flush_body')
        end_bb  = self.function.append_basic_block('flush_end')
        self.builder.branch(cond_bb)
        self.builder.position_at_end(cond_bb)
        i = self.builder.load(idx)
        self.builder.cbranch(self.builder.icmp_signed('<', i, count), body_bb, end_bb)
        self.builder.position_at_end(body_bb)
        i = self.builder.load(idx)
        aslot = self.builder.gep(self.g_wq_addrs,  [ir.Constant(self.i32,0), i], inbounds=True)
        vslot = self.builder.gep(self.g_wq_values, [ir.Constant(self.i32,0), i], inbounds=True)
        a = self.builder.load(aslot); v = self.builder.load(vslot)
        self.builder.call(self._rt_mizan_modbus_write, [mb, a, v])
        self.builder.store(self.builder.add(i, ir.Constant(self.i32, 1)), idx)
        self.builder.branch(cond_bb)
        self.builder.position_at_end(end_bb)
        self.builder.store(ir.Constant(self.i32, 0), self.g_wq_count)

    def _emit_reports_tick(self):
        for rpt_id, rpt in enumerate(self.report_defs):
            save_dir, fmt = self.data_dir, "json"
            schedule = None
            for f in rpt.fields:
                if f.key == 'SAVE_IN': save_dir = f.value
                elif f.key == 'FORMAT': fmt = f.value.lower()
                elif f.key == 'SCHEDULE': schedule = f.value
            
            if not schedule: continue
            
            if schedule.frequency == 'INTERVAL':
                timer_key = f"__rpt_timer_{rpt_id}"
                if timer_key not in self.global_syms:
                    tg = ir.GlobalVariable(self.module, self.i64, name=timer_key)
                    tg.linkage = 'internal'
                    tg.initializer = ir.Constant(self.i64, -1)
                    self.global_syms[timer_key] = {'gv': tg, 'type': self.i64}
                timer_gv = self.global_syms[timer_key]['gv']
                now = self.builder.call(self._rt_mizan_now_ms, [], "rpt_now")
                next_fire = self.builder.load(timer_gv, "next_fire")
                is_first = self.builder.icmp_signed('==', next_fire, ir.Constant(self.i64, -1))
                with self.builder.if_then(is_first):
                    self.builder.store(self.builder.add(now, ir.Constant(self.i64, schedule.interval_ms)), timer_gv)
                is_due = self.builder.icmp_signed('>=', now, next_fire)
                with self.builder.if_then(is_due):
                    self._emit_single_report(rpt, save_dir, fmt, rpt_id)
                    self.builder.store(self.builder.add(now, ir.Constant(self.i64, schedule.interval_ms)), timer_gv)
            else:
                type_id = {'DAILY': 1, 'WEEKLY': 2, 'MONTHLY': 3}[schedule.frequency]
                day = schedule.target_day if schedule.target_day is not None else 0
                hour, min = map(int, schedule.time_str.split(':'))
                is_last = 1 if schedule.is_last_day else 0
                
                should_fire = self.builder.call(self._rt_mizan_schedule_check, [
                    ir.Constant(self.i32, rpt_id), ir.Constant(self.i32, type_id),
                    ir.Constant(self.i32, day), ir.Constant(self.i32, hour), ir.Constant(self.i32, min),
                    ir.Constant(self.i32, is_last)
                ])
                with self.builder.if_then(self.builder.icmp_signed('!=', should_fire, ir.Constant(self.i32, 0))):
                    self._emit_single_report(rpt, save_dir, fmt, rpt_id)

    def _emit_single_report(self, rpt, save_dir, fmt, rpt_id):
        buf_ptr = self.builder.bitcast(self.g_rpt_buf, self.i8ptr)
        parts, args = ["{"], []
        first = True
        for item in rpt.content:
            comma = "" if first else ","
            first = False
            if item.kind == 'AGGREGATE':
                sid = self.global_syms.get(item.identifier, {}).get('sensor_id')
                if sid is None: continue
                wms = int(item.duration.to_seconds() * 1000)
                fn_map = {'متوسط': self._rt_mizan_ring_avg, 'اقصى': self._rt_mizan_ring_max,
                          'ادنى': self._rt_mizan_ring_min, 'مجموع': self._rt_mizan_ring_sum,
                          'معدل_التغيير': self._rt_mizan_ring_rate}
                rfn = fn_map.get(item.function_name)
                if rfn: val = self.builder.call(rfn, [ir.Constant(self.i32, sid), ir.Constant(self.i64, wms)]); parts.append(f'{comma}"{item.title}":%f'); args.append(val)
            elif item.kind == 'INSTANT':
                info = self._lookup(item.identifier)
                if info: val = self._cast(self.builder.load(info['gv']), self.double); parts.append(f'{comma}"{item.title}":%f'); args.append(val)
            elif item.kind == 'CYCLE_COUNT':
                aid = self.global_syms.get(item.identifier, {}).get('actuator_id')
                if aid is not None: val = self.builder.call(self._rt_mizan_actuator_cycles, [ir.Constant(self.i32, aid)]); parts.append(f'{comma}"{item.title}":%d'); args.append(val)
            elif item.kind == 'ACTUATOR_STATE':
                aid = self.global_syms.get(item.identifier, {}).get('actuator_id')
                if aid is not None: val = self.builder.call(self._rt_mizan_actuator_state, [ir.Constant(self.i32, aid)]); parts.append(f'{comma}"{item.title}":%d'); args.append(val)
            elif item.kind == 'SENSOR_HEALTH':
                sid = self.global_syms.get(item.identifier, {}).get('sensor_id')
                if sid is not None: val = self.builder.call(self._rt_mizan_sensor_health, [ir.Constant(self.i32, sid)]); parts.append(f'{comma}"{item.title}":%d'); args.append(val)
            elif item.kind == 'CURRENT_MODE':
                val = self._cast(self.builder.load(self.g_current_mode), self.double); parts.append(f'{comma}"{item.title}":%f'); args.append(val)
                
        parts.append("}")
        fmt_str = "".join(parts)
        fmt_gv  = self._str_const(fmt_str, "rpt_fmt")
        self.builder.call(self._rt_snprintf, [buf_ptr, ir.Constant(self.i64, 2048), fmt_gv] + args)
        id_str  = self._str_const(rpt.identifier, "rpt_id")
        fmt_arg = self._str_const(fmt, "rpt_fmtarg")
        dir_str = self._str_const(save_dir, "rpt_dir")
        self.builder.call(self._rt_mizan_report_write, [id_str, fmt_arg, dir_str, buf_ptr])

    def _emit_mode_switch(self):
        pending  = self.builder.load(self.g_pending_goto, "pending")
        has_goto = self.builder.icmp_signed('!=', pending, ir.Constant(self.i32, -1))
        with self.builder.if_then(has_goto):
            self.builder.store(pending, self.g_current_mode)
            self.builder.store(ir.Constant(self.i32, -1), self.g_pending_goto)

    def _emit_cycle_sleep(self, cycle_start: ir.Value):
        now     = self.builder.call(self._rt_mizan_now_ms, [], "now")
        elapsed = self.builder.sub(now, cycle_start, "elapsed")
        target  = ir.Constant(self.i64, self.scan_cycle_ms)
        remain  = self.builder.sub(target, elapsed, "remain")
        pos     = self.builder.icmp_signed('>', remain, ir.Constant(self.i64, 0))
        with self.builder.if_then(pos):
            self.builder.call(self._rt_mizan_sleep_ms, [remain])

    def _emit_stmt(self, node):
        if node is None or self.builder.block.is_terminated: return
        m = getattr(self, f"_stmt_{type(node).__name__}", None)
        if m: m(node)

    def _stmt_CommandStmtNode(self, node: CommandStmtNode):
        info = self._lookup(node.identifier)
        if info is None or info['kind'] != 'actuator': return
        VALS = {'تشغيل':1.0,'ايقاف':0.0,'مفتوح':1.0,'مغلق':0.0,'نشط':1.0,'غير_نشط':0.0}
        wv = ir.Constant(self.double, VALS.get(node.value, 1.0)) if isinstance(node.value, str) else self._cast(self._emit_expr(node.value), self.double)
        self.builder.store(wv, info['gv'])
        self.builder.call(self._rt_mizan_actuator_cmd, [ir.Constant(self.i32, info['actuator_id']), wv])
        self._queue_write(info['address'], wv)

    def _stmt_AlertStmtNode(self, node: AlertStmtNode):
        lvl_map = {'مستوى_1': 1, 'مستوى_2': 2, 'مستوى_3': 3}
        lvl = ir.Constant(self.i32, lvl_map.get(node.level, 1))
        msg = self._str_const(f"[تنبيه {node.level}] {node.message}", "alert")
        self.builder.call(self._rt_mizan_alert, [lvl, msg])

    def _stmt_LogStmtNode(self, node: LogStmtNode):
        msg = self._str_const(node.message, "log")
        self.builder.call(self._rt_mizan_log, [msg])

    def _stmt_GotoStmtNode(self, node: GotoStmtNode):
        tid = self.mode_ids.get(node.target_mode, -1)
        self.builder.store(ir.Constant(self.i32, tid), self.g_pending_goto)

    def _stmt_WaitStmtNode(self, node: WaitStmtNode):
        ms = int(node.duration.to_seconds() * 1000)
        self.builder.call(self._rt_mizan_sleep_ms, [ir.Constant(self.i64, ms)])

    def _stmt_AssignStmtNode(self, node: AssignStmtNode):
        info = self._lookup(node.identifier)
        if info is None: return
        val  = self._emit_expr(node.expr)
        if node.index_expr is not None and info.get('is_array'):
            idx  = self._cast(self._emit_expr(node.index_expr), self.i32)
            slot = self.builder.gep(info['gv'], [ir.Constant(self.i32,0), idx], inbounds=True)
            self.builder.store(self._cast(val, info['type'].element), slot)
        else:
            self.builder.store(self._cast(val, info['type']), info['gv'])

    def _stmt_DefaultValStmtNode(self, node: DefaultValStmtNode): pass
    def _stmt_ExprStmtNode(self, node: ExprStmtNode): self._emit_expr(node.expr)

    def _stmt_IfStmtNode(self, node: IfStmtNode):
        cond = self._emit_cond(node.condition)
        then_bb = self.function.append_basic_block('if_then'); else_bb = self.function.append_basic_block('if_else'); merge_bb = self.function.append_basic_block('if_end')
        self.builder.cbranch(cond, then_bb, else_bb)
        self.builder.position_at_end(then_bb)
        for s in node.then_branch: self._emit_stmt(s)
        if not self.builder.block.is_terminated: self.builder.branch(merge_bb)
        self.builder.position_at_end(else_bb)
        for s in node.else_branch: self._emit_stmt(s)
        if not self.builder.block.is_terminated: self.builder.branch(merge_bb)
        self.builder.position_at_end(merge_bb)

    def _stmt_WhileStmtNode(self, node: WhileStmtNode):
        cond_bb = self.function.append_basic_block('while_cond'); body_bb = self.function.append_basic_block('while_body'); end_bb = self.function.append_basic_block('while_end')
        self.builder.branch(cond_bb); self.builder.position_at_end(cond_bb)
        self.builder.cbranch(self._emit_cond(node.condition), body_bb, end_bb)
        self.builder.position_at_end(body_bb); self._loop_stack.append((cond_bb, end_bb))
        for s in node.body: self._emit_stmt(s)
        self._loop_stack.pop()
        if not self.builder.block.is_terminated: self.builder.branch(cond_bb)
        self.builder.position_at_end(end_bb)

    def _stmt_ReturnStmtNode(self, node: ReturnStmtNode):
        rt = self.function.function_type.return_type
        if node.expr: self.builder.ret(self._cast(self._emit_expr(node.expr), rt))
        else: self.builder.ret_void()

    def _emit_cond(self, node) -> ir.Value:
        m = getattr(self, f"_cond_{type(node).__name__}", None)
        if m: return m(node)
        return self._as_i1(self._emit_expr(node))

    def _cond_BinaryCondNode(self, node: BinaryCondNode) -> ir.Value:
        if node.op == 'AND':
            lhs = self._emit_cond(node.left); rhs_bb = self.function.append_basic_block('and_rhs'); merge_bb = self.function.append_basic_block('and_end'); entry_bb = self.builder.block
            self.builder.cbranch(lhs, rhs_bb, merge_bb); self.builder.position_at_end(rhs_bb)
            rhs = self._emit_cond(node.right); rhs_end = self.builder.block; self.builder.branch(merge_bb)
            self.builder.position_at_end(merge_bb); phi = self.builder.phi(self.i1, "and_res")
            phi.add_incoming(ir.Constant(self.i1, 0), entry_bb); phi.add_incoming(rhs, rhs_end); return phi
        else:
            lhs = self._emit_cond(node.left); rhs_bb = self.function.append_basic_block('or_rhs'); merge_bb = self.function.append_basic_block('or_end'); entry_bb = self.builder.block
            self.builder.cbranch(lhs, merge_bb, rhs_bb); self.builder.position_at_end(rhs_bb)
            rhs = self._emit_cond(node.right); rhs_end = self.builder.block; self.builder.branch(merge_bb)
            self.builder.position_at_end(merge_bb); phi = self.builder.phi(self.i1, "or_res")
            phi.add_incoming(ir.Constant(self.i1, 1), entry_bb); phi.add_incoming(rhs, rhs_end); return phi

    def _cond_NotCondNode(self, node: NotCondNode) -> ir.Value: return self.builder.not_(self._emit_cond(node.operand), "not_res")

    def _cond_CompExprNode(self, node: CompExprNode) -> ir.Value:
        lv = self._emit_expr(node.left); rv = self._emit_expr(node.right)
        is_f = isinstance(lv.type, ir.DoubleType) or isinstance(rv.type, ir.DoubleType)
        if is_f: lv = self._cast(lv, self.double); rv = self._cast(rv, self.double); return self.builder.fcmp_ordered(node.op, lv, rv, "fcmp")
        return self.builder.icmp_signed(node.op, lv, rv, "icmp")

    def _cond_TemporalCondNode(self, node: TemporalCondNode) -> ir.Value:
        key = f"__sustain_{id(node)}"
        if key not in self.global_syms:
            tg = ir.GlobalVariable(self.module, self.i64, name=key); tg.linkage = 'internal'; tg.initializer = ir.Constant(self.i64, -1)
            self.global_syms[key] = {'gv': tg, 'type': self.i64, 'kind': 'sustain'}
        tg = self.global_syms[key]['gv']
        inner = self._emit_cond(node.condition); now = self.builder.call(self._rt_mizan_now_ms, [], "t_now")
        res_ptr = self.builder.alloca(self.i1, name="sus_res"); self.builder.store(ir.Constant(self.i1, 0), res_ptr)
        true_bb = self.function.append_basic_block('sus_true'); false_bb = self.function.append_basic_block('sus_false'); done_bb = self.function.append_basic_block('sus_done')
        self.builder.cbranch(inner, true_bb, false_bb)
        self.builder.position_at_end(true_bb); tv = self.builder.load(tg); unset = self.builder.icmp_signed('==', tv, ir.Constant(self.i64, -1))
        set_bb = self.function.append_basic_block('sus_set'); chk_bb = self.function.append_basic_block('sus_chk'); self.builder.cbranch(unset, set_bb, chk_bb)
        self.builder.position_at_end(set_bb); self.builder.store(now, tg); self.builder.branch(chk_bb)
        self.builder.position_at_end(chk_bb); started = self.builder.load(tg); elapsed = self.builder.sub(now, started)
        thr = ir.Constant(self.i64, int(node.duration.to_seconds() * 1000)); ok = self.builder.icmp_signed('>=', elapsed, thr)
        self.builder.store(ok, res_ptr); self.builder.branch(done_bb)
        self.builder.position_at_end(false_bb); self.builder.store(ir.Constant(self.i64, -1), tg); self.builder.store(ir.Constant(self.i1, 0), res_ptr); self.builder.branch(done_bb)
        self.builder.position_at_end(done_bb); return self.builder.load(res_ptr)

    def _cond_VotingCondNode(self, node: VotingCondNode) -> ir.Value:
        cnt_ptr = self.builder.alloca(self.i32, name="vote_cnt"); self.builder.store(ir.Constant(self.i32, 0), cnt_ptr)
        for comp in node.comparisons:
            cv = self._cond_CompExprNode(comp); cur = self.builder.load(cnt_ptr); inc = self.builder.add(cur, ir.Constant(self.i32, 1))
            self.builder.store(self.builder.select(cv, inc, cur), cnt_ptr)
        final = self.builder.load(cnt_ptr); return self.builder.icmp_signed('>=', final, ir.Constant(self.i32, node.threshold))

    def _cond_BooleanLiteralNode(self, node: BooleanLiteralNode) -> ir.Value: return ir.Constant(self.i1, 1 if node.value else 0)
    def _cond_VariableCondNode(self, node: VariableCondNode) -> ir.Value: return self._as_i1(self._load_var(node.identifier))

    def _emit_expr(self, node) -> ir.Value:
        m = getattr(self, f"_expr_{type(node).__name__}", None)
        if m: return m(node)
        return ir.Constant(self.double, 0.0)

    def _expr_NumberLiteralNode(self, node: NumberLiteralNode) -> ir.Value:
        return ir.Constant(self.double, float(node.value)) if isinstance(node.value, float) else ir.Constant(self.i32, int(node.value))
    def _expr_BooleanLiteralNode(self, node: BooleanLiteralNode) -> ir.Value: return ir.Constant(self.i1, 1 if node.value else 0)
    def _expr_StringLiteralNode(self, node: StringLiteralNode) -> ir.Value: return self._str_const(node.value, "strlit")

    # ✅ UPGRADED: Array Bounds Checking
    def _expr_VariableExprNode(self, node: VariableExprNode) -> ir.Value:
        info = self._lookup(node.identifier)
        if info is None: return ir.Constant(self.double, 0.0)
        if node.index_expr is not None and info.get('is_array'):
            idx = self._cast(self._emit_expr(node.index_expr), self.i32)
            size = info.get('array_size', 0)
            
            is_out_of_bounds = self.builder.or_(
                self.builder.icmp_signed('<', idx, ir.Constant(self.i32, 0)),
                self.builder.icmp_signed('>=', idx, ir.Constant(self.i32, size))
            )
            panic_bb = self.function.append_basic_block("array_panic")
            safe_bb = self.function.append_basic_block("array_safe")
            self.builder.cbranch(is_out_of_bounds, panic_bb, safe_bb)
            
            self.builder.position_at_end(panic_bb)
            self.builder.call(self._rt_panic_array_bounds, [idx, ir.Constant(self.i32, size)])
            self.builder.unreachable()
            
            self.builder.position_at_end(safe_bb)
            slot = self.builder.gep(info['gv'], [ir.Constant(self.i32,0), idx], inbounds=True)
            return self.builder.load(slot, f"{node.identifier}_el")
            
        return self.builder.load(info['gv'], node.identifier)

    def _expr_BinaryOpNode(self, node: BinaryOpNode) -> ir.Value:
        lv = self._emit_expr(node.left)
        rv = self._emit_expr(node.right)
        
        is_f = isinstance(lv.type, ir.DoubleType) or isinstance(rv.type, ir.DoubleType)
        
        # ✅ RUNTIME PANIC MODE: Check for Division by Zero
        if node.op in ('/', '%'):
            rv_dbl = self._cast(rv, self.double)
            is_zero = self.builder.fcmp_ordered('==', rv_dbl, ir.Constant(self.double, 0.0), "is_zero")
            
            panic_bb = self.function.append_basic_block("div_zero_panic")
            safe_bb  = self.function.append_basic_block("div_safe")
            
            self.builder.cbranch(is_zero, panic_bb, safe_bb)
            
            self.builder.position_at_end(panic_bb)
            self.builder.call(self._rt_panic_div_zero, [])
            self.builder.unreachable() 
            
            self.builder.position_at_end(safe_bb)
            lv_dbl = self._cast(lv, self.double)
            if node.op == '/': return self.builder.fdiv(lv_dbl, rv_dbl, "fdiv")
            if node.op == '%': return self.builder.frem(lv_dbl, rv_dbl, "frem")

        if is_f:
            lv = self._cast(lv, self.double); rv = self._cast(rv, self.double)
            if node.op == '+': return self.builder.fadd(lv, rv, "fadd")
            if node.op == '-': return self.builder.fsub(lv, rv, "fsub")
            if node.op == '*': return self.builder.fmul(lv, rv, "fmul")
        else:
            if node.op == '+': return self.builder.add(lv, rv, "add")
            if node.op == '-': return self.builder.sub(lv, rv, "sub")
            if node.op == '*': return self.builder.mul(lv, rv, "mul")
            if node.op == '%': return self.builder.srem(lv, rv, "rem")
            
        return ir.Constant(self.double, 0.0)

    def _expr_UnaryMinusNode(self, node: UnaryMinusNode) -> ir.Value:
        v = self._emit_expr(node.operand)
        return self.builder.fneg(v, "fneg") if isinstance(v.type, ir.DoubleType) else self.builder.neg(v, "neg")

    def _expr_AggregateExprNode(self, node: AggregateExprNode) -> ir.Value:
        info = self.global_syms.get(node.identifier)
        if info is None: return ir.Constant(self.double, 0.0)
        sid = ir.Constant(self.i32, info['sensor_id']); wms = ir.Constant(self.i64, int(node.duration.to_seconds() * 1000))
        fn_map = {'متوسط': self._rt_mizan_ring_avg, 'اقصى': self._rt_mizan_ring_max, 'ادنى': self._rt_mizan_ring_min, 'مجموع': self._rt_mizan_ring_sum, 'معدل_التغيير': self._rt_mizan_ring_rate}
        if node.function_name == 'اخر': return self.builder.call(self._rt_mizan_ring_last, [sid], "last")
        rfn = fn_map.get(node.function_name)
        return self.builder.call(rfn, [sid, wms], "agg") if rfn else ir.Constant(self.double, 0.0)

    def _expr_ProcCallExprNode(self, node: ProcCallExprNode) -> ir.Value:
        fn = self.procedures.get(node.identifier)
        if fn is None: return ir.Constant(self.double, 0.0)
        args = [self._cast(self._emit_expr(e), p.type) for e, p in zip(node.arguments, fn.args)]
        result = self.builder.call(fn, args, "pcall")
        return ir.Constant(self.double, 0.0) if isinstance(fn.function_type.return_type, ir.VoidType) else result