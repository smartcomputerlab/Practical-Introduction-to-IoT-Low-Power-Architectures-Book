from machine import Pin, SPI, deepsleep
import esp32
from time import sleep

def lora_off():
    # SPI instance
    spi = SPI(1, sck=Pin(9), mosi=Pin(10), miso=Pin(11))
    cs  = Pin(8, Pin.OUT)
    cs.value(0);sleep(0.1)
    spi.write(bytes([0x84, 0x80]))  # SetSleep, 0x01 -warm sleep, , 0x00 - cold sleep, 
                                    # 0x80-freeze sleep - external wakeup only
    sleep(0.1);cs.value(1);sleep(0.1)

WAKE_PIN = 4
led = Pin(35, Pin.OUT)
Pin(36, Pin.OUT).value(0); sleep(0.1)
wake = Pin(WAKE_PIN, Pin.IN, Pin.PULL_DOWN)
esp32.wake_on_ext0(pin=wake, level=1)  # wake on HIGH
print("Active 5 seconds")
led.on() ; sleep(5)
led.off(); lora_off()
Pin(36, Pin.OUT).value(1); sleep(0.5)   # vext off
print("Sleeping... trigger GPIO2 to wake")
sleep(1)
deepsleep()
