from machine import Pin, I2C, SPI
import machine,ustruct, time, ubinascii
from lora_init import *
from oled_tools import *
from aes_tools import *
from wifi_tools import *
from umqtt.simple import MQTTClient
# WiFi credentials
SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
# MQTT broker details
# MQTT broker details
MQTT_BROKER = "test.mosquitto.org"
CLIENT_ID = "esp32_test_pub"
#MQTT_TOPIC = b"esp32/test/topic"
MQTT_PORT = 1883
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Unique client ID

# Initialize MQTT client
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
topic = ""
AES_KEY = b'smartcomputerlab'  # Replace with your actual 16-byte AES key
lora  = lora_init()
def connect_mqtt():
    """Connect to the MQTT broker."""
    try:
        client.connect()
        print("Connected to MQTT broker.")
    except Exception as e:
        print("Failed to connect to MQTT broker:", e)

def disconnect_mqtt():
    client.disconnect()
    print("Disconnected from MQTT broker.")
    
def publish_sensor_data(lumi, temp, humi ):
    """Publish sensor data to MQTT broker."""
    global topic
    if lumi is not None and temp is not None and humi is not None:
        message = {
            "lumi": lumi,
            "temp": temp,
            "humi": humi
        }
        client.publish(topic.decode(), str(message))
        print("Topic:", topic.decode());print("Published:", message)
    else:
        print("Failed to publish sensor data.")
    
# --- Receive LoRa Packet ---
def onReceive(lora ,enc_payload):
    global topic
    if len(enc_payload)==32:
        rssi = lora.packetRssi()
        payload=aes_decrypt(enc_payload,AES_KEY)
        chan, topic, lumi, temp, humi = ustruct.unpack('i16s3f', payload)
        print("Received LoRa packet RSSI:"+str(rssi)); print(chan,topic,lumi,temp,humi)
        sensors_display(lumi,temp,humi,0); 
        ack=ustruct.pack('2i2f',chan,10,0.1,32.9)  # chan, cycle, delta, thold
        enc_ack=aes_encrypt(ack,AES_KEY)
        lora.println(enc_ack)  # sending ACK packet 
        try:
            # Attempt MQTT sequence
            connect_mqtt()
            publish_sensor_data(lumi, temp, humi)
            disconnect_mqtt()
        except Exception as e:
            # Handle any errors
            print("MQTT error:", e)
            try:
                disconnect_mqtt()  # Ensure we disconnect if something went wrong
            except:
                pass
        lora.receive()

def main():
    lora.onReceive(onReceive)
    lora.receive()
    if connect_WiFi(SSID,PASSWORD):
        print("WiFi connected")
    while True:
        time.sleep(2)
        print("in the loop")
        
main()

