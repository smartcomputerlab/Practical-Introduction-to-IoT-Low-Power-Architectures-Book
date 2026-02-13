# udp_sender.py
import socket
import time
import network

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

while True:
    print("Sending:", MESSAGE)
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
    time.sleep(2)
    