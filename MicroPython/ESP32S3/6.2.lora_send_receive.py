import time
from lora_init import *
sx=lora_init()
print("LoRa ready")
i = 0
while True:
    rf_tx();time.sleep(0.2)
    sx.setOutputPower(22);time.sleep(0.2)
    sx.send(b"Hello %d" % i);time.sleep(0.2)
    rf_rx()
    print("TX", i)
    i += 1
    data, state = sx.recv(timeout_en=True, timeout_ms=5000)
    if state == 0 and data:
        print("RX:", data)
        print("RSSI:", sx.rssi(), "dBm")
    time.sleep(2)
    