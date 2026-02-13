import time
from lora_init import *
sx=lora_init()
print("LoRa ready")
i = 0
while True:           # sending optimal , max power packet
    rf_tx();time.sleep(0.2)
    sx.setOutputPower(22);time.sleep(0.2)
    sx.send(b"Hello %d" % i);time.sleep(0.2)
    rf_rx()
    print("TX", i)
    i += 1
    time.sleep(2)
    