# udp_send_deepsleep.py
import esp32, network, socket, ustruct, time
from machine import RTC, deepsleep
from sensors import *
from lora_off import *
SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
UDP_IP = "192.168.1.21"   # IP of the receiver
UDP_PORT = 5005
MESSAGE = "Hello from ESP32!"
delta=0.1

WAKE_PIN = 4
# Connect to WiFi
Pin(36, Pin.OUT).value(0); time.sleep(0.5)
wake = Pin(WAKE_PIN, Pin.IN, Pin.PULL_DOWN)
esp32.wake_on_ext0(pin=wake, level=1)  # wake on HIGH

rtc = machine.RTC()
# # Read the current memory contents
rtc_mem = rtc.memory()
if len(rtc_mem) == 0:
    # If empty, this is the first cycle
    stemp = 25.0
else:
    # Convert stored bytes to integer
    stemp = float(rtc_mem.decode())
    
lumi, temp, humi = sensors(sda=6, scl=7)
print(lumi,temp,humi)

if abs(stemp-temp)> delta:
    rtc.memory(str(temp).encode())
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID,PASSWORD)
    while not wlan.isconnected():
        print("Connecting to WiFi...")
        time.sleep(0.5)
    print("Connected, IP:", wlan.ifconfig()[0])
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # preparing data : buffer with bytes
    data=ustruct.pack('i3f',5,lumi,temp,humi)
    sock.sendto(data, (UDP_IP, UDP_PORT))
    wlan.disconnect(); wlan.active(False); time.sleep(0.2);gc.collect()
    
time.sleep(5); lora_off()  # additional time to enable STOP
Pin(36, Pin.OUT).value(1); sleep(0.5)   # vext offlora_off()
deepsleep()  # waiting for interruption signal
