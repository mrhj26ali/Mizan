# sim/mqtt_monitor.py
"""
Subscribe to all Mizan MQTT topics and print live traffic to the terminal.

Run in a separate terminal:
  pip install paho-mqtt
  python sim/mqtt_monitor.py

Requires mosquitto running on localhost:1883.
Windows: winget install EclipseMosquitto.Mosquitto  then  mosquitto -v
"""
import sys
import os
import json
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

# ✅ ROBUST UTF-8 FIX FOR WINDOWS
# 1. Tell Python to safely reconfigure the output stream to UTF-8
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# 2. Tell the Windows Terminal to interpret bytes as UTF-8 (Code Page 65001)
import json
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion   # paho-mqtt >= 2.0


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("✅ متصل بوسيط MQTT على localhost:1883")
        client.subscribe("mizan/#")
        print("📡 يستمع على mizan/# ... (Ctrl+C للإيقاف)\n")
    else:
        print(f"❌ فشل الاتصال بالوسيط (reason_code={reason_code})")


def on_message(client, userdata, msg):
    topic   = msg.topic
    raw     = msg.payload.decode("utf-8", errors="replace")
    try:
        pretty = json.dumps(json.loads(raw), ensure_ascii=False, indent=2)
    except Exception:
        pretty = raw

    bar = "─" * 55
    print(f"\n{bar}")
    print(f"📨  {topic}")
    print(bar)
    print(pretty)


def on_disconnect(client, userdata, flags, reason_code, properties):
    print(f"⚠️  انقطع الاتصال (reason_code={reason_code})")


# paho-mqtt 2.x requires CallbackAPIVersion
client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
client.on_connect    = on_connect
client.on_message    = on_message
client.on_disconnect = on_disconnect

try:
    client.connect("localhost", 1884, keepalive=60)
    client.loop_forever()
except KeyboardInterrupt:
    print("\n\nإيقاف المراقب.")
except ConnectionRefusedError:
    print("❌ تعذر الاتصال — تأكد من تشغيل mosquitto أولاً:")
    print("   mosquitto -v")