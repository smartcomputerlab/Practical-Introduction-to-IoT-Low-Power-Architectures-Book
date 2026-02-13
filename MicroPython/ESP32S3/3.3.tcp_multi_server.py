import socket, network, time, ustruct
SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
PORT = 5056
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
s.listen(4)
print("TCP server listening on port", PORT)
while True:
    conn, addr = s.accept()
    print("Client connected from:", addr)
    data = conn.recv(1024)
    if not data:
        break
    count,lumi,temp,humi =ustruct.unpack('i3f',data)
    print("Received from", addr, ":", count, lumi, temp, humi)
    conn.send(b"ACK\n")   # Optional reply
    conn.close()
s.close()
