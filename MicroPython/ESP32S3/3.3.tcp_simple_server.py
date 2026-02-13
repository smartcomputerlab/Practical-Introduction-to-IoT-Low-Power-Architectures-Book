# tcp_server.py
import socket
import network
import time
SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
PORT = 5000
# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep(1)
print("Connected to WiFi")
print("Server IP:", wlan.ifconfig()[0])
# Create TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', PORT))        # '' means all interfaces
s.listen(1)
print("TCP server listening on port", PORT)
conn, addr = s.accept()
print("Client connected from:", addr)
while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Received:", data.decode())
    conn.send(b"ACK\n")   # Optional reply

conn.close()
s.close()
