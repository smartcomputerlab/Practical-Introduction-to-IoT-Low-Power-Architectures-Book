import time
from lora_init import *
print("LoRa RX ready")
sx=lora_init()
rf_rx()
while True:
    data, state = sx.recv(timeout_en=True, timeout_ms=5000)
    if state == 0 and data:
        print("RX:", data)
        print("RSSI:", sx.rssi(), "dBm")
    time.sleep(0.1)
    