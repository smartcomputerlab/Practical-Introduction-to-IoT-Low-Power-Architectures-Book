# tcp_client.py
import socket
import network
import time

SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
SERVER_IP = "192.168.1.21"   # <-- server ESP32 IP
PORT = 5000
# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep(1)

print("Connected to WiFi")
# Create socket and connect
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_IP, PORT))
print("Connected to server")
counter = 0
while True:
    msg = "Hello from ESP32! {}\n".format(counter)
    s.send(msg.encode())
    print("Sent:", msg.strip())
    # Optional receive ACK
    data = s.recv(1024)
    print("Server says:", data.decode().strip())
    counter += 1
    