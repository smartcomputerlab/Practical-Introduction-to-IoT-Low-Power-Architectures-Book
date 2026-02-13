import time, ustruct
from machine import I2C, Pin, deepsleep
from sensors import sensors
from lora_init import lora_init
ACK_wait_time = 5 
# Initialize LoRa communication
lora = lora_init()

def onReceive(lora_modem,payload):
    #print("Waiting for LoRa packets...")
    ACK=payload.decode()
    print("Received LoRa packet:"+str(ACK))   #, payload.decode())
    lora.receive()

# Function to send sensor data over LoRa
def send_lora_data(l, t, h):
    try:
        # Create the message with temperature, humidity, and luminosity
        message = f"L:{l:.2f},T:{t:.2f},H:{h:.2f}"
        print("Sending LoRa packet:", message)
        # prepare data packet with bytes
        data = ustruct.pack('i16s3f', 1254,'smartcomputerlab',l,t,h)
        # Convert message to bytes
        # lora.println(bytes(message, 'utf-8'))
        lora.println(data)
        print("LoRa packet sent successfully.")
    except Exception as e:
        print("Failed to send LoRa packet:", e)
                                 
def main():
    lora.onReceive(onReceive)
    lora.receive()
    while True:
        # Capture sensor data
        lumi, temp, humi = sensors(sda=21, scl=22)
        print("Luminosity:", lumi, "lux")
        print("Temperature:", temp, "C")
        print("Humidity:", humi, "%")
        # Send sensor data over LoRa
        send_lora_data(lumi, temp, humi)
        lora.receive()
        time.sleep(ACK_wait_time)           # waiting for ACK frame
        
        