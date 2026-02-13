from machine import Pin
import time
button = Pin(0, Pin.IN, Pin.PULL_UP)   # PRG button on the board (active low)
led = Pin(35, Pin.OUT)                # LED
while True:
    if button.value() == 0:   # Button pressed
        led.on()
    else:                     # Button released
        led.off()
    time.sleep(0.05)          # Small delay for stability
    