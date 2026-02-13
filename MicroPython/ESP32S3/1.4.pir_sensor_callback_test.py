from pir_sensor_callback import *
import time

# Define the callback function
def motion_detected():
    print("Motion detected! ")
# Initialize PIR sensor on GPIO03 with callback
pir = PIRSensor(3, callback=motion_detected)
print("PIR sensor active. Waiting for motion...")
while True:
    # Main loop can do other tasks; PIR triggers callback automatically
    time.sleep(1)
    print("main loop")
    