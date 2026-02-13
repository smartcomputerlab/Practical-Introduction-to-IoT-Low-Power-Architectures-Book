from wifi_tools import *
# Replace with your own WiFi credentials
SSID="Livebox-2E80"
PASSWORD="DTPbgKhpV6M3c4mE6s"
# Scan available networks
networks = scan_WiFi()
print("Available networks:")
for net in networks:
    ssid, bssid, channel, RSSI, authmode, hidden = net
    print("SSID:", ssid.decode('utf-8'), "| RSSI:", RSSI)
    
if connect_WiFi(SSID, PASSWORD):
    print("Connected to WiFi:", SSID)
    print("Network config:", network.WLAN(network.STA_IF).ifconfig())
else:
    print("Failed to connect to WiFi:", SSID)

# Disconnect from current WiFi network
disconnect_WiFi()
print("Disconnected from WiFi")
