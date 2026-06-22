// runtime/mizan_modbus.h
#ifndef MIZAN_MODBUS_H
#define MIZAN_MODBUS_H
void*  mizan_modbus_connect      (const char* ip, int port);
double mizan_modbus_read         (void* ctx, int address);
void   mizan_modbus_write        (void* ctx, int address, double value);
int    mizan_modbus_is_connected (void* ctx);
void   mizan_modbus_close        (void* ctx);
#endif