import json  
import time
import psutil
import paho.mqtt.client as mqtt
from mqttconn import USERNAME,PASSWORD,STATUS_TOPIC,METRIC_TOPIC,BROKER,PORT

esp_online = False

boot_time = psutil.boot_time()

def setLog(msg):
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')}-{msg}\n")
    
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        setLog("Connected to MQTT Broker")
        client.subscribe(STATUS_TOPIC)
    else:
        setLog("Connection failed:", rc)


def on_message(client, userdata, msg):
    global esp_online

    payload = msg.payload.decode()

    setLog(f"[{msg.topic}] {payload}")

    if msg.topic == STATUS_TOPIC:

        if payload == "online":
            esp_online = True
            setLog("ESP8266 is ONLINE")

        elif payload == "offline":
            esp_online = False
            setLog("ESP8266 is OFFLINE")


client = mqtt.Client()

client.username_pw_set(USERNAME, PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

client.loop_start()

while True:
    if esp_online:
        cpu_percent = psutil.cpu_percent(interval=1)
        vm = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        net = psutil.net_io_counters()
        data = {
            "cpu": {
                "usage": cpu_percent,
                "cores": psutil.cpu_count(logical=True),
                "freq": psutil.cpu_freq().current if psutil.cpu_freq() else 0
            },
            "memory": {
                "used_mb": round(vm.used / 1024 / 1024, 2),
                "total_mb": round(vm.total / 1024 / 1024, 2),
                "percent": vm.percent
            },
            "disk": {
                "used_gb": round(disk.used / 1024 / 1024 / 1024, 2),
                "total_gb": round(disk.total / 1024 / 1024 / 1024, 2),
                "percent": disk.percent
            },
            "uptime_seconds": int(time.time() - boot_time),
        }
        payload = json.dumps(data)
        result = client.publish(
            METRIC_TOPIC,
            payload,
            qos=0,
            retain=False
        )
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            setLog("Metrics Published")
        else:
            setLog("Publish Failed")
        setLog(payload)

    else:
        setLog("ESP8266 Offline -> Skip Publish")

    time.sleep(5)
