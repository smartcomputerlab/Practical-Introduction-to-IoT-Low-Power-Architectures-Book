import network, time, ustruct, random, urequests
from lora_init import *
from aes_tools import *
from oled_tools import *
aes_key="smartcomputerlab"
# WiFi credentials
SSID = "Livebox-2E80"
PASSWORD = "DTPbgKhpV6M3c4mE6s"
WRITE_API_KEY = "YOX31M0EDKO0JATK"  # to be replaced with wkey sent by terminal
URL = "http://api.thingspeak.com/update"

print("LoRa RX ready")
sx=lora_init()
rf_rx();time.sleep(0.2)
chan=1234; cycle=10; delta=0.05;thold=29.25
while True:
    print("waiting on recv");message_display("waiting","       for","       data",0)
    data, state = sx.recv(timeout_en=True, timeout_ms=64000); rf_tx()
    if state == 0 and data:
        print("RX:", data); rssi=sx.rssi()
        print("RSSI:", rssi, "dBm")
        payload=aes_decrypt(data[:-1],aes_key)
        print("RX:", payload)
        chan, wkey, lumi, temp, humi = ustruct.unpack('i16s3f', payload)
        print(chan, wkey, lumi, temp, humi)
        sensors_display(lumi,temp,humi,0)
        time.sleep(1)
        sx.setOutputPower(-5);time.sleep(0.2)
        cycle = random.randint(6, 14);time.sleep(0.2)
        ack=ustruct.pack('2i2f',chan,cycle,delta,thold)  # chan, cycle, delta, thold
        enc_ack=aes_encrypt(ack,aes_key); pos=16
        enc_ack = enc_ack[:pos] + b'\x00' + enc_ack[pos:]
        sx.send(enc_ack);time.sleep(0.2)
        print("control cycle,delta,thold:"); print(cycle,delta,thold)
        rf_rx();time.sleep(0.1)
         # WiFi connect
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True); wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
        print("WiFi connected")
        # Limit to 2 decimals
        lumi = round(lumi, 2); temp = round(temp, 2)
        humi = round(humi, 2); rssi = round(rssi, 2)
        payload = {
            "api_key":wkey,"field1":lumi,"field2":temp,"field3":humi,"field4":rssi
        }
        try:
            message_display("sending","       to","ThingSpeak",0)
            r = urequests.post(URL, json=payload)
            print("Sent:", payload, "Response:", r.text)
            r.close();  
        except Exception as e:
            print("Send error:", e)
        wlan.active(False)
    else:
        print("recv timeout");
        