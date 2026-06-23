#ifndef MIZAN_MQTT_H
#define MIZAN_MQTT_H

#ifdef __cplusplus
extern "C" {
#endif

// Core MQTT Functions
void* mizan_mqtt_connect(const char* host, int port, const char* cid);
void  mizan_mqtt_publish(void* ctx, const char* topic, const char* payload);
void  mizan_mqtt_close(void* ctx);

// Internal helper used by runtime.c to share the global context
extern void* _g_mqtt; 
void __mizan_set_mqtt_ctx(void* ctx);

#ifdef __cplusplus
}
#endif

#endif // MIZAN_MQTT_H