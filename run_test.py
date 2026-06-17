import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import traceback
from antlr4 import *
from Mizan.Frontend.MizanLexer import MizanLexer
from Mizan.Frontend.MizanParser import MizanParser
from Mizan.Ast.ast_builder import ASTBuilder
from Mizan.semantic.semantic_analyzer import SemanticAnalyzer
from Utils.text_utils import normalize_mizan_code

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
    file_path = "Mizan.arabic" # Make sure this path is correct for your setup
    try:
        # ✅ 1. Read the raw Arabic code from the file
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_code = f.read()
            
        # ✅ 2. Normalize the text (strips diacritics, unifies hamzas)
        normalized_code = normalize_mizan_code(raw_code)
        
        # ✅ 3. Use InputStream instead of FileStream
        input_stream = InputStream(normalized_code)
        
        # 4. إعداد Lexer و TokenStream
        lexer = MizanLexer(input_stream)
        stream = CommonTokenStream(lexer)
        
        # 5. إعداد Parser
        parser = MizanParser(stream)
        parser.removeErrorListeners() # Good practice: remove default noisy listener
        parser.addErrorListener(MizanErrorListener()) 
        
        # 6. استدعاء القاعدة الجذرية
        tree = parser.program() 
        
        # 7. بناء الـ AST
        builder = ASTBuilder()
        ast = builder.visit(tree)
        print("✅ تم بناء الـ AST بنجاح!")

        # 8. التحليل الدلالي
        analyzer = SemanticAnalyzer()
        analyzer.visit(ast)
        analyzer.print_report()

        print("\n--- تقرير النطاقات الكامل ---")
        analyzer.current_scope.print_node()

    except Exception:
        print(f"❌ حدث خطأ أثناء المعالجة:")
        traceback.print_exc()

if __name__ == "__main__":
    main()