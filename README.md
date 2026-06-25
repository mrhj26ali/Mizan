# ميزان (Mizan) — Arabic Domain-Specific Language for Industrial Automation

**Mizan** (ميزان, Arabic for "balance/scale") is a compiled, domain-specific programming language written entirely in Arabic, designed for industrial control systems and IoT automation. It compiles down to native machine code via LLVM IR and integrates natively with Modbus and MQTT protocols.

---

## Overview

Mizan allows engineers to write industrial control logic in Arabic — defining sensors, actuators, devices, operating modes, control rules, alerts, and scheduled reports — and compiles it into a standalone executable. It is designed to operate in real-time industrial environments such as water treatment plants, manufacturing lines, and process automation systems.

The compiler pipeline is:

```
Source (.mizan) → ANTLR4 Parser → AST → Semantic Analyzer → LLVM IR → Optimized IR → Object File → Executable
```

---

## Features

- **Arabic-first syntax** — all keywords, identifiers, operators, and error messages are in Arabic
- **Physical unit type system** — variables carry physical units (bar, °C, RPM, LPM, etc.) and the compiler enforces dimensional compatibility at compile time
- **Finite-state machine (FSM) support** — define operating modes and an explicit transition table; the compiler rejects unauthorized mode jumps
- **Sensor health monitoring** — built-in rules for disconnect, stuck-value, and out-of-range detection
- **Modbus TCP integration** — native read/write from Modbus registers compiled directly into the binary
- **MQTT integration** — publishes telemetry and alerts to an MQTT broker
- **Temporal conditions** — express logic like "if pressure has been high for more than 5 seconds"
- **Voting conditions** — express n-of-m sensor agreement conditions
- **Escalation policies** — define multi-level alert escalation with timeouts and receivers
- **Scheduled reports** — generate JSON/CSV reports on a schedule (immediate, daily, weekly, monthly)
- **Predictive maintenance** — track actuator cycle counts, sensor health scores, and runtime statistics
- **Plant simulator** — interactive Modbus TCP simulator for testing without physical hardware

---

## Project Structure

```
.
├── compiler.py               # Main compiler entry point
├── requirements.txt          # Python dependencies
├── view_reports.py           # Utility to summarize generated JSON reports
│
├── Frontend/
│   └── Mizan.g4              # ANTLR4 grammar (lexer + parser)
│
├── Ast/
│   ├── ast_builder.py        # Builds clean AST from ANTLR parse tree
│   ├── ast_visitor.py        # Base visitor pattern
│   ├── ast_visualizer.py     # Graphviz-based AST diagram generator
│   └── nodes.py              # All AST node definitions
│
├── semantic/
│   ├── semantic_analyzer.py  # Type checking, unit compatibility, FSM enforcement
│   ├── symbols.py            # Symbol table (sensors, actuators, variables, modes, etc.)
│   ├── types_system.py       # Physical unit type system (ISO 80000)
│   └── environment.py        # Scoped symbol table environment
│
├── Backend/
│   └── ir_generator.py       # LLVM IR code generation
│
├── runtime/
│   ├── runtime.c             # Core runtime (logging, timing, ring buffers)
│   ├── mizan_modbus.c/h      # Modbus TCP client wrapper (libmodbus)
│   └── mizan_mqtt.c/h        # MQTT client wrapper (libmosquitto)
│
├── sim/
│   ├── plant_simulator.py    # Interactive Modbus TCP plant simulator
│   └── mqtt_monitor.py       # MQTT topic monitor for debugging
│
├── Utils/
│   └── text_utils.py         # Arabic text normalization (diacritics, hamza, presentation forms)
│
├── examples/
│   ├── 1.mizan               
│   ├── 2.mizan               
│   ├── 3.mizan              
│   ├── 4.mizan              
│   └── 5.mizan               
│
└── mizan-doc/
    ├── mizan_language_reference.docx
    └── mizan_presentation.pptx
```

---

## Prerequisites

### Python dependencies

```bash
pip install -r requirements.txt
```

| Package | Version |
|---|---|
| antlr4-python3-runtime | 4.13.2 |
| llvmlite | 0.47.0 |
| graphviz | 0.20.3 |
| paho-mqtt | 2.1.0 |
| pymodbus | 3.8.1 |

### System dependencies

- **ANTLR4** runtime (for generating the lexer/parser from `Mizan.g4`)
- **LLVM** (compatible with llvmlite 0.47, i.e. LLVM 14)
- **clang** or **gcc** (for linking the compiled object file with the C runtime)
- **libmodbus** — Modbus TCP client library
- **libmosquitto** — Eclipse Mosquitto MQTT client library
- **Mosquitto broker** — for MQTT functionality (can run locally: `mosquitto -v`)

On Ubuntu/Debian:
```bash
sudo apt install clang libmodbus-dev libmosquitto-dev mosquitto
```

On Windows (MSYS2/MinGW64):
```bash
pacman -S mingw-w64-x86_64-clang mingw-w64-x86_64-libmodbus mingw-w64-x86_64-mosquitto
```

### Generating the ANTLR4 lexer and parser

Before running the compiler for the first time, generate the Python parser from the grammar:

```bash
antlr4 -Dlanguage=Python3 -visitor Frontend/Mizan.g4 -o Frontend/
```

---

## Usage

### Compile a `.mizan` file

```bash
python compiler.py examples/1.mizan
```

### Compile and run immediately

```bash
python compiler.py examples/5.mizan --run
```

### Compile and visualize the AST

```bash
python compiler.py examples/2.mizan --ast
```

### Compile all five examples

```bash
python compiler.py --all
```

### Specify a custom MQTT broker port

```bash
python compiler.py examples/5.mizan --mqtt-port 1883
```

### Full CLI reference

```
usage: compiler.py [-h] [--run] [--ast] [--all] [--mqtt-port MQTT_PORT] [source]

positional arguments:
  source                Path to .mizan source file (default: examples/05_full_control.mizan)

options:
  --run                 Run the executable after a successful build
  --ast                 Generate and display an AST diagram (requires Graphviz)
  --all                 Compile and optionally run all five example programs
  --mqtt-port           MQTT broker port (default: 1884)
```

---

## Running the simulator

To test a compiled program without physical hardware, start the interactive plant simulator in one terminal and the compiled executable in another.

**Terminal 1 — start the plant simulator:**
```bash
python sim/plant_simulator.py
```

This starts a Modbus TCP server on `localhost:5020` and exposes an interactive CLI:
```
Commands: set level <val> | set temp <val> | disconnect | reconnect | auto
```

**Terminal 2 — start the MQTT broker:**
```bash
mosquitto -p 1884 -v
```

**Terminal 3 — monitor MQTT topics:**
```bash
python sim/mqtt_monitor.py
```

**Terminal 4 — run the compiled program:**
```bash
./mizan_app
```

---

## Language quick reference

A Mizan program is structured around five top-level constructs: device configuration, sensor/actuator declarations, operating modes, control rules, and optional reports.

```
// Define the target device
جهاز PLC_الرئيسي {
    نوع: "Modbus-TCP"
    عنوان_IP: "127.0.0.1"
    منفذ: 5020
    دورة_المسح: 500 مللي_ثانية
}

// Declare a sensor
حساس الضغط {
    نوع: حقيقي بالوحدة بار
    نطاق: 0..100
    عنوان: 0x0002
    صحة {
        عند_انقطاع_الاتصال: تنبيه خطر "انقطاع الاتصال"
        عند_قيمة_ثابتة مدة 10 ثانية: تنبيه تحذير "قيمة ثابتة"
        عند_خروج_عن_النطاق: تنبيه خطر "خروج عن النطاق"
    }
}

// Declare an actuator
مشغّل صمام_الضغط {
    نوع: حقيقي بالوحدة بالمئة
    نطاق: 0..100
    عنوان: 0x0024
}

// Define operating modes
الأوضاع: تشغيل، إيقاف

// Define allowed FSM transitions
انتقالات {
    إيقاف الى تشغيل
    تشغيل الى إيقاف
}

// Control logic
وضع تشغيل {
    قاعدة التحكم_بالضغط {
        اذا الضغط > 8.0 بار {
            أمر صمام_الضغط = 1.0
            تنبيه خطر "ضغط عالٍ"
        }
        والا {
            أمر صمام_الضغط = 0.0
        }
    }
}

// Scheduled report
تقرير تقرير_الضغط {
    جدول: كل 5000 مللي_ثانية
    تنسيق: json
    حفظ_في: "reports/cbm"
    محتوى {
        قيمة_لحظية الضغط بعنوان "متوسط_الضغط"
    }
}
```

### Data types

| Keyword | Description |
|---|---|
| `صحيح` | Integer |
| `حقيقي` | Float |
| `منطقي` | Boolean |
| `نص` | String |
| `حقيقي بالوحدة <unit>` | Float with physical unit |

### Control flow

| Keyword | Meaning |
|---|---|
| `اذا ... والا` | if / else |
| `طالما` | while loop |
| `انتقل_الى` | go-to mode (FSM transition) |
| `انتظر` | wait for a duration |

### Built-in units (sample)

Pressure: `بار`, `باسكال` · Temperature: `سيلزيوس` · Flow: `لتر_في_الدقيقة`, `لتر_في_الساعة`, `متر_مكعب_في_الساعة` · Speed: `متر_في_الثانية`, `دورة_في_الدقيقة` · Electrical: `فولت`, `امبير`, `أوم`, `واط` · Other: `بالمئة`, `NTU`, `جزء_في_المليون`, `لوكس`, `سيمنز`

---

## Viewing reports

After a run, use the report viewer to print all generated JSON reports to a summary file:

```bash
python view_reports.py
# Output written to reports_summary.txt
```

---

