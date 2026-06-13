from typing import Optional, Dict, List
from Mizan.semantic.symbols import Symbol


# =====================================================================
# استثناء مخصص لأخطاء التحليل الدلالي
# =====================================================================

class SemanticError(Exception):
    """استثناء مخصص لأخطاء التحليل الدلالي في لغة ميزان."""

    def __init__(self, message: str, node: None):
        line = getattr(node, 'line', '؟')
        # إذا كان لديك خاصية column في العقد، أضفها
        col = getattr(node, 'column', '؟') 
        super().__init__(f"❌ خطأ في السطر {line}:{col} -> {message}")


# =====================================================================
# بيئة التنفيذ (النطاق)
# =====================================================================

class Environment:
    """
    يمثّل نطاق رؤية واحداً (Scope) في لغة ميزان.

    كل نطاق يحمل:
    - name       : اسم النطاق للتشخيص (مثل 'Global', 'Proc_حساب', 'Mode_تشغيل')
    - _symbols   : جدول الرموز المُعرَّفة في هذا النطاق تحديداً
    - enclosing  : النطاق الأب (None للنطاق العام)

    قاعدة البحث (Lexical Scoping):
      ابحث في الحالي → ثم الأب → ثم جده ... حتى Global.
      إذا لم تجد → أرجع None (لا ترمي استثناءً — المحلل الدلالي يقرر).
    """

    def __init__(self, name: str, enclosing: Optional['Environment'] = None):
        self.name = name
        self._symbols: Dict[str, Symbol] = {}
        self.enclosing: Optional['Environment'] = enclosing

    @property
    def symbols(self) -> Dict[str, Symbol]:
        return self._symbols

    # ─────────────────────────────────────────────────────────────
    # تعريف الرموز
    # ─────────────────────────────────────────────────────────────

    def define(self, name: str, symbol: Symbol) -> None:
        """
        يُعرِّف رمزاً جديداً في النطاق الحالي.
        يسمح بإعادة التعريف (تحديث) الرموز — الـ SemanticAnalyzer
        يتحقق من التكرار غير المقصود بنفسه عند الحاجة.
        """
        self._symbols[name] = symbol

    def define_strict(self, name: str, symbol: Symbol, node) -> None:
        if name in self._symbols:
            raise SemanticError(f"الرمز '{name}' مُعرَّف مسبقاً.", node)
        self._symbols[name] = symbol

    # ─────────────────────────────────────────────────────────────
    # البحث عن الرموز
    # ─────────────────────────────────────────────────────────────

    def resolve(self, name: str) -> Optional[Symbol]:
        """
        يبحث عن رمز في النطاق الحالي ثم يصعد عبر النطاقات الأب.
        يُعيد None إذا لم يجد — لا يرمي استثناءً.
        (المحلل الدلالي مسؤول عن إصدار رسالة الخطأ المناسبة.)
        """
        if name in self._symbols:
            return self._symbols[name]
        if self.enclosing is not None:
            return self.enclosing.resolve(name)
        return None

    def resolve_local(self, name: str) -> Optional[Symbol]:
        """
        يبحث في النطاق الحالي فقط دون الصعود للأب.
        مفيد للتحقق من إعادة التعريف في نفس النطاق.
        """
        return self._symbols.get(name)

    def is_defined(self, name: str) -> bool:
        """يتحقق من وجود رمز في أي نطاق (الحالي أو الأب)."""
        return self.resolve(name) is not None

    def is_defined_local(self, name: str) -> bool:
        """يتحقق من وجود رمز في النطاق الحالي فقط."""
        return name in self._symbols

    # ─────────────────────────────────────────────────────────────
    # معلومات النطاق
    # ─────────────────────────────────────────────────────────────

    def depth(self) -> int:
        """يحسب عمق النطاق (0 = Global)."""
        if self.enclosing is None:
            return 0
        return 1 + self.enclosing.depth()

    def all_symbols(self) -> Dict[str, Symbol]:
        """
        يجمع كل الرموز المرئية من هذا النطاق (الحالي + الأجداد).
        عند التعارض، يأخذ الأقرب (الحالي يطغى على الأب).
        """
        result: Dict[str, Symbol] = {}
        if self.enclosing is not None:
            result.update(self.enclosing.all_symbols())
        result.update(self._symbols)  # current scope symbols override enclosing ones
        return result

    def ancestor_chain(self) -> List['Environment']:
        """يُعيد قائمة النطاقات من الحالي وصولاً للـ Global."""
        chain = [self]
        current = self.enclosing
        while current is not None:
            chain.append(current)
            current = current.enclosing
        return chain

    # ─────────────────────────────────────────────────────────────
    # طباعة وتشخيص
    # ─────────────────────────────────────────────────────────────

    def print_stack(self, level: int = 0) -> None:
        """
        يطبع هيكل النطاقات من الحالي إلى الـ Global.
        مفيد لجلسات التشخيص (Debugging).
        """
        indent = "  " * level
        sym_names = list(self._symbols.keys())
        print(f"{indent}📦 Scope '{self.name}' (عمق {self.depth()}): {sym_names}")
        if self.enclosing:
            self.enclosing.print_stack(level + 1)

    def print_node(self, level: int = 0) -> None:
        """
        يطبع هيكل النطاقات بتنسيق شجري.
        """
        sym_names = list(self._symbols.keys())
        prefix = "  " * level + ("└─ " if level > 0 else "")
        print(f"{prefix}Scope '{self.name}' [{', '.join(sym_names) or 'فارغ'}]")
        if self.enclosing:
            self.enclosing.print_node(level + 1)

    def print_flat(self) -> None:
        """
        يطبع جدول الرموز في النطاق الحالي فقط بتنسيق جدول.
        """
        print(f"\n{'─'*50}")
        print(f"📋 النطاق: '{self.name}' (عمق {self.depth()})")
        print(f"{'─'*50}")
        if not self._symbols:
            print("  (فارغ)")
        else:
            for name, sym in self._symbols.items():
                print(f"  {name:<30} {repr(sym)}")
        print(f"{'─'*50}\n")

    def __repr__(self) -> str:
        return f"<Environment '{self.name}' depth={self.depth()} symbols={len(self._symbols)}>"

    def __contains__(self, name: str) -> bool:
        """دعم عامل `in` — يبحث في الحالي فقط."""
        return name in self._symbols