// runtime/mizan_modbus.c
#include <modbus/modbus.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>

typedef struct {
    modbus_t* ctx;
    char      ip[64];
    int       port;
    int       connected;
} MBCtx;

void* mizan_modbus_connect(const char* ip, int port) {
    const char* env_ip   = getenv("MIZAN_DEVICE_IP");
    const char* env_port = getenv("MIZAN_DEVICE_PORT");
    if (env_ip)   ip   = env_ip;
    if (env_port) port = atoi(env_port);

    MBCtx* c = (MBCtx*)calloc(1, sizeof(MBCtx));
    if (!c) return NULL;
    strncpy(c->ip, ip, sizeof(c->ip)-1);
    c->port = port;
    c->ctx  = modbus_new_tcp(ip, port);
    if (!c->ctx) { c->connected = 0; return c; }
    modbus_set_response_timeout(c->ctx, 0, 500000);
    c->connected = (modbus_connect(c->ctx) != -1) ? 1 : 0;
    if (c->connected)
        printf("[Modbus] ✅ اتصال ناجح بـ %s:%d\n", ip, port);
    else
        fprintf(stderr,"[Modbus] ⚠️ فشل الاتصال بـ %s:%d -> %s\n", ip, port, modbus_strerror(errno));
    return c;
}

static int _reconnect(MBCtx* c) {
    if (!c->ctx) {
        c->ctx = modbus_new_tcp(c->ip, c->port);
        if (!c->ctx) return 0;
        modbus_set_response_timeout(c->ctx, 0, 500000);
    }
    modbus_close(c->ctx);
    c->connected = (modbus_connect(c->ctx) != -1);
    return c->connected;
}

double mizan_modbus_read(void* raw, int address) {
    MBCtx* c = (MBCtx*)raw;
    if (!c) return 0.0;
    if (!c->connected && !_reconnect(c)) return 0.0;
    uint16_t regs[2] = {0,0};
    if (modbus_read_registers(c->ctx, address, 2, regs) == -1) {
        c->connected = 0;
        return 0.0;
    }
    float v = modbus_get_float_abcd(regs);
    return (double)v;
}

void mizan_modbus_write(void* raw, int address, double value) {
    MBCtx* c = (MBCtx*)raw;
    if (!c) return;
    if (!c->connected && !_reconnect(c)) return;
    uint16_t regs[2];
    modbus_set_float_abcd((float)value, regs);
    if (modbus_write_registers(c->ctx, address, 2, regs) == -1)
        c->connected = 0;
}

int mizan_modbus_is_connected(void* raw) {
    MBCtx* c = (MBCtx*)raw;
    return (c && c->connected) ? 1 : 0;
}

void mizan_modbus_close(void* raw) {
    MBCtx* c = (MBCtx*)raw;
    if (!c) return;
    if (c->ctx) { modbus_close(c->ctx); modbus_free(c->ctx); }
    free(c);
}