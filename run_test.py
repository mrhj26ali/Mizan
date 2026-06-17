import os
import sys
# ✅ FIX: Add the parent directory to the path so 'Mizan' can be resolved
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import traceback
from antlr4 import *
from Mizan.Frontend.MizanLexer import MizanLexer
from Mizan.Frontend.MizanParser import MizanParser
from Mizan.Ast.ast_builder import ASTBuilder
from Mizan.semantic.semantic_analyzer import SemanticAnalyzer
from Utils.text_utils import normalize_mizan_code

# ✅ NEW: Import the AST Visualizer (since we moved it to the Ast folder)
from Mizan.Ast.ast_visualizer import ASTVisualizerVisitor 

from antlr4.error.ErrorListener import ErrorListener
from Backend.ir_generator import IRGenerator

class MizanErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # استخراج الكلمة التي سببت الخطأ
        offending_text = offendingSymbol.text if offendingSymbol else "رمز غير معروف"
        print(f"❌ [خطأ نحوي] في السطر {line}:{column} -> الكلمة '{offending_text}' غير متوقعة.")

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

        # ✅ NEW: Generate the AST Visualization (Graphviz)
        visualizer = ASTVisualizerVisitor()
        visualizer.render(ast, output_filename='mizan_ast_output')
        print("✅ تم إنشاء صورة الـ AST (mizan_ast_output.png) بنجاح!")
        # ---------------------------------------------------------

        # 8. التحليل الدلالي
        analyzer = SemanticAnalyzer()
        analyzer.visit(ast)
        analyzer.print_report()

        print("\n--- تقرير النطاقات الكامل ---")
        analyzer.current_scope.print_node()

    except Exception:
        print(f"❌ حدث خطأ أثناء المعالجة:")
        traceback.print_exc()
 # 9. توليد كود الآلة (Backend / LLVM)
    if not analyzer.errors:
            ir_generator = IRGenerator()
            llvm_ir_code = ir_generator.generate(ast)
            
            # حفظ كود LLVM في ملف نصي للمراجعة
            with open("output.ll", "w", encoding="utf-8") as f:
                f.write(llvm_ir_code)
            print("✅ تم حفظ كود LLVM IR في الملف: output.ll")
    else:
            print("⛔ تم إيقاف توليد الكود بسبب وجود أخطاء دلالية.")
if __name__ == "__main__":
    main()