#include <stdio.h>
#include <stdlib.h>

#ifdef _WIN32
#include <windows.h>
#endif

// دالة تهيئة يتم استدعاؤها آليًا لضبط شاشة ويندوز على UTF-8
void setup_arabic_console() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif
}

// دالة الطوارئ التي يستدعيها مترجمنا عند القسمة على صفر
void panic_div_zero() {
    setup_arabic_console(); // نضمن أن رسالة الخطأ سُتطبع بشكل صحيح
    printf("\n [خطأ وقت التشغيل]: محاولة قسمة على صفر! تم إيقاف البرنامج بأمان \n");
    exit(1);
}