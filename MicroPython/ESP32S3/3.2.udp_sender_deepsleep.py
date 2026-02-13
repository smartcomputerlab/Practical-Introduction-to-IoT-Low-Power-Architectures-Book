# udp_sender.py
import machine, time
from machine import RTC, deepsleep, SPI, Pin
import socket, network, gc, esp32
from lora_off import *
SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
UDP_IP = "192.168.1.21"   # IP of the receiver
UDP_PORT = 5005
MESSAGE = "Hello from ESP32!"
Pin(36, Pin.OUT).value(0); sleep(0.5)
# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    print("Connecting to WiFi...")
    time.sleep(0.5)

print("Connected, IP:", wlan.ifconfig()[0])
# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Sending:", MESSAGE)
sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT));time.sleep(0.5)
wlan.disconnect(); wlan.active(False); time.sleep(0.2);gc.collect()
time.sleep(5)
lora_off()           # must be used to freeze the sx1276 modem power consumption
Pin(36, Pin.OUT).value(1); sleep(0.5)   # vext offlora_off()
deepsleep(10*1000)
