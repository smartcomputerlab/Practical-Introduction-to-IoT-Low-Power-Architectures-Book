# thingspeak_send.py
import network, time,  urequests
from machine import RTC, deepsleep
from sensors import *
from lora_off import *

# WiFi credentials
SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
WRITE_API_KEY = "YOX31M0EDKO0JATK"
URL = "http://api.thingspeak.com/update"

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
    # WiFi connect
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
    print("WiFi connected")
    lumi, temp, humi = sensors(sda=6, scl=7)
    # Limit to 2 decimals
    lumi = round(lumi, 2)
    temp = round(temp, 2)
    humi = round(humi, 2)
    payload = {
        "api_key": WRITE_API_KEY,
        "field1": lumi,
        "field2": temp,
        "field3": humi
    }
    try:
        r = urequests.post(URL, json=payload)
        print("Sent:", payload, "Response:", r.text)
        r.close();  
    except Exception as e:
        print("Send error:", e)
    wlan.active(False)
    
time.sleep(5); lora_off()
Pin(36, Pin.OUT).value(1); sleep(0.5)   # vext offlora_off()
deepsleep(20*1000)
