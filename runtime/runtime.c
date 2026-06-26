#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <sys/stat.h>
#include <stdint.h>

#ifdef _WIN32
#include <windows.h>
#include <direct.h>
#define SLEEP_MS(ms) Sleep((DWORD)(ms))
#define LOCALTIME(t, tm) localtime_s(tm, t)
#define MKDIR(dir) _mkdir(dir)
#else
#include <unistd.h>
#define SLEEP_MS(ms) do { struct timespec ts = {(ms)/1000, ((ms)%1000)*1000000L}; nanosleep(&ts,NULL); } while(0)
#define LOCALTIME(t, tm) localtime_r(t, tm)
#define MKDIR(dir) mkdir(dir, 0755)
#endif

// ✅ Include the proper header to get access to _g_mqtt and mizan_mqtt_publish
#include "mizan_mqtt.h"

// ════════════════════════════════════════════════════════════════════
// 🧠 TERMINAL CAPABILITY DETECTION (Systems-Level Programming)
// ════════════════════════════════════════════════════════════════════
#ifdef _WIN32
int is_modern_windows_terminal() {
    // 1. Check environment variables for known modern terminal emulators
    if (getenv("WT_SESSION")) return 1; // Windows Terminal
    const char* term_program = getenv("TERM_PROGRAM");
    if (term_program && strstr(term_program, "vscode")) return 1; // VS Code
    
    // 2. Query the Windows Console API to check the current font
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    if (hOut != INVALID_HANDLE_VALUE && GetFileType(hOut) == FILE_TYPE_CHAR) {
        CONSOLE_FONT_INFOEX cfi;
        cfi.cbSize = sizeof(cfi);
        if (GetCurrentConsoleFontEx(hOut, FALSE, &cfi)) {
            // Check if the font is a known modern font that supports Arabic shaping
            if (wcsstr(cfi.FaceName, L"Consolas") ||
                wcsstr(cfi.FaceName, L"Cascadia") ||
                wcsstr(cfi.FaceName, L"Tahoma") ||
                wcsstr(cfi.FaceName, L"Segoe") ||
                wcsstr(cfi.FaceName, L"Lucida") ||
                wcsstr(cfi.FaceName, L"Courier New")) {
                return 1; // Font supports Arabic shaping
            }
        }
    }
    return 0; // Fallback to legacy if font is unknown (e.g., "Raster Fonts")
}
#endif

int is_modern_terminal() {
#ifdef _WIN32
    return is_modern_windows_terminal();
#else
    // On Unix/Linux/macOS, assume modern terminal if TERM is set
    const char* term = getenv("TERM");
    return (term != NULL);
#endif
}

// ─── Console & Arabic output ───────────────────────────────────────
void setup_arabic_console(void) {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif
    setvbuf(stdout, NULL, _IOLBF, 0);
}

static int decode_utf8(const char* s, unsigned int* cp) {
    unsigned char c = (unsigned char)s[0];
    if (c < 0x80) { *cp = c; return 1; }
    if ((c & 0xE0) == 0xC0) { *cp = ((c&0x1F)<<6)|((unsigned char)s[1]&0x3F); return 2; }
    if ((c & 0xF0) == 0xE0) { *cp = ((c&0x0F)<<12)|(((unsigned char)s[1]&0x3F)<<6)|((unsigned char)s[2]&0x3F); return 3; }
    *cp = c; return 1;
}

static int encode_utf8(unsigned int cp, char* out) {
    if (cp < 0x80) { out[0]=cp; return 1; }
    if (cp < 0x800) { out[0]=0xC0|(cp>>6); out[1]=0x80|(cp&0x3F); return 2; }
    out[0]=0xE0|(cp>>12); out[1]=0x80|((cp>>6)&0x3F); out[2]=0x80|(cp&0x3F); return 3;
}

unsigned int reshape_character(unsigned int cp) {
    switch(cp) {
        case 0x0621: return 0xFE80; case 0x0622: return 0xFE81;
        case 0x0623: return 0xFE83; case 0x0624: return 0xFE85;
        case 0x0625: return 0xFE87; case 0x0626: return 0xFE89;
        case 0x0627: return 0xFE8D; case 0x0628: return 0xFE8F;
        case 0x0629: return 0xFE93; case 0x062A: return 0xFE95;
        case 0x062B: return 0xFE99; case 0x062C: return 0xFE9D;
        case 0x062D: return 0xFEA1; case 0x062E: return 0xFEA5;
        case 0x062F: return 0xFEA9; case 0x0630: return 0xFEAB;
        case 0x0631: return 0xFEAD; case 0x0632: return 0xFEAF;
        case 0x0633: return 0xFEB1; case 0x0634: return 0xFEB5;
        case 0x0635: return 0xFEB9; case 0x0636: return 0xFEBD;
        case 0x0637: return 0xFEC1; case 0x0638: return 0xFEC5;
        case 0x0639: return 0xFEC9; case 0x063A: return 0xFECD;
        case 0x0641: return 0xFED1; case 0x0642: return 0xFED5;
        case 0x0643: return 0xFED9; case 0x0644: return 0xFEDD;
        case 0x0645: return 0xFEE1; case 0x0646: return 0xFEE5;
        case 0x0647: return 0xFEE9; case 0x0648: return 0xFEED;
        case 0x0649: return 0xFEEF; case 0x064A: return 0xFEF1;
        default: return cp; 
    }
}

void print_arabic(const char* utf8) {
    if (is_modern_terminal()) {
        // 🟢 Modern Approach: Terminal handles shaping and Bidi natively.
        fputs(utf8, stdout);
        putchar('\n');
    } else {
        // 🔴 Lab 26 Approach: Manual reshape and reverse for legacy/dumb terminals.
        size_t n = strlen(utf8);
        if (n == 0) { putchar('\n'); return; }
        
        unsigned int cps[1024]; int cnt = 0;
        for (size_t i = 0; i < n && cnt < 1023;) {
            int r = decode_utf8(utf8+i, &cps[cnt++]);
            i += r;
            cps[cnt-1] = reshape_character(cps[cnt-1]);
        }
        
        // Reverse the codepoints
        for (int i = 0; i < cnt / 2; i++) {
            unsigned int temp = cps[i];
            cps[i] = cps[cnt - 1 - i];
            cps[cnt - 1 - i] = temp;
        }
        
        char buf[4096]; int bi = 0;
        for (int i = 0; i < cnt && bi < 4090; i++) bi += encode_utf8(cps[i], buf+bi);
        buf[bi] = '\0';
        
        fputs(buf, stdout);
        putchar('\n');
    }
}

void mizan_log(const char* msg) {
    printf("[سجل] "); print_arabic(msg);
}

void mizan_alert(int level, const char* msg) {
    const char* lvl = level==3?"🔴 حرج":level==2?"🟠 تحذير":"🟡 إعلامي";
    fprintf(stderr, "[تنبيه %s] ", lvl); print_arabic(msg);
    
    // ✅ Publish Alerts to MQTT for SCADA integration
    if (_g_mqtt) {
        char topic[64], payload[512];
        snprintf(topic, sizeof(topic), "mizan/alerts/%d", level);
        snprintf(payload, sizeof(payload), "{\"level\":%d,\"message\":\"%s\",\"ts\":%lld}", 
                 level, msg, (long long)time(NULL));
        mizan_mqtt_publish(_g_mqtt, topic, payload);
    }
}

void panic_div_zero(void) {
    fprintf(stderr, "\n🛑 خطأ فادح: قسمة على صفر — توقف البرنامج فوراً\n");
    exit(101);
}

// ─── Time ──────────────────────────────────────────────────────────
int64_t mizan_now_ms(void) {
#ifdef _WIN32
return (int64_t)GetTickCount64();
#else
struct timespec ts;
clock_gettime(CLOCK_MONOTONIC, &ts);
return (int64_t)(ts.tv_sec*1000L + ts.tv_nsec/1000000L);
#endif
}

void mizan_sleep_ms(int64_t ms) {
    if (ms > 0) SLEEP_MS(ms);
}

// ─── Ring buffers (For Aggregates like Average/Max) ────────────────
#define MAX_SENSORS  64
#define RING_CAP    4096

typedef struct { double val; int64_t ts; } Sample;
typedef struct { Sample s[RING_CAP]; int head; int cnt; } Ring;
static Ring g_rings[MAX_SENSORS];

void mizan_ring_push(int sid, double v) {
    if (sid<0||sid>=MAX_SENSORS) return;
    Ring* r = &g_rings[sid];
    r->s[r->head].val = v;
    r->s[r->head].ts  = mizan_now_ms();
    r->head = (r->head+1)%RING_CAP;
    if (r->cnt < RING_CAP) r->cnt++;
}

typedef struct { double sum,mn,mx; int n; } Acc;
static void _acc(double v, Acc* a) {
    a->sum+=v; if(v<a->mn)a->mn=v; if(v>a->mx)a->mx=v; a->n++;
}

static Acc _scan(int sid, int64_t wms) {
    Acc a = {0.0, 1e18, -1e18, 0};
    Ring* r = &g_rings[sid];
    if (r->cnt == 0) return a;
    int64_t cut = mizan_now_ms()-wms;
    int idx = (r->head-1+RING_CAP)%RING_CAP;
    for (int i=0;i<r->cnt;i++) {
        if (r->s[idx].ts < cut) break;
        _acc(r->s[idx].val, &a);
        idx = (idx-1+RING_CAP)%RING_CAP;
    }
    return a;
}

double mizan_ring_avg (int sid, int64_t wms) { Acc a=_scan(sid,wms); return a.n ? a.sum/a.n : 0.0; }
double mizan_ring_max (int sid, int64_t wms) { Acc a=_scan(sid,wms); return a.n ? a.mx : 0.0; }
double mizan_ring_min (int sid, int64_t wms) { Acc a=_scan(sid,wms); return a.n ? a.mn : 0.0; }
double mizan_ring_sum (int sid, int64_t wms) { return _scan(sid,wms).sum; }

double mizan_ring_last(int sid) {
    Ring* r=&g_rings[sid];
    if(!r->cnt) return 0;
    return r->s[(r->head-1+RING_CAP)%RING_CAP].val;
}

double mizan_ring_rate(int sid, int64_t wms) {
    Ring* r=&g_rings[sid];
    if(r->cnt<2) return 0;
    int64_t cut=mizan_now_ms()-wms;
    int hi=(r->head-1+RING_CAP)%RING_CAP;
    Sample newest=r->s[hi], oldest=newest;
    int idx=hi;
    for(int i=0;i<r->cnt;i++){
        if(r->s[idx].ts<cut) break;
        oldest=r->s[idx];
        idx=(idx-1+RING_CAP)%RING_CAP;
    }
    double dt=(newest.ts-oldest.ts)/1000.0;
    return dt>0?(newest.val-oldest.val)/dt:0;
}

// ─── Health tracking (EDGE-TRIGGERED TO PREVENT ALARM FLOODING) ────
// ✅ UPDATED: Added edge flags (disc_fired, stuck_fired, oor_fired)
typedef struct {
    int64_t first_stuck;
    double last_val;
    int has_last;
    int fault_flag;
    int disc_fired;
    int stuck_fired;
    int oor_fired;
} Health;
static Health g_health[MAX_SENSORS] = {0};

// ✅ Edge-triggered Disconnect (Called by LLVM IR)
int mizan_health_track_disconnect(int sid, int is_connected) {
    if(sid<0||sid>=MAX_SENSORS) return 0;
    Health* h = &g_health[sid];
    int is_disc = (is_connected == 0);
    if (is_disc && !h->disc_fired) {
        h->disc_fired = 1;
        return 1;
    }
    if (!is_disc) {
        h->disc_fired = 0;
    }
    return 0;
}

// ✅ Edge-triggered Stuck (Returns i32 boolean, NOT int64 elapsed time)
int mizan_health_track_stuck(int sid, double v, int64_t thr) {
    if(sid<0||sid>=MAX_SENSORS) return 0;
    Health* h=&g_health[sid];
    int same = h->has_last && fabs(v-h->last_val)<1e-9;
    if(!same){
        h->first_stuck=-1;
        h->last_val=v;
        h->has_last=1;
        h->stuck_fired = 0;
        return 0;
    }
    if(h->first_stuck==-1){
        h->first_stuck=mizan_now_ms();
        return 0;
    }
    int64_t elapsed = mizan_now_ms() - h->first_stuck;
    if (elapsed >= thr && !h->stuck_fired) {
        h->stuck_fired = 1;
        h->fault_flag = 1;
        return 1;
    }
    return 0;
}

// ✅ Edge-triggered Out of Range (Now takes `sid` as first argument)
int mizan_health_out_of_range(int sid, double v, double mn, double mx) {
    if(sid<0||sid>=MAX_SENSORS) return 0;
    Health* h = &g_health[sid];
    int is_oor = (v<mn||v>mx)?1:0;
    if (is_oor && !h->oor_fired) {
        h->oor_fired = 1;
        h->fault_flag = 1;
        return 1;
    }
    if (!is_oor) {
        h->oor_fired = 0;
    }
    return 0;
}

// ✅ Sensor Health Status for Reports (Called by LLVM IR)
int mizan_sensor_health(int sid) {
    if (sid<0||sid>=MAX_SENSORS) return 1;
    int h = g_health[sid].fault_flag ? 0 : 1;
    return h;
}

// ─── Predictive Maintenance: Actuator Tracking ───────────────────
#define MAX_ACTUATORS 64
static int g_act_cycles[MAX_ACTUATORS] = {0};
static int g_act_state[MAX_ACTUATORS] = {0};

void mizan_actuator_cmd(int aid, double val) {
    if (aid < 0 || aid >= MAX_ACTUATORS) return;
    int new_state = (val >= 0.5) ? 1 : 0;
    if (new_state == 1 && g_act_state[aid] == 0) {
        g_act_cycles[aid]++;
    }
    g_act_state[aid] = new_state;
}

int mizan_actuator_cycles(int aid) {
    return (aid >= 0 && aid < MAX_ACTUATORS) ? g_act_cycles[aid] : 0;
}

int mizan_actuator_state(int aid) {
    return (aid >= 0 && aid < MAX_ACTUATORS) ? g_act_state[aid] : 0;
}

// ─── Escalation engine (ISA-18.2) ────────────────────────────────
#define MAX_ESC 32
typedef struct { int active; int chain; int level; int64_t deadline; char msg[256]; char recv[128]; } EscTimer;
static EscTimer g_esc[MAX_ESC]; static int g_esc_n=0;

void mizan_escalation_arm(int chain, int level, int64_t tms, const char* msg, const char* recv) {
    if(g_esc_n>=MAX_ESC) return;
    EscTimer* t=&g_esc[g_esc_n++];
    t->active=1; t->chain=chain; t->level=level;
    t->deadline=mizan_now_ms()+tms;
    strncpy(t->msg, msg, 255); strncpy(t->recv, recv, 127);
    printf("[تصعيد] تم تسليح المؤقت -> %s (مهلة: %lldms)\n", recv, (long long)tms);
}

void mizan_escalation_tick(void) {
    int64_t now=mizan_now_ms();
    for(int i=0;i<g_esc_n;i++){
        if(!g_esc[i].active) continue;
        if(now>=g_esc[i].deadline){
            fprintf(stderr,"[تصعيد] 🔺 انتهت المهلة! المستلم: %s | الرسالة: %s\n",
                    g_esc[i].recv, g_esc[i].msg);
            if (_g_mqtt) {
                char topic[128], payload[512];
                snprintf(topic, sizeof(topic), "mizan/escalations/%s", g_esc[i].recv);
                snprintf(payload, sizeof(payload), "{\"level\":%d,\"message\":\"%s\",\"receiver\":\"%s\",\"ts\":%lld}",
                         g_esc[i].level, g_esc[i].msg, g_esc[i].recv, (long long)time(NULL));
                mizan_mqtt_publish(_g_mqtt, topic, payload);
            }
            g_esc[i].active=0;
        }
    }
}

// ─── Enterprise Wall-Clock Scheduler ─────────────────────────────
static int64_t g_schedule_last_fire[64] = {0};

int mizan_schedule_check(int rpt_id, int type, int target_day, int target_hour, int target_min, int is_last_day) {
    if (rpt_id < 0 || rpt_id >= 64) return 0;
    time_t now = time(NULL);
    struct tm tm_now;
    LOCALTIME(&now, &tm_now);
    int current_mins = tm_now.tm_hour * 60 + tm_now.tm_min;
    int target_mins = target_hour * 60 + target_min;
    int should_fire = 0;
    int64_t period_id = 0;
    if (type == 1) {
        period_id = tm_now.tm_yday;
        if (current_mins >= target_mins && g_schedule_last_fire[rpt_id] != period_id) should_fire = 1;
    } else if (type == 2) {
        if (tm_now.tm_wday == target_day && current_mins >= target_mins) {
            period_id = tm_now.tm_year * 100 + tm_now.tm_yday / 7;
            if (g_schedule_last_fire[rpt_id] != period_id) should_fire = 1;
        }
    } else if (type == 3) {
        int target_mday = target_day;
        if (is_last_day) {
            int days_in_month[] = {31,28,31,30,31,30,31,31,30,31,30,31};
            int year = tm_now.tm_year + 1900;
            int mon = tm_now.tm_mon;
            if (mon == 1 && ((year % 4 == 0 && year % 100 != 0) || (year % 400 == 0))) target_mday = 29;
            else target_mday = days_in_month[mon];
        }
        if (tm_now.tm_mday == target_mday && current_mins >= target_mins) {
            period_id = tm_now.tm_year * 100 + tm_now.tm_mon;
            if (g_schedule_last_fire[rpt_id] != period_id) should_fire = 1;
        }
    }
    if (should_fire) {
        g_schedule_last_fire[rpt_id] = period_id;
        return 1;
    }
    return 0;
}

// ─── Report persistence ──────────────────────────────────────────
static void _mkdirs(const char* path) {
    char tmp[512]; snprintf(tmp,sizeof(tmp),"%s",path);
    for(char* p=tmp+1;*p;p++) if(*p=='/'){*p=0; MKDIR(tmp); *p='/';}
    MKDIR(tmp);
}

void mizan_report_write(const char* rid, const char* fmt, const char* dir, const char* payload) {
    const char* env_dir = getenv("MIZAN_DATA_DIR");
    if (env_dir) dir = env_dir;
    _mkdirs(dir);
    time_t now = time(NULL);
    struct tm tm_now;
    LOCALTIME(&now, &tm_now);
    char timestamp[32];
    strftime(timestamp, sizeof(timestamp), "%Y%m%d_%H%M%S", &tm_now);
    char path[768];
    snprintf(path, sizeof(path), "%s/%s_%s.%s", dir, rid, timestamp, fmt);
    FILE* f = NULL;
#ifdef _WIN32
    int wlen = MultiByteToWideChar(CP_UTF8, 0, path, -1, NULL, 0);
    if (wlen > 0) {
        wchar_t* wpath = (wchar_t*)malloc(wlen * sizeof(wchar_t));
        if (wpath) {
            MultiByteToWideChar(CP_UTF8, 0, path, -1, wpath, wlen);
            f = _wfopen(wpath, L"w");
            free(wpath);
        }
    }
#else
    f = fopen(path, "w");
#endif
    if(f){
        fprintf(f, "%s\n", payload);
        fclose(f);
        printf("[تقرير] 📄 تم حفظ: %s\n", path);
    } else {
        fprintf(stderr, "❌ فشل إنشاء ملف التقرير: %s\n", path);
    }
    if(_g_mqtt){
        char topic[128];
        snprintf(topic, sizeof(topic), "mizan/reports/%s", rid);
        mizan_mqtt_publish(_g_mqtt, topic, payload);
    }
}