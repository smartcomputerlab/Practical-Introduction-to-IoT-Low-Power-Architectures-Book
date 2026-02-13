from machine import Pin, I2C, SPI
import ustruct, time
from lora_init import *
from v2_display_tools import *
lora = lora_init()
# --- Receive LoRa Packet ---
def onReceive(lora,payload):
    rssi = lora.packetRssi()
    chan, wkey, lumi, temp, humi = ustruct.unpack('i16s3f', payload)
    print("Received LoRa packet RSSI:"+str(rssi)); print(chan,wkey,lumi,temp,humi)
    sensors_display(lumi,temp,humi,0)
    lora.println("ACK_packet")  # sending ACK packet
    lora.receive()

def main():
    lora.onReceive(onReceive)
    lora.receive()
    while True:
        time.sleep(2)
        print("in the loop")
        
main()

