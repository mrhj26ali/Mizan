# Backend/ir_generator.py
import llvmlite.ir as ir
import llvmlite.binding as llvm
from Mizan.Ast.nodes import *

# Initialize LLVM Target for the host machine
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

class IRGenerator:
    def __init__(self):
        self.module = ir.Module(name="mizan_program")
        self.module.triple = llvm.get_default_triple()
        
        self.builder = None
        self.function = None
        
        # Symbol table: maps Mizan ID -> (LLVM Pointer, LLVM Type)
        self.symbol_table = {}
        self._str_counter = 0
        
        self._declare_external_functions()

    def _unique_name(self, prefix):
        self._str_counter += 1
        return f"{prefix}_{self._str_counter}"

    def _declare_external_functions(self):
        """Declare C functions like printf for industrial logging."""
        printf_ty = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True)
        ir.Function(self.module, printf_ty, name="printf")

    def _get_llvm_type(self, ast_type_node):
        """Maps Mizan AST types to LLVM IR types."""
        if isinstance(ast_type_node, BaseTypeNode):
            if ast_type_node.type_name in ('حقيقي', 'عدد_حقيقي'):
                return ir.DoubleType() # 64-bit float
            elif ast_type_node.type_name in ('صحيح', 'عدد_صحيح'):
                return ir.IntType(32)  # 32-bit integer
            elif ast_type_node.type_name in ('منطقي',):
                return ir.IntType(1)   # 1-bit boolean
        # Default to double for physical units (e.g., سيلزيوس, بار)
        return ir.DoubleType()

    def _get_string_ptr(self, text):
        """Creates a global UTF-8 string constant and returns an i8* pointer for printf."""
        text_bytes = text.encode('utf-8') + b'\0' # Null-terminate for C
        str_type = ir.ArrayType(ir.IntType(8), len(text_bytes))
        name = self._unique_name("str")
        str_global = ir.GlobalVariable(self.module, str_type, name=name)
        str_global.global_constant = True
        str_global.initializer = ir.Constant(str_type, bytearray(text_bytes))
        # Cast array pointer to i8*
        return self.builder.bitcast(str_global, ir.PointerType(ir.IntType(8)))

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

    def generic_visit(self, node):
        # Silently ignore nodes we haven't implemented yet (like DeviceBlock, SensorDecl)
        return None

    # ─────────────────────────────────────────────────────────────────
    # 1. Program & Procedures Entry Points
    # ─────────────────────────────────────────────────────────────────
    def visit_ProgramNode(self, node: ProgramNode):
        main_ty = ir.FunctionType(ir.IntType(32), [])
        self.function = ir.Function(self.module, main_ty, name="main")
        block = self.function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        
        for decl in node.declarations:
            self.visit(decl)
            
        self.builder.ret(ir.Constant(ir.IntType(32), 0))

    def visit_ProcedureDefNode(self, node: ProcedureDefNode):
        ret_type = self._get_llvm_type(node.return_type) if node.return_type else ir.VoidType()
        func_ty = ir.FunctionType(ret_type, [])
        func = ir.Function(self.module, func_ty, name=node.identifier)
        block = func.append_basic_block(name="entry")
        
        old_builder, old_function = self.builder, self.function
        self.function, self.builder = func, ir.IRBuilder(block)
        
        for stmt in node.body:
            self.visit(stmt)
            
        if ret_type == ir.VoidType():
            self.builder.ret_void()
        else:
            self.builder.ret(ir.Constant(ret_type, 0))
            
        self.builder, self.function = old_builder, old_function

    def visit_ExecProcStmtNode(self, node: ExecProcStmtNode):
        func = self.module.get_global(node.identifier)
        if func:
            self.builder.call(func, [], name="call_tmp")

    def visit_ProcCallExprNode(self, node: ProcCallExprNode):
        func = self.module.get_global(node.identifier)
        if func:
            return self.builder.call(func, [], name="call_expr_tmp")
        return ir.Constant(ir.DoubleType(), 0.0)

    # ─────────────────────────────────────────────────────────────────
    # 2. Variables & Constants (Memory Allocation)
    # ─────────────────────────────────────────────────────────────────
    def visit_VarDeclNode(self, node: VarDeclNode):
        var_type = self._get_llvm_type(node.var_type)
        ptr = self.builder.alloca(var_type, name=node.identifier)
        init_val = self.visit(node.expr)
        if init_val:
            self.builder.store(init_val, ptr)
        self.symbol_table[node.identifier] = (ptr, var_type)

    def visit_ConstDeclNode(self, node: ConstDeclNode):
        var_type = self._get_llvm_type(node.var_type)
        ptr = self.builder.alloca(var_type, name=node.identifier)
        init_val = self.visit(node.expr)
        if init_val:
            self.builder.store(init_val, ptr)
        self.symbol_table[node.identifier] = (ptr, var_type)

    def visit_AssignStmtNode(self, node: AssignStmtNode):
        if node.identifier not in self.symbol_table: return
        ptr, var_type = self.symbol_table[node.identifier]
        val = self.visit(node.expr)
        if val:
            self.builder.store(val, ptr)

    # ─────────────────────────────────────────────────────────────────
    # 3. Industrial Statements (Simulation via printf)
    # ─────────────────────────────────────────────────────────────────
    def visit_LogStmtNode(self, node: LogStmtNode):
        fmt = self._get_string_ptr(f"[سجل] {node.message}\n")
        printf_func = self.module.get_global("printf")
        self.builder.call(printf_func, [fmt], name="printf_call")

    def visit_AlertStmtNode(self, node: AlertStmtNode):
        fmt = self._get_string_ptr(f"[تنبيه {node.level}] {node.message}\n")
        printf_func = self.module.get_global("printf")
        self.builder.call(printf_func, [fmt], name="printf_call")

    def visit_CommandStmtNode(self, node: CommandStmtNode):
        val_str = node.value if isinstance(node.value, str) else "قيمة_ديناميكية"
        fmt = self._get_string_ptr(f"[أمر] إرسال إلى '{node.identifier}' -> {val_str}\n")
        printf_func = self.module.get_global("printf")
        self.builder.call(printf_func, [fmt], name="printf_call")

    # ─────────────────────────────────────────────────────────────────
    # 4. Control Flow (Conditionals & Loops)
    # ─────────────────────────────────────────────────────────────────
    def _ensure_boolean(self, val):
        """Helper to ensure a value is an i1 (boolean) for branching."""
        if val is None: return ir.Constant(ir.IntType(1), 0)
        if isinstance(val.type, ir.IntType) and val.type.width == 1:
            return val
        if isinstance(val.type, ir.DoubleType):
            zero = ir.Constant(ir.DoubleType(), 0.0)
            # ✅ FIX: llvmlite uses fcmp_ordered for floats
            return self.builder.fcmp_ordered('!=', val, zero, "boolcast")
        zero = ir.Constant(val.type, 0)
        # ✅ FIX: llvmlite uses icmp_signed for integers
        return self.builder.icmp_signed('!=', val, zero, "boolcast")

    def visit_IfStmtNode(self, node: IfStmtNode):
        cond_val = self._ensure_boolean(self.visit(node.condition))
        
        then_bb = self.function.append_basic_block("then")
        merge_bb = self.function.append_basic_block("ifmerge")

        if node.else_branch:
            else_bb = self.function.append_basic_block("else")
            self.builder.cbranch(cond_val, then_bb, else_bb)
        else:
            self.builder.cbranch(cond_val, then_bb, merge_bb)
            else_bb = None

        self.builder.position_at_end(then_bb)
        for stmt in node.then_branch: self.visit(stmt)
        self.builder.branch(merge_bb)

        if else_bb:
            self.builder.position_at_end(else_bb)
            for stmt in node.else_branch: self.visit(stmt)
            self.builder.branch(merge_bb)

        self.builder.position_at_end(merge_bb)

    def visit_WhileStmtNode(self, node: WhileStmtNode):
        cond_bb = self.function.append_basic_block("while.cond")
        body_bb = self.function.append_basic_block("while.body")
        end_bb = self.function.append_basic_block("while.end")

        self.builder.branch(cond_bb)
        
        self.builder.position_at_end(cond_bb)
        cond_val = self._ensure_boolean(self.visit(node.condition))
        self.builder.cbranch(cond_val, body_bb, end_bb)

        self.builder.position_at_end(body_bb)
        for stmt in node.body: self.visit(stmt)
        self.builder.branch(cond_bb)

        self.builder.position_at_end(end_bb)

    def visit_ReturnStmtNode(self, node: ReturnStmtNode):
        if node.expr:
            val = self.visit(node.expr)
            self.builder.ret(val)
        else:
            self.builder.ret_void()

    # ─────────────────────────────────────────────────────────────────
    # 5. Expressions (Math, Literals, Comparisons)
    # ─────────────────────────────────────────────────────────────────
    def visit_NumberLiteralNode(self, node: NumberLiteralNode):
        if isinstance(node.value, float):
            return ir.Constant(ir.DoubleType(), float(node.value))
        return ir.Constant(ir.IntType(32), int(node.value))

    def visit_BooleanLiteralNode(self, node: BooleanLiteralNode):
        return ir.Constant(ir.IntType(1), 1 if node.value else 0)

    def visit_StringLiteralNode(self, node: StringLiteralNode):
        return self._get_string_ptr(node.value)

    def visit_VariableExprNode(self, node: VariableExprNode):
        if node.identifier not in self.symbol_table: 
            return ir.Constant(ir.DoubleType(), 0.0)
        
        ptr, var_type = self.symbol_table[node.identifier]
        
        # ✅ FIX: llvmlite 0.47.0 uses opaque pointers. We only pass the pointer!
        return self.builder.load(ptr, name=node.identifier) 

    def visit_BinaryOpNode(self, node: BinaryOpNode):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        if not left_val or not right_val: return left_val or right_val
        
        is_float = isinstance(left_val.type, ir.DoubleType) or isinstance(right_val.type, ir.DoubleType)
        
        # Professional Type Promotion: Int -> Float if mixed
        if is_float:
            if not isinstance(left_val.type, ir.DoubleType): left_val = self.builder.sitofp(left_val, ir.DoubleType())
            if not isinstance(right_val.type, ir.DoubleType): right_val = self.builder.sitofp(right_val, ir.DoubleType())

        if node.op == '+': return self.builder.fadd(left_val, right_val, "addtmp") if is_float else self.builder.add(left_val, right_val, "addtmp")
        elif node.op == '-': return self.builder.fsub(left_val, right_val, "subtmp") if is_float else self.builder.sub(left_val, right_val, "subtmp")
        elif node.op == '*': return self.builder.fmul(left_val, right_val, "multmp") if is_float else self.builder.mul(left_val, right_val, "multmp")
        elif node.op == '/': return self.builder.fdiv(left_val, right_val, "divtmp") if is_float else self.builder.sdiv(left_val, right_val, "divtmp")
        return left_val

    def visit_UnaryMinusNode(self, node: UnaryMinusNode):
        val = self.visit(node.operand)
        if isinstance(val.type, ir.DoubleType):
            return self.builder.fsub(ir.Constant(ir.DoubleType(), 0.0), val, "negtmp")
        return self.builder.sub(ir.Constant(val.type, 0), val, "negtmp")

    def visit_CompExprNode(self, node: CompExprNode):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        if not left_val or not right_val: return ir.Constant(ir.IntType(1), 0)
        
        is_float = isinstance(left_val.type, ir.DoubleType) or isinstance(right_val.type, ir.DoubleType)
        if is_float:
            if not isinstance(left_val.type, ir.DoubleType): left_val = self.builder.sitofp(left_val, ir.DoubleType())
            if not isinstance(right_val.type, ir.DoubleType): right_val = self.builder.sitofp(right_val, ir.DoubleType())
            
            # ✅ FIX: llvmlite uses fcmp_ordered and accepts standard operators ('>', '<', '==') directly!
            return self.builder.fcmp_ordered(node.op, left_val, right_val, "cmptmp")
        else:
            # ✅ FIX: llvmlite uses icmp_signed and accepts standard operators directly!
            return self.builder.icmp_signed(node.op, left_val, right_val, "cmptmp")

    def visit_BinaryCondNode(self, node: BinaryCondNode):
        left_val = self._ensure_boolean(self.visit(node.left))
        right_val = self._ensure_boolean(self.visit(node.right))
        if node.op == 'AND': return self.builder.and_(left_val, right_val, "andtmp")
        elif node.op == 'OR': return self.builder.or_(left_val, right_val, "ortmp")
        return left_val

    def visit_NotCondNode(self, node: NotCondNode):
        val = self._ensure_boolean(self.visit(node.operand))
        return self.builder.not_(val, "nottmp")