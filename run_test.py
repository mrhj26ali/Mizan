import sys
from antlr4 import *
from Mizan.Frontend.MizanLexer import MizanLexer
from Mizan.Frontend.MizanParser import MizanParser
from Mizan.Ast.ast_builder import ASTBuilder
from Mizan.Frontend.ast_visualizer import ASTVisualizerVisitor
from Mizan.Utils.text_utils import normalize_mizan_code 

def main():
    # 1. قراءة الملف
    file_path = "Mizan/Mizan.arabic"
    with open(file_path, "r", encoding="utf-8") as f:
        raw_code = f.read()

    processed_code = normalize_mizan_code(raw_code)
    input_stream = InputStream(processed_code)
    # 2. إعداد الـ Lexer والـ Parser
    lexer = MizanLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = MizanParser(token_stream)
    
    # 3. بناء الـ Parse Tree
    parse_tree = parser.program()
    
    # 4. بناء الـ AST المخصصة
    builder = ASTBuilder()
    ast = builder.visit(parse_tree)
    print("✅ تم بناء الـ AST بنجاح! جاري توليد الرسم الهندسي...")

    # 5. رسم الشجرة
    visualizer = ASTVisualizerVisitor()
    visualizer.render(ast, 'my_arabic_ast') 
    print("🎨 تم حفظ الرسم في ملف: my_arabic_ast.png")

if __name__ == '__main__':
    main()