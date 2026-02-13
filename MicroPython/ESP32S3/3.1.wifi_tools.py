import network
import time

def wifi_off():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)     # THIS is the critical line
    time.sleep_ms(50)

def connect_WiFi(ssid, password, timeout=10):
    wlan = network.WLAN(network.STA_IF)
    if wlan.active():
        return True
    wlan.active(True)
    time.sleep_ms(100)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        t0 = time.time()
        while not wlan.isconnected():
            if time.time() - t0 > timeout:
                raise RuntimeError("WiFi connect timeout")
            time.sleep(0.2)
    return True

def disconnect_WiFi():
    """
    Disconnect from the currently connected WiFi network.
    """
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        wlan.disconnect()

def scan_WiFi():
    """
    Scan for available WiFi networks.
    :return: A list of tuples containing network information:
             (ssid, bssid, channel, RSSI, authmode, hidden)
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    return wlan.scan()

# SSID="Livebox-2E80"
# PASS="DTPbgKhpV6M3c4mE6s"
# 
# # print(scan_WiFi())
# if connect_WiFi(SSID, PASS, timeout=10):
#     print("connected")
# else:
#     print("not connected")
#
