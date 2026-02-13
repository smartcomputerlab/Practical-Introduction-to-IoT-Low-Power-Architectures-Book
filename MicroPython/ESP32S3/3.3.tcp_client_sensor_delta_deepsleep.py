import network, socket, ustruct, time
from machine import RTC, deepsleep
from sensors import *
from lora_off import *
SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
SERVER_IP = "192.168.1.17"   # IP of the receiver
PORT = 5056
MESSAGE = "Hello from ESP32!"
delta=0.1
# Connect to WiFi
Pin(36, Pin.OUT).value(0); time.sleep(0.5)
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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, PORT))
    print("Connected to server")
    # preparing data : buffer with bytes
    data=ustruct.pack('i3f',5,lumi,temp,humi)
    s.send(data); time.sleep(0.5); s.close();
    wlan.disconnect(); wlan.active(False); time.sleep(0.2);gc.collect()
    
time.sleep(5); lora_off()
Pin(36, Pin.OUT).value(1); sleep(0.5)   # vext offlora_off()
deepsleep(10*1000)
