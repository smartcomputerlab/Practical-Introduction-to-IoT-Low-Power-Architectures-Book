from machine import UART, Pin
import utime
uart = UART(1, baudrate=9600, tx=Pin(5), rx=Pin(4))  # TX on GPIO5, RX on GPIO4
print("UART Test Program")
test_data = "Hello, UART interface on our DevKit"
try:
    print("Sending data: ", test_data)
    uart.write(test_data)
    utime.sleep(1)
    if uart.any():
        received_data = uart.read()
        print("Received data: ", received_data.decode('utf-8'))
    else:
        print("No data received.")
except Exception as e:
    print("An error occurred:", e)
finally:
    print("Program completed.")
    