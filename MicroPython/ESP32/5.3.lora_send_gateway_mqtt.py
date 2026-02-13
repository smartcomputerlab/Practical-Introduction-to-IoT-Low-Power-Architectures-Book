import time, ustruct
from machine import I2C, Pin, deepsleep
from sensors import sensors
from lora_init import lora_init
from aes_tools import *
ACK_wait_time = 10; SEND_wait_time = 10
AES_KEY = b'smartcomputerlab'  # Replace with your actual 16-byte AES key
WRITE_API_KEY = "YOX31M0EDKO0JATK"  # or MQTT topic

lora = lora_init()

def onReceive(lora,payload):
    #print("Waiting for LoRa packets...")
    if len(payload)==16:
        ack=aes_decrypt(payload,AES_KEY)
        rchan, cycle, delta, thold = ustruct.unpack('2i2f', ack)
        print("ACK:",rchan,cycle,delta,thold)   #, payload.decode())
# Function to send sensor data over LoRa
def send_lora_data(l,t,h):
    try:
        # Create the message with temperature, humidity, and luminosity
        message = f"L:{l:.2f},T:{t:.2f},H:{h:.2f}"
        print("Sending LoRa packet:", message)
        # prepare data packet with bytes
        data = ustruct.pack('i16s3f', 1254,WRITE_API_KEY,l,t,h)
        enc_data=aes_encrypt(data,AES_KEY)
        lora.println(enc_data)
        print("LoRa packet sent successfully.")
    except Exception as e:
        print("Failed to send LoRa packet:", e)
                                 
def main():
    lora.onReceive(onReceive)
    lora.receive()
    while True:
        lumi, temp, humi = sensors(sda=21, scl=22)
        print("Luminosity:", lumi, "lux")
        print("Temperature:", temp, "C")
        print("Humidity:", humi, "%"); time.sleep(SEND_wait_time)
        # Send sensor data over LoRa
        send_lora_data(lumi, temp, humi)
        lora.receive()
        time.sleep(ACK_wait_time)           # waiting for ACK frame
# Run the main program
main()
