# udp_receiver_sensors_display.py
import socket, ustruct
import network
import time
from oled_tools import *

SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
UDP_PORT = 5005
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
sock.bind(("", UDP_PORT))   # Listen on all interfaces
print("Listening for UDP packets...")
while True:
    data, addr = sock.recvfrom(1024)
    count,lumi,temp,humi =ustruct.unpack('i3f',data)
    print("Received from", addr, ":", count, lumi, temp, humi)
    sensors_display(lumi,temp,humi,5)
    