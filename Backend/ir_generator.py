# Backend/ir_generator.py
import llvmlite.ir as ir
import llvmlite.binding as llvm
from Mizan.Ast.nodes import *
from Mizan.semantic.symbols import SensorSymbol, ActuatorSymbol

# Initialize LLVM Target
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

class IRGenerator:
    def __init__(self, semantic_symbols=None):
        self.module = ir.Module(name="mizan_program")
        self.module.triple = llvm.get_default_triple()
        
        self.builder = None
        self.function = None
        
        # Mizan Symbol Table from Semantic Analyzer (for hardware mapping)
        self.mizan_symbols = semantic_symbols or {}
        
        # LLVM Symbol Table: maps Mizan ID -> (LLVM Pointer, LLVM Type)
        self.symbol_table = {}
        
        self._str_counter = 0
        self._declare_external_functions()

    def _declare_external_functions(self):
        """Declare C Runtime functions for Hardware I/O and Logging."""
        i32 = ir.IntType(32)
        double = ir.DoubleType()
        i8_ptr = ir.PointerType(ir.IntType(8))
        void = ir.VoidType()

        # printf for logs
        printf_ty = ir.FunctionType(i32, [i8_ptr], var_arg=True)
        self.printf_func = ir.Function(self.module, printf_ty, name="printf")
        
        # Hardware I/O stubs (to be implemented in runtime.c)
        read_ty = ir.FunctionType(double, [i32])
        self.read_sensor_func = ir.Function(self.module, read_ty, name="read_sensor_register")
        
        write_ty = ir.FunctionType(void, [i32, double])
        self.write_actuator_func = ir.Function(self.module, write_ty, name="write_actuator_register")
        # Panic handler for division by zero
    
        panic_ty = ir.FunctionType(void, [])
        self.panic_func = ir.Function(self.module, panic_ty, name="panic_div_zero")

        # Console setup for UTF-8 Arabic output
        setup_ty = ir.FunctionType(void, [])
        self.setup_console_func = ir.Function(self.module, setup_ty, name="setup_arabic_console")

    def _get_llvm_type(self, ast_type_node):
        if isinstance(ast_type_node, BaseTypeNode):
            if ast_type_node.type_name in ('حقيقي', 'عدد_حقيقي'): return ir.DoubleType()
            elif ast_type_node.type_name in ('صحيح', 'عدد_صحيح'): return ir.IntType(32)
            elif ast_type_node.type_name in ('منطقي',): return ir.IntType(1)
        return ir.DoubleType() # Default physical units to double

    def _get_string_ptr(self, text):
        text_bytes = text.encode('utf-8') + b'\0'
        str_type = ir.ArrayType(ir.IntType(8), len(text_bytes))
        name = f"str_{self._str_counter}"
        self._str_counter += 1
        str_global = ir.GlobalVariable(self.module, str_type, name=name)
        str_global.global_constant = True
        str_global.initializer = ir.Constant(str_type, bytearray(text_bytes))
        return self.builder.bitcast(str_global, ir.PointerType(ir.IntType(8)))

    def _cast_if_needed(self, val, target_type):
        """Ensures LLVM strict type matching by casting Int to Float if needed."""
        if isinstance(target_type, ir.DoubleType) and isinstance(val.type, ir.IntType):
            return self.builder.sitofp(val, ir.DoubleType(), "cast_to_float")
        if isinstance(target_type, ir.IntType) and isinstance(val.type, ir.DoubleType):
            return self.builder.fptosi(val, target_type, "cast_to_int")
        return val
    
    def emit_runtime_trap(self, is_danger_i1, panic_function):
        """
        Creates a defensive control-flow graph:
        1. Checks the danger condition.
        2. Branches to a panic block (calls C runtime exit) or a safe math block.
        """
        current_func = self.builder.function
        
        # 1. Create two blocks: one for crashing, one for safe continuation
        panic_bb = current_func.append_basic_block("panic_block")
        continue_bb = current_func.append_basic_block("math_block")
        
        # 2. Conditional branch: if danger is true, go to panic, else go to math
        self.builder.cbranch(is_danger_i1, panic_bb, continue_bb)
        
        # 3. Program the Panic Block
        self.builder.position_at_end(panic_bb)
        self.builder.call(panic_function, [])
        self.builder.unreachable() # Crucial: tells LLVM optimizer this path ends here
        
        # 4. Move the "pen" to the safe zone to resume normal IR generation
        self.builder.position_at_end(continue_bb)

    def generate(self, ast_root):
        print("🏭 بدء توليد كود LLVM IR...")
        self.visit(ast_root)
        print("✅ تم توليد كود LLVM IR بنجاح!")
        return str(self.module)

    def visit(self, node):
        if node is None: return None
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node): return None

    # ─────────────────────────────────────────────────────────────────
    # 1. Program & Procedures (Global vs Local Scope Management)
    # ─────────────────────────────────────────────────────────────────
    def visit_ProgramNode(self, node: ProgramNode):
        # First pass: Create Global Variables & Procedure Signatures
        for decl in node.declarations:
            if isinstance(decl, (VarDeclNode, ConstDeclNode)):
                self._create_global_variable(decl)
            elif isinstance(decl, ProcedureDefNode):
                self._create_procedure_signature(decl)

        # Second pass: Generate main() and procedure bodies
        main_ty = ir.FunctionType(ir.IntType(32), [])
        self.function = ir.Function(self.module, main_ty, name="main")
        block = self.function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        # ✅ LAB 24: Inject console setup at the very beginning of main!
        # This ensures UTF-8 is active before any printf is called.
        self.builder.call(self.setup_console_func, [])
        
        for decl in node.declarations:
            if isinstance(decl, ProcedureDefNode):
                self._generate_procedure_body(decl)
            elif isinstance(decl, (VarDeclNode, ConstDeclNode)):
                # Initialize global variables inside main's entry block
                self._initialize_global_variable(decl)

        # ✅ LAB 24 FIX: Automatically call the first procedure found from main()
        # so the executable actually executes the user's logic.
        for decl in node.declarations:
            if isinstance(decl, ProcedureDefNode):
                func = self.module.get_global(decl.identifier)
                if func:
                    self.builder.call(func, [])
                break # Only call the first one for this test

        self.builder.ret(ir.Constant(ir.IntType(32), 0))

    def _create_global_variable(self, node):
        var_type = self._get_llvm_type(node.var_type)
        global_var = ir.GlobalVariable(self.module, var_type, name=node.identifier)
        global_var.initializer = ir.Constant(var_type, 0) # Default init to 0
        global_var.global_constant = isinstance(node, ConstDeclNode)
        self.symbol_table[node.identifier] = (global_var, var_type)

    def _initialize_global_variable(self, node):
        if node.expr:
            ptr, var_type = self.symbol_table[node.identifier]
            init_val = self.visit(node.expr)
            if init_val:
                init_val = self._cast_if_needed(init_val, var_type)
                self.builder.store(init_val, ptr)

    def _create_procedure_signature(self, node):
        ret_type = self._get_llvm_type(node.return_type) if node.return_type else ir.VoidType()
        param_types = [self._get_llvm_type(p.var_type) for p in node.params]
        func_ty = ir.FunctionType(ret_type, param_types)
        ir.Function(self.module, func_ty, name=node.identifier)

    def _generate_procedure_body(self, node):
        func = self.module.get_global(node.identifier)
        block = func.append_basic_block(name="entry")
        
        old_builder, old_function = self.builder, self.function
        self.function, self.builder = func, ir.IRBuilder(block)
        
        # Allocate stack memory for parameters
        for i, param in enumerate(node.params):
            param_type = self._get_llvm_type(param.var_type)
            ptr = self.builder.alloca(param_type, name=param.identifier)
            self.builder.store(func.args[i], ptr)
            self.symbol_table[param.identifier] = (ptr, param_type)
            
        for stmt in node.body:
            self.visit(stmt)
            
        if isinstance(func.function_type.return_type, ir.VoidType):
            self.builder.ret_void()
        else:
            self.builder.ret(ir.Constant(func.function_type.return_type, 0))
            
        self.builder, self.function = old_builder, old_function

    # ─────────────────────────────────────────────────────────────────
    # 2. Local Variables & Assignments
    # ─────────────────────────────────────────────────────────────────
    def visit_VarDeclNode(self, node: VarDeclNode):
        # If we are here, it's a LOCAL variable (inside a procedure)
        var_type = self._get_llvm_type(node.var_type)
        ptr = self.builder.alloca(var_type, name=node.identifier)
        if node.expr:
            init_val = self.visit(node.expr)
            if init_val:
                init_val = self._cast_if_needed(init_val, var_type)
                self.builder.store(init_val, ptr)
        self.symbol_table[node.identifier] = (ptr, var_type)

    def visit_ConstDeclNode(self, node: ConstDeclNode):
        self.visit_VarDeclNode(node) 

    def visit_AssignStmtNode(self, node: AssignStmtNode):
        if node.identifier not in self.symbol_table: return
        ptr, var_type = self.symbol_table[node.identifier]
        val = self.visit(node.expr)
        if val:
            val = self._cast_if_needed(val, var_type)
            self.builder.store(val, ptr)

    # ─────────────────────────────────────────────────────────────────
    # 3. Hardware I/O (Sensors & Actuators) & Logging
    # ─────────────────────────────────────────────────────────────────
    def visit_VariableExprNode(self, node: VariableExprNode):
        # Check if it's a Hardware Sensor
        sym = self.mizan_symbols.get(node.identifier)
        if sym and isinstance(sym, SensorSymbol):
            addr_str = sym.address or "0x0"
            addr_int = int(addr_str, 16) if addr_str.startswith('0x') else int(addr_str)
            addr_val = ir.Constant(ir.IntType(32), addr_int)
            return self.builder.call(self.read_sensor_func, [addr_val], name=f"read_{node.identifier}")

        # Fallback to normal variable
        if node.identifier not in self.symbol_table: return ir.Constant(ir.DoubleType(), 0.0)
        ptr, var_type = self.symbol_table[node.identifier]
        return self.builder.load(ptr, name=node.identifier)

    def visit_CommandStmtNode(self, node: CommandStmtNode):
        sym = self.mizan_symbols.get(node.identifier)
        if sym and isinstance(sym, ActuatorSymbol):
            addr_str = sym.address or "0x0"
            addr_int = int(addr_str, 16) if addr_str.startswith('0x') else int(addr_str)
            addr_val = ir.Constant(ir.IntType(32), addr_int)
            
            if isinstance(node.value, str):
                val_map = {'تشغيل': 1.0, 'ايقاف': 0.0, 'نشط': 1.0, 'غير_نشط': 0.0, 'مفتوح': 1.0, 'مغلق': 0.0}
                write_val = ir.Constant(ir.DoubleType(), val_map.get(node.value, 1.0))
            else:
                write_val = self.visit(node.value)
                write_val = self._cast_if_needed(write_val, ir.DoubleType())
                
            self.builder.call(self.write_actuator_func, [addr_val, write_val])
            return
            
        if isinstance(node.value, ASTNode): self.visit(node.value)

    def visit_LogStmtNode(self, node: LogStmtNode):
        msg_ptr = self._get_string_ptr(f"[سجل] {node.message}\n")
        self.builder.call(self.printf_func, [msg_ptr])

    def visit_AlertStmtNode(self, node: AlertStmtNode):
        msg_ptr = self._get_string_ptr(f"[تنبيه {node.level}] {node.message}\n")
        self.builder.call(self.printf_func, [msg_ptr])

    # ─────────────────────────────────────────────────────────────────
    # 4. Math & Logic
    # ─────────────────────────────────────────────────────────────────
    def visit_NumberLiteralNode(self, node: NumberLiteralNode):
        if isinstance(node.value, float): return ir.Constant(ir.DoubleType(), float(node.value))
        return ir.Constant(ir.IntType(32), int(node.value))

    def visit_BooleanLiteralNode(self, node: BooleanLiteralNode):
        return ir.Constant(ir.IntType(1), 1 if node.value else 0)

    def visit_BinaryOpNode(self, node: BinaryOpNode):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        if not left_val or not right_val: return left_val or right_val
        
        is_float = isinstance(left_val.type, ir.DoubleType) or isinstance(right_val.type, ir.DoubleType)
        
        if is_float:
            # --- Float Operations ---
            if not isinstance(left_val.type, ir.DoubleType): left_val = self.builder.sitofp(left_val, ir.DoubleType())
            if not isinstance(right_val.type, ir.DoubleType): right_val = self.builder.sitofp(right_val, ir.DoubleType())
            
            if node.op == '+': return self.builder.fadd(left_val, right_val, "addtmp")
            elif node.op == '-': return self.builder.fsub(left_val, right_val, "subtmp")
            elif node.op == '*': return self.builder.fmul(left_val, right_val, "multmp")
            elif node.op == '/': return self.builder.fdiv(left_val, right_val, "divtmp")
        else:
            # --- Integer Operations (✅ FIXED: Previously these were ignored!) ---
            if node.op == '+': return self.builder.add(left_val, right_val, "addtmp")
            elif node.op == '-': return self.builder.sub(left_val, right_val, "subtmp")
            elif node.op == '*': return self.builder.mul(left_val, right_val, "multmp")
            
            elif node.op == '/':
                # --- LAB 20: Runtime Trap for Integer Division ---
                zero_val = ir.Constant(left_val.type, 0)
                is_zero = self.builder.icmp_signed('==', right_val, zero_val, name="is_zero_trap")
                self.emit_runtime_trap(is_zero, self.panic_func)
                return self.builder.sdiv(left_val, right_val, name="divtmp")
                
            elif node.op == '%':
                # --- LAB 20: Runtime Trap for Integer Modulo (Bonus Safety) ---
                zero_val = ir.Constant(left_val.type, 0)
                is_zero = self.builder.icmp_signed('==', right_val, zero_val, name="is_zero_trap_mod")
                self.emit_runtime_trap(is_zero, self.panic_func)
                return self.builder.srem(left_val, right_val, name="modtmp")
                
        return left_val

    def visit_CompExprNode(self, node: CompExprNode):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        if not left_val or not right_val: return ir.Constant(ir.IntType(1), 0)
        
        is_float = isinstance(left_val.type, ir.DoubleType) or isinstance(right_val.type, ir.DoubleType)
        if is_float:
            if not isinstance(left_val.type, ir.DoubleType): left_val = self.builder.sitofp(left_val, ir.DoubleType())
            if not isinstance(right_val.type, ir.DoubleType): right_val = self.builder.sitofp(right_val, ir.DoubleType())
            return self.builder.fcmp_ordered(node.op, left_val, right_val, "cmptmp")
        else:
            return self.builder.icmp_signed(node.op, left_val, right_val, "cmptmp")