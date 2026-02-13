# udp_sender.py
import socket, ustruct
import time
import network
from v2_sensors import *

SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
UDP_IP = "192.168.1.21"   # IP of the receiver
UDP_PORT = 5005
MESSAGE = "Hello from ESP32!"
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
count = 0
while True:
    count=count+1
    
    lumi,temp,humi=sensors(sda=21, scl=22)
    print(lumi,temp,humi)
    # preparing data : buffer with bytes
    data=ustruct.pack('i3f',count,lumi,temp,humi)
    print("Sending:", data)
    sock.sendto(data, (UDP_IP, UDP_PORT))
    time.sleep(2)
    