from machine import Pin
import time

class PIRSensor:
    def __init__(self, pin_num, callback=None):
        self.pin = Pin(pin_num, Pin.IN)
        self.callback = callback
        # Setup interrupt on rising edge (motion detected)
        if callback:
            self.pin.irq(trigger=Pin.IRQ_RISING, handler=self._handle_motion)

    def _handle_motion(self, pin):
        if self.callback:
            self.callback()

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
            