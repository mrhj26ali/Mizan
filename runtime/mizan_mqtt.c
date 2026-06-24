// runtime/mizan_mqtt.c
#include <mosquitto.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

typedef struct { struct mosquitto* m; int connected; } MQCtx;
MQCtx* _g_mqtt = NULL;

void __mizan_set_mqtt_ctx(void* ctx) { _g_mqtt = (MQCtx*)ctx; }

static void _on_connect(struct mosquitto* m, void* obj, int rc) {
    MQCtx* c = (MQCtx*)obj;
    c->connected = (rc == 0);
    if (rc == 0) printf("[MQTT] ✅ اتصال ناجح بالوسيط\n");
    else fprintf(stderr,"[MQTT] ⚠️ فشل الاتصال (rc=%d)\n", rc);
}

static void _on_disconnect(struct mosquitto* m, void* obj, int rc) {
    ((MQCtx*)obj)->connected = 0;
    fprintf(stderr,"[MQTT] ⚠️ انقطع الاتصال\n");
}

void* mizan_mqtt_connect(const char* host, int port, const char* cid) {
    const char* eh = getenv("MIZAN_MQTT_HOST");
    const char* ep = getenv("MIZAN_MQTT_PORT");
    if (eh) host = eh;
    if (ep) port = atoi(ep);

    static int lib_init = 0;
    if (!lib_init) { mosquitto_lib_init(); lib_init = 1; }

    MQCtx* c = (MQCtx*)calloc(1, sizeof(MQCtx));
    if (!c) return NULL;

    c->m = mosquitto_new(cid, true, c);
    if (!c->m) { free(c); return NULL; }

    mosquitto_connect_callback_set(c->m, _on_connect);
    mosquitto_disconnect_callback_set(c->m, _on_disconnect);
    mosquitto_connect(c->m, host, port, 60);
    mosquitto_loop_start(c->m);

    return c;
}

void mizan_mqtt_publish(void* raw, const char* topic, const char* payload) {
    MQCtx* c = (MQCtx*)raw;
    if (!c || !c->m) return;
    mosquitto_publish(c->m, NULL, topic, (int)strlen(payload), payload, 1, false);
}

void mizan_mqtt_close(void* raw) {
    MQCtx* c = (MQCtx*)raw;
    if (!c) return;
    if (c->m) { mosquitto_loop_stop(c->m, true); mosquitto_disconnect(c->m); mosquitto_destroy(c->m); }
    free(c);
    mosquitto_lib_cleanup();
}