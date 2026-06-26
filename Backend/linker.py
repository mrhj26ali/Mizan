# Backend/linker.py
import os
import sys
import subprocess
import platform

def link_and_run(obj: str, runtime_dir: str, run_after: bool, out_name=None) -> str:
    """Phase 3: Backend Linking and Execution"""
    is_win = platform.system() == "Windows"
    exe    = out_name or ("mizan_app.exe" if is_win else "./mizan_app")
    
    rt_sources = [os.path.join(runtime_dir, f) 
                  for f in ["runtime.c", "mizan_modbus.c", "mizan_mqtt.c"]]
    
    missing = [p for p in rt_sources if not os.path.isfile(p)]
    if missing:
        print(f"⚠️ ملفات runtime مفقودة: {missing}")
        rt_sources = [s for s in rt_sources if os.path.isfile(s)]
        
    for compiler in ["clang", "gcc"]:
        try:
            subprocess.run([compiler, "--version"], capture_output=True, check=True)
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