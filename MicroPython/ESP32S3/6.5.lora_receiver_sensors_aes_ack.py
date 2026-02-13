import time, ustruct
from lora_init import *
from aes_tools import *
from oled_tools import *
aes_key="smartcomputerlab"

print("LoRa RX ready")
sx=lora_init()
rf_rx();time.sleep(0.2)
chan=1234
while True:
    print("waiting on recv")
    data, state = sx.recv(timeout_en=True, timeout_ms=64000); rf_tx()
    if state == 0 and data:
        print("RX:", data)
        print("RSSI:", sx.rssi(), "dBm")
        payload=aes_decrypt(data[:-1],aes_key)
        print("RX:", payload)
        chan, wkey, lumi, temp, humi = ustruct.unpack('i16s3f', payload)
        print(chan, wkey, lumi, temp, humi)
        sensors_display(lumi,temp,humi,0)
    else:
        print("recv timeout")

    time.sleep(1)
    sx.setOutputPower(-5);time.sleep(0.2)
    cycle=10; delta=0.1;thold=29.25
    ack=ustruct.pack('2i2f',chan,cycle,delta,thold)  # chan, cycle, delta, thold
    enc_ack=aes_encrypt(ack,aes_key); pos=16
    enc_ack = enc_ack[:pos] + b'\x00' + enc_ack[pos:]
    sx.send(enc_ack);time.sleep(0.2)
    print("control cycle,delta,thold:"); print(cycle,delta,thold)
    rf_rx();time.sleep(0.1)
    