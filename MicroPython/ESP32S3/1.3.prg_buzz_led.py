from machine import Pin
import time

# Define pins
button = Pin(0, Pin.IN, Pin.PULL_UP)   # PRG button (active low)
led = Pin(35, Pin.OUT)                 # LED line on DevKit
buzz = Pin(3, Pin.OUT)                 # SIG line on DevKit

while True:
    if button.value() == 0:   # Button pressed
        led.on()
        buzz.on()
    else:                     # Button released
        led.off()
        buzz.off()
        
    time.sleep(0.05)          # Small delay for stability
    