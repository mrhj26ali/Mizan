# compiler.py
import os, sys, subprocess, tempfile, platform, argparse, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener
from Frontend.MizanLexer   import MizanLexer
from Frontend.MizanParser  import MizanParser
from Ast.ast_builder       import ASTBuilder
from Ast.ast_visualizer    import ASTVisualizerVisitor
from semantic.semantic_analyzer import SemanticAnalyzer
from Backend.ir_generator        import IRGenerator
from Utils.text_utils            import normalize_mizan_code
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

def get_target_machine():
    triple = llvm.get_default_triple()
    print(f"🎯 المعمارية: {triple}")
    target = llvm.Target.from_default_triple()
    tm = target.create_target_machine(reloc='static')
    return tm, triple

def optimize_ir(raw_ir: str, tm) -> str:
    mod = llvm.parse_assembly(raw_ir)
    mod.verify()
    try:
        if hasattr(llvm, 'create_pipeline_tuning_options') and hasattr(llvm, 'PassBuilder'):
            pto = llvm.create_pipeline_tuning_options(speed_level=2, size_level=0)
            pb  = llvm.PassBuilder(tm, pto)
            mpm = pb.getModulePassManager()
            mpm.run(mod, pb)
            print("✅ تم التحسين (New PassManager)")
            return str(mod)
    except Exception as e:
        print(f"⚠️ New PassManager فشل: {e}")
    return raw_ir

def emit_obj(optimized_ir: str, tm, out_path="output.o") -> str:
    mod = llvm.parse_assembly(optimized_ir)
    mod.verify()
    with open(out_path,"wb") as f: f.write(tm.emit_object(mod))
    print(f"✅ ملف الكائن: {out_path} ({os.path.getsize(out_path)} بايت)")
    return out_path

def link_and_run(obj: str, runtime_dir: str, run_after: bool, out_name=None) -> str:
    is_win = platform.system() == "Windows"
    exe    = out_name or ("mizan_app.exe" if is_win else "./mizan_app")
    rt_sources = [os.path.join(runtime_dir, f) 
                  for f in ["runtime.c","mizan_modbus.c","mizan_mqtt.c"]]
    missing = [p for p in rt_sources if not os.path.isfile(p)]
    if missing:
        print(f"⚠️ ملفات runtime مفقودة: {missing}")
    rt_sources = [s for s in rt_sources if os.path.isfile(s)]
    
    for compiler in ["clang","gcc"]:
        try:
            subprocess.run([compiler,"--version"], capture_output=True, check=True)
            cmd = [compiler, "-finput-charset=UTF-8", "-fexec-charset=UTF-8", obj] + rt_sources + ["-o", exe]
            cmd += ["-lmodbus", "-lmosquitto", "-lm"]
            if is_win:
                cmd += ["-lws2_32"]
            else:
                cmd += ["-lpthread"]
            print(f"🔧 الرابط: {compiler}")
            r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
            if r.returncode != 0:
                print(f"❌ فشل الربط:\n{r.stderr}")
                return ""
            print(f"✅ الملف التنفيذي: {exe}")
            break
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
            
    if run_after:
        print("\n" + "="*50 + "\n🚀 تشغيل البرنامج\n" + "="*50)
        env = os.environ.copy()
        if is_win:
            msys2_bin = r"C:\msys64\mingw64\bin"
            if os.path.exists(msys2_bin):
                env["PATH"] = msys2_bin + os.pathsep + env.get("PATH", "")
        result = subprocess.run([exe], env=env)
        if result.returncode != 0:
            print(f"\n⚠️ البرنامج توقف بكود خطأ: {result.returncode}")
    return exe

# ✅ FIX 3: Added mqtt_port parameter
def compile_file(source_path: str, run_after=False, visualize=False, mqtt_port=1884):
    runtime_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runtime")
    print(f"\n{'='*60}\n🔨 تجميع: {source_path}\n{'='*60}")
    
    with open(source_path, "r", encoding="utf-8") as f:
        src = normalize_mizan_code(f.read())
        
    print("1️⃣  التحليل اللفظي والنحوي...")
    err = ArabicErrorListener()
    lex = MizanLexer(InputStream(src))
    lex.removeErrorListeners(); lex.addErrorListener(err)
    tokens = CommonTokenStream(lex)
    parser = MizanParser(tokens)
    parser.removeErrorListeners(); parser.addErrorListener(err)
    tree = parser.program()
    if err.had_error:
        print("🛑 أخطاء نحوية — التوقف."); return
        
    print("2️⃣  بناء شجرة AST...")
    ast = ASTBuilder().visit(tree)
    
    print("3️⃣  التحليل الدلالي...")
    analyzer = SemanticAnalyzer()
    analyzer.visit(ast)
    analyzer.print_report()
    if analyzer.errors:
        print("🛑 أخطاء دلالية — التوقف."); return
        
    print("4️⃣  تهيئة LLVM وتحديد المعمارية...")
    initialize_llvm()
    tm, target_triple = get_target_machine()
    
    print("5️⃣  توليد LLVM IR...")
    # ✅ FIX 3: Pass mqtt_port to IRGenerator
    irgen  = IRGenerator(semantic_symbols=analyzer.current_scope.all_symbols(), mqtt_port=mqtt_port)
    raw_ir = irgen.generate(ast)
    with open("output_raw.ll","w",encoding="utf-8") as f: f.write(raw_ir)
    print("   محفوظ: output_raw.ll")
    
    print("6️⃣  التحسين...")
    opt_ir = optimize_ir(raw_ir, tm)
    with open("output_opt.ll","w",encoding="utf-8") as f: f.write(opt_ir)
    mod = llvm.parse_assembly(opt_ir); mod.verify()
    asm = tm.emit_assembly(mod)
    with open("output.s","w",encoding="utf-8") as f: f.write(asm)
    print("   كود التجميع: output.s")
    
    print("7️⃣  توليد ملف الكائن...")
    obj = emit_obj(opt_ir, tm)
    
    print("8️⃣  الربط...")
    link_and_run(obj, runtime_dir, run_after)

def main():
    ap = argparse.ArgumentParser(description="مُجمِّع لغة ميزان")
    ap.add_argument("source", nargs="?", default="examples/05_full_control.mizan")
    ap.add_argument("--run",  action="store_true", help="تشغيل البرنامج بعد البناء")
    ap.add_argument("--ast",  action="store_true", help="توليد رسم AST")
    ap.add_argument("--all",  action="store_true", help="تجميع وتشغيل جميع الأمثلة الخمسة")
    # ✅ FIX 3: Added MQTT port argument
    ap.add_argument("--mqtt-port", type=int, default=1884, help="منفذ وسيط MQTT (Default: 1884)")
    args = ap.parse_args()

    if args.all:
        programs = [f"examples/0{i}_{'hello' if i==1 else 'conditionals' if i==2 else 'loops' if i==3 else 'procedures' if i==4 else 'full_control'}.mizan" 
                    for i in range(1,6)]
        for prog in programs:
            if os.path.isfile(prog):
                try:
                    compile_file(prog, run_after=args.run, visualize=args.ast, mqtt_port=args.mqtt_port)
                except Exception:
                    print(f"❌ فشل: {prog}"); traceback.print_exc()
    else:
        try:
            compile_file(args.source, run_after=args.run, visualize=args.ast, mqtt_port=args.mqtt_port)
        except Exception:
            traceback.print_exc()

if __name__ == "__main__":
    main()