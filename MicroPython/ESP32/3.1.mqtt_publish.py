import network, socket, time
from v2_sensors import *
from umqtt.simple import MQTTClient
# WiFi credentials
SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
# MQTT broker details
MQTT_BROKER = "test.mosquitto.org"
CLIENT_ID = "esp32_test_pub"
MQTT_TOPIC = b"esp32/test/topic"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep(1)

print("WiFi connected:", wlan.ifconfig())
# Test DNS
try:
    print("DNS:", socket.getaddrinfo(MQTT_BROKER, 1883))
except Exception as e:
    print("DNS failed:", e)

try:
    client = MQTTClient(CLIENT_ID, MQTT_BROKER)
    client.connect()
    print("MQTT connected")
    lumi, temp, humi = sensors(sda=21, scl=22)
    if lumi is not None and temp is not None and humi is not None:
        message = "{:.2f},{:.2f},{:.2f}".format(lumi,temp,humi)
        client.publish(MQTT_TOPIC, str(message))
        print("Published:", message)
    else:
        print("Failed to publish sensor data.")
    
    client.disconnect()
except Exception as e:
    print("MQTT error:", e)

# Run the main function
main()
