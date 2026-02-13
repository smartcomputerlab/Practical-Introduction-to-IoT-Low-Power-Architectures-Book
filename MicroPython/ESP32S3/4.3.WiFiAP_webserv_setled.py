# esp32_ap_web_led_fixed.py
import network
import socket
from machine import Pin
import time
# LED pin (GPI35 on V4)
led = Pin(35, Pin.OUT)
led.off()
# Create Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="ESP32-LED", password="12345678")
while not ap.active():
    time.sleep(1)
print("AP started"); print("Connect to WiFi: ESP32-LED")
print("Open browser at: http://192.168.4.1")
# HTML page
html = """<!DOCTYPE html>
<html>
<head>
    <title>ESP32 LED Control</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: Arial;
            background-color: #f2f2f2;
        }
        .container {
            text-align: center;
        }
        button {
            width: 200px;
            height: 80px;
            font-size: 24px;
            margin: 15px;
            border-radius: 12px;
            border: none;
        }
        .on { background-color: #4CAF50; color: white; }
        .off { background-color: #f44336; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h1>ESP32 LED Control</h1>
        <a href="/on"><button class="on">LED ON</button></a><br>
        <a href="/off"><button class="off">LED OFF</button></a>
    </div>
</body>
</html>
"""
# Create socket
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
print("Web server running...")
while True:
    try:
        conn, addr = s.accept()
        conn.settimeout(5)
        request = conn.recv(1024).decode()
        print("Request:", request)
        if "/on" in request:
            led.on()
            print("LED ON")
        elif "/off" in request:
            led.off()
            print("LED OFF")
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "Connection: close\r\n\r\n"
            + html
        )
        conn.sendall(response)
    except Exception as e:
        print("Connection error:", e)
    finally:
        try:
            conn.close()
        except:
            pass
        