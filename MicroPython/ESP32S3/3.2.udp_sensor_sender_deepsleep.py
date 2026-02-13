import network, socket, ustruct, time
from machine import deepsleep
from sensors import *
from lora_off import *
SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
UDP_IP = "192.168.1.21"   # IP of the receiver
UDP_PORT = 5005
MESSAGE = "Hello from ESP32!"
# Connect to WiFi
Pin(36, Pin.OUT).value(0); time.sleep(0.5)
lumi, temp, humi = sensors(sda=6, scl=7)
print(lumi,temp,humi)
# preparing data : buffer with bytes
data=ustruct.pack('i3f',5,lumi,temp,humi)
print("Sensor data:", data)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID,PASSWORD)
while not wlan.isconnected():
    print("Connecting to WiFi...")
    time.sleep(0.5)
print("Connected, IP:", wlan.ifconfig()[0])
# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(data, (UDP_IP, UDP_PORT))
wlan.disconnect(); wlan.active(False); time.sleep(0.2);gc.collect()
time.sleep(5); lora_off()
Pin(36, Pin.OUT).value(1); sleep(0.5)   # vext offlora_off()
deepsleep(10*1000)
