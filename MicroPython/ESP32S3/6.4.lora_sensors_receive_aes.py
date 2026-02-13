import time, ustruct
from lora_init import *
from aes_tools import *
aes_key="smartcomputerlab"

print("LoRa RX ready")
sx=lora_init()
rf_rx()
i = 0
while True:
    data, state = sx.recv(timeout_en=True, timeout_ms=32000); rf_tx() # longer than sender cycle
    if state == 0 and data:
        print("RX:", data)
        print("RSSI:", sx.rssi(), "dBm")
        payload=aes_decrypt(data[:-1],aes_key)
        print("RX:", payload)
        chan, wkey, lumi, temp, humi = ustruct.unpack('i16s3f', payload)
        print(chan, wkey, lumi, temp, humi)
    else:
        print("recv timeout")


    i += 1
    time.sleep(2)
    sx.setOutputPower(-5);time.sleep(0.2)
    sx.send(b"Hello %d" % i);time.sleep(0.2)
    print("packet sent")
    rf_rx();time.sleep(0.1)
    print("in the loop")
    
    