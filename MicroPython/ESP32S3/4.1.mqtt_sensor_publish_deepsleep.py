import network, socket, ustruct, time
from machine import RTC, deepsleep
from sensors import *
from umqtt.simple import MQTTClient
from lora_off import *
# WiFi credentials
SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
# MQTT broker details
MQTT_BROKER = "test.mosquitto.org"
CLIENT_ID = "esp32_test_pub"
MQTT_TOPIC = b"esp32/test/topic"
delta=0.1
# Connect to WiFi
Pin(36, Pin.OUT).value(0); time.sleep(0.5)
rtc = machine.RTC()
# # Read the current memory contents
rtc_mem = rtc.memory()
if len(rtc_mem) == 0:
    # If empty, this is the first cycle
    stemp = 25.0
else:
    # Convert stored bytes to integer
    stemp = float(rtc_mem.decode())
    
lumi, temp, humi = sensors(sda=6, scl=7)
print(lumi,temp,humi)
if abs(stemp-temp)> delta:
    rtc.memory(str(temp).encode())
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
        lumi, temp, humi = sensors(sda=6, scl=7)
        if lumi is not None and temp is not None and humi is not None:
            message = "{:.2f},{:.2f},{:.2f}".format(lumi,temp,humi)
            client.publish(MQTT_TOPIC, str(message))
            print("Published:", message)
        else:
            print("Failed to publish sensor data.")
        
        client.disconnect(); wlan.active(False)
    except Exception as e:
        print("MQTT error:", e)
    
time.sleep(5); lora_off()
Pin(36, Pin.OUT).value(1); sleep(0.5)   # vext offlora_off()
deepsleep(10*1000)
