import sys
import traceback
from antlr4 import *
from Mizan.Frontend.MizanLexer import MizanLexer
from Mizan.Frontend.MizanParser import MizanParser
from Mizan.Ast.ast_builder import ASTBuilder
from Mizan.semantic.semantic_analyzer import SemanticAnalyzer


from antlr4.error.ErrorListener import ErrorListener

class MizanErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # استخراج الكلمة التي سببت الخطأ
        offending_text = offendingSymbol.text if offendingSymbol else "رمز غير معروف"
        print(f"❌ [خطأ نحوي] في السطر {line}:{column} -> الكلمة '{offending_text}' غير متوقعة.")
        # اختياري: إيقاف المترجم إذا حدث خطأ نحوي
        # raise Exception("توقف التحليل بسبب خطأ نحوي.")

# داخل دالة main في run_test.py:
# parser = MizanParser(stream)
# parser.removeErrorListeners() # إزالة المستمع الافتراضي المزعج
# parser.addErrorListener(MizanErrorListener()) # إضافة مستمعنا الجديد

def main():
    file_path = "Mizan/Mizan.arabic"
    try:
        # 1. إعداد الـ InputStream الخاص بـ ANTLR
        input_stream = FileStream(file_path, encoding='utf-8')
        
        # 2. إعداد Lexer و TokenStream
        lexer = MizanLexer(input_stream)
        stream = CommonTokenStream(lexer)
        
        # 3. إعداد Parser
        parser = MizanParser(stream)
        parser.addErrorListener(MizanErrorListener()) # إضافة مستمعنا الجديد        # 4. استدعاء القاعدة الجذرية (تأكد أن اسمها 'program' في ملف القواعد .g4)
        tree = parser.program() 
        
        # 5. بناء الـ AST باستخدام الـ Builder الخاص بك
        builder = ASTBuilder()
        ast = builder.visit(tree)
        print("✅ تم بناء الـ AST بنجاح!")

        # 6. التحليل الدلالي
        analyzer = SemanticAnalyzer()
        analyzer.visit(ast)
        # اطبع تقرير التحليل الدلالي الكامل (يشمل الأخطاء والتحذيرات)
        analyzer.print_report()

        # 7. تقرير النطاقات (طباعة مفصّلة للـ scope الحالي إذا رغبت)
        print("\n--- تقرير النطاقات الكامل ---")
        analyzer.current_scope.print_node()

    except Exception:
        print(f"❌ حدث خطأ أثناء المعالجة:")
        traceback.print_exc()

if __name__ == "__main__":
    main()