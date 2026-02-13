import time
from lora_init import *

print("LoRa RX ready")
sx=lora_init()
rf_rx()
i = 0
while True:
    data, state = sx.recv(timeout_en=True, timeout_ms=5000)
    if state == 0 and data:
        print("RX:", data)
        print("RSSI:", sx.rssi(), "dBm")
    i += 1
    time.sleep(2)
    sx.setOutputPower(22);time.sleep(0.2)
    sx.send(b"Hello %d" % i);time.sleep(0.2)
    time.sleep(0.1)
    
    