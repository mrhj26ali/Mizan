# Backend/codegen.py
import os
import llvmlite.binding as llvm

def get_target_machine():
    """Phase 3: Backend Target Machine Setup"""
    triple = llvm.get_default_triple()
    print(f"🎯 المعمارية: {triple}")
    target = llvm.Target.from_default_triple()
    tm = target.create_target_machine(reloc='static')
    return tm, triple

def emit_asm(optimized_ir: str, tm, out_path="output.s") -> str:
    """Phase 3: Backend Assembly Emission"""
    mod = llvm.parse_assembly(optimized_ir)
    mod.verify()
    asm = tm.emit_assembly(mod)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(asm)
    print(f"   كود التجميع: {out_path}")
    return out_path

def emit_obj(optimized_ir: str, tm, out_path="output.o") -> str:
    """Phase 3: Backend Object File Emission"""
    mod = llvm.parse_assembly(optimized_ir)
    mod.verify()
    with open(out_path, "wb") as f: 
        f.write(tm.emit_object(mod))
    print(f"✅ ملف الكائن: {out_path} ({os.path.getsize(out_path)} بايت)")
    return out_path