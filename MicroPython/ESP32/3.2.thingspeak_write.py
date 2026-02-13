# thingspeak_send.py
import network, time
import urequests
from v2_sensors import *

# WiFi credentials
SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
WRITE_API_KEY = "YOX31M0EDKO0JATK"
URL = "http://api.thingspeak.com/update"
# WiFi connect
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep(1)

print("WiFi connected")

while True:
    lumi, temp, humi = sensors(sda=21, scl=22)
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
        r.close()
    except Exception as e:
        print("Send error:", e)

    time.sleep(20)   # ThingSpeak limit
    