import machine, time
from machine import RTC, deepsleep, SPI, Pin
from time import sleep
from oled_tools import *
from sensors import *
from lora_off import *
Pin(36, Pin.OUT).value(0); sleep(0.5)   
sleep(5)  # small delay before entering sleep
print("Going to deep sleep for 10 seconds...")
lora_off()
Pin(36, Pin.OUT).value(1); sleep(0.5)   # vext off
deepsleep(10*1000)
