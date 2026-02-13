import machine, time
from machine import RTC, deepsleep, SPI, Pin
from time import sleep
from oled_tools import *
from sensors import *
from lora_off import *

# Get the RTC object
rtc = machine.RTC()
# # Read the current memory contents
rtc_mem = rtc.memory()
if len(rtc_mem) == 0:
    # If empty, this is the first cycle
    cycle = 0
else:
    # Convert stored bytes to integer
    cycle = int(rtc_mem.decode())
# Print the current cycle count
print("Current cycle count:", cycle)
# Increment the cycle counter
cycle += 1
# Save the new cycle count to RTC memory
rtc.memory(str(cycle).encode())
Pin(36, Pin.OUT).value(0); sleep(0.5)   
lumi,temp,humi=sensors(sda=6, scl=7)
sensors_display(lumi,temp,humi,0)  #
sleep(5)  # small delay before entering sleep
print("Going to deep sleep for 10 seconds...")
lora_off()
Pin(36, Pin.OUT).value(1); sleep(0.5)   # vext off
deepsleep(10*1000)
