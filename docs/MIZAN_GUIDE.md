# دليل لغة ميزان — The Mizan Language Guide

> **Mizan** is an Arabic-first, compiled Domain-Specific Language (DSL) for industrial
> automation and SCADA systems. It compiles to native ELF binaries via LLVM, targeting
> Modbus TCP and MQTT deployments. This guide covers the complete grammar with annotated
> examples so you can write correct Mizan programs without errors.

---

## Table of Contents

1. [Program Structure & Order of Declarations](#1-program-structure--order-of-declarations)
2. [Identifiers, Comments, and Punctuation](#2-identifiers-comments-and-punctuation)
3. [Program Declaration — `برنامج`](#3-program-declaration--برنامج)
4. [Device Block — `جهاز`](#4-device-block--جهاز)
5. [Custom Units — `وحدات_مخصصة`](#5-custom-units--وحدات_مخصصة)
6. [Custom Modes — `اوضاع_مخصصة`](#6-custom-modes--اوضاع_مخصصة)
7. [Sensor Declaration — `حساس`](#7-sensor-declaration--حساس)
8. [Actuator Declaration — `مشغل`](#8-actuator-declaration--مشغل)
9. [Variable & Constant Declarations](#9-variable--constant-declarations)
10. [Procedures — `اجراء`](#10-procedures--اجراء)
11. [Modes & Rules — `وضع` / `قاعدة`](#11-modes--rules--وضع--قاعدة)
12. [Statements Reference](#12-statements-reference)
13. [Expressions & Arithmetic](#13-expressions--arithmetic)
14. [Conditions & Boolean Logic](#14-conditions--boolean-logic)
15. [Type System & Units](#15-type-system--units)
16. [Sensor Health Rules — `صحة`](#16-sensor-health-rules--صحة)
17. [Escalation Chains — `تصعيد`](#17-escalation-chains--تصعيد)
18. [Reports — `تقرير`](#18-reports--تقرير)
19. [Transition Table — `انتقالات`](#19-transition-table--انتقالات)
20. [Semantic Rules & Common Mistakes](#20-semantic-rules--common-mistakes)
21. [Complete Example Programs](#21-complete-example-programs)

---

## 1. Program Structure & Order of Declarations

A Mizan source file is a flat sequence of **top-level declarations**. There are no
mandatory ordering rules enforced by the parser, but the following canonical order is
strongly recommended to avoid forward-reference semantic errors:

```
برنامج <اسم>؛                      ← Required, declare first
جهاز ...                            ← Device/hardware config
وحدات_مخصصة { ... }؛               ← Custom units (before their first use)
اوضاع_مخصصة { ... }؛               ← Custom mode names (before mode blocks)
حساس ... ؛                          ← Sensor hardware
مشغل ... ؛                          ← Actuator hardware
متغير / ثابت ...                   ← Global variables & constants
اجراء ...                           ← Procedure definitions
وضع <اسم> { ... }                  ← Operating mode blocks
تصعيد ...؛                         ← Escalation chains
تقرير ...؛                         ← Report definitions
انتقالات { ... }                    ← FSM transition table (last)
```

A minimal valid program requires at minimum:
- A `برنامج` declaration
- At least one `وضع` (mode) block

---

## 2. Identifiers, Comments, and Punctuation

### Identifiers (`ID`)

Identifiers can use Arabic letters, Latin letters, digits, and underscores. They **must
start** with a letter or underscore (not a digit).

```mizan
// Valid identifiers:
مستوى_الخزان
الحرارة_وهمي_1
sensorA
valve_3

// INVALID — starts with a digit:
// 1حساس   ← ❌ parser error
```

### Comments

```mizan
// This is a single-line comment — ignored by the compiler

/* This is a
   multi-line block comment */
```

### Punctuation

Mizan accepts **both Arabic and Latin** punctuation variants:

| Symbol | Arabic form | Latin form | Used for |
|--------|-------------|------------|----------|
| Semicolon | `؛` | `;` | Statement terminator |
| Comma | `،` | `,` | Field/argument separator |

Both forms are interchangeable. You may freely mix them in the same file.

### Numbers

Integer and float literals use ASCII digits `0–9` **or** Arabic-Indic digits `٠–٩`.
```mizan
5020      // ASCII integer
٥٠٢٠     // Arabic-Indic integer — identical meaning
3.14      // float
```

### String Literals

Strings use double quotes. No escape sequences beyond what the host OS supports.
```mizan
"بدء نظام التحكم..."
"127.0.0.1"
"modbus_tcp"
```

### Register Literals

Used for Modbus addresses — hexadecimal only:
```mizan
0x0000
0x0020
0xFF04
```

---

## 3. Program Declaration — `برنامج`

**Syntax:**
```
برنامج <اسم_البرنامج>؛
```

This **must appear once** at the top of the file. It gives the program a name. The name
must be a valid identifier.

```mizan
برنامج التحكم_الاساسي؛
```

**Common mistakes:**
- Forgetting the terminating semicolon → syntax error
- Using a string literal instead of an identifier: `برنامج "اسم"؛` → ❌

---

## 4. Device Block — `جهاز`

Declares the PLC/controller hardware this program targets.

**Syntax:**
```
جهاز <اسم_الجهاز> {
    <حقل>: <قيمة>،
    ...
}؛
```

### Device Fields

| Keyword | Arabic | Value type | Description |
|---------|--------|------------|-------------|
| `نوع` | TYPE | String | Device type, e.g. `"PLC"` |
| `نظام` | OS | String | Operating system |
| `بروتوكول` | PROTOCOL | String | `"modbus_tcp"`, `"mqtt"`, `"opcua"`, `"http"` |
| `عنوان_ip` | IP | String | IP address in `x.x.x.x` format |
| `منفذ` | PORT | Number | Port number 0–65535 |
| `منفذ_تسلسلي` | SERIAL_PORT | String | Serial port path |
| `دورة_مسح` | SCAN_CYCLE | Duration | Polling interval |

**`عنوان_ip` and `منفذ` are mandatory** — the semantic analyzer will reject a device
block missing either one.

**`duration`** syntax: `<number> <time_unit>` where time units are:
`مللي_ثانية` `ثانية` `دقيقة` `ساعة` `يوم` `اسبوع` `شهر`

```mizan
جهاز وحدة_التحكم {
    نوع: "PLC"،
    بروتوكول: "modbus_tcp"،
    عنوان_ip : "192.168.1.100"،
    منفذ: 502،
    دورة_مسح: 250 مللي_ثانية،
}؛
```

**Trailing comma** after the last field is **allowed** (the grammar accepts optional
trailing commas throughout).

**Validated fields:**
- IP must match `x.x.x.x` pattern — `"localhost"` will trigger a semantic error.
- Port must be between 0 and 65535.
- An unrecognized protocol produces a **warning** (not an error).

---

## 5. Custom Units — `وحدات_مخصصة`

Defines new physical units composed of built-in unit atoms. Must be declared **before**
any sensor or variable uses them.

**Syntax:**
```
وحدات_مخصصة {
    <اسم_الوحدة> : <تعبير_وحدة>،
    ...
}؛
```

A `unit_expr` is a composition of built-in units using `*` (multiplication) or `/`
(division), with parentheses allowed:

```mizan
وحدات_مخصصة {
    سرعة_تدفق  : لتر / دقيقة،
    طاقة_خاصة  : واط / كيلوجرام،
    ضغط_محدد   : بار * متر،
}؛
```

Then use the custom unit name as a type:
```mizan
حساس عداد_التدفق {
    نوع: سرعة_تدفق،
    ...
}؛
متغير تدفق_اللحظي: سرعة_تدفق = 0.0؛
```

**Rules:**
- The right-hand side must use **only built-in unit atoms** (see Section 15). You cannot
  chain custom units on the right-hand side of another custom unit.
- Duplicate names in the same block are a semantic error.

---

## 6. Custom Modes — `اوضاع_مخصصة`

Registers new mode names beyond the four built-in modes. Must appear **before** the
corresponding `وضع` blocks and before any `انتقل_الى` that uses them.

**Syntax:**
```
اوضاع_مخصصة {
    <اسم_1>، <اسم_2>، ...
}؛
```

```mizan
اوضاع_مخصصة {
    معايرة، فحص_مبدئي، تبريد_اضطراري،
}؛
```

**Built-in modes** (always available, no declaration needed):
- `اقلاع` — startup
- `تشغيل` — run
- `صيانة` — maintenance
- `طوارئ` — emergency

---

## 7. Sensor Declaration — `حساس`

Declares a physical sensor connected to a Modbus register.

**Syntax:**
```
حساس <اسم_الحساس> {
    نوع:    <نوع_البيانات>،
    نطاق:   [<min>..<max>]،
    عنوان:  <عنوان_هكس>،
    صحة {
        <قواعد_الصحة>
    }
}؛
```

| Field | Keyword | Required | Description |
|-------|---------|----------|-------------|
| Type | `نوع` | ✅ | Data type of the reading (unit or primitive) |
| Range | `نطاق` | No | Valid reading range `[min..max]` |
| Address | `عنوان` | ✅ | Modbus register in hex (`0x....`) |
| Health | `صحة` | No | Fault-handling rules block |

```mizan
حساس الحرارة {
    نوع:    سيلزيوس،
    نطاق:   [0..150]،
    عنوان:  0x0008،
}؛

حساس مستوى_الخزان {
    نوع:    متر،
    نطاق:   [0..4]،
    عنوان:  0x0000،
}؛
```

**Semantic rules:**
- The `عنوان` field is **mandatory** — omitting it is a semantic error.
- Range `min` must be strictly less than `max`.
- Sensors are **read-only** — assigning to a sensor name in a statement is a semantic error.

---

## 8. Actuator Declaration — `مشغل`

Declares a physical output device (valve, pump, motor, etc.).

**Syntax:**
```
مشغل <اسم_المشغل> {
    نوع:    <نوع_البيانات>،
    نطاق:   [<min>..<max>]،       ← optional
    عنوان:  <عنوان_هكس>،
}؛
```

```mizan
مشغل مضخة_التبريد {
    نوع:    منطقي،
    عنوان:  0x0022،
}؛

مشغل صمام_ضغط {
    نوع:    بالمئة،
    نطاق:   [0..100]،
    عنوان:  0x0030،
}؛
```

**Semantic rules:**
- `عنوان` is **mandatory**.
- Actuators are **write-only** — reading an actuator's value in an expression is a
  semantic error.
- In maintenance mode (`صيانة`), sending a `امر` command to any actuator is **forbidden**
  by the IEC 62443 safety rule.

---

## 9. Variable & Constant Declarations

### Variables — `متغير`

```
متغير <اسم> : <نوع> (= <تعبير>)؟؛
```

The initializer is optional. If omitted the variable is zero-initialized.

```mizan
متغير عداد: صحيح = 0؛
متغير درجة_حرارة: سيلزيوس = 25.0؛
متغير نشط: منطقي = خطا؛
متغير مخزن: حقيقي؛          // no initializer — OK
```

### Constants — `ثابت`

```
ثابت <اسم> : <نوع> = <تعبير>؛
```

The initializer is **mandatory** for constants. Constants cannot be reassigned after
declaration.

```mizan
ثابت الحد_الاقصى: حقيقي = 150.0؛
ثابت معامل_K: حقيقي = 1.732؛
```

### Arrays

Append `[<size>]` to any type for a static array:

```mizan
متغير قراءات: سيلزيوس[10]؛      // array of 10 celsius readings
متغير أعلام: منطقي[4]؛           // boolean flags array
```

Array element access uses `[index_expr]`:
```mizan
قراءات[0] = الحرارة؛
اذا (أعلام[2]) { ... }
```

### Primitive Types

| Type keyword | Meaning |
|---|---|
| `منطقي` | Boolean |
| `صحيح` or `عدد_صحيح` | Integer |
| `حقيقي` or `عدد_حقيقي` | Float |

Any unit name (built-in or custom) is also a valid type — see Section 15.

---

## 10. Procedures — `اجراء`

Reusable named subroutines with typed parameters and an optional return type.

**Syntax:**
```
اجراء <اسم> (<معاملات>؟) (يرجع <نوع>)؟ {
    <جمل>*
}
```

Parameters are declared as `<اسم> : <نوع>` and separated by commas. The return type
follows the `يرجع` keyword.

```mizan
// Procedure with a parameter, returning a boolean
اجراء فحص_المستوى(الحد: حقيقي) يرجع منطقي {
    اذا (مستوى_الخزان < الحد) {
        ارجع صح؛
    }
    ارجع خطا؛
}

// Procedure with no return value (void)
اجراء تهيئة_النظام() {
    سجل "جاري التهيئة..."؛
    انتظر 2 ثانية؛
}
```

**Calling a procedure** — procedures are called as **expressions**, not statements:
```mizan
متغير يحتاج_فتح: منطقي = فحص_المستوى(1.5)؛
اذا (فحص_المستوى(2.0)) { ... }
تهيئة_النظام()؛    // expression statement
```

**Rules:**
- Procedure must be declared at top level (global scope) before use.
- Argument count must match parameter count exactly.
- Return type mismatch between `ارجع` expression and `يرجع` clause is a semantic error.
- Procedures may not be defined inside modes or rules.

---

## 11. Modes & Rules — `وضع` / `قاعدة`

Modes represent operating states of the machine. Each mode contains an optional
startup block and one or more rule blocks.

**Syntax:**
```
وضع <اسم_الوضع> {
    عند_بدء {          ← optional: runs once when mode is entered
        <جمل>*
    }
    قاعدة <اسم_القاعدة> {
        <تعريفات_محلية>*
        <جمل>*
    }
    ...
}
```

### `عند_بدء` — On-Start Block

Executes **exactly once** when the mode is entered. Use it for initialization,
safe-state setup, or logging.

```mizan
وضع اقلاع {
    عند_بدء {
        سجل "بدء نظام التحكم..."؛
        عداد = 0؛
        انتقل_الى تشغيل؛
    }
}
```

### `قاعدة` — Rule Block

Executes **every scan cycle** while the mode is active. Local variables and sensors may
be declared at the top of a rule (before statements).

```mizan
وضع تشغيل {
    قاعدة التحكم_التلقائي {
        // Local declarations (optional)
        متغير يحتاج_فتح: منطقي = فحص_النظام(1.5)؛

        // Statements
        اذا (يحتاج_فتح) {
            امر صمام_الدخول: تشغيل؛
            سجل "المستوى منخفض، جاري الفتح."؛
        } والا {
            امر صمام_الدخول: ايقاف؛
        }
    }

    قاعدة مراقبة_الضغط {
        اذا (الضغط > 9.0) {
            تنبيه مستوى_2 "ضغط مرتفع جداً!"؛
        }
    }
}
```

**Rules:**
- Rule names must be **unique within the same mode**.
- Local declarations must come before statements within the rule.
- A mode may have zero rules (only an `عند_بدء` block is fine).

---

## 12. Statements Reference

### Command Statement — `امر`

Sends a value to an actuator.

**Syntax:** `امر <مشغل> : <قيمة>؛`

```mizan
امر مضخة_التبريد: تشغيل؛
امر صمام_الدخول: ايقاف؛
امر صمام_ضغط: مفتوح؛
امر صمام_ضغط: مغلق؛
امر حالة_المشغل: نشط؛
امر حالة_المشغل: غير_نشط؛
امر صمام_ضغط: 75.0؛       // numeric expression for analog actuator
```

Valid keyword values: `تشغيل` `ايقاف` `مفتوح` `مغلق` `نشط` `غير_نشط`
Or any numeric expression for analog outputs.

**Forbidden in `وضع صيانة`** — produces a semantic error (IEC 62443).

---

### Alert Statement — `تنبيه`

Triggers an industrial alarm at a specified severity level.

**Syntax:** `تنبيه <مستوى> "<رسالة>"؛`

```mizan
تنبيه مستوى_1 "تحذير: درجة حرارة مرتفعة."؛
تنبيه مستوى_2 "خطر: ضغط يتجاوز الحد الآمن!"؛
تنبيه مستوى_3 "حرج: فقدان اتصال الحساس."؛
```

Levels: `مستوى_1` (low) → `مستوى_2` (medium) → `مستوى_3` (high).
Extended levels use the pattern `مستوى_` followed by digits, e.g. `مستوى_4`.

---

### Log Statement — `سجل`

Writes a diagnostic string to the runtime log.

**Syntax:** `سجل "<رسالة>"؛`

```mizan
سجل "بدء نظام التحكم..."؛
سجل "اكتملت المعايرة."؛
```

---

### Goto Statement — `انتقل_الى`

Transitions to a different operating mode.

**Syntax:** `انتقل_الى <اسم_الوضع>؛`

```mizan
انتقل_الى تشغيل؛
انتقل_الى طوارئ؛
انتقل_الى معالجة؛
```

**Critical rule:** Every `انتقل_الى` must have a corresponding entry in the
`انتقالات` table — otherwise it is a **semantic error**. See Section 19.

---

### Wait Statement — `انتظر`

Suspends execution for a specified duration.

**Syntax:** `انتظر <number> <time_unit>؛`

```mizan
انتظر 500 مللي_ثانية؛
انتظر 1 ثانية؛
انتظر 5 دقيقة؛
انتظر 2 ساعة؛
```

---

### Assignment Statement

Assigns a value to a variable (or array element).

**Syntax:** `<اسم> (= | [<index>] =) <تعبير>؛`

```mizan
عداد = 0؛
حالة_النظام = 1؛
قراءات[0] = الحرارة؛
درجة = متوسط(الحرارة لمدة: 10 ثانية)؛
```

**Cannot** assign to a sensor (read-only) or a constant (immutable).

---

### If / Else Statement

```mizan
اذا (<شرط>) {
    <جمل>*
} والا {
    <جمل>*
}
```

The `والا` branch is optional.

```mizan
اذا (الحرارة > 90.0) {
    امر مضخة_التبريد: تشغيل؛
    تنبيه مستوى_2 "درجة حرارة حرجة!"؛
} والا {
    امر مضخة_التبريد: ايقاف؛
}
```

Nested if-else is fully supported:
```mizan
اذا (الضغط > 9.0) {
    تنبيه مستوى_3 "ضغط حرج!"؛
    انتقل_الى طوارئ؛
} والا {
    اذا (الضغط > 7.0) {
        تنبيه مستوى_1 "ضغط مرتفع."؛
    }
}
```

---

### While Loop — `طالما`

```mizan
طالما (<شرط>) {
    <جمل>*
}
```

```mizan
طالما (عداد < 3) {
    سجل "جاري الفحص..."؛
    عداد = عداد + 1؛
    انتظر 1 ثانية؛
}
```

---

### Return Statement — `ارجع`

Returns a value from a procedure. Required in procedures that declare `يرجع <نوع>`.

```mizan
ارجع صح؛
ارجع خطا؛
ارجع عداد * 2؛
ارجع؛         // void return (for procedures without a return type)
```

---

### Default Value — `قيمة_افتراضية`

Used inside sensor health rules to set a safe fallback value when the sensor faults.

**Syntax:** `قيمة_افتراضية: <number>؛`

```mizan
صحة {
    عند_انقطاع_الاتصال {
        قيمة_افتراضية: 25.0؛
        تنبيه مستوى_3 "فقدان الاتصال!"؛
    }
}
```

---

## 13. Expressions & Arithmetic

### Operator Precedence (highest to lowest)

| Priority | Operators | Description |
|---|---|---|
| 1 | `- expr` | Unary minus |
| 2 | `* / %` | Multiply, divide, modulo |
| 3 | `+ -` | Add, subtract |

Parentheses `( )` can override precedence.

```mizan
متغير نتيجة: حقيقي = (الحرارة - 20.0) * 1.5 + 5.0؛
متغير باقي: صحيح = عداد % 4؛
متغير سالب: حقيقي = -الحرارة؛
```

### Aggregate Functions

Query historical sensor data over a time window:

**Syntax:** `<دالة>(<حساس> لمدة: <مدة>)`

| Function | Arabic | Description |
|---|---|---|
| `متوسط` | AVG | Average over window |
| `اقصى` | MAX | Maximum value |
| `ادنى` | MIN | Minimum value |
| `مجموع` | SUM | Sum over window |
| `معدل_التغيير` | RATE | Rate of change |
| `اخر` | LAST | Last recorded value |

```mizan
متغير متوسط_الحرارة: حقيقي = متوسط(الحرارة لمدة: 5 دقيقة)؛
متغير ذروة_الضغط: حقيقي = اقصى(الضغط لمدة: 1 ساعة)؛
متغير معدل: حقيقي = معدل_التغيير(مستوى_الخزان لمدة: 10 ثانية)؛
```

**Important:** Aggregate functions only accept **sensor identifiers**, not variables.
Using a plain variable will trigger a semantic error.

### Procedure Call Expression

```mizan
متغير x: منطقي = فحص_المستوى(1.5)؛
اذا (حساب_الكفاءة(الحرارة، الضغط)) { ... }
```

### Boolean Literals

```mizan
متغير علم: منطقي = صح؛
متغير آخر: منطقي = خطا؛
```

---

## 14. Conditions & Boolean Logic

Conditions appear inside `اذا(...)`, `طالما(...)`, `عند_استمرار(...)`, and `تصويت(...)`.

### Operators

| Operator | Arabic | Precedence | Meaning |
|---|---|---|---|
| `او` | OR | lowest | Logical OR |
| `و` | AND | medium | Logical AND |
| `ليس` | NOT | highest | Logical NOT |

```mizan
// OR — lowest precedence (evaluated last)
اذا (الحرارة > 100 او الضغط > 9.0) { ... }

// AND — binds tighter than OR
اذا (الحرارة > 50 و الضغط < 8.0) { ... }

// NOT — highest precedence (prefix)
اذا (ليس نشط) { ... }

// Complex — use parentheses for clarity
اذا ((الحرارة > 80 او الضغط > 7.0) و ليس وضع_الطوارئ) { ... }
```

### Comparison Operators

| Operator | Meaning |
|---|---|
| `==` | Equal |
| `!=` | Not equal |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal |
| `<=` | Less than or equal |

```mizan
اذا (الحرارة >= 90.0 و الضغط != 0.0) { ... }
```

### Temporal Condition — `عند_استمرار`

True only if the condition has been **continuously true** for the full duration.

**Syntax:** `عند_استمرار(<شرط> لمدة: <مدة>)`

```mizan
اذا (عند_استمرار(الحرارة > 90 لمدة: 5 ثانية)) {
    امر مضخة_التبريد: تشغيل؛
    سجل "حرارة مرتفعة باستمرار لمدة 5 ثوانٍ."؛
}
```

If temperature dips below 90 at any point in the 5 seconds, the clock resets.

### Voting Condition — `تصويت`

True when at least N out of M comparisons are true. Essential for redundant sensor setups.

**Syntax:** `تصويت(<N> من <M> : <comparison_1>, ..., <comparison_M>)`

```mizan
اذا (تصويت(2 من 3 : الحرارة > 100، حرارة_مستشعر_2 > 100، حرارة_مستشعر_3 > 100)) {
    تنبيه مستوى_2 "إجماع: درجة حرارة حرجة!"؛
    انتقل_الى طوارئ؛
}
```

**Rules:**
- N (threshold) must be ≤ M (total) and > 0.
- All comparisons should involve variables or sensors of the **same unit type**.

### Using a Boolean Variable Directly

A boolean variable or sensor can be used directly as a condition without comparison:

```mizan
اذا (نشط) { ... }           // boolean variable
اذا (ليس حالة_التبريد) { ... }
طالما (يعمل) { ... }
```

---

## 15. Type System & Units

### Primitive Types

| Type | Keywords |
|---|---|
| Boolean | `منطقي` |
| Integer | `صحيح`، `عدد_صحيح` |
| Float | `حقيقي`، `عدد_حقيقي` |

### Built-in Unit Types

All of the following are valid as sensor types, variable types, and in arithmetic:

**Temperature & Angles**
```
سيلزيوس       ← Celsius
درجة          ← Degree (valve positioning)
راديان        ← Radian
```

**Pressure**
```
بار           ← Bar
باسكال        ← Pascal
```

**Electrical**
```
فولت          ← Volt
امبير         ← Ampere
أوم           ← Ohm
واط           ← Watt
كيلو_واط      ← Kilowatt
جول           ← Joule
```

**Flow & Volume**
```
لتر           ← Liter
متر_مكعب      ← Cubic meter
```

**Mass**
```
كيلوجرام      ← Kilogram
جرام          ← Gram
طن            ← Ton
```

**Length & Speed**
```
متر           ← Meter
```

**Frequency & Counting**
```
هرتز          ← Hertz
دورة          ← Cycle
عدد           ← Count
```

**Other**
```
بالمئة        ← Percent
لا_وحدة       ← Dimensionless
NTU           ← Turbidity
لوكس          ← Lux
سيمنز         ← Siemens (conductivity)
جزء_في_المليون ← PPM
بت / بايت     ← Digital
```

**Time units** (also usable as types):
```
مللي_ثانية    ثانية    دقيقة    ساعة    يوم    اسبوع    شهر
```

### Pre-defined Composite Units ("Famous Mixes")

These composite units are built in and do not require a `وحدات_مخصصة` declaration:

```
دورة_في_الدقيقة   ← RPM
دورة_في_الثانية   ← RPS
لتر_في_الدقيقة    ← LPM
لتر_في_الساعة     ← LPH
متر_مكعب_في_الساعة ← CMH (m³/h)
متر_في_الثانية    ← MPS
متر_في_الدقيقة    ← MPM
بار_في_الثانية    ← Bar/s
سيلزيوس_في_الثانية ← °C/s
```

### Type Compatibility Rules

- Integer can be assigned to a float variable.
- A unit-typed variable can receive an integer or float (raw numeric).
- A float variable can receive a unit-typed value.
- Two unit-typed variables are compatible only if they have **identical physical dimensions
  and atomic unit compositions**.
  - `سيلزيوس` and `بار` are NOT compatible — semantic error.
  - A custom unit `سرعة_تدفق: لتر / دقيقة` is compatible only with variables also
    declared as `سرعة_تدفق`.

---

## 16. Sensor Health Rules — `صحة`

Embedded inside a sensor declaration, the health block defines automatic fault responses.

**Syntax:**
```
صحة {
    عند_انقطاع_الاتصال {
        <جمل>*
    }،
    عند_قيمة_ثابتة(مدة: <duration>) {
        <جمل>*
    }،
    عند_خروج_عن_النطاق {
        <جمل>*
    }،
}
```

| Rule | Keyword | Trigger |
|---|---|---|
| Disconnect | `عند_انقطاع_الاتصال` | Sensor stops responding |
| Stuck | `عند_قيمة_ثابتة(مدة: ...)` | Value unchanged for duration |
| Out-of-Range | `عند_خروج_عن_النطاق` | Reading outside `نطاق` |

```mizan
حساس الحرارة {
    نوع:   سيلزيوس،
    نطاق:  [0..150]،
    عنوان: 0x0008،
    صحة {
        عند_انقطاع_الاتصال {
            تنبيه مستوى_3 "فقدان الاتصال بحساس الحرارة!"؛
            قيمة_افتراضية: 25.0؛
        }،
        عند_قيمة_ثابتة(مدة: 30 ثانية) {
            تنبيه مستوى_2 "قيمة الحرارة ثابتة، قد يكون الحساس معطوباً."؛
        }،
        عند_خروج_عن_النطاق {
            تنبيه مستوى_2 "قراءة الحرارة خارج النطاق الآمن!"؛
        }،
    }
}؛
```

**Rules:**
- `عند_قيمة_ثابتة` requires a `مدة` parameter with a positive duration.
- All three rule types are optional and combinable.
- An empty health rule block triggers a warning.
- Inside health rules you can use any valid statement (`سجل`, `تنبيه`, `قيمة_افتراضية`, etc.)

---

## 17. Escalation Chains — `تصعيد`

Defines a structured, timed alarm escalation chain (ISA-18.2 compliant).

**Syntax:**
```
تصعيد <اسم_السلسلة> {
    مستوى_<N> {
        رسالة:             "<نص>"،
        مستلم:             "<اسم_المستلم>"،
        مهلة:              <duration>،
        عند_انتهاء_المهلة: انتقل_الى مستوى_<M>،
    }،
    مستوى_<M> {
        رسالة:    "<نص>"،
        مستلم:    "<اسم>"،
        مهلة:     <duration>،
    }،
}؛
```

| Field | Keyword | Description |
|---|---|---|
| Message | `رسالة` | Alert text sent to the receiver |
| Receiver | `مستلم` | Recipient identifier (operator, manager) |
| Timeout | `مهلة` | How long to wait for acknowledgment |
| On Timeout | `عند_انتهاء_المهلة` | Action: escalate to next level or call a procedure |

```mizan
تصعيد سلسلة_الطوارئ {
    مستوى_1 {
        رسالة:             "ضغط حرج"،
        مستلم:             "مشغل_الوردية"،
        مهلة:              10 ثانية،
        عند_انتهاء_المهلة: انتقل_الى مستوى_2،
    }،
    مستوى_2 {
        رسالة:   "خطر انفجار!"،
        مستلم:   "مدير_المصنع"،
        مهلة:    5 ثانية،
    }،
}؛
```

**Rules:**
- Level names follow the pattern `مستوى_<N>` where N is a digit string.
- `عند_انتهاء_المهلة` must reference another level **within the same escalation chain**.
- Circular escalation (infinite loop between levels) is detected and rejected.
- Trigger the escalation chain from a mode rule using `تنبيه` + the escalation chain is
  activated automatically by the runtime when the alert level matches.

---

## 18. Reports — `تقرير`

Defines an automated data report with scheduling and content specification.

**Syntax:**
```
تقرير <اسم_التقرير> {
    جدول:    <specification>،
    تنسيق:   json | csv،
    حفظ_في:  "<مسار>"،
    نوع:     فوري،              ← optional, for immediate one-shot reports
    محتوى {
        <عناصر_التقرير>
    }
}؛
```

### Schedule Specifications

**Every N units (interval):**
```mizan
جدول: كل 5 ثانية،
جدول: كل 1 دقيقة،
جدول: كل 4 ساعة،
جدول: كل 1 اسبوع،
جدول: كل 1 شهر،
```

**Daily at a fixed time:**
```mizan
جدول: كل_يوم الساعة "08:00"،
```

**Weekly on a specific day:**
```mizan
جدول: كل_اسبوع يوم "1" الساعة "06:00"،   // 0=Sunday, 1=Monday ... 6=Saturday
```

**Monthly on a specific day:**
```mizan
جدول: كل_شهر يوم 15 الساعة "00:00"،
جدول: كل_شهر اخر_يوم الساعة "23:59"،
```

Time strings must follow `HH:MM` 24-hour format — `"8:00"` is invalid, use `"08:00"`.

### Report Content Items

```mizan
محتوى {
    // Aggregate over a sensor for the past window
    متوسط(الحرارة لمدة: 1 ساعة) بعنوان "متوسط_الحرارة"،
    اقصى(الضغط لمدة: 1 يوم) بعنوان "ذروة_الضغط"،

    // Instant (current) reading of a sensor
    قيمة_لحظية(مستوى_الخزان) بعنوان "المستوى_الحالي"،

    // Count of alerts over window
    عدد_التنبيهات لمدة: 1 ساعة بعنوان "تنبيهات_الساعة"،

    // System uptime in the window
    وقت_التشغيل_الفعلي لمدة: 1 يوم بعنوان "وقت_التشغيل"،

    // Current operating mode
    الوضع_الحالي بعنوان "الوضع"،

    // Timestamp of report generation
    طابع_زمني بعنوان "وقت_التقرير"،

    // Predictive maintenance: actuator cycle count
    عدد_تشغيلات(مضخة_الحقن) بعنوان "دورات_المضخة"،

    // Actuator current state (ON/OFF)
    حالة_مشغل(مضخة_الحقن) بعنوان "حالة_المضخة"،

    // Sensor health status (OK/FAULT)
    حالة_صحة(حساس_الضغط) بعنوان "سلامة_الحساس"،
}
```

**Semantic rules:**
- `عدد_تشغيلات` and `حالة_مشغل` require an **actuator** identifier.
- `حالة_صحة` requires a **sensor** identifier.
- Aggregate functions and `قيمة_لحظية` require a **sensor** identifier.
- The title string following `بعنوان` is arbitrary.

**Complete example:**
```mizan
تقرير تقرير_الصيانة_الدوري {
    جدول:    كل_يوم الساعة "06:00"،
    تنسيق:   json،
    حفظ_في:  "./reports/daily"،
    محتوى {
        متوسط(الحرارة لمدة: 24 ساعة) بعنوان "متوسط_الحرارة_اليومي"،
        اقصى(الضغط لمدة: 24 ساعة) بعنوان "اقصى_ضغط"،
        عدد_التنبيهات لمدة: 24 ساعة بعنوان "تنبيهات_اليوم"،
        عدد_تشغيلات(مضخة_التبريد) بعنوان "دورات_المضخة"،
        حالة_صحة(الحرارة) بعنوان "سلامة_حساس_الحرارة"،
        طابع_زمني بعنوان "وقت_التقرير"،
    }
}؛
```

---

## 19. Transition Table — `انتقالات`

Declares which mode-to-mode transitions are permitted. This is enforced strictly by the
semantic analyzer — any `انتقل_الى` not listed here will be rejected.

**Syntax:**
```
انتقالات {
    من <وضع_المصدر> الى <وضع_الهدف>؛
    ...
}
```

```mizan
انتقالات {
    من اقلاع    الى تشغيل؛
    من تشغيل    الى طوارئ؛
    من طوارئ    الى تشغيل؛
    من تشغيل    الى صيانة؛
    من صيانة    الى تشغيل؛
}
```

**Rules:**
- Both source and target modes must be defined (either built-in or declared in
  `اوضاع_مخصصة`).
- A transition from a mode to itself triggers a **warning** (self-loop, no effect).
- Duplicate pairs trigger a warning.
- There is no implicit allowed transition — every `انتقل_الى` call must have a matching
  entry here.
- The table may be placed anywhere at the top level but is typically placed last.

---

## 20. Semantic Rules & Common Mistakes

This section collects the most frequent errors and the rules that enforce them.

### ❌ Assigning to a sensor

```mizan
// WRONG — sensors are read-only
الحرارة = 50.0؛       // ❌ semantic error

// CORRECT — read the sensor, assign to a variable
متغير temp: سيلزيوس = الحرارة؛  // ✅
```

### ❌ Reading an actuator in an expression

```mizan
// WRONG — actuators are write-only
اذا (مضخة_التبريد == صح) { ... }   // ❌ semantic error

// CORRECT — maintain a shadow variable
متغير حالة_مضخة: منطقي = خطا؛
// ... when you turn the pump on:
امر مضخة_التبريد: تشغيل؛
حالة_مضخة = صح؛
// ... then read the variable:
اذا (حالة_مضخة) { ... }
```

### ❌ Actuator command in maintenance mode

```mizan
وضع صيانة {
    قاعدة فحص {
        امر مضخة_التبريد: تشغيل؛   // ❌ IEC 62443 violation
    }
}
// CORRECT — use alerts and logging only in maintenance:
وضع صيانة {
    قاعدة فحص {
        سجل "النظام في وضع الصيانة."؛  // ✅
        تنبيه مستوى_1 "الصيانة جارية."؛ // ✅
    }
}
```

### ❌ Unlisted goto

```mizan
انتقالات {
    من اقلاع الى تشغيل؛
}

وضع تشغيل {
    قاعدة مراقبة {
        انتقل_الى طوارئ؛   // ❌ not in transition table!
    }
}
// FIX: add to transition table
انتقالات {
    من اقلاع الى تشغيل؛
    من تشغيل الى طوارئ؛   // ✅
}
```

### ❌ Missing address on sensor/actuator

```mizan
// WRONG
حساس بدون_عنوان {
    نوع: سيلزيوس،
}؛   // ❌ address is mandatory

// CORRECT
حساس الحرارة {
    نوع:   سيلزيوس،
    عنوان: 0x0008،
}؛
```

### ❌ IP address missing from device

```mizan
// WRONG
جهاز وحدة_التحكم {
    نوع:      "PLC"،
    منفذ:     502،
}؛  // ❌ missing عنوان_ip

// CORRECT
جهاز وحدة_التحكم {
    نوع:       "PLC"،
    عنوان_ip:  "192.168.1.10"،
    منفذ:      502،
}؛
```

### ❌ Mismatched units in comparison

```mizan
// WRONG — comparing Celsius to Bar
اذا (الحرارة > الضغط) { ... }   // ❌ incompatible physical dimensions

// CORRECT — compare to a literal or same-unit variable
اذا (الحرارة > 90.0) { ... }    // ✅ numeric literals are dimension-agnostic
```

### ❌ Voting threshold > total

```mizan
// WRONG
اذا (تصويت(4 من 3 : ...)) { ... }   // ❌ threshold 4 > total 3

// CORRECT
اذا (تصويت(2 من 3 : ...)) { ... }   // ✅
```

### ❌ Aggregate on a variable (not sensor)

```mizan
متغير عداد: صحيح = 0؛
متغير avg: حقيقي = متوسط(عداد لمدة: 5 دقيقة)؛  // ❌ must be a sensor

// CORRECT — only sensor identifiers work with aggregates
متغير avg: حقيقي = متوسط(الحرارة لمدة: 5 دقيقة)؛  // ✅
```

### ❌ Calling undefined procedure

```mizan
اذا (فحص_الضغط(8.0)) { ... }   // ❌ if not declared with اجراء

// CORRECT — declare the procedure first
اجراء فحص_الضغط(حد: حقيقي) يرجع منطقي {
    ارجع الضغط > حد؛
}
// ... then use it:
اذا (فحص_الضغط(8.0)) { ... }   // ✅
```

### ❌ Wrong number of arguments

```mizan
اجراء حساب(أ: حقيقي، ب: حقيقي) يرجع حقيقي {
    ارجع أ + ب؛
}

حساب(1.0)؛           // ❌ needs 2 arguments
حساب(1.0، 2.0، 3.0)؛ // ❌ too many

حساب(1.0، 2.0)؛      // ✅
```

### ❌ Assigning a constant

```mizan
ثابت الحد: حقيقي = 100.0؛
الحد = 90.0؛   // ❌ cannot modify a constant

// CORRECT — use a متغير if mutability is needed
متغير الحد: حقيقي = 100.0؛
الحد = 90.0؛   // ✅
```

### ❌ Daily/Weekly/Monthly schedule with wrong time format

```mizan
// WRONG — time must be zero-padded HH:MM
جدول: كل_يوم الساعة "8:00"،      // ❌ must be "08:00"
جدول: كل_يوم الساعة "8:5"،       // ❌ must be "08:05"

// CORRECT
جدول: كل_يوم الساعة "08:00"،     // ✅
جدول: كل_يوم الساعة "23:30"،     // ✅
```

---

## 21. Complete Example Programs

### Example A — Tank Level Control with Calibration Loop

```mizan
// A — Basic control: startup calibration, then automatic level regulation

برنامج التحكم_الاساسي؛

جهاز وحدة_التحكم {
    نوع:       "PLC"،
    بروتوكول:  "modbus_tcp"،
    عنوان_ip:  "127.0.0.1"،
    منفذ:      5020،
    دورة_مسح:  500 مللي_ثانية،
}؛

حساس مستوى_الخزان {
    نوع:   متر،
    نطاق:  [0..4]،
    عنوان: 0x0000،
}؛

مشغل صمام_الدخول {
    نوع:   منطقي،
    عنوان: 0x0020،
}؛

متغير عداد_المعايرة: صحيح = 0؛

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

---

### Example B — Sensor Health Monitoring with Fault Handling

```mizan
// B — Sensor health rules: disconnect, stuck, and out-of-range

برنامج مراقبة_الصحة؛

جهاز وحدة_التحكم {
    نوع:       "PLC"،
    بروتوكول:  "modbus_tcp"،
    عنوان_ip:  "127.0.0.1"،
    منفذ:      5020،
    دورة_مسح:  500 مللي_ثانية،
}؛

حساس الحرارة {
    نوع:   سيلزيوس،
    نطاق:  [0..150]،
    عنوان: 0x0008،
    صحة {
        عند_انقطاع_الاتصال {
            تنبيه مستوى_3 "فقدان الاتصال بحساس الحرارة!"؛
            قيمة_افتراضية: 25.0؛
        }،
        عند_قيمة_ثابتة(مدة: 30 ثانية) {
            تنبيه مستوى_2 "قيمة الحرارة ثابتة لمدة 30 ثانية!"؛
        }،
        عند_خروج_عن_النطاق {
            تنبيه مستوى_2 "قراءة خارج النطاق الآمن!"؛
        }،
    }
}؛

متغير حالة_النظام: صحيح = 0؛

وضع اقلاع {
    عند_بدء {
        سجل "بدء مراقبة الصحة..."؛
        انتقل_الى مراقبة؛
    }
}

وضع مراقبة {
    قاعدة المراقبة {
        اذا (الحرارة > 50.0) {
            سجل "النظام يعمل بشكل طبيعي."؛
            حالة_النظام = 1؛
        } والا {
            حالة_النظام = 0؛
        }
    }
}

انتقالات {
    من اقلاع الى مراقبة؛
}
```

---

### Example C — Escalation Chain with Reports (Predictive Maintenance)

```mizan
// C — Escalation + predictive maintenance report

برنامج التقارير_والتصعيد؛

جهاز وحدة_التحكم {
    نوع:       "PLC"،
    بروتوكول:  "modbus_tcp"،
    عنوان_ip:  "127.0.0.1"،
    منفذ:      5020،
    دورة_مسح:  500 مللي_ثانية،
}؛

حساس الضغط {
    نوع:   بار،
    نطاق:  [0..10]،
    عنوان: 0x0002،
}؛

مشغل مضخة_الحقن {
    نوع:   منطقي،
    عنوان: 0x0024،
}؛

تصعيد سلسلة_الطوارئ {
    مستوى_1 {
        رسالة:             "ضغط حرج"،
        مستلم:             "مشغل_الوردية"،
        مهلة:              10 ثانية،
        عند_انتهاء_المهلة: انتقل_الى مستوى_2،
    }،
    مستوى_2 {
        رسالة:   "خطر انفجار!"،
        مستلم:   "مدير_المصنع"،
        مهلة:    5 ثانية،
    }،
}؛

تقرير تقرير_الصيانة {
    جدول:    كل 5 ثانية،
    تنسيق:   json،
    حفظ_في:  "./reports/cbm"،
    محتوى {
        عدد_تشغيلات(مضخة_الحقن)  بعنوان "دورات_المضخة"،
        حالة_مشغل(مضخة_الحقن)    بعنوان "حالة_المضخة"،
        حالة_صحة(الضغط)           بعنوان "سلامة_الحساس"،
        طابع_زمني                  بعنوان "وقت_التقرير"،
    }
}؛

متغير حالة_الحقن: صحيح = 0؛

وضع اقلاع {
    عند_بدء {
        سجل "بدء نظام التقارير..."؛
        انتقل_الى تشغيل؛
    }
}

وضع تشغيل {
    قاعدة الحقن {
        اذا (الضغط > 8.0) {
            امر مضخة_الحقن: تشغيل؛
            تنبيه مستوى_1 "الضغط مرتفع جداً!"؛
            حالة_الحقن = 1؛
        } والا {
            امر مضخة_الحقن: ايقاف؛
            حالة_الحقن = 0؛
        }
    }
}

انتقالات {
    من اقلاع الى تشغيل؛
}
```

---

### Example D — Redundant Sensor Voting with Emergency Mode

```mizan
// D — 2-of-3 voting, emergency mode, full FSM

برنامج التصويت_والتحكم؛

جهاز وحدة_التحكم {
    نوع:       "PLC"،
    بروتوكول:  "modbus_tcp"،
    عنوان_ip:  "127.0.0.1"،
    منفذ:      5020،
    دورة_مسح:  500 مللي_ثانية،
}؛

حساس الحرارة {
    نوع:   سيلزيوس،
    نطاق:  [0..150]،
    عنوان: 0x0008،
}؛

متغير الحرارة_وهمي_1: سيلزيوس = 0.0؛
متغير الحرارة_وهمي_2: سيلزيوس = 0.0؛

مشغل صمام_الدخول {
    نوع:   منطقي،
    عنوان: 0x0020،
}؛

متغير حالة_الطوارئ: صحيح = 0؛

وضع اقلاع {
    عند_بدء {
        سجل "تهيئة نظام التصويت..."؛
        انتقل_الى معالجة؛
    }
}

وضع معالجة {
    قاعدة التشغيل {
        // Mirror hardware sensor to virtual sensors for voting
        الحرارة_وهمي_1 = الحرارة؛
        الحرارة_وهمي_2 = الحرارة؛

        // Require at least 2 of 3 readings to agree before acting
        اذا (تصويت(2 من 3 :
                الحرارة > 100،
                الحرارة_وهمي_1 > 100،
                الحرارة_وهمي_2 > 100)) {
            تنبيه مستوى_2 "إجماع على درجة الحرارة الحرجة!"؛
            حالة_الطوارئ = 1؛
            انتقل_الى طوارئ؛
        }

        امر صمام_الدخول: تشغيل؛
        حالة_الطوارئ = 0؛
    }
}

وضع طوارئ {
    عند_بدء {
        سجل "وضع الطوارئ: إغلاق جميع المشغلات."؛
        امر صمام_الدخول: ايقاف؛
    }
    قاعدة التبريد {
        اذا (الحرارة < 70.0) {
            سجل "بردت درجة الحرارة، العودة للمعالجة."؛
            انتقل_الى معالجة؛
        }
    }
}

انتقالات {
    من اقلاع  الى معالجة؛
    من معالجة الى طوارئ؛
    من طوارئ  الى معالجة؛
}
```

---

### Example E — Custom Units & Temporal Logic

```mizan
// E — Custom unit, temporal condition, rate-of-change report

برنامج الأمان_الفيزيائي؛

وحدات_مخصصة {
    سرعة_تدفق : لتر / دقيقة،
}؛

جهاز وحدة_التحكم {
    نوع:       "PLC"،
    بروتوكول:  "modbus_tcp"،
    عنوان_ip:  "127.0.0.1"،
    منفذ:      502،
    دورة_مسح:  500 مللي_ثانية،
}؛

حساس الحرارة {
    نوع:   سيلزيوس،
    نطاق:  [0..150]،
    عنوان: 0x0008،
}؛

حساس عداد_التدفق {
    نوع:   سرعة_تدفق،
    نطاق:  [0..500]،
    عنوان: 0x0010،
}؛

مشغل مضخة_التبريد {
    نوع:   منطقي،
    عنوان: 0x0022،
}؛

متغير حالة_التبريد: منطقي = خطا؛

تقرير تقرير_التدفق {
    جدول:    كل_يوم الساعة "08:00"،
    تنسيق:   csv،
    حفظ_في:  "./reports/flow"،
    محتوى {
        متوسط(الحرارة لمدة: 24 ساعة)    بعنوان "متوسط_الحرارة"،
        معدل_التغيير(عداد_التدفق لمدة: 5 دقيقة) بعنوان "معدل_التدفق"،
        طابع_زمني                          بعنوان "تاريخ_التقرير"،
    }
}؛

وضع اقلاع {
    عند_بدء {
        سجل "بدء اختبار الأمان الفيزيائي..."؛
        انتقل_الى تشغيل؛
    }
}

وضع تشغيل {
    قاعدة التبريد_الزمني {
        // Pump only activates if temperature stays above 90°C for 5+ continuous seconds
        اذا (عند_استمرار(الحرارة > 90 لمدة: 5 ثانية)) {
            امر مضخة_التبريد: تشغيل؛
            سجل "حرارة مرتفعة باستمرار، تشغيل المضخة."؛
            حالة_التبريد = صح؛
        } والا {
            امر مضخة_التبريد: ايقاف؛
            حالة_التبريد = خطا؛
        }
    }
}

انتقالات {
    من اقلاع الى تشغيل؛
}
```

---

## Quick Reference Card

### Top-level keywords
`برنامج` `جهاز` `وحدات_مخصصة` `اوضاع_مخصصة` `حساس` `مشغل`
`متغير` `ثابت` `اجراء` `وضع` `تصعيد` `تقرير` `انتقالات`

### Statement keywords
`امر` `تنبيه` `سجل` `انتقل_الى` `انتظر` `اذا` `والا` `طالما` `ارجع` `قيمة_افتراضية`

### Logical operators
`و` (AND) `او` (OR) `ليس` (NOT)

### Boolean literals
`صح` (true) `خطا` (false)

### Mode names (built-in)
`اقلاع` `تشغيل` `صيانة` `طوارئ`

### Actuator values (keywords)
`تشغيل` `ايقاف` `مفتوح` `مغلق` `نشط` `غير_نشط`

### Aggregate functions
`متوسط` `اقصى` `ادنى` `مجموع` `معدل_التغيير` `اخر`

### Time units
`مللي_ثانية` `ثانية` `دقيقة` `ساعة` `يوم` `اسبوع` `شهر`

### Report schedule keywords
`كل` `كل_يوم` `كل_اسبوع` `كل_شهر` `الساعة` `يوم` `اخر_يوم`

### Primitive types
`منطقي` `صحيح` / `عدد_صحيح` `حقيقي` / `عدد_حقيقي`
