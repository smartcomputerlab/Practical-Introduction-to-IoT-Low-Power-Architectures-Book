from pir_sensor import *
import time
pir = PIRSensor(18)  # Connect PIR OUT to GPIO18

while True:
    if pir.is_motion():
        print("Motion detected!")
    else:
        print("No motion")
    time.sleep(0.5)
    
    