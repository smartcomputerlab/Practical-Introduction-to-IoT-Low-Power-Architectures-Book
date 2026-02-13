from machine import Pin
import time

# Define pins
button = Pin(0, Pin.IN, Pin.PULL_UP)   # PRG button (active low)
led = Pin(25, Pin.OUT)                # LED

while True:
    if button.value() == 0:   # Button pressed
        led.on()
    else:                     # Button released
        led.off()
        
    time.sleep(0.05)          # Small delay for stability