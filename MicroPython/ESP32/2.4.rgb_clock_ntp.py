import time
import ntptime
from rgb.clock import *
from wifi_tools import *
# Replace with your Wi-Fi credentials
SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
# Connect to WiFi
if connect_WiFi(SSID, PASSWORD):
    print("Connected to WiFi:", SSID)
else:
    print("Failed to connect to WiFi:", SSID)
    # If cannot connect to WiFi, can't access NTP. Stop here.
    while True:
        pass
# Synchronize time with NTP server once
try:
    ntptime.settime()
    print("Time synchronized with NTP server.")
except OSError as e:
    print("Failed to synchronize time:", e)

# Now enter an infinite loop where we print the current time every 10 seconds
clock = RGBClock(pin=18)   # GPI18 for LED ring
while True:
    current_time = time.localtime()
    hour = current_time[3]
    minute = current_time[4]
    second = current_time[5]
    print("Current UTC Time: {:02d}:{:02d}:{:02d}".format(hour, minute, second))
    clock.show_time(hour, minute, second)
    time.sleep(1)
    