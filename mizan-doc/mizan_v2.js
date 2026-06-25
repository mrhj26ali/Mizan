// mizan_v2.js
// Run with: node mizan_v2.js
// Requires: npm install pptxgenjs

const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "ميزان - لغة برمجة صناعية عربية";
pres.author = "فريق ميزان";

// ─── Theme Colors ───────────────────────────────────────────────────
const NAVY       = "0A1931";
const NAVY_CARD  = "112244";
const NAVY_MID   = "1A3A6B";
const TEAL_CARD  = "0D3349";
const GOLD       = "C9A84C";
const GOLD_LIGHT = "E8C96A";
const WHITE      = "FFFFFF";
const OFFWHITE   = "E8ECF4";
const CODE_BG    = "0D1F3C";

const makeShadow = () => ({
  type: "outer", color: "000000", blur: 5, offset: 2, angle: 45, opacity: 0.28
});

// ===================================================================
// SLIDE 1 — العنوان
// ===================================================================
{
  const s = pres.addSlide();
  s.background = { color: NAVY };

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.3, w: 9.0, h: 0.04,
    fill: { color: GOLD }, line: { color: GOLD, width: 0 }
  });

  s.addText("مِيزَان", {
    x: 0.5, y: 1.45, w: 9.0, h: 1.25,
    fontSize: 58, bold: true, color: GOLD,
    fontFace: "Cambria", align: "center", valign: "middle", margin: 0
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 2.72, w: 9.0, h: 0.04,
    fill: { color: GOLD }, line: { color: GOLD, width: 0 }
  });

  s.addText("لغة برمجة صناعية عربية — من المصدر إلى الحديد بلا مُفسِّر وسيط", {
    x: 0.5, y: 2.82, w: 9.0, h: 0.5,
    fontSize: 15, bold: false, color: OFFWHITE,
    fontFace: "Arial", align: "center", valign: "middle", italic: true, margin: 0
  });

  s.addText("DSL عربية كاملة لأنظمة التحكم الصناعي · تُنتج ملفاً تنفيذياً أصلياً عبر LLVM · متصلة بـ Modbus وMQTT على العتاد الحقيقي", {
    x: 0.8, y: 3.38, w: 8.4, h: 0.45,
    fontSize: 10.5, color: "7A90B8", fontFace: "Arial",
    align: "center", valign: "middle", margin: 0
  });

  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 4.92, w: 9.0, h: 0.52,
    fill: { color: NAVY_CARD }, line: { color: GOLD, width: 1 },
    rectRadius: 0.07, shadow: makeShadow()
  });
  s.addText("اسم الطالب الأول   |   اسم الطالب الثاني   |   اسم الطالب الثالث   |   المشرف: د. ـــــ", {
    x: 0.5, y: 4.92, w: 9.0, h: 0.52,
    fontSize: 11, color: GOLD_LIGHT, fontFace: "Arial",
    align: "center", valign: "middle", margin: 0
  });
}

// ===================================================================
// SLIDE 2 — فكرة المشروع، المراجع، والتطويرات
// ===================================================================
{
  const s = pres.addSlide();
  s.background = { color: NAVY };

  s.addText("فكرة المشروع · المراجع · التطويرات", {
    x: 0.35, y: 0.15, w: 9.3, h: 0.48,
    fontSize: 21, bold: true, color: GOLD,
    fontFace: "Cambria", align: "center", valign: "middle", margin: 0
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.35, y: 0.65, w: 9.3, h: 0.03,
    fill: { color: GOLD_LIGHT }, line: { color: GOLD_LIGHT, width: 0 }
  });

  // ── Left: الفكرة + المراجع ──────────────────────────────
  // Card: الفكرة
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.35, y: 0.76, w: 4.6, h: 2.1,
    fill: { color: TEAL_CARD }, line: { color: GOLD, width: 1 },
    rectRadius: 0.08, shadow: makeShadow()
  });
  s.addText("المشكلة التي يحلّها ميزان", {
    x: 0.45, y: 0.81, w: 4.4, h: 0.28,
    fontSize: 11, bold: true, color: GOLD, fontFace: "Cambria",
    align: "right", margin: 0
  });
  s.addText(
    "لا يوجد حتى الآن نموذج برمجي عربي لأنظمة الأتمتة الصناعية. يضطر مهندسو SCADA وPLC في المنطقة العربية إلى العمل بلغات برمجة أجنبية كـ IEC 61131-3 وStructured Text، مما يُفضي إلى حاجز معرفي وتشغيلي كبير. جاء ميزان ليُزيل هذا الحاجز بتقديم لغة DSL عربية كاملة تُنتج ملفات تنفيذية أصلية دون مُفسِّر وسيط.",
    {
      x: 0.45, y: 1.12, w: 4.4, h: 1.67,
      fontSize: 9.5, color: OFFWHITE, fontFace: "Arial",
      align: "right", valign: "top", margin: 0
    }
  );

  // Card: المراجع
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.35, y: 2.94, w: 4.6, h: 2.68,
    fill: { color: TEAL_CARD }, line: { color: NAVY_MID, width: 1 },
    rectRadius: 0.08, shadow: makeShadow()
  });
  s.addText("المعايير الدولية المُعتمَدة", {
    x: 0.45, y: 2.99, w: 4.4, h: 0.28,
    fontSize: 11, bold: true, color: GOLD, fontFace: "Cambria",
    align: "right", margin: 0
  });
  s.addText([
    { text: "IEC 61131-3  ", options: { bold: true, color: GOLD_LIGHT } },
    { text: "المعيار الدولي للغات PLC (Ladder Logic, ST). يستوحي ميزان منه نموذج الوضع-القاعدة-الإجراء.", options: { color: OFFWHITE, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "IEC 61499  ", options: { bold: true, color: GOLD_LIGHT } },
    { text: "معيار الكتل الوظيفية للتحكم الموزَّع. مَثَل نموذج انتقالات الحالة (FSM) في ميزان.", options: { color: OFFWHITE, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "ISO 80000  ", options: { bold: true, color: GOLD_LIGHT } },
    { text: "نظام الكميات الدولي. يرتبط نظام الأنواع والوحدات في ميزان بالتحليل الأبعادي لـ ISO 80000.", options: { color: OFFWHITE, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "ISA-18.2  ", options: { bold: true, color: GOLD_LIGHT } },
    { text: "معيار إدارة التنبيهات الصناعية. يُطبّقه نظام التصعيد متعدد المستويات في ميزان.", options: { color: OFFWHITE } },
  ], {
    x: 0.45, y: 3.3, w: 4.4, h: 2.25,
    fontSize: 9, fontFace: "Arial", align: "right", valign: "top", margin: 0
  });

  // ── Right: التطويرات ────────────────────────────────────
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 5.05, y: 0.76, w: 4.6, h: 4.86,
    fill: { color: TEAL_CARD }, line: { color: GOLD, width: 1 },
    rectRadius: 0.08, shadow: makeShadow()
  });
  s.addText("التطويرات العلمية وأهميتها", {
    x: 5.15, y: 0.81, w: 4.4, h: 0.28,
    fontSize: 11, bold: true, color: GOLD, fontFace: "Cambria",
    align: "right", margin: 0
  });

  const enhancements = [
    {
      title: "نظام الأنواع الأبعادي للوحدات",
      body: "يمنع العمليات غير المنطقية فيزيائياً (كجمع الضغط مع الحرارة) في مرحلة الترجمة. يستند إلى ذرّات ISO 80000 — فوارق الوحدات تُولِّد خطأ دلالياً قبل توليد أي ملف تنفيذي."
    },
    {
      title: "الشروط الزمنية وشروط التصويت",
      body: "عند_استمرار: تضمن أن الشرط صحيح لمدة محددة قبل التنفيذ، مما يمنع اضطرابات المشغلات من الضوضاء. تصويت N من M: يُضيف إجماع التكرار المطلوب في منشآت IEC 61511."
    },
    {
      title: "مراقبة صحة الحساسات",
      body: "أوضاع الأعطال (انقطاع، قيمة ثابتة، خروج عن النطاق) تُعلَن مباشرةً على الحساس. يُولِّد المُجمِّع حرّاس وقت التشغيل التي تُطلق انتقالات الوضع الآمن تلقائياً."
    },
    {
      title: "تقارير الصيانة التنبؤية",
      body: "تقارير JSON مجدوَلة (يومي/أسبوعي/شهري) تُنشَر عبر MQTT وتزوّد المشغلين ببيانات التشغيل وعدد الدورات — الطبقة المطلوبة للصيانة الشرطية (CBM) وفق ISO 13381."
    },
  ];

  let ey = 1.17;
  for (const e of enhancements) {
    s.addText(e.title, {
      x: 5.15, y: ey, w: 4.4, h: 0.24,
      fontSize: 10, bold: true, color: GOLD_LIGHT, fontFace: "Cambria",
      align: "right", margin: 0
    });
    s.addText(e.body, {
      x: 5.15, y: ey + 0.25, w: 4.4, h: 0.68,
      fontSize: 9, color: OFFWHITE, fontFace: "Arial",
      align: "right", valign: "top", margin: 0
    });
    // divider
    if (ey < 3.5) {
      s.addShape(pres.shapes.RECTANGLE, {
        x: 5.15, y: ey + 1.0, w: 4.2, h: 0.01,
        fill: { color: NAVY_MID }, line: { color: NAVY_MID, width: 0 }
      });
    }
    ey += 1.13;
  }
}

// ===================================================================
// SLIDE 3 — معمارية المشروع
// ===================================================================
{
  const s = pres.addSlide();
  s.background = { color: NAVY };

  s.addText("معمارية المُجمِّع", {
    x: 0.35, y: 0.12, w: 9.3, h: 0.44,
    fontSize: 21, bold: true, color: GOLD,
    fontFace: "Cambria", align: "center", valign: "middle", margin: 0
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.35, y: 0.57, w: 9.3, h: 0.03,
    fill: { color: GOLD_LIGHT }, line: { color: GOLD_LIGHT, width: 0 }
  });

  // ================================================================
  // TOP: Horizontal Pipeline (كود ميزان → ... → ELF Binary)
  // ================================================================
  const pipeY   = 0.68;
  const pipeH   = 0.62;
  const nodes   = [
    { label: "كود ميزان\n.mizan",         gold: true  },
    { label: "ANTLR4\nParser",             gold: false },
    { label: "AST\nBuilder",              gold: false },
    { label: "Semantic\nAnalyzer",        gold: false },
    { label: "LLVM IR\nGenerator",        gold: false },
    { label: "ELF\nBinary",              gold: true  },
  ];
  const totalW   = 9.3;
  const startX   = 0.35;
  const nodeW    = 1.32;
  const gapW     = (totalW - nodes.length * nodeW) / (nodes.length - 1);

  for (let i = 0; i < nodes.length; i++) {
    const nx = startX + i * (nodeW + gapW);
    const n  = nodes[i];

    // connector arrow between nodes
    if (i < nodes.length - 1) {
      const arrowX = nx + nodeW;
      const arrowMid = pipeY + pipeH / 2;
      // line
      s.addShape(pres.shapes.LINE, {
        x: arrowX, y: arrowMid, w: gapW, h: 0,
        line: { color: GOLD, width: 2 }
      });
      // arrowhead triangle approximated with a small right-pointing shape
      s.addShape(pres.shapes.RECTANGLE, {
        x: arrowX + gapW - 0.01, y: arrowMid - 0.07, w: 0.13, h: 0.14,
        fill: { color: GOLD }, line: { color: GOLD, width: 0 }
      });
    }

    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: nx, y: pipeY, w: nodeW, h: pipeH,
      fill:  { color: n.gold ? GOLD : NAVY_MID },
      line:  { color: GOLD, width: n.gold ? 0 : 1 },
      rectRadius: 0.07,
      shadow: makeShadow()
    });
    s.addText(n.label, {
      x: nx, y: pipeY, w: nodeW, h: pipeH,
      fontSize: 9, bold: true,
      color: n.gold ? NAVY : GOLD_LIGHT,
      fontFace: "Arial", align: "center", valign: "middle", margin: 0
    });
  }

  // ================================================================
  // BOTTOM: Three column cards  (Frontend | Semantic Layer | Backend+Runtime)
  // ================================================================
  const colY  = 1.42;
  const colH  = 3.98;
  const colW  = 2.93;
  const colGap = 0.155;

  const columns = [
    {
      header: "Frontend",
      items: [
        { bold: "Mizan.g4", rest: " — قواعد نحوية ANTLR4 تُعرِّف بنية لغة ميزان بالكامل: الأوضاع، الحساسات، المشغّلات، القواعد، والإجراءات." },
        { bold: "ArabicErrorListener", rest: " — يُعيد رسائل الخطأ النحوي باللغة العربية مع رقم السطر والعمود." },
        { bold: "normalize_mizan_code", rest: " — يُزيل التشكيل، يُوحِّد صيغ الهمزة، ويُحوِّل بيانات Unicode التقديمية إلى أشكالها الأصلية قبل الإدخال إلى المُحلِّل." },
        { bold: "ASTBuilder", rest: " — يُحوِّل شجرة ANTLR إلى 40+ نوعاً من عقد AST الخاصة بميزان (SensorDeclNode, ModeBlockNode, RuleBlockNode…)." },
      ]
    },
    {
      header: "Semantic Layer",
      items: [
        { bold: "Type System + Unit Checker", rest: " — يتتبع الأبعاد الفيزيائية (Pa, °C, m/s) عبر طبقة UnitType مبنية على ذرّات ISO 80000. أي عملية غير متوافقة تُوقف التجميع." },
        { bold: "Symbol Table + Scoping", rest: " — Environment متداخلة تضمن عدم تضارب أسماء المتغيرات والحساسات والإجراءات عبر الأوضاع المختلفة." },
        { bold: "ISA-18.2 Validator", rest: " — يتحقق من صحة مستويات التنبيه (1-3)، وسلاسل التصعيد، وقواعد صحة الحساسات قبل توليد أي IR." },
        { bold: "FSM Transition Checker", rest: " — يُنفِّذ DFS على جدول الانتقالات للكشف عن أوضاع غير قابلة للوصول أو حلقات انتقال لا نهائية." },
      ]
    },
    {
      header: "Backend + Runtime",
      items: [
        { bold: "LLVM IR via llvmlite", rest: " — يُولِّد IR مع فحوصات حدود المصفوفات والقسمة على صفر. يُحسِّنه PassManager (O2) ثم يُصدره كـ .o يُربط بـ clang/gcc." },
        { bold: "Modbus TCP (C runtime)", rest: " — runtime.c يستخدم libmodbus لقراءة السجلات وكتابتها على عناوين الحساسات والمشغّلات المُعرَّفة في الكود. يعمل فورياً مع أي PLC." },
        { bold: "MQTT bridge + JSON reports", rest: " — كل تنبيه وتصعيد يُنشر على mizan/alerts/{level}. التقارير الدورية تُكتب بصيغة JSON ويُرسَل إشعار عبر MQTT لأنظمة SCADA." },
        { bold: "ring buffers + health guards", rest: " — بنية ring buffer لكل حساس تحسب avg/max/min/rate على نوافذ زمنية. حرّاس الصحة تُولِّد انتقالات الوضع الآمن عند كشف عطل." },
      ]
    }
  ];

  for (let ci = 0; ci < 3; ci++) {
    const cx = 0.35 + ci * (colW + colGap);
    const col = columns[ci];

    // outer card
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: cx, y: colY, w: colW, h: colH,
      fill: { color: TEAL_CARD }, line: { color: NAVY_MID, width: 1 },
      rectRadius: 0.09, shadow: makeShadow()
    });

    // header label
    s.addText(col.header, {
      x: cx + 0.1, y: colY + 0.1, w: colW - 0.2, h: 0.32,
      fontSize: 12, bold: true, color: GOLD,
      fontFace: "Cambria", align: "center", valign: "middle", margin: 0
    });

    // divider under header
    s.addShape(pres.shapes.RECTANGLE, {
      x: cx + 0.15, y: colY + 0.44, w: colW - 0.3, h: 0.02,
      fill: { color: GOLD }, line: { color: GOLD, width: 0 }
    });

    // bullet items
    let iy = colY + 0.54;
    const itemH = (colH - 0.6) / col.items.length;
    for (const item of col.items) {
      s.addText([
        { text: item.bold, options: { bold: true, color: GOLD_LIGHT } },
        { text: item.rest, options: { color: OFFWHITE } },
      ], {
        x: cx + 0.1, y: iy, w: colW - 0.2, h: itemH - 0.08,
        fontSize: 8.5, fontFace: "Arial",
        align: "right", valign: "top", margin: 0
      });
      // mini divider between items (except last)
      if (item !== col.items[col.items.length - 1]) {
        s.addShape(pres.shapes.RECTANGLE, {
          x: cx + 0.2, y: iy + itemH - 0.1, w: colW - 0.4, h: 0.01,
          fill: { color: NAVY_MID }, line: { color: NAVY_MID, width: 0 }
        });
      }
      iy += itemH;
    }
  }
}

// ===================================================================
// SLIDE 4 — مثال برمجي حي
// ===================================================================
{
  const s = pres.addSlide();
  s.background = { color: NAVY };

  s.addText("مثال برمجي حي — من كود ميزان إلى التنفيذ", {
    x: 0.35, y: 0.12, w: 9.3, h: 0.44,
    fontSize: 21, bold: true, color: GOLD,
    fontFace: "Cambria", align: "center", valign: "middle", margin: 0
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.35, y: 0.57, w: 9.3, h: 0.03,
    fill: { color: GOLD_LIGHT }, line: { color: GOLD_LIGHT, width: 0 }
  });

  // ── Left: code block ─────────────────────────────────
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.35, y: 0.68, w: 5.0, h: 4.76,
    fill: { color: CODE_BG }, line: { color: NAVY_MID, width: 1 },
    rectRadius: 0.08
  });

  s.addText("02_safety_and_health.mizan — مراقبة المحرك الحراري", {
    x: 0.45, y: 0.72, w: 4.8, h: 0.24,
    fontSize: 8.5, bold: true, color: GOLD, fontFace: "Cambria",
    align: "right", margin: 0
  });

  s.addText([
    { text: "برنامج", options: { color: GOLD_LIGHT, bold: true } },
    { text: " مراقبة_المحرك_الحراري؛\n", options: { color: OFFWHITE } },
    { text: "\n", options: { color: OFFWHITE } },
    { text: "جهاز", options: { color: GOLD_LIGHT, bold: true } },
    { text: " وحدة_التحكم {\n", options: { color: OFFWHITE } },
    { text: "  بروتوكول: ", options: { color: OFFWHITE } },
    { text: '"modbus_tcp"', options: { color: "90EE90" } },
    { text: ", منفذ: ", options: { color: OFFWHITE } },
    { text: "5020", options: { color: GOLD_LIGHT } },
    { text: ", دورة_مسح: ", options: { color: OFFWHITE } },
    { text: "1 ثانية", options: { color: GOLD_LIGHT } },
    { text: ";\n};\n\n", options: { color: OFFWHITE } },
    { text: "حساس", options: { color: GOLD_LIGHT, bold: true } },
    { text: " حرارة_المحرك {\n", options: { color: OFFWHITE } },
    { text: "  نوع: ", options: { color: OFFWHITE } },
    { text: "سيلزيوس", options: { color: "90EE90" } },
    { text: ", نطاق: [0..150], عنوان: 0x0008,\n  صحة {\n", options: { color: OFFWHITE } },
    { text: "    عند_انقطاع_الاتصال", options: { color: GOLD_LIGHT } },
    { text: " {\n      تنبيه مستوى_3 ", options: { color: OFFWHITE } },
    { text: '"فقدان الاتصال بحساس الحرارة!"', options: { color: "90EE90" } },
    { text: ";\n      قيمة_افتراضية: 25.0;\n    },\n", options: { color: OFFWHITE } },
    { text: "    عند_قيمة_ثابتة", options: { color: GOLD_LIGHT } },
    { text: "(مدة: 10 ثانية) {\n      تنبيه مستوى_2 ", options: { color: OFFWHITE } },
    { text: '"قراءة ثابتة — ربما عطل!"', options: { color: "90EE90" } },
    { text: ";\n    },\n    عند_خروج_عن_النطاق", options: { color: OFFWHITE } },
    { text: " { تنبيه مستوى_1 ", options: { color: OFFWHITE } },
    { text: '"خارج النطاق الآمن!"', options: { color: "90EE90" } },
    { text: "; }\n  }\n};\n\n", options: { color: OFFWHITE } },
    { text: "مشغل", options: { color: GOLD_LIGHT, bold: true } },
    { text: " مروحة_التبريد { نوع: منطقي, عنوان: 0x0020 };\n\n", options: { color: OFFWHITE } },
    { text: "وضع", options: { color: GOLD_LIGHT, bold: true } },
    { text: " مراقبة {\n  ", options: { color: OFFWHITE } },
    { text: "قاعدة", options: { color: GOLD_LIGHT } },
    { text: " استمرار_الحرارة {\n    ", options: { color: OFFWHITE } },
    { text: "اذا", options: { color: GOLD_LIGHT } },
    { text: " (", options: { color: OFFWHITE } },
    { text: "عند_استمرار", options: { color: GOLD_LIGHT } },
    { text: "(حرارة_المحرك > ", options: { color: OFFWHITE } },
    { text: "90", options: { color: GOLD_LIGHT } },
    { text: " لمدة: ", options: { color: OFFWHITE } },
    { text: "5 ثانية", options: { color: GOLD_LIGHT } },
    { text: ")) {\n      ", options: { color: OFFWHITE } },
    { text: "امر", options: { color: GOLD_LIGHT } },
    { text: " مروحة_التبريد: تشغيل;\n      سجل ", options: { color: OFFWHITE } },
    { text: '"الحرارة مرتفعة. تشغيل المروحة."', options: { color: "90EE90" } },
    { text: ";\n    } والا {\n      ", options: { color: OFFWHITE } },
    { text: "امر", options: { color: GOLD_LIGHT } },
    { text: " مروحة_التبريد: ايقاف;\n    }\n  }\n}", options: { color: OFFWHITE } },
  ], {
    x: 0.45, y: 0.98, w: 4.8, h: 4.38,
    fontSize: 8.2, fontFace: "Courier New",
    align: "left", valign: "top", margin: 0
  });

  // ── Right: explanation cards ─────────────────────────
  const cards = [
    {
      title: "١  تعريف الجهاز → Modbus",
      body: "كلمة جهاز تُنشئ اتصال Modbus TCP حقيقياً. المُجمِّع يُولِّد mizan_modbus_connect(\"127.0.0.1\", 5020) في LLVM IR. دورة المسح (1 ثانية) تُترجَم إلى حلقة رئيسية مع mizan_sleep_ms(1000)."
    },
    {
      title: "٢  صحة الحساس ← ISA-18.2",
      body: "ثلاث قواعد صحة تُولِّد كوداً في runtime.c: mizan_modbus_is_connected() للانقطاع، mizan_health_track_stuck() للقيم الثابتة، mizan_health_out_of_range() لخروج النطاق. كل قاعدة تُطلق تنبيه ISA-18.2 بالمستوى الصحيح."
    },
    {
      title: "٣  الشرط الزمني → LLVM IR",
      body: "عند_استمرار(...لمدة: 5s) يُولِّد عداداً زمنياً كمتغير عالمي في IR: elapsed = now - first_seen_ms. لا يُفعِّل الأمر إلا عند elapsed ≥ 5000 ms. يمنع الاستجابة للتقلبات اللحظية في حساسات الضجيج."
    },
    {
      title: "٤  الأمر → write queue",
      body: "امر مروحة_التبريد: تشغيل يُولِّد: (أ) تحديث المتغير العالمي s_مروحة. (ب) استدعاء mizan_actuator_cmd() لتسجيل rising-edge وعدّ الدورة. (ج) إضافة كتابة Modbus إلى wq_addrs/wq_values لتنفيذها دفعةً واحدة."
    },
  ];

  const rcH = 1.13;
  const rcGap = 0.063;
  let ry = 0.68;
  for (const c of cards) {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 5.45, y: ry, w: 4.2, h: rcH,
      fill: { color: TEAL_CARD }, line: { color: NAVY_MID, width: 1 },
      rectRadius: 0.07, shadow: makeShadow()
    });
    s.addText(c.title, {
      x: 5.55, y: ry + 0.07, w: 4.0, h: 0.24,
      fontSize: 9.5, bold: true, color: GOLD, fontFace: "Cambria",
      align: "right", margin: 0
    });
    s.addText(c.body, {
      x: 5.55, y: ry + 0.33, w: 4.0, h: 0.73,
      fontSize: 8.5, color: OFFWHITE, fontFace: "Arial",
      align: "right", valign: "top", margin: 0
    });
    ry += rcH + rcGap;
  }
}

// ===================================================================
// SLIDE 5 — الاستعداد للتشغيل الحقيقي
// ===================================================================
{
  const s = pres.addSlide();
  s.background = { color: NAVY };

  s.addText("جاهز للتشغيل الحقيقي — البروتوكولات والمعايير", {
    x: 0.35, y: 0.12, w: 9.3, h: 0.44,
    fontSize: 21, bold: true, color: GOLD,
    fontFace: "Cambria", align: "center", valign: "middle", margin: 0
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.35, y: 0.57, w: 9.3, h: 0.03,
    fill: { color: GOLD_LIGHT }, line: { color: GOLD_LIGHT, width: 0 }
  });

  // Intro
  s.addText(
    "لا يكفي أن تُنتج لغة برمجة ملفاً تنفيذياً — يجب أن يتحدث هذا الملف لغة الصناعة الحقيقية. الكود الناتج عن ميزان لا يُحاكي: يتصل بالعتاد مباشرةً عبر بروتوكولين هما الأكثر انتشاراً في أتمتة المصانع عالمياً.",
    {
      x: 0.35, y: 0.68, w: 9.3, h: 0.5,
      fontSize: 10, color: OFFWHITE, fontFace: "Arial",
      align: "right", valign: "middle", margin: 0
    }
  );

  // ── Two main protocol cards ──────────────────────────
  // Modbus
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.35, y: 1.26, w: 4.6, h: 2.4,
    fill: { color: TEAL_CARD }, line: { color: GOLD, width: 1 },
    rectRadius: 0.09, shadow: makeShadow()
  });
  s.addText("Modbus TCP", {
    x: 0.45, y: 1.31, w: 4.4, h: 0.3,
    fontSize: 13, bold: true, color: GOLD, fontFace: "Cambria",
    align: "right", margin: 0
  });
  s.addText([
    { text: "ما هو؟  ", options: { bold: true, color: GOLD_LIGHT } },
    { text: "بروتوكول قراءة/كتابة السجلات عبر TCP/IP. معيار صناعي منذ 1979، يدعمه أكثر من 90% من وحدات PLC في السوق العالمي (Siemens S7, Allen-Bradley, Schneider…).\n\n", options: { color: OFFWHITE } },
    { text: "كيف يُطبِّقه ميزان؟  ", options: { bold: true, color: GOLD_LIGHT } },
    { text: "كل حساس ومشغّل لديه عنوان Modbus (0x0000…). المُجمِّع يُولِّد mizan_modbus_read() في كل دورة مسح وكتابة الأوامر عبر write-queue متزامنة. runtime.c يستخدم libmodbus — المكتبة الرسمية.\n\n", options: { color: OFFWHITE } },
    { text: "الأثر؟  ", options: { bold: true, color: GOLD_LIGHT } },
    { text: "الملف الثنائي الناتج يعمل فوراً على أي PLC حقيقي يدعم Modbus TCP دون أي تعديل إضافي.", options: { color: OFFWHITE } },
  ], {
    x: 0.45, y: 1.64, w: 4.4, h: 1.95,
    fontSize: 9, fontFace: "Arial", align: "right", valign: "top", margin: 0
  });

  // MQTT
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 5.05, y: 1.26, w: 4.6, h: 2.4,
    fill: { color: TEAL_CARD }, line: { color: GOLD, width: 1 },
    rectRadius: 0.09, shadow: makeShadow()
  });
  s.addText("MQTT v3.1.1", {
    x: 5.15, y: 1.31, w: 4.4, h: 0.3,
    fontSize: 13, bold: true, color: GOLD, fontFace: "Cambria",
    align: "right", margin: 0
  });
  s.addText([
    { text: "ما هو؟  ", options: { bold: true, color: GOLD_LIGHT } },
    { text: "بروتوكول رسائل publish/subscribe خفيف الوزن. معيار OASIS الدولي، الأساس المعتمد في IoT وأنظمة SCADA الحديثة (AWS IoT, Azure IoT Hub, Ignition SCADA).\n\n", options: { color: OFFWHITE } },
    { text: "كيف يُطبِّقه ميزان؟  ", options: { bold: true, color: GOLD_LIGHT } },
    { text: "كل تنبيه وتصعيد يُنشر تلقائياً على mizan/alerts/{level} بصيغة JSON. runtime.c يستخدم libmosquitto مع non-blocking loop. المنفذ قابل للتخصيص (--mqtt-port).\n\n", options: { color: OFFWHITE } },
    { text: "الأثر؟  ", options: { bold: true, color: GOLD_LIGHT } },
    { text: "أي منظومة SCADA أو سحابة صناعية تستطيع الاشتراك في موضوعات ميزان فوراً دون تعديل الكود الناتج.", options: { color: OFFWHITE } },
  ], {
    x: 5.15, y: 1.64, w: 4.4, h: 1.95,
    fontSize: 9, fontFace: "Arial", align: "right", valign: "top", margin: 0
  });

  // ── Bottom: 3 readiness cards ───────────────────────
  const rcards = [
    {
      title: "وقت التشغيل C المُحمول",
      body: "runtime.c يُصرَّف مع clang/gcc ويُربط مباشرةً بالملف الثنائي. يعمل على Linux وWindows وأي نظام POSIX — بما فيها لوحات مدمجة كـ Raspberry Pi."
    },
    {
      title: "المُحاكي التفاعلي الحقيقي",
      body: "plant_simulator.py يُشغّل Modbus TCP فعلياً مع نموذج فيزيائي للمصنع. يمكن محاكاة قطع الاتصال وحقن قيم الحساسات يدوياً أثناء التشغيل لاختبار قواعد الصحة."
    },
    {
      title: "بنية مفتوحة للتمديد",
      body: "Visitor Pattern في كل طبقة يجعل إضافة بروتوكولات جديدة (OPC-UA, EtherNet/IP, CANbus) مسألة تمديد للـ IRGenerator فقط دون إعادة كتابة المُجمِّع."
    },
  ];
  const rbW = 2.93, rbH = 1.42;
  const rbY = 3.75;
  for (let i = 0; i < 3; i++) {
    const rbX = 0.35 + i * (rbW + 0.155);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: rbX, y: rbY, w: rbW, h: rbH,
      fill: { color: CODE_BG }, line: { color: NAVY_MID, width: 1 },
      rectRadius: 0.08, shadow: makeShadow()
    });
    s.addText(rcards[i].title, {
      x: rbX + 0.1, y: rbY + 0.1, w: rbW - 0.2, h: 0.26,
      fontSize: 10, bold: true, color: GOLD_LIGHT, fontFace: "Cambria",
      align: "right", margin: 0
    });
    s.addText(rcards[i].body, {
      x: rbX + 0.1, y: rbY + 0.38, w: rbW - 0.2, h: 0.97,
      fontSize: 9, color: OFFWHITE, fontFace: "Arial",
      align: "right", valign: "top", margin: 0
    });
  }
}

// ===================================================================
// SLIDE 6 — الخاتمة والمستودع
// ===================================================================
{
  const s = pres.addSlide();
  s.background = { color: NAVY };

  s.addText("ما الذي أنجزناه؟", {
    x: 0.35, y: 0.12, w: 9.3, h: 0.44,
    fontSize: 21, bold: true, color: GOLD,
    fontFace: "Cambria", align: "center", valign: "middle", margin: 0
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.35, y: 0.57, w: 9.3, h: 0.03,
    fill: { color: GOLD_LIGHT }, line: { color: GOLD_LIGHT, width: 0 }
  });

  // 6 cards 2×3
  const achievements = [
    {
      title: "مُجمِّع كامل من الصفر",
      body: "8 مراحل متسلسلة: Lexer → Parser → AST → Semantic → IR → Optimizer → Object → Linker. كل مرحلة مكتوبة يدوياً بـ Python وC وANTLR4 وllvmlite."
    },
    {
      title: "DSL صناعية عربية",
      body: "ليست لغة عامة. هي DSL يُعبِّر بدقة عن مفاهيم PLC: الأوضاع، القواعد، الحساسات، المشغّلات، الانتقالات — بكلمات مفاتيح عربية أصيلة ودلالات صناعية واضحة."
    },
    {
      title: "أمان على مستوى المُجمِّع",
      body: "فحص الوحدات الفيزيائية، حدود المصفوفات، والقسمة على صفر — أخطاء تُكتشَف قبل التشغيل لا بعده. لا undefined behavior، لا تلف ذاكرة صامت في أنظمة حرجة."
    },
    {
      title: "وقت تشغيل صناعي حقيقي",
      body: "ring buffers للتجميعات الزمنية (avg/max/min/rate)، تتبع صحة الحساسات، عدّادات دورات المشغّلات، جدولة تقارير دقيقة، وتكامل MQTT كامل — كلها في runtime.c."
    },
    {
      title: "تكامل SCADA فوري",
      body: "Modbus TCP وMQTT مُدمجان في الإخراج. أي منظومة SCADA تجارية (Ignition, Node-RED, AWS IoT) تستطيع الاشتراك في موضوعات ميزان دون أي تعديل إضافي."
    },
    {
      title: "بنية قابلة للتمديد",
      body: "Visitor Pattern في كل طبقة يجعل إضافة بروتوكولات أو أنواع بيانات أو تحسينات IR مسألة تمديد لا إعادة كتابة. المشروع مُهيَّأ للتطوير الأكاديمي والصناعي المستمر."
    },
  ];

  const cW = 2.93, cH = 1.27;
  const cGapX = 0.155, cGapY = 0.12;
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 3; col++) {
      const idx = row * 3 + col;
      const cx = 0.35 + col * (cW + cGapX);
      const cy = 0.68 + row * (cH + cGapY);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: cx, y: cy, w: cW, h: cH,
        fill: { color: TEAL_CARD }, line: { color: GOLD, width: 1 },
        rectRadius: 0.08, shadow: makeShadow()
      });
      s.addText(achievements[idx].title, {
        x: cx + 0.1, y: cy + 0.09, w: cW - 0.2, h: 0.27,
        fontSize: 10, bold: true, color: GOLD, fontFace: "Cambria",
        align: "right", margin: 0
      });
      s.addText(achievements[idx].body, {
        x: cx + 0.1, y: cy + 0.38, w: cW - 0.2, h: 0.83,
        fontSize: 8.5, color: OFFWHITE, fontFace: "Arial",
        align: "right", valign: "top", margin: 0
      });
    }
  }

  // Closing quote
  s.addText(
    "ميزان تُثبت أن اللغة الأم ليست عائقاً أمام الهندسة الصناعية — بل يمكن أن تكون قوّتها.",
    {
      x: 0.35, y: 3.6, w: 9.3, h: 0.38,
      fontSize: 11, color: GOLD_LIGHT, fontFace: "Cambria",
      italic: true, align: "center", valign: "middle", margin: 0
    }
  );

  // Repo card
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.35, y: 4.05, w: 9.3, h: 1.35,
    fill: { color: CODE_BG }, line: { color: GOLD, width: 1 },
    rectRadius: 0.1, shadow: makeShadow()
  });
  s.addText("المستودع على GitHub", {
    x: 0.45, y: 4.1, w: 9.1, h: 0.28,
    fontSize: 11, bold: true, color: GOLD, fontFace: "Cambria",
    align: "center", margin: 0
  });
  s.addText("https://github.com/YOUR_USERNAME/mizan", {
    x: 0.45, y: 4.42, w: 9.1, h: 0.32,
    fontSize: 13, bold: true, color: GOLD_LIGHT, fontFace: "Courier New",
    align: "center", valign: "middle", margin: 0,
    hyperlink: { url: "https://github.com/YOUR_USERNAME/mizan" }
  });
  s.addText("استبدل YOUR_USERNAME برابط مستودعك الحقيقي قبل العرض", {
    x: 0.45, y: 4.78, w: 9.1, h: 0.55,
    fontSize: 9, color: "5A7090", fontFace: "Arial",
    align: "center", valign: "middle", italic: true, margin: 0
  });
}

// ─── Write ─────────────────────────────────────────────────────────
pres.writeFile({ fileName: "mizan_presentation.pptx" })
  .then(() => console.log("✅ تم الإنشاء: mizan_presentation.pptx"))
  .catch(err => console.error("❌ خطأ:", err));