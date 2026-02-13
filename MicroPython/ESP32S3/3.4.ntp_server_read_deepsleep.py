import time, network, ntptime
from machine import RTC, deepsleep
from lora_off import *
# Replace with your Wi-Fi credentials
SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"

Pin(36, Pin.OUT).value(0); time.sleep(0.5)
rtc = machine.RTC()
# # Read the current memory contents
rtc_mem = rtc.memory()
if len(rtc_mem) == 0:
    # If empty, this is the first cycle
    count = 0.0
else:
    # Convert stored bytes to integer
    count = float(rtc_mem.decode())
if count==0.0:    
# Connect to WiFi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID,PASSWORD)
    while not wlan.isconnected():
        print("Connecting to WiFi...")
        time.sleep(0.5)
    count+=1.0;rtc.memory(str(count).encode())
    # Synchronize time with NTP server once
    try:
        ntptime.settime()
        print("Time synchronized with NTP server.")
    except OSError as e:
        print("Failed to synchronize time:", e)
# Now enter an infinite loop where we print the current time every 10 seconds
current_time = time.localtime()
hour = current_time[3]
minute = current_time[4]
second = current_time[5]
print("Current UTC Time: {:02d}:{:02d}:{:02d}".format(hour, minute, second))
# Wait 10 seconds before the next print
time.sleep(5); lora_off()
Pin(36, Pin.OUT).value(1); sleep(0.5)   # vext offlora_off()
deepsleep(10*1000)
