# mqtt_subscribe.py
import network
import time
from umqtt.simple import MQTTClient
# WiFi credentials
SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
# MQTT broker details
MQTT_BROKER = "test.mosquitto.org"
CLIENT_ID = "esp32_test_sub"
TOPIC = b"esp32/test/topic"
# WiFi connect
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep(1)

print("WiFi connected:", wlan.ifconfig())
# Callback when message arrives
def sub_cb(topic, msg):
    print("Received on", topic, ":", msg)
# MQTT setup
client = MQTTClient(CLIENT_ID, MQTT_BROKER)
client.set_callback(sub_cb)
client.connect()
print("Connected to broker")
client.subscribe(TOPIC)
print("Subscribed to:", TOPIC)
# Main loop
while True:
    client.check_msg()   # non-blocking
    time.sleep(0.1)
    