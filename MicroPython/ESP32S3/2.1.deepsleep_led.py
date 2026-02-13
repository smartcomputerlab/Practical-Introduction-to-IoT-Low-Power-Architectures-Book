from machine import Pin, deepsleep
import time
# Initialize the led pin
led = Pin(35, Pin.OUT)
# Turn on the led
led.value(1)
print("led is ON")
time.sleep(3)  
# Turn off the LED
led.value(0)
print("led is OFF")
time.sleep(3)    
print("Going to sleep for 6 seconds…"); time.sleep(1)
deepsleep(6000)  # 6 seconds in milliseconds
