# thingspeak_read.py
import network, time, urequests, ujson
from v2_display_tools import * 
# WiFi credentials
SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
WRITE_API_KEY = "YOX31M0EDKO0JATK"
CHANNEL_ID = "1538804"
READ_API_KEY = "20E9AQVFW7Z6XXOM"

URL = "http://api.thingspeak.com/channels/{}/feeds/last.json?api_key={}".format(
    CHANNEL_ID, READ_API_KEY
)
# WiFi connect
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep(1)

print("WiFi connected")
while True:
    try:
        r = urequests.get(URL)
        data = r.json()
        r.close()
        lumi = data["field1"]
        temp = data["field2"]
        humi = data["field3"]
        print("Luminosity:", lumi)
        print("Temperature:", temp)
        print("Humidity:", humi)
        print("------------------")
        sensors_display_str(lumi, temp, humi, 5)

    except Exception as e:
        print("Read error:", e)
    time.sleep(10)
    