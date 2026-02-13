from rgb_clock import RGBClock
import time

clock = RGBClock(pin=18)   # GPIO5 for LED ring

while True:
    # Suppose you already have NTP time
    tm = time.localtime()
    hour = tm[3]
    minute = tm[4]
    second = tm[5]
    clock.show_time(hour, minute, second)
    time.sleep(1)
    