import time, ustruct
from machine import deepsleep, Pin
from lora_init import *
from aes_tools import *
from sensors import *
aes_key="smartcomputerlab"

led=Pin(35, Pin.OUT)
print("LoRa ready")
i = 0
Pin(36, Pin.OUT).value(0);time.sleep(0.2)
led.value(1)
lumi, temp, humi = sensors(sda=6, scl=7)
data=ustruct.pack('i16s3f',1254,'YOX31M0EDKO0JATK',lumi,temp,humi)
enc_data=aes_encrypt(data,aes_key); pos=32
enc_data = enc_data[:pos] + b'\x00' + enc_data[pos:]  # must end with b'\x00
print(enc_data)
sx=lora_init()
rf_tx();time.sleep(0.2)
sx.setOutputPower(-5);time.sleep(0.2)
sx.send(enc_data);time.sleep(0.2)
rf_rx()
print("TX", i)
i += 1
data, state = sx.recv(timeout_en=True, timeout_ms=3500)
if state == 0 and data:
    print("RX:", data)
    print("RSSI:", sx.rssi(), "dBm")
time.sleep(5); led.value(0)
Pin(36, Pin.OUT).value(1);time.sleep(0.2)
sx.sleep();time.sleep(0.2)
deepsleep(10*1000)
