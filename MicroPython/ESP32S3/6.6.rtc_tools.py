from machine import RTC
import struct

rtc = RTC()
FMT = 'fi2f'  # size is 16 bytes

def store_values(temp: float, cycle: int, delta: float, thold: float):
    data = struct.pack(FMT, temp, cycle, delta, thold)
    rtc.memory(data)

def load_values():
    data = rtc.memory()
    if len(data) != struct.calcsize(FMT):
        # Memory empty or invalid → initialize defaults
        temp, cycle, delta, thold = 25.0, 10, 0.1,32.0
        store_values(temp, cycle, delta, thold)
        return temp, cycle, delta, thold
    temp, cycle, delta, thold = struct.unpack(FMT, data)
    return temp, cycle, delta, thold

# Example usage
# t, c, d, h = load_values()
# store_values(round(t+0.1,2), c+5, d+0.1, round(h+0.2,2))
# t, c, d, h = load_values()
# print("Temp:", t, "Cycle:", c, "Delta:", d, "Thold:", h)

