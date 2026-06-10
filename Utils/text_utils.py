import re
import unicodedata

def normalize_mizan_code(text):
    # 1. إزالة التشكيل (الحركات)
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    
    # 2. توحيد أشكال الهمزات (أ، إ، آ -> ا)
    text = re.sub(r'[أإآ]', 'ا', text)
    
    # 3. توحيد الياء والهاء    
    return text