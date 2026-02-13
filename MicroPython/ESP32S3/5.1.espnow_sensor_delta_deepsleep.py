import network, espnow, time, ustruct
from machine import RTC, Pin, deepsleep
from sensors import *
from lora_off import *
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
    sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
    sta.active(True)
    #sta.config(txpower=5.0)
    sta.config(channel=1) # must be provide from gateway channel
    sta.disconnect()      
    # Initialize ESP-NOW
    esp = espnow.ESPNow()
    esp.active(True)
    print("now active")
    #peer= b'\x54\x32\x04\x0B\x3C\xF8'  # Replace with receiver's MAC address
    peer= b'\xFF\xFF\xFF\xFF\xFF\xFF'  #  broadcast MAC address
    esp.add_peer(peer)
    lumi, temp, humi = sensors(sda=6, scl=7)
    print("Luminosity:", lumi, "lux")
    print("Temperature:", temp, "C")
    print("Humidity:", humi, "%")
    data=ustruct.pack('i16s3f',1254,'YOX31M0EDKO0JATK',lumi,temp,humi)
    print(str(data))
    esp.send(peer,data); sleep(0.1); sta.active(False)
    
    
time.sleep(5); lora_off()
Pin(36, Pin.OUT).value(1); sleep(0.5)   # vext offlora_off()
deepsleep(10*1000)
