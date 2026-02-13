import time, ustruct
from machine import deepsleep, Pin, RTC
from lora_init import *
from aes_tools import *
from sensors import *
from oled_tools import *
aes_key="smartcomputerlab"
delta=0.1
led=Pin(35, Pin.OUT);print("LoRa ready")
Pin(36, Pin.OUT).value(0);time.sleep(0.2)
led.value(1)
rtc = RTC()
rtc_mem = rtc.memory()
if len(rtc_mem) == 0:
    stemp = 25.0
else:
    stemp = float(rtc_mem.decode())
    
lumi, temp, humi = sensors(sda=6, scl=7); print(lumi,temp,humi)
sx=lora_init()
if abs(stemp-temp)> delta:
    rtc.memory(str(temp).encode())
    data=ustruct.pack('i16s3f',1254,'YOX31M0EDKO0JATK',lumi,temp,humi)
    enc_data=aes_encrypt(data,aes_key); pos=32
    enc_data = enc_data[:pos] + b'\x00' + enc_data[pos:]  # must end with b'\x00
    print(enc_data)
    rf_tx();time.sleep(0.2)
    sx.setOutputPower(-5);time.sleep(0.2)
    sx.send(enc_data);time.sleep(0.2)
    rf_rx()
    enc_ack, state = sx.recv(timeout_en=True, timeout_ms=10000) # wait for full transaction time
    if state == 0 and enc_ack:
        ack=aes_decrypt(enc_ack[:-1],aes_key)
        rchan, cycle, delta, thold = ustruct.unpack('2i2f', ack)
        print("ACK:",rchan,cycle,delta,thold)   #, payload.decode())
        control_display(rchan,cycle,delta,thold,0)
        print("RSSI:", sx.rssi(), "dBm")
else:
    print("data not sent")
               
time.sleep(5); led.value(0)
Pin(36, Pin.OUT).value(1);time.sleep(0.2)
sx.sleep();time.sleep(0.2)
deepsleep(10*1000)
