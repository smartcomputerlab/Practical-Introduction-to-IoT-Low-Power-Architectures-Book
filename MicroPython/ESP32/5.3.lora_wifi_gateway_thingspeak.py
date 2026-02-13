from machine import Pin, I2C, SPI
import machine,ustruct, time, ubinascii
from lora_init import *
from v2_display_tools import *
from aes_tools import *
from wifi_tools import *
import urequests
# WiFi credentials
SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
URL = "http://api.thingspeak.com/update"
WRITE_API_KEY = "YOX31M0EDKO0JATK"  # not used !

AES_KEY = b'smartcomputerlab'  # Replace with your actual 16-byte AES key
lora  = lora_init()
# WiFi connect
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep(1)
print("WiFi connected")
# --- Receive LoRa Packet ---
def onReceive(lora ,enc_payload):
    if len(enc_payload)==32:
        rssi = lora.packetRssi()
        payload=aes_decrypt(enc_payload,AES_KEY)
        chan, wkey, lumi, temp, humi = ustruct.unpack('i16s3f', payload)
        print("Received LoRa packet RSSI:"+str(rssi)); print(chan,wkey,lumi,temp,humi)
        sensors_display(lumi,temp,humi,0)
        ack=ustruct.pack('2i2f',chan,10,0.1,32.9)  # chan, cycle, delta, thold
        enc_ack=aes_encrypt(ack,AES_KEY)
        lora.println(enc_ack)  # sending ACK packet
        payload = {
            "api_key": wkey,      # WRITE_API_KEY sent by the terminal
            "field1": lumi,
            "field2": temp,
            "field3": humi,
            "field4": rssi
        }
        try:
            r = urequests.post(URL, json=payload)
            print("Sent:", payload, "Response:", r.text)
            r.close()
        except Exception as e:
             print("Send error:", e)
        time.sleep(18)
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
