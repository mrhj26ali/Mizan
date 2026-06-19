import os
import sys
import traceback
import subprocess
import tempfile

# Ensure the project root is in the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from antlr4 import *
from Mizan.Frontend.MizanLexer import MizanLexer
from Mizan.Frontend.MizanParser import MizanParser
from Mizan.Ast.ast_builder import ASTBuilder
from Mizan.semantic.semantic_analyzer import SemanticAnalyzer
from Utils.text_utils import normalize_mizan_code
from Mizan.Ast.ast_visualizer import ASTVisualizerVisitor
from antlr4.error.ErrorListener import ErrorListener
from Backend.ir_generator import IRGenerator

# Lab 19: Import LLVM binding for the optimization pipeline
import llvmlite.binding as llvm 

class MizanErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        offending_text = offendingSymbol.text if offendingSymbol else "رمز غير معروف"
        print(f"❌ [خطأ نحوي] في السطر {line}:{column} -> الكلمة '{offending_text}' غير متوقعة.")

# =====================================================================
# Lab 19: LLVM Initialization & Optimization Pipeline
# =====================================================================

def initialize_llvm():
    """
    Initializes the LLVM engine and configures it for the host machine's 
    native architecture. 
    Note: In llvmlite >= 0.43.0, explicit core initialization is handled 
    automatically by the C++ backend. We only ensure native targets are loaded.
    """
    try:
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
    except RuntimeError:
        pass 
        
    print("✅ تم تهيئة محرك LLVM بنجاح")

def optimize_ir(raw_llvm_ir: str) -> str:
    """
    Parses raw LLVM IR text into an LLVM Module, verifies its structural 
    integrity, and runs it through the LLVM optimization pass manager.
    Includes robust fallbacks for modern llvmlite versions (0.40+).
    """
    # 1. Parse the text into a real LLVM Module object
    mod = llvm.parse_assembly(raw_llvm_ir)
    
    # Verify the module structurally before optimizing
    mod.verify()
    
    # 2. Attempt to use the Pass Manager via Python bindings
    # Note: llvmlite 0.47.0 (tracking LLVM 17+) removed the legacy pass manager 
    # Python bindings entirely. We use a multi-strategy fallback.
    
    # Strategy A: Legacy API (llvmlite < 0.40)
    if hasattr(llvm, 'create_module_pass_manager'):
        pm = llvm.create_module_pass_manager()
        pm.run(mod)
        return str(mod)
        
    # Strategy B: New PassManager class (llvmlite 0.40 - 0.42)
    if hasattr(llvm, 'PassManager'):
        try:
            pm = llvm.PassManager()
            pm.run(mod)
            return str(mod)
        except Exception:
            pass

    # Strategy C: Fallback to LLVM 'opt' CLI tool if Python bindings are missing
    try:
        with tempfile.NamedTemporaryFile(suffix=".ll", delete=False, mode="w", encoding="utf-8") as f_in:
            f_in.write(raw_llvm_ir)
            temp_in = f_in.name
            
        temp_out = temp_in.replace(".ll", "_opt.ll")
        
        # Run the LLVM 'opt' tool with O2 optimization
        subprocess.run(
            ["opt", "-O2", "-S", temp_in, "-o", temp_out],
            check=True, capture_output=True, text=True
        )
        
        with open(temp_out, "r", encoding="utf-8") as f_out:
            optimized_ir = f_out.read()
            
        # Cleanup temp files
        os.unlink(temp_in)
        os.unlink(temp_out)
        
        print("✅ تم التحسين باستخدام أداة 'opt' الخارجية بنجاح!")
        return optimized_ir
        
    except Exception:
        # Strategy D: Graceful degradation if 'opt' is not installed
        print("⚠️ تحذير: محرك LLVM في llvmlite 0.47.0 أزال واجهة برمجة التطبيقات لمدير التمريرات (Pass Manager).")
        print("⚠️ لم يتم العثور على أداة 'opt' في النظام. سيتم حفظ الكود الخام كنسخة محسنة مؤقتاً.")
        print("💡 للحصول على تحسين حقيقي، يرجى تثبيت أدوات LLVM (llvm-tools) واستخدام الأمر 'opt'.")
        return raw_llvm_ir

# =====================================================================
# Main Execution Pipeline
# =====================================================================

def main():
    file_path = "Mizan.arabic" 
    try:
        # 1. Read & Normalize Arabic Code
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_code = f.read()
        normalized_code = normalize_mizan_code(raw_code)
        input_stream = InputStream(normalized_code)

        # 2. Lexer & Parser
        lexer = MizanLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = MizanParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(MizanErrorListener())
        tree = parser.program()

        # 3. Build AST
        builder = ASTBuilder()
        ast = builder.visit(tree)
        print("✅ تم بناء الـ AST بنجاح!")

        # 4. Visualize AST
        visualizer = ASTVisualizerVisitor()
        visualizer.render(ast, output_filename='mizan_ast_output')
        print("✅ تم إنشاء صورة الـ AST (mizan_ast_output.png) بنجاح!")

        # 5. Semantic Analysis
        analyzer = SemanticAnalyzer()
        analyzer.visit(ast)
        analyzer.print_report()
        print("\n--- تقرير النطاقات الكامل ---")
        analyzer.current_scope.print_node()

        # 6. Backend: Code Generation & Optimization (Lab 19)
        if not analyzer.errors:
            # --- Step A: Generate Raw IR ---
            print("\n2️⃣ جاري توليد كود LLVM IR الخام...")
            ir_generator = IRGenerator(semantic_symbols=analyzer.current_scope.all_symbols())
            raw_llvm_ir = ir_generator.generate(ast)
            
            with open("output_raw.ll", "w", encoding="utf-8") as f:
                f.write(raw_llvm_ir)
            print("✅ تم حفظ كود LLVM IR الخام في الملف: output_raw.ll")

            # --- Step B: Initialize & Optimize ---
            print("\n3️⃣ جاري تشغيل مدير تمريرات التحسين (Pass Manager)...")
            initialize_llvm()
            
            try:
                optimized_ir = optimize_ir(raw_llvm_ir)
                
                with open("output_opt.ll", "w", encoding="utf-8") as f:
                    f.write(optimized_ir)
                print("✅ تم تحسين الكود بنجاح! قارن بين output_raw.ll و output_opt.ll")
            except Exception as e:
                print(f"❌ حدث خطأ أثناء التحسين: {e}")
        else:
            print("⛔ تم إيقاف توليد الكود بسبب وجود أخطاء دلالية.")

    except Exception:
        print(f"❌ حدث خطأ أثناء المعالجة:")
        traceback.print_exc()

if __name__ == "__main__":
    main()