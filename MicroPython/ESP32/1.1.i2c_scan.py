from machine import Pin, I2C
import time

rst=Pin(16, Pin.OUT); rst.value(0); time.sleep_ms(400); rst.value(1)
time.sleep_ms(400)
# Configure I2C
i2c = I2C(0, scl=Pin(15), sda=Pin(4))  # I2C bus 0 with custom pins
# Scan for I2C devices
devices = i2c.scan()
print("I2C devices found:", devices)