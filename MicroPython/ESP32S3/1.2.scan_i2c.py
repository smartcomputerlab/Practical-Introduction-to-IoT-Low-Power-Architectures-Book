from machine import Pin, I2C
import time
Pin(36, Pin.OUT).value(0); time.sleep(0.1)  # 0 to turn on Vext
time.sleep_ms(400)
# Configure I2C
i2c = I2C(0, scl=Pin(7), sda=Pin(6))  # I2C bus 0 with custom pins
# Scan for I2C devices
devices = i2c.scan()
print("I2C devices found:", devices)
