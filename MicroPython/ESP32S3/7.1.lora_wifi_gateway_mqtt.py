import machine, network, socket, time, ustruct, random, ubinascii
from umqtt.simple import MQTTClient
from lora_init import *
from aes_tools import *
from oled_tools import *
aes_key="smartcomputerlab"
# WiFi credentials
SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
# MQTT broker details
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = b"esp32/test/topic"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Unique client ID

print("LoRa RX ready")
sx=lora_init()
rf_rx();time.sleep(0.2)
wlan = network.WLAN(network.STA_IF)
wlan.active(True); wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep(1)
print("WiFi connected:", wlan.ifconfig())
chan=1234; cycle=10; delta=0.05;thold=29.25
while True:
    print("waiting on recv");message_display("waiting","       for","       data",0)
    data, state = sx.recv(timeout_en=True, timeout_ms=64000); rf_tx()
    if state == 0 and data:
        print("RX:", data); rssi=sx.rssi()
        print("RSSI:", rssi, "dBm")
        payload=aes_decrypt(data[:-1],aes_key)
        print("RX:", payload)
        chan, wkey, lumi, temp, humi = ustruct.unpack('i16s3f', payload)
        print(chan, wkey, lumi, temp, humi)
        sensors_display(lumi,temp,humi,0)
        time.sleep(1)
        sx.setOutputPower(-5);time.sleep(0.2)
        cycle = random.randint(6, 14)
        ack=ustruct.pack('2i2f',chan,cycle,delta,thold)  # chan, cycle, delta, thold
        enc_ack=aes_encrypt(ack,aes_key); pos=16
        enc_ack = enc_ack[:pos] + b'\x00' + enc_ack[pos:]
        sx.send(enc_ack);time.sleep(0.2)
        print("control cycle,delta,thold:"); print(cycle,delta,thold)
        rf_rx();time.sleep(0.1)
        # Test DNS
        print("DNS:", socket.getaddrinfo(MQTT_BROKER, 1883))
        try:
            while not wlan.isconnected():
                time.sleep(1)
            message_display("sending"," data to ","mqtt broker",0)
            client = MQTTClient(CLIENT_ID, MQTT_BROKER)
            client.connect()
            print("MQTT connected")
            if lumi is not None and temp is not None and humi is not None:
                message = "{:.2f},{:.2f},{:.2f}".format(lumi,temp,humi)
                client.publish(wkey, str(message))
                print("Published:", wkey, message)
                message_display("data"," published ","to mqtt broker",3)
            else:
                print("Failed to publish sensor data.")
                message_display("failed"," to publish ","to mqtt broker",3)
            
            client.disconnect()
        except Exception as e:
            print("MQTT error:", e)
    else:
        print("recv timeout");

