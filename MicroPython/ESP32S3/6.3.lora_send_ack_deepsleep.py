import time
from machine import deepsleep, Pin
from lora_init import *

led=Pin(35, Pin.OUT)
print("LoRa ready")
i = 0
Pin(36, Pin.OUT).value(0);time.sleep(0.2)
led.value(1)
sx=lora_init()
rf_tx();time.sleep(0.2)
sx.setOutputPower(22);time.sleep(0.2)
sx.send(b"Much, much longer message: Hello, how are you today %d" % i);time.sleep(0.2)
rf_rx()
print("TX", i)
i += 1
data, state = sx.recv(timeout_en=True, timeout_ms=5000)
if state == 0 and data:
    print("RX:", data)
    print("RSSI:", sx.rssi(), "dBm")
time.sleep(5); led.value(0)
Pin(36, Pin.OUT).value(1);time.sleep(0.2)
sx.sleep();time.sleep(0.2)
deepsleep(10*1000)
