// runtime/runtime.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <sys/stat.h>
#include <stdint.h>   // REQUIRED for int64_t
#include <direct.h>

#ifdef _WIN32
#include <windows.h>
#define SLEEP_MS(ms) Sleep((DWORD)(ms))
#else
#include <unistd.h>
#define SLEEP_MS(ms) do { struct timespec ts = {(ms)/1000, ((ms)%1000)*1000000L}; nanosleep(&ts,NULL); } while(0)
#endif

#include "mizan_mqtt.h"
void mizan_mqtt_publish(void* ctx, const char* topic, const char* payload);

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
    if ((c & 0xF0) == 0xE0) { *cp = ((c&0x0F)<<12)|((unsigned char)s[1]&0x3F)<<6|((unsigned char)s[2]&0x3F); return 3; }
    *cp = c; return 1;
}
static int encode_utf8(unsigned int cp, char* out) {
    if (cp < 0x80) { out[0]=cp; return 1; }
    if (cp < 0x800) { out[0]=0xC0|(cp>>6); out[1]=0x80|(cp&0x3F); return 2; }
    out[0]=0xE0|(cp>>12); out[1]=0x80|((cp>>6)&0x3F); out[2]=0x80|(cp&0x3F); return 3;
}

void print_arabic(const char* utf8) {
    size_t n = strlen(utf8);
    if (n == 0) { putchar('\n'); return; }
    unsigned int cps[1024]; int cnt = 0;
    for (size_t i = 0; i < n && cnt < 1023;) {
        int r = decode_utf8(utf8+i, &cps[cnt++]);
        i += r;
    }
    // Reverse for RTL visual order
    for (int a=0, b=cnt-1; a<b; a++, b--) { unsigned int t=cps[a]; cps[a]=cps[b]; cps[b]=t; }
    char buf[4096]; int bi = 0;
    for (int i = 0; i < cnt && bi < 4090; i++) bi += encode_utf8(cps[i], buf+bi);
    buf[bi] = '\0';
    fputs(buf, stdout);
    putchar('\n');
}

void mizan_log(const char* msg) {
    printf("[سجل] "); print_arabic(msg);
}

void mizan_alert(int level, const char* msg) {
    const char* lvl = level==3?"🔴 حرج":level==2?"🟠 تحذير":"🟡 إعلامي";
    fprintf(stderr, "[تنبيه %s] ", lvl); print_arabic(msg);
    extern void* _g_mqtt;
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

// ─── Time (FIXED: int64_t instead of long) ─────────────────────────
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

// ─── Ring buffers (FIXED: int64_t for timestamps and window) ───────
#define MAX_SENSORS  64
#define RING_CAP    4096

typedef struct { double val; int64_t ts; } Sample; // FIXED: int64_t ts
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

static Acc _scan(int sid, int64_t wms) { // FIXED: int64_t wms
    Acc a = {0.0, 1e18, -1e18, 0};
    Ring* r = &g_rings[sid];
    int64_t cut = mizan_now_ms()-wms;
    int idx = (r->head-1+RING_CAP)%RING_CAP;
    for (int i=0;i<r->cnt;i++) {
        if (r->s[idx].ts < cut) break;
        _acc(r->s[idx].val, &a);
        idx = (idx-1+RING_CAP)%RING_CAP;
    }
    return a;
}

double mizan_ring_avg (int sid, int64_t wms) { Acc a=_scan(sid,wms); return a.n?a.sum/a.n:0; }
double mizan_ring_max (int sid, int64_t wms) { Acc a=_scan(sid,wms); return a.n?a.mx:0; }
double mizan_ring_min (int sid, int64_t wms) { Acc a=_scan(sid,wms); return a.n?a.mn:0; }
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

// ─── Health tracking (FIXED: int64_t) ──────────────────────────────
typedef struct { int64_t first_stuck; double last_val; int has_last; } Health; // FIXED
static Health g_health[MAX_SENSORS];

int64_t mizan_health_track_stuck(int sid, double v, int64_t thr) { // FIXED
    if(sid<0||sid>=MAX_SENSORS) return 0;
    Health* h=&g_health[sid];
    int same = h->has_last && fabs(v-h->last_val)<1e-9;
    if(!same){ h->first_stuck=-1; h->last_val=v; h->has_last=1; return 0; }
    if(h->first_stuck==-1){ h->first_stuck=mizan_now_ms(); return 0; }
    return mizan_now_ms()-h->first_stuck;
}

int mizan_health_out_of_range(double v, double mn, double mx) {
    return (v<mn||v>mx)?1:0;
}

// ─── Escalation engine (FIXED: int64_t) ────────────────────────────
#define MAX_ESC 32
typedef struct { int active; int chain; int level; int64_t deadline; char msg[256]; char recv[128]; } EscTimer; // FIXED
static EscTimer g_esc[MAX_ESC]; static int g_esc_n=0;

void mizan_escalation_arm(int chain, int level, int64_t tms, const char* msg, const char* recv) { // FIXED
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
            g_esc[i].active=0;
        }
    }
}

// ─── Report persistence ────────────────────────────────────────────
static void _mkdirs(const char* path) {
    char tmp[512]; snprintf(tmp,sizeof(tmp),"%s",path);
    for(char* p=tmp+1;*p;p++) if(*p=='/'){*p=0;
#ifdef _WIN32
        _mkdir(tmp);
#else
        mkdir(tmp,0755);
#endif
        *p='/';}
#ifdef _WIN32
    _mkdir(tmp);
#else
    mkdir(tmp,0755);
#endif
}

extern void* _g_mqtt;

void mizan_report_write(const char* rid, const char* fmt, const char* dir, const char* payload) {
    const char* env_dir = getenv("MIZAN_DATA_DIR");
    if (env_dir) dir = env_dir;
    _mkdirs(dir);
    char path[768];
    snprintf(path,sizeof(path),"%s/%s_%lld.%s", dir, rid, (long long)time(NULL), fmt);
    FILE* f=fopen(path,"w");
    if(f){ fprintf(f,"%s\n",payload); fclose(f);
           printf("[تقرير] 📄 تم حفظ: %s\n",path); }
    if(_g_mqtt){
        char topic[128]; snprintf(topic,sizeof(topic),"mizan/reports/%s",rid);
        mizan_mqtt_publish(_g_mqtt, topic, payload);
    }
}