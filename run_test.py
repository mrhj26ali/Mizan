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

# Lab 19/22: Import LLVM binding for optimization and target machine setup
import llvmlite.binding as llvm 

class MizanErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        offending_text = offendingSymbol.text if offendingSymbol else "رمز غير معروف"
        print(f"❌ [خطأ نحوي] في السطر {line}:{column} -> الكلمة '{offending_text}' غير متوقعة.")

# =====================================================================
# Lab 19 & 22: LLVM Initialization, Optimization & Target Machine
# =====================================================================

def initialize_llvm():
    """Initializes the LLVM engine and native target architecture."""
    try:
        llvm.initialize()
    except RuntimeError:
        pass
        
    try:
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
    except RuntimeError:
        pass 
        
    print("✅ تم تهيئة محرك LLVM بنجاح")

def initialize_target_machine():
    """
    Lab 22: Extracts the Target Triple and creates the Target Machine.
    """
    target_triple = llvm.get_default_triple()
    print(f"🎯 المعمارية المستهدفة: {target_triple}")
    
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    
    return target_machine, target_triple

def optimize_ir(raw_llvm_ir: str) -> str:
    """
    Parses raw LLVM IR text, verifies it, and runs it through the O2 optimization 
    pipeline. Uses external 'clang' as a robust fallback for modern llvmlite.
    """
    mod = llvm.parse_assembly(raw_llvm_ir)
    mod.verify()
    
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

    # Strategy C: Fallback to LLVM 'clang' CLI tool
    try:
        with tempfile.NamedTemporaryFile(suffix=".ll", delete=False, mode="w", encoding="utf-8") as f_in:
            f_in.write(raw_llvm_ir)
            temp_in = f_in.name
            
        temp_out = temp_in.replace(".ll", "_opt.ll")
        
        subprocess.run(
            ["clang", "-O2", "-S", "-emit-llvm", temp_in, "-o", temp_out],
            check=True, capture_output=True, text=True
        )
        
        with open(temp_out, "r", encoding="utf-8") as f_out:
            optimized_ir = f_out.read()
            
        os.unlink(temp_in)
        os.unlink(temp_out)
        
        print("✅ تم التحسين باستخدام أداة 'clang' الخارجية بنجاح!")
        return optimized_ir
        
    except FileNotFoundError:
        print("⚠️ تحذير: لم يتم العثور على أداة 'clang' في مسار النظام (PATH).")
        return raw_llvm_ir
        
    except subprocess.CalledProcessError as e:
        print("⚠️ تم العثور على 'clang' لكنه رفض الكود الخام!")
        print(f"❌ خطأ المحسن (clang stderr): {e.stderr}")
        return raw_llvm_ir
        
    except Exception as e:
        print(f"⚠️ خطأ غير متوقع أثناء التحسين: {e}")
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

        # 6. Backend: Code Generation, Optimization, Assembly & Object File
        if not analyzer.errors:
            # --- Step A: Generate Raw IR ---
            print("\n2️⃣ جاري توليد كود LLVM IR الخام...")
            ir_generator = IRGenerator(semantic_symbols=analyzer.current_scope.all_symbols())
            raw_llvm_ir = ir_generator.generate(ast)
            
            with open("output_raw.ll", "w", encoding="utf-8") as f:
                f.write(raw_llvm_ir)
            print("✅ تم حفظ كود LLVM IR الخام في الملف: output_raw.ll")

            # --- Step B: Initialize LLVM & Optimize ---
            print("\n3️⃣ جاري تشغيل مدير تمريرات التحسين (Pass Manager)...")
            initialize_llvm()
            optimized_ir = optimize_ir(raw_llvm_ir)
            
            with open("output_opt.ll", "w", encoding="utf-8") as f:
                f.write(optimized_ir)
            print("✅ تم حفظ الكود المحسن في الملف: output_opt.ll")

            # --- Step C: Lab 22 - Target Machine & Assembly Emission ---
            print("\n4️⃣ جاري تهيئة آلة الهدف (Target Machine) وتوليد كود التجميع...")
            target_machine, target_triple = initialize_target_machine()
            
            # Parse the optimized IR back into a binding Module
            final_mod = llvm.parse_assembly(optimized_ir)
            final_mod.verify()
            
            # Bind the module to the specific hardware architecture
            final_mod.triple = target_triple
            final_mod.data_layout = str(target_machine.target_data)
            
            # Emit the actual Assembly code for the CPU (Human-readable)
            asm_code = target_machine.emit_assembly(final_mod)
            with open("output.s", "w", encoding="utf-8") as f:
                f.write(asm_code)
            print("✅ تم توليد كود التجميع (output.s) بنجاح!")

            # --- Step D: Lab 23 - Raw Object File Emission ---
            print("5️⃣ جاري توليد ملف كود الآلة الثنائي (Object File)...")
            
            # emit_object executes Instruction Selection & Register Allocation 
            # and returns raw machine code bytes.
            obj_data = target_machine.emit_object(final_mod)
            
            # CRITICAL: Must be saved in binary mode ("wb")
            with open("output.o", "wb") as f:
                f.write(obj_data)
                
            print(f"✅ تم توليد ملف الهدف (output.o) بنجاح! الحجم: {len(obj_data)} بايت.")

        else:
            print("⛔ تم إيقاف توليد الكود بسبب وجود أخطاء دلالية.")

    except Exception:
        print(f"❌ حدث خطأ أثناء المعالجة:")
        traceback.print_exc()

if __name__ == "__main__":
    main()