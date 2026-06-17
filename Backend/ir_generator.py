# Backend/ir_generator.py
import llvmlite.ir as ir
import llvmlite.binding as llvm
from Mizan.Ast.nodes import *

# ✅ FIX: llvm.initialize() is deprecated in llvmlite 0.47.0+
# The core initialization is now handled automatically.
# We only need to initialize the native target and asm printer for execution.
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

class IRGenerator:
    def __init__(self):
        # 1. Create a new LLVM Module
        self.module = ir.Module(name="mizan_program")
        self.module.triple = llvm.get_default_triple()
        
        # 2. Internal state for code generation
        self.builder = None
        self.function = None
        
        # 3. Symbol table for LLVM variables (maps Mizan ID to LLVM Pointer/Value)
        self.symbol_table = {}
        
        # 4. Pre-define C standard library functions we will use
        self._declare_external_functions()

    def _declare_external_functions(self):
        """Declare C functions like printf so we can print Arabic logs to the console."""
        # int printf(const char *format, ...)
        printf_ty = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True)
        ir.Function(self.module, printf_ty, name="printf")

    def generate(self, ast_root):
        """Entry point: Traverse the AST and generate LLVM IR."""
        print("🏭 بدء توليد كود LLVM IR...")
        self.visit(ast_root)
        print("✅ تم توليد كود LLVM IR بنجاح!")
        return str(self.module)

    def visit(self, node):
        """Visitor pattern dispatcher."""
        if node is None:
            return None
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        # We will implement specific nodes step-by-step
        return None

    # ─────────────────────────────────────────────────────────────────
    # 1. Program Entry Point
    # ─────────────────────────────────────────────────────────────────
    def visit_ProgramNode(self, node: ProgramNode):
        # Create the main() function: i32 main()
        main_ty = ir.FunctionType(ir.IntType(32), [])
        self.function = ir.Function(self.module, main_ty, name="main")
        
        # Create the entry basic block
        block = self.function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        
        # Visit all top-level declarations
        for decl in node.declarations:
            self.visit(decl)
            
        # Return 0 from main()
        self.builder.ret(ir.Constant(ir.IntType(32), 0))

    # ─────────────────────────────────────────────────────────────────
    # 2. Device & Hardware (We will simulate initialization logs)
    # ─────────────────────────────────────────────────────────────────
    def visit_DeviceBlockNode(self, node: DeviceBlockNode):
        # TODO: Generate printf("✅ تم تهيئة الجهاز: %s\n", node.identifier)
        pass

    def visit_SensorDeclNode(self, node: SensorDeclNode):
        # TODO: Allocate memory for the sensor register
        pass

    # ─────────────────────────────────────────────────────────────────
    # 3. Variables & Constants (Labs 14 & 15)
    # ─────────────────────────────────────────────────────────────────
    def visit_VarDeclNode(self, node: VarDeclNode):
        # TODO: builder.alloca() and builder.store()
        pass

    def visit_ConstDeclNode(self, node: ConstDeclNode):
        # TODO: Create LLVM Constants
        pass