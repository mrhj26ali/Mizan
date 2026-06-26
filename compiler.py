# compiler.py - Mizan Compiler Driver
import os
import sys
import argparse
import traceback
import platform

# ══════════════════════════════════════════════════════════
# 🔧 WINDOWS MSYS2 PATH INJECTION
# ══════════════════════════════════════════════════════════
# This allows the compiler to find gcc/clang and the C runtime libraries 
# (libmodbus, libmosquitto) without needing to open the MSYS2 terminal.
if platform.system() == "Windows":
    msys2_bin = r"C:\msys64\mingw64\bin"
    if os.path.exists(msys2_bin):
        os.environ["PATH"] = msys2_bin + os.pathsep + os.environ.get("PATH", "")

# Add root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ══════════════════════════════════════════════════════════
# 🟢 PHASE 1: FRONTEND IMPORTS
# ══════════════════════════════════════════════════════════
from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener
from Frontend.MizanLexer import MizanLexer
from Frontend.MizanParser import MizanParser
from Frontend.Ast.ast_builder import ASTBuilder
from Frontend.Ast.ast_visualizer import ASTVisualizerVisitor
from Frontend.semantic.semantic_analyzer import SemanticAnalyzer
from Utils.text_utils import normalize_mizan_code

# ══════════════════════════════════════════════════════════
# 🟡 PHASE 2: MIDDLE-END IMPORTS
# ══════════════════════════════════════════════════════════
from Middleend.ir_generator import IRGenerator
from Middleend.optimizer import optimize_ir

# ══════════════════════════════════════════════════════════
# 🔴 PHASE 3: BACKEND IMPORTS
# ══════════════════════════════════════════════════════════
from Backend.codegen import get_target_machine, emit_asm, emit_obj
from Backend.linker import link_and_run

import llvmlite.binding as llvm

class ArabicErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.had_error = False
        
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.had_error = True
        tok = offendingSymbol.text if offendingSymbol else "رمز مجهول"
        print(f"❌ [خطأ نحوي] السطر {line}:{column} — الرمز '{tok}' غير متوقع.")

def initialize_llvm():
    try: llvm.initialize()
    except RuntimeError: pass
    try: llvm.initialize_native_target(); llvm.initialize_native_asmprinter()
    except RuntimeError: pass
    print("✅ تم تهيئة محرك LLVM")

def compile_file(source_path: str, run_after=False, visualize=False, mqtt_port=1884):
    runtime_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runtime")
    print(f"\n{'='*60}\n🔨 تجميع: {source_path}\n{'='*60}")
    
    with open(source_path, "r", encoding="utf-8") as f:
        src = normalize_mizan_code(f.read())

    # ══════════════════════════════════════════════════════════
    # 🟢 PHASE 1: FRONTEND (Lexing, Parsing, AST, Semantic)
    # ══════════════════════════════════════════════════════════
    print("\n🟢 [المرحلة الأولى: الواجهة الأمامية] التحليل اللفظي والنحوي والدلالي...")
    err = ArabicErrorListener()
    lex = MizanLexer(InputStream(src))
    lex.removeErrorListeners(); lex.addErrorListener(err)
    tokens = CommonTokenStream(lex)
    parser = MizanParser(tokens)
    parser.removeErrorListeners(); parser.addErrorListener(err)
    tree = parser.program()
    
    if err.had_error:
        print("🛑 أخطاء نحوية — التوقف."); return

    ast = ASTBuilder().visit(tree)
    
    if visualize:
        ASTVisualizerVisitor().render(ast, "mizan_ast")

    analyzer = SemanticAnalyzer()
    analyzer.visit(ast)
    analyzer.print_report()
    if analyzer.errors:
        print("🛑 أخطاء دلالية — التوقف."); return

    # ══════════════════════════════════════════════════════════
    # 🟡 PHASE 2: MIDDLE-END (IR Generation & Optimization)
    # ══════════════════════════════════════════════════════════
    print("\n🟡 [المرحلة الثانية: الواجهة الوسطية] توليد LLVM IR والتحسين...")
    initialize_llvm()
    tm, target_triple = get_target_machine()
    
    irgen = IRGenerator(semantic_symbols=analyzer.current_scope.all_symbols(), mqtt_port=mqtt_port)
    raw_ir = irgen.generate(ast)
    with open("output_raw.ll", "w", encoding="utf-8") as f: 
        f.write(raw_ir)
    print("   محفوظ: output_raw.ll")
    
    opt_ir = optimize_ir(raw_ir, tm)
    with open("output_opt.ll", "w", encoding="utf-8") as f: 
        f.write(opt_ir)

    # ══════════════════════════════════════════════════════════
    # 🔴 PHASE 3: BACKEND (Target Machine, Assembly, Linking)
    # ══════════════════════════════════════════════════════════
    print("\n🔴 [المرحلة الثالثة: الواجهة الخلفية] توليد الكود الثنائي والربط...")
    
    emit_asm(opt_ir, tm)
    obj = emit_obj(opt_ir, tm)
    
    link_and_run(obj, runtime_dir, run_after)

def main():
    ap = argparse.ArgumentParser(description="مُجمِّع لغة ميزان")
    ap.add_argument("source", nargs="?", default="examples/05_full_control.mizan")
    ap.add_argument("--run", action="store_true", help="تشغيل البرنامج بعد البناء")
    ap.add_argument("--ast", action="store_true", help="توليد رسم AST")
    ap.add_argument("--all", action="store_true", help="تجميع وتشغيل جميع الأمثلة")
    ap.add_argument("--mqtt-port", type=int, default=1884, help="منفذ وسيط MQTT")
    args = ap.parse_args()
    
    if args.all:
        programs = [f"examples/0{i}_{name}.mizan" for i, name in 
                    enumerate(['hello', 'conditionals', 'loops', 'procedures', 'full_control'], 1)]
        for prog in programs:
            if os.path.isfile(prog):
                try: compile_file(prog, run_after=args.run, visualize=args.ast, mqtt_port=args.mqtt_port)
                except Exception: print(f"❌ فشل: {prog}"); traceback.print_exc()
    else:
        try: compile_file(args.source, run_after=args.run, visualize=args.ast, mqtt_port=args.mqtt_port)
        except Exception: traceback.print_exc()

if __name__ == "__main__":
    main()