from sx1262 import SX1262
import time
from machine import Pin

# RF switch
TXEN = Pin(46, Pin.OUT)  # transmit enable : V4.1
RXEN = Pin(45, Pin.OUT)  # receive enable : V4.1
FEMEN = Pin(2, Pin.OUT)  # frontend enable

def rf_tx():
    TXEN.value(1); RXEN.value(0)

def rf_rx():
    TXEN.value(0); RXEN.value(1)
# Start in RX mode

def lora_init():
    # Radio
    sx = SX1262(
        spi_bus=1,
        clk=9, mosi=10, miso=11,
        cs=8, irq=14, rst=12, gpio=13
        )
    sx.begin(freq=868.0, bw=500.0, sf=8, cr=8, power=22)
    FEMEN.value(1); time.sleep(0.2)
    return sx
