               1.3.2 Animating 12-RGB-LED ring
-----------------------------------------------------------------------------------------
from machine import Pin
import neopixel
import time
# Configuration
NUM_LEDS = 12       # Number of LEDs on the ring
PIN = 3             # Data pin connected to the ring
# Initialize NeoPixel
np = neopixel.NeoPixel(Pin(PIN), NUM_LEDS) 
# Function to set all LEDs to off
def clear():
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 0)
    np.write()
# Function to create a color wheel (RGB)
def color_wheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)
# Animate the ring
try:
    while True:
        for j in range(255):          # Cycle through color wheel
            for i in range(NUM_LEDS):
                idx = (i * 256 // NUM_LEDS + j) & 255
                np[i] = color_wheel(idx)
            np.write()
            time.sleep(0.05)

except KeyboardInterrupt:
    clear()  # Turn off LEDs on exit
    