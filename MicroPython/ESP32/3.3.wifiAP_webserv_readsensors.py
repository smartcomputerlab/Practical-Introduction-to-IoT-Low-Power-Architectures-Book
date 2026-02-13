# esp32_ap_web_sensors.py
import network
import socket
import time
from machine import Pin
from v2_sensors  import *
# LED (optional) to indicate server is running
led = Pin(25, Pin.OUT)
led.off()
# Create Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="ESP32-SENSORS", password="")

while not ap.active():
    time.sleep(1)
print("AP started")
print("Connect to WiFi: ESP32-SENSORS")
print("Open browser at: http://192.168.4.1")
# HTML template (will insert sensor values dynamically)
html_template = """<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Sensor Readings</title>
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: Arial;
            background-color: #e6f7ff;
        }}
        .container {{
            text-align: center;
            padding: 20px;
            border-radius: 12px;
            background-color: #ffffff;
            box-shadow: 0 0 10px #888888;
        }}
        h1 {{ color: #333; }}
        p {{ font-size: 24px; margin: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>ESP32 Sensor Readings</h1>
        <p>Luminosity: {lumi} lx</p>
        <p>Temperature: {temp} °C</p>
        <p>Humidity: {humi} %</p>
        <p>Refresh page to update values</p>
    </div>
</body>
</html>
"""
# Create socket server
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
        print("Request from:", addr)
        # Read sensors
        try:
            lumi, temp, humi = sensors(sda=21, scl=22)
            # Round values for display
            lumi = round(lumi, 2)
            temp = round(temp, 2)
            humi = round(humi, 2)
        except Exception as e:
            print("Sensor read error:", e)
            lumi, temp, humi = 0, 0, 0
        # Fill HTML template
        html = html_template.format(lumi=lumi, temp=temp, humi=humi)
        # Send HTTP response
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