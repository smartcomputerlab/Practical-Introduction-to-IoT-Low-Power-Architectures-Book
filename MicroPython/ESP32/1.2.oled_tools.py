from machine import Pin, I2C
import ssd1306 
import time

def oled_init():
    # Power OLED
    #Pin(36, Pin.OUT).value(0);time.sleep_ms(50)
    # Reset OLED
    rst=Pin(16, Pin.OUT); rst.value(0); time.sleep_ms(400); rst.value(1)
    time.sleep_ms(400)
    # I2C init — ONLY 3 args
    i2c = I2C(0, scl=15, sda=4)
    # Assuming a 128x64 display:
    width = 128; height = 64
    # Initialize the OLED display
    oled = ssd1306.SSD1306_I2C(width, height, i2c,0x3C)
    oled.fill(0)
    return oled

# display on OLED of V3 or V4 
def sensors_display(luminosity, temperature, humidity, duration):
    oled = oled_init()  
    # Write text to display
    oled.text("Sensor readings", 0, 0)
    oled.text("Lux: {:.2f}".format(luminosity), 0, 16)
    oled.text("Temp: {:.2f}".format(temperature), 0, 32)
    oled.text("Humi: {:.2f}".format(humidity), 0, 48)
    oled.show()
    if duration!=0:
        time.sleep(duration)
        oled.poweroff()
        
def sensors_display_str(luminosity, temperature, humidity, duration):
    oled = oled_init()  
    # Write text to display
    oled.text("Sensor readings", 0, 0)
    oled.text("Lux:"+luminosity, 0, 16)
    oled.text("Temp:"+temperature, 0, 32)
    oled.text("Humi:"+humidity, 0, 48)
    oled.show()
    if duration!=0:
        time.sleep(duration)
        oled.poweroff()        
 
def time_display(hour, minute, second, duration):
    oled = oled_init() 
    # Write text to display
    oled.text("Time readings", 0, 0)
    oled.text("Hour: {:.d}".format(hour), 0, 16)
    oled.text("Min: {:.d}".format(minute), 0, 32)
    oled.text("Sec: {:.d}".format(second), 0, 48)
    oled.show()
    if duration!=0:
        time.sleep(duration)
        oled.poweroff()

def message_display(text1,text2,text3, duration):
    oled = oled_init() 
    # Write text to display
    oled.text("Message", 0, 0)
    oled.text(text1, 0, 16)
    oled.text(text2, 0, 32)
    oled.text(text3, 0, 48)
    oled.show()
    if duration!=0:
        time.sleep(duration)
        oled.poweroff()
