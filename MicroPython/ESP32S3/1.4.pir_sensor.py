from machine import Pin
import time

class PIRSensor:
    
    def __init__(self, pin_num):
        self.pin = Pin(pin_num, Pin.IN)
    
    def is_motion(self):
        return self.pin.value() == 1
    
    def wait_for_motion(self, timeout=None):
        start = time.ticks_ms()
        while True:
            if self.is_motion():
                return True
            if timeout is not None:
                elapsed = (time.ticks_ms() - start) / 1000
                if elapsed >= timeout:
                    return False
            time.sleep(0.05)
            