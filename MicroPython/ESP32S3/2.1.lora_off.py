def lora_off():
    # SPI instance
    spi = SPI(1, sck=Pin(9), mosi=Pin(10), miso=Pin(11))
    cs  = Pin(8, Pin.OUT)
    cs.value(0);sleep(0.1)
    spi.write(bytes([0x84, 0x80]))  # SetSleep, 0x01 -warm sleep, , 0x00 - cold sleep, 
                                    # 0x80-freeze sleep - external wakeup only
    sleep(0.1);cs.value(1);sleep(0.1)
    