# Middleend/optimizer.py
import llvmlite.binding as llvm

def optimize_ir(raw_ir: str, tm) -> str:
    """Phase 2: Middle-end Optimization Pass Manager"""
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