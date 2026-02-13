import network, time, espnow, ustruct, urequests
from machine import Pin

def wifi_reset():   # Reset wifi to AP_IF off, STA_IF on and disconnected
  sta = network.WLAN(network.STA_IF); sta.active(False)
  ap = network.WLAN(network.AP_IF); ap.active(False)
  sta.active(True)
  while not sta.active():
      time.sleep(0.1)
  sta.disconnect()   # For ESP8266
  while sta.isconnected():
      time.sleep(0.1)
  return sta, ap

# ThingSpeak API details
WRITE_API_KEY = "YOX31M0EDKO0JATK"
URL = "http://api.thingspeak.com/update"

# Function to send data to ThingSpeak
def send_data_to_thingspeak(wkey, lumi, temp, humi):
    payload = {
    "api_key": wkey,
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

sta, ap = wifi_reset()  # Reset wifi to AP off, STA on and disconnected
sta.connect('Livebox-2E80', 'DTPbgKhpV6M3c4mE6s')
while not sta.isconnected():  # Wait until connected...
    time.sleep(0.1)
sta.config(pm=sta.PM_NONE)  # ..then disable power saving
print(sta.ifconfig())
# Print the wifi channel used AFTER finished connecting to access point
print("Proxy running on channel:", sta.config("channel"))
e = espnow.ESPNow(); e.active(True)
for peer, msg in e:
        while True:
            host, data = e.recv()
            if data:
                chan, wkey, lumi, temp, humi = ustruct.unpack('i16s3f', data)   # wkey may be topic
                print(host)
                for_wkey="{:s}".format(wkey)
                print("wkey:"+str(for_wkey)+" lumi:"+str(lumi)+" temp:"+str(temp)+" humi:"+str(humi))
                msg= "lumi:"+str(lumi)+"; temp:"+str(temp)+"; humi:"+str(humi)
                # Send data to ThingSpeak
                send_data_to_thingspeak(for_wkey,lumi, temp, humi)
                