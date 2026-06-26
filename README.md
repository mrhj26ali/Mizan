# ميزان (Mizan) — Arabic Domain-Specific Language for Industrial Automation

**Mizan** (ميزان, Arabic for "balance/scale") is a compiled, domain-specific programming language written entirely in Arabic, designed for industrial control systems and IoT automation. It compiles down to native machine code via LLVM IR and integrates natively with Modbus and MQTT protocols.

---

## Overview

Mizan allows engineers to write industrial control logic in Arabic — defining sensors, actuators devices, operating modes, control rules, alerts, and scheduled reports — and compiles it into a standalone executable. It is designed to operate in real-time industrial environments such as water treatment plants, manufacturing lines, and process automation systems.

The compiler pipeline follows three distinct phases:

```
Source (.mizan)
  │
  ├─ 🟢 Phase 1: Frontend
  │    ANTLR4 Lexer/Parser → Concrete Syntax Tree → AST Builder → Clean AST
  │    → Semantic Analyzer (Type checking, Unit compatibility, FSM enforcement)
  │
  ├─ 🟡 Phase 2: Middleend
  │    LLVM IR Generator → Raw IR → Optimization Passes (O2) → Optimized IR
  │
  └─ 🔴 Phase 3: Backend
       Target Machine Setup → Assembly Emission (.s) → Object File (.o)
       → Linking with C Runtime (libmodbus, libmosquitto) → Native Executable
```

---

## Features

- **Arabic-first syntax** — all keywords, identifiers, operators, and error messages are in Arabic
- **Physical unit type system** — variables carry physical units (bar, °C, RPM, LPM, etc.) and the compiler enforces dimensional compatibility at compile time
- **Finite-state machine (FSM) support** — define operating modes and an explicit transition table; the compiler rejects unauthorized mode jumps
- **Sensor health monitoring** — built-in edge-triggered rules for disconnect, stuck-value, and out-of-range detection (ISA-18.2 compliant)
- **Modbus TCP integration** — native read/write from Modbus registers compiled directly into the binary
- **MQTT integration** — publishes telemetry, alerts, and reports to an MQTT broker
- **Temporal conditions** — express logic like "if pressure has been high for more than 5 seconds" (`عند_استمرار`)
- **Voting conditions** — express n-of-m sensor agreement conditions (`تصويت`)
- **Escalation policies** — define multi-level alert escalation with timeouts and receivers
- **Scheduled reports** — generate JSON/CSV reports on a schedule (immediate, daily, weekly, monthly)
- **Predictive maintenance** — track actuator cycle counts, sensor health scores, and runtime statistics
- **Plant simulator** — interactive Modbus TCP simulator with Tkinter GUI for testing without physical hardware

---

## Project Structure

```
.
├── compiler.py                 # Main compiler entry point (orchestrates all 3 phases)
├── requirements.txt            # Python dependencies
│
├── Frontend/                   # 🟢 Phase 1: Lexing, Parsing, AST, Semantic Analysis
│   ├── Mizan.g4                # ANTLR4 grammar (lexer + parser rules)
│   ├── Ast/
│   │   ├── nodes.py            # All AST node definitions (dataclasses)
│   │   ├── ast_builder.py      # Builds clean AST from ANTLR parse tree
│   │   ├── ast_visitor.py      # Base visitor pattern interface
│   │   └── ast_visualizer.py   # Graphviz-based AST diagram generator
│   └── semantic/
│       ├── semantic_analyzer.py # Type checking, unit compatibility, FSM enforcement
│       ├── symbols.py          # Symbol table classes (Sensor, Actuator, Mode, etc.)
│       ├── types_system.py     # Physical unit type system (ISO 80000 atoms)
│       └── environment.py      # Scoped symbol table environment
│
├── Middleend/                  # 🟡 Phase 2: IR Generation & Optimization
│   ├── ir_generator.py         # LLVM IR code generation from AST
│   └── optimizer.py            # LLVM optimization passes (O2)
│
├── Backend/                    # 🔴 Phase 3: Code Generation & Linking
│   ├── codegen.py              # Target machine setup, Assembly (.s) & Object (.o) emission
│   └── linker.py               # Links object file with C runtime via GCC/Clang
│
├── runtime/                    # C Runtime Library (linked into final executable)
│   ├── runtime.c / runtime.h   # Core runtime (logging, timing, ring buffers, health tracking)
│   ├── mizan_modbus.c/h        # Modbus TCP client wrapper (libmodbus)
│   └── mizan_mqtt.c/h          # MQTT client wrapper (libmosquitto)
│
├── sim/                        # Simulation & Debugging Tools
│   ├── plant_simulator.py      # Interactive Modbus TCP plant simulator (Tkinter GUI + CLI)
│   └── mqtt_monitor.py         # MQTT topic monitor for debugging
│
├── Utils/
│   └── text_utils.py           # Arabic text normalization (diacritics, hamza, presentation forms)
│
├── examples/                   # Example Mizan programs
│   ├── 1.mizan                 # Basic control (sensors, actuators, modes, procedures)
│   ├── 2.mizan                 # Temporal logic & custom units
│   ├── 3.mizan                 # Sensor health monitoring rules
│   ├── 4.mizan                 # Escalation chains & scheduled reports
│   └── 5.mizan                 # Voting logic & full FSM transitions
│
├── reports/                    # Generated JSON reports (output directory)
│   └── cbm/                    # Condition-Based Maintenance reports
│
└── mizan-doc/                  # Documentation
    ├── mizan_documentation.docx # Full language reference (Arabic)
    ├── mizan_presentation.pptx  # Project presentation slides
    └── build_mizan_doc.js       # Script to regenerate documentation (uses docx library)
```

---

## Getting Started on Windows (Complete Setup Guide)

This section walks you through everything you need to go from a fresh clone to a running compiler. Follow the steps in order.

### Step 1 — Install system tools

You need four tools installed on your machine before touching Python. Install them in this order.

**1a. LLVM 18**

Download and run `LLVM-18.1.8-win64.exe`. During installation, when asked about PATH, select **"Add LLVM to the system PATH for all users"**. This is required by `llvmlite` for IR generation and optimization.

**1b. MSYS2**

Download and run `msys2-x86_64-*.exe`. Install it to the default path `C:\msys64` — the compiler looks for libraries there. After installation, open the **MSYS2 MINGW64** terminal (not MSYS2 MSYS, not MSYS2 UCRT64 — specifically **MINGW64**) and run:

```bash
pacman -Syu
```

Close and reopen the terminal if it asks you to, then run:

```bash
pacman -S mingw-w64-x86_64-gcc mingw-w64-x86_64-make
pacman -S mingw-w64-x86_64-libmodbus mingw-w64-x86_64-mosquitto
```

This installs GCC (for linking) and the two C libraries that the Mizan runtime links against (libmodbus for Modbus TCP, libmosquitto for MQTT).

**1c. Mosquitto broker**

Download and run `mosquitto-2.1.2-install-windows-x64.exe`. This installs the MQTT broker that compiled Mizan programs publish to. The default installation path is `C:\Program Files\mosquitto`.

**1d. Graphviz** *(optional — only needed for the `--ast` flag)*

Download and run the Graphviz installer. During installation, select **"Add Graphviz to the system PATH"**. Skip this if you do not plan to use AST visualization.

---

### Step 2 — Set up Python and the virtual environment

Open a regular **Windows PowerShell** or **Command Prompt** (not MSYS2) and navigate to the folder where you cloned the repo:

```powershell
cd C:\path\to\mizan
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

Your prompt should now start with `(venv)`. Install all Python dependencies:

```powershell
pip install -r requirements.txt
```

> **Keep this virtual environment active** whenever you run the simulation scripts (`plant_simulator.py`, `mqtt_monitor.py`) from PowerShell. You will re-activate it the same way each time you open a new terminal session.

---

### Step 3 — Generate the ANTLR4 parser

The grammar file `Frontend/Mizan.g4` must be compiled into Python source files before the compiler can run. You only need to do this once (or again if the grammar changes).

Download the ANTLR4 tool JAR: [antlr-4.13.2-complete.jar](https://www.antlr.org/download/antlr-4.13.2-complete.jar) and place it somewhere convenient, e.g. `C:\tools\antlr-4.13.2-complete.jar`.

Make sure you have Java installed (JDK 11 or later), then run this from the **root of the repo** in PowerShell:

```powershell
cd Frontend
java -jar C:\tools\antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor Mizan.g4
cd ..
```

This generates `Frontend/MizanLexer.py`, `Frontend/MizanParser.py`, `Frontend/MizanVisitor.py`, and `Frontend/MizanListener.py`. These files are listed in `.gitignore` so they will not appear in the repository — you must generate them yourself.

---

### Step 4 — Check and configure the Mosquitto port

Mizan uses MQTT port **1884** by default (not the standard 1883, to avoid conflicts with any existing broker). Before running anything, confirm that port 1884 is free on your machine.

Open PowerShell and run:

```powershell
netstat -ano | findstr :1884
```

If nothing is returned, the port is free and you can proceed. If something is already using it, you have two options:

**Option A — Use a different port when compiling:**

```powershell
python compiler.py examples/5.mizan --mqtt-port 1885
```

And start the broker on that port instead:

```powershell
mosquitto -p 1885 -v
```

**Option B — Change the default port in the source:**

Open `compiler.py` and find the argument definition:

```python
ap.add_argument("--mqtt-port", type=int, default=1884, ...)
```

Change `1884` to whatever port you want as your new default. Then start the broker on that same port.

Also update `sim/mqtt_monitor.py` — at the bottom of the file, find:

```python
client.connect("localhost", 1884, keepalive=60)
```

Change `1884` to match your chosen port.

---

### Step 5 — Run the compiler via MSYS2 MINGW64

The compilation step (which links C runtime files) **must be run from the MSYS2 MINGW64 terminal**, because it needs access to the MinGW GCC toolchain and the native libraries installed in Step 1b.

Open the **MSYS2 MINGW64** terminal and navigate to your repo. MSYS2 uses Unix-style paths — a Windows path like `C:\Users\you\projects\mizan` becomes `/c/Users/you/projects/mizan`:

```bash
cd /c/Users/you/projects/mizan
```

Now when you want to compile use the Python virtual environment you created in Step 2. From MSYS2 MINGW64 like this example :

```bash
$ ./venv/Scripts/python.exe compiler.py examples/3.mizan --run
```



You are now ready to compile `.mizan` files.

---

## Running a Full Test Session

Running Mizan requires **three terminals open at the same time**. Here is the recommended setup:

**Terminal 1 — Mosquitto broker (PowerShell)**

```powershell
mosquitto -p 1884 -v
```

Leave this running. It will print a log line every time a Mizan program connects or publishes a message.

**Terminal 2 — Plant simulator (PowerShell with venv active)**

```powershell
venv\Scripts\activate
python sim/plant_simulator.py
```

This starts a fake Modbus TCP server on `localhost:5020` that simulates a physical plant (temperature, level, pressure, pH, turbidity, flow). It also exposes an interactive CLI:

```
Commands:
  set temp <val>     - e.g., set temp 105
  set level <val>    - e.g., set level 1.0
  set pressure <val> - e.g., set pressure 9.5
  fault <sensor> stuck|oor_high|oor_low
  clear_faults       - Restore all sensors
  disconnect         - Simulate network drop
  reconnect          - Restore network
```

You can type these commands at any time to simulate sensor changes or network faults while the compiled program is running.

**Terminal 3 — MQTT monitor (PowerShell with venv active)**

```powershell
venv\Scripts\activate
python sim/mqtt_monitor.py
```

This subscribes to all MQTT topics (`mizan/#`) and prints every message the compiled program publishes — alerts, telemetry, logs, and reports.

**Terminal 4 — Compiler (MSYS2 MINGW64 with Python venv)**

```bash
cd /c/Users/you/projects/mizan
$ ./venv/Scripts/python.exe compiler.py examples/3.mizan --run

```

The `--run` flag compiles the program and immediately executes the resulting `mizan_app.exe`. You should see output in Terminals 1, 2, and 3 as the program connects to the simulator and broker.

---

## Usage in MINGW64 window

### Compile a `.mizan` file in 

```bash
python compiler.py examples/1.mizan
```

This produces:
- `output_raw.ll` — Unoptimized LLVM IR
- `output_opt.ll` — Optimized LLVM IR (O2)
- `output.s` — Assembly code for your target architecture
- `mizan_app.exe` — The final native executable

### Compile and run immediately

```bash
$ ./venv/Scripts/python.exe compiler.py examples/3.mizan --run
```

### Compile and visualize the AST

```bash
$ ./venv/Scripts/python.exe compiler.py examples/3.mizan  --ast
```

This generates `mizan_ast.pdf` showing the Abstract Syntax Tree with color-coded nodes.


### Specify a custom MQTT broker port

```bash
python compiler.py examples/5.mizan --mqtt-port 1883
```

### Full CLI reference

```
usage: compiler.py [-h] [--run] [--ast]  [--mqtt-port MQTT_PORT] [source]

positional arguments:
  source                Path to .mizan source file (default: examples/1.mizan)

options:
  --run                 Run the executable after a successful build
  --ast                 Generate and display an AST diagram (requires Graphviz)
  --mqtt-port           MQTT broker port (default: 1884)
```

---

## Language Quick Reference

A Mizan program is structured around five top-level constructs: device configuration, sensor/actuator declarations, operating modes, control rules, and optional reports/escalations.

```arabic
// sample_1_basics.mizan
برنامج التحكم_الاساسي؛

جهاز وحدة_التحكم {
    نوع: "PLC",
    بروتوكول: "modbus_tcp",
    عنوان_ip: "127.0.0.1",
    منفذ: 5020,
    دورة_مسح: 500 مللي_ثانية
};

حساس مستوى_الخزان {
    نوع: متر,
    نطاق: [0..4],
    عنوان: 0x0000,
};

مشغل صمام_الدخول {
    نوع: منطقي,
    عنوان: 0x0020,
};

متغير عداد_المعايرة: صحيح = 0؛
متغير حالة_النظام: صحيح = 0؛

اجراء فحص_النظام(الحد: حقيقي) يرجع منطقي {
    اذا (مستوى_الخزان < الحد) {
        ارجع صح؛
    }
    ارجع خطا؛
}

وضع اقلاع {
    عند_بدء {
        سجل "بدء نظام التحكم..."؛
        عداد_المعايرة = 0؛
        طالما (عداد_المعايرة < 3) {
            سجل "جاري الفحص..."؛
            عداد_المعايرة = عداد_المعايرة + 1؛
            انتظر 1 ثانية؛
        }
        سجل "اكتملت المعايرة."؛
        انتقل_الى تشغيل_عادي؛
    }
}

وضع تشغيل_عادي {
    قاعدة التحكم_التلقائي {
        متغير يحتاج_فتح: منطقي = فحص_النظام(1.5)؛
        اذا (يحتاج_فتح) {
            امر صمام_الدخول: تشغيل؛
            سجل "المستوى منخفض، جاري الفتح."؛
        } والا {
            امر صمام_الدخول: ايقاف؛
            سجل "المستوى طبيعي."؛
        }
    }
}

انتقالات {
    من اقلاع الى تشغيل_عادي؛
}
```

### Supported Physical Units

- **Pressure:** `بار`, `باسكال`
- **Temperature:** `سيلزيوس`
- **Flow:** `لتر_في_الدقيقة`, `لتر_في_الساعة`, `متر_مكعب_في_الساعة`
- **Speed:** `متر_في_الثانية`, `دورة_في_الدقيقة`
- **Electrical:** `فولت`, `امبير`, `أوم`, `واط`
- **Other:** `بالمئة`, `NTU`, `جزء_في_المليون`, `لوكس`, `سيمنز`, `متر`, `لتر`, `كيلوجرام`, `ثانية`, `دقيقة`, `ساعة`

Custom units can be defined using the `وحدات_مخصصة` block:

```arabic
وحدات_مخصصة {
    معدل_الجرعة: لتر / ثانية,
    حمل_الطاقة: واط * ساعة
};
```

---

## Viewing Generated Reports

After a run that includes report definitions (see `examples/4.mizan`), JSON reports are automatically saved to the `reports/cbm/` directory. You can inspect them directly:

```bash
# On Windows PowerShell
type reports\cbm\*.json

# On MSYS2 MINGW64
cat reports/cbm/*.json
```

Example output:
```json
{"دورات_المضخة":1,"حالة_المضخة":1,"سلامة_الحساس":1}
```

---

## Troubleshooting

**"MizanLexer not found" or import errors on first run**
You have not generated the ANTLR4 parser yet. See Step 3 above.

**"gcc not found" or linking fails**
Make sure you are running `compiler.py` from the **MSYS2 MINGW64** terminal, not PowerShell. The MinGW GCC installed via pacman is required for linking the C runtime.

**"libmodbus not found" or "libmosquitto not found"**
Run `pacman -S mingw-w64-x86_64-libmodbus mingw-w64-x86_64-mosquitto` in the MSYS2 MINGW64 terminal.

**"Cannot connect" in the compiled program**
Make sure the plant simulator (Terminal 2) and Mosquitto broker (Terminal 1) are both running before you launch the compiled executable.

**Port conflict on 1884**
Run `netstat -ano | findstr :1884` in PowerShell to check. See Step 4 for how to switch ports.

**Arabic text displays as boxes or question marks**
Ensure your terminal supports UTF-8. In Windows Terminal this is the default. In older cmd.exe, run `chcp 65001` before launching anything. The MSYS2 MINGW64 terminal handles Arabic correctly by default.

**"ImportError: llvmlite"**
Make sure LLVM 18 is installed and was added to the system PATH before installing `llvmlite` via pip.

---

## Documentation

For the complete language reference (in Arabic), see:
- **`mizan-doc/mizan_documentation.docx`** — Comprehensive guide covering syntax, semantics, all keywords, error messages, and extension points
- **`mizan-doc/mizan_presentation.pptx`** — Project overview slides

---

## License & Acknowledgments

Mizan is an academic/research project demonstrating the feasibility of Arabic-native compiled DSLs for industrial automation. The compiler leverages:
- **ANTLR4** for parsing
- **llvmlite / LLVM** for code generation and optimization
- **libmodbus** for Modbus TCP communication
- **libmosquitto** for MQTT messaging
