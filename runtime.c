#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>
#include <stdint.h>

void print_arabic(const char* raw_str);

// --- Console Setup ---
#ifdef _WIN32
void setup_arabic_console() {
    SetConsoleOutputCP(CP_UTF8); // Output
    SetConsoleCP(CP_UTF8);       // Input
}
#else
void setup_arabic_console() {}
#endif

void panic_div_zero() {
    setup_arabic_console();
    print_arabic("[خطأ وقت التشغيل]: محاولة قسمة على صفر! تم إيقاف البرنامج بأمان");
    printf("\n");
    exit(1);
}

// ==========================================
// 1. UTF-8 Utilities
// ==========================================
uint32_t decode_utf8(const char* str, int* bytes_read) {
    unsigned char c = str[0];
    if (c < 0x80) { *bytes_read = 1; return c; }
    else if ((c & 0xE0) == 0xC0) {
        *bytes_read = 2;
        return ((c & 0x1F) << 6) | (str[1] & 0x3F);
    } else if ((c & 0xF0) == 0xE0) {
        *bytes_read = 3;
        return ((c & 0x0F) << 12) | ((str[1] & 0x3F) << 6) | (str[2] & 0x3F);
    } else if ((c & 0xF8) == 0xF0) {
        *bytes_read = 4;
        return ((c & 0x07) << 18) | ((str[1] & 0x3F) << 12) | ((str[2] & 0x3F) << 6) | (str[3] & 0x3F);
    }
    *bytes_read = 1; return 0;
}

int encode_utf8(uint32_t cp, char* out) {
    if (cp < 0x80) { out[0] = cp; return 1; }
    else if (cp < 0x800) {
        out[0] = 0xC0 | (cp >> 6); out[1] = 0x80 | (cp & 0x3F); return 2;
    } else if (cp < 0x10000) {
        out[0] = 0xE0 | (cp >> 12); out[1] = 0x80 | ((cp >> 6) & 0x3F); out[2] = 0x80 | (cp & 0x3F); return 3;
    } else {
        out[0] = 0xF0 | (cp >> 18); out[1] = 0x80 | ((cp >> 12) & 0x3F); out[2] = 0x80 | ((cp >> 6) & 0x3F); out[3] = 0x80 | (cp & 0x3F); return 4;
    }
}

// ==========================================
// 2. Arabic Reshaper Engine (AI-Generated)
// ==========================================
typedef struct { uint32_t base, iso, fin, ini, med; } ArChar;

const ArChar ar_table[] = {
    {0x0621, 0xFE80, 0xFE80, 0xFE80, 0xFE80}, {0x0622, 0xFE81, 0xFE82, 0xFE81, 0xFE82},
    {0x0623, 0xFE83, 0xFE84, 0xFE83, 0xFE84}, {0x0624, 0xFE85, 0xFE86, 0xFE85, 0xFE86},
    {0x0625, 0xFE87, 0xFE88, 0xFE87, 0xFE88}, {0x0626, 0xFE89, 0xFE8A, 0xFE8B, 0xFE8C},
    {0x0627, 0xFE8D, 0xFE8E, 0xFE8D, 0xFE8E}, {0x0628, 0xFE8F, 0xFE90, 0xFE91, 0xFE92},
    {0x0629, 0xFE93, 0xFE94, 0xFE93, 0xFE94}, {0x062A, 0xFE95, 0xFE96, 0xFE97, 0xFE98},
    {0x062B, 0xFE99, 0xFE9A, 0xFE9B, 0xFE9C}, {0x062C, 0xFE9D, 0xFE9E, 0xFE9F, 0xFEA0},
    {0x062D, 0xFEA1, 0xFEA2, 0xFEA3, 0xFEA4}, {0x062E, 0xFEA5, 0xFEA6, 0xFEA7, 0xFEA8},
    {0x062F, 0xFEA9, 0xFEAA, 0xFEA9, 0xFEAA}, {0x0630, 0xFEAB, 0xFEAC, 0xFEAB, 0xFEAC},
    {0x0631, 0xFEAD, 0xFEAE, 0xFEAD, 0xFEAE}, {0x0632, 0xFEAF, 0xFEB0, 0xFEAF, 0xFEB0},
    {0x0633, 0xFEB1, 0xFEB2, 0xFEB3, 0xFEB4}, {0x0634, 0xFEB5, 0xFEB6, 0xFEB7, 0xFEB8},
    {0x0635, 0xFEB9, 0xFEBA, 0xFEBB, 0xFEBC}, {0x0636, 0xFEBD, 0xFEBE, 0xFEBF, 0xFEC0},
    {0x0637, 0xFEC1, 0xFEC2, 0xFEC3, 0xFEC4}, {0x0638, 0xFEC5, 0xFEC6, 0xFEC7, 0xFEC8},
    {0x0639, 0xFEC9, 0xFECA, 0xFECB, 0xFECC}, {0x063A, 0xFECD, 0xFECE, 0xFECF, 0xFED0},
    {0x0641, 0xFED1, 0xFED2, 0xFED3, 0xFED4}, {0x0642, 0xFED5, 0xFED6, 0xFED7, 0xFED8},
    {0x0643, 0xFED9, 0xFEDA, 0xFEDB, 0xFEDC}, {0x0644, 0xFEDD, 0xFEDE, 0xFEDF, 0xFEE0},
    {0x0645, 0xFEE1, 0xFEE2, 0xFEE3, 0xFEE4}, {0x0646, 0xFEE5, 0xFEE6, 0xFEE7, 0xFEE8},
    {0x0647, 0xFEE9, 0xFEEA, 0xFEEB, 0xFEEC}, {0x0648, 0xFEED, 0xFEEE, 0xFEED, 0xFEEE},
    {0x0649, 0xFEEF, 0xFEF0, 0xFEEF, 0xFEF0}, {0x064A, 0xFEF1, 0xFEF2, 0xFEF3, 0xFEF4},
    {0, 0, 0, 0, 0}
};

const ArChar* find_char(uint32_t cp) {
    for (int i = 0; ar_table[i].base != 0; i++) if (ar_table[i].base == cp) return &ar_table[i];
    return NULL;
}

int connects_left(uint32_t cp) {
    if (cp < 0x0621 || cp > 0x064A) return 0;
    if (cp == 0x0621 || cp == 0x0627 || cp == 0x0629 || cp == 0x062F || cp == 0x0630 || 
        cp == 0x0631 || cp == 0x0632 || cp == 0x0648 || cp == 0x0649) return 0;
    return 1;
}

uint32_t get_lam_alef(uint32_t alef_cp, int prev_conn) {
    if (alef_cp == 0x0622) return prev_conn ? 0xFEF6 : 0xFEF5;
    if (alef_cp == 0x0623) return prev_conn ? 0xFEF8 : 0xFEF7;
    if (alef_cp == 0x0625) return prev_conn ? 0xFEFA : 0xFEF9;
    if (alef_cp == 0x0627) return prev_conn ? 0xFEFC : 0xFEFB;
    return 0;
}

void reshape_arabic_string(const char* input, char* shaped_output) {
    int len = strlen(input);
    uint32_t* cps = malloc((len + 1) * sizeof(uint32_t));
    int count = 0, idx = 0;
    while (idx < len) { int br; cps[count++] = decode_utf8(input + idx, &br); idx += br; }
    cps[count] = 0;
    
    int out_i = 0;
    for (int j = 0; j < count; j++) {
        uint32_t curr = cps[j], prev = (j > 0) ? cps[j-1] : 0, next = (j < count - 1) ? cps[j+1] : 0;
        
        // Handle Lam-Alef Ligatures
        if (curr == 0x0644 && (next == 0x0627 || next == 0x0622 || next == 0x0623 || next == 0x0625)) {
            out_i += encode_utf8(get_lam_alef(next, connects_left(prev)), shaped_output + out_i);
            j++; continue;
        }
        
        const ArChar* ar = find_char(curr);
        if (ar) {
            int p_conn = connects_left(prev), n_conn = connects_left(next), c_right = connects_left(curr);
            uint32_t form = ar->iso;
            if (p_conn && c_right) form = n_conn ? ar->med : ar->ini;
            else form = n_conn ? ar->fin : ar->iso;
            out_i += encode_utf8(form, shaped_output + out_i);
        } else {
            out_i += encode_utf8(curr, shaped_output + out_i);
        }
    }
    shaped_output[out_i] = '\0';
    free(cps);
}

void reverse_string(char* str) {
    int len = strlen(str);
    uint32_t* cps = malloc((len + 1) * sizeof(uint32_t));
    int count = 0, idx = 0;
    while (idx < len) { int br; cps[count++] = decode_utf8(str + idx, &br); idx += br; }
    for (int i = 0; i < count / 2; i++) { uint32_t t = cps[i]; cps[i] = cps[count-1-i]; cps[count-1-i] = t; }
    idx = 0;
    for (int i = 0; i < count; i++) idx += encode_utf8(cps[i], str + idx);
    str[idx] = '\0';
    free(cps);
}

void normalize_arabic_string(char* str) {
    int len = strlen(str);
    uint32_t* cps = malloc((len + 1) * sizeof(uint32_t));
    int count = 0, idx = 0;
    while (idx < len) { int br; cps[count++] = decode_utf8(str + idx, &br); idx += br; }
    for (int i = 0; i < count; i++) {
        uint32_t cp = cps[i];
        if (cp >= 0xFE70 && cp <= 0xFEFF) {
            for (int j = 0; ar_table[j].base != 0; j++) {
                if (cp == ar_table[j].iso || cp == ar_table[j].fin || cp == ar_table[j].ini || cp == ar_table[j].med) {
                    cps[i] = ar_table[j].base; break;
                }
            }
        }
    }
    idx = 0;
    for (int i = 0; i < count; i++) idx += encode_utf8(cps[i], str + idx);
    str[idx] = '\0';
    free(cps);
}

// ==========================================
// 3. Terminal I/O Wrappers
// ==========================================
void print_arabic(const char* raw_str) {
    size_t len = strlen(raw_str);
    
    char* reversed_str = (char*)malloc(len + 1);
    
    // ✅ CRITICAL FIX: Standard Arabic is 2 bytes/char in UTF-8.
    // Presentation Forms (the shaped output) are 3 bytes/char in UTF-8.
    // We must allocate enough space to prevent a heap buffer overflow!
    char* shaped_str = (char*)malloc(len * 2 + 1); 
    
    if (!reversed_str || !shaped_str) { 
        printf("\n!خطأ داخلي: نفدت الذاكرة"); 
        exit(1); 
    }
    
    strcpy(reversed_str, raw_str);
    reverse_string(reversed_str);
    reshape_arabic_string(reversed_str, shaped_str);
    
    printf("%s", shaped_str);
    
    free(reversed_str);
    free(shaped_str);
}

char* read_arabic() {
    size_t buffer_size = 128, position = 0;
    char* buffer = (char*)malloc(buffer_size);
    if (!buffer) exit(1);
    int c;
    while (1) {
        c = getchar();
        if (c == EOF || c == '\n') { buffer[position] = '\0'; break; }
        buffer[position++] = c;
        if (position >= buffer_size) { buffer_size += 128; buffer = realloc(buffer, buffer_size); }
    }
    normalize_arabic_string(buffer);
    return buffer;
}