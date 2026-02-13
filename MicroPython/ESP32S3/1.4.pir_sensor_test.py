from pir_sensor import *
import time
pir = PIRSensor(3)  # Connect PIR OUT to GPIO03

while True:
    if pir.is_motion():
        print("Motion detected!")
    else:
        print("No motion")
    time.sleep(0.5)