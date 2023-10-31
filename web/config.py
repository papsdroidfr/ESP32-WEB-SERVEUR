''' config global variables of the web module:
    - WIFI-SSID: wifi ssid to connect
    - WIFI-PASSWORD: my wifi password
    - STATION: is the network.WLAN to activate
    - LED: RGB led of the PYBSTICK ESP32-C3 for managing connection status
        blue: WLAN activated, not yet connected to a wifi
        blue blinking: waiting for a wifi connection
        green: connected to a wifi
        red: wifi connection error
'''

import network
from .RGBLed import RGB_led

#########################################
WIFI_SSID = "MY-SSID-WIFI"
WIFI_PASSWORD = "MY-WIFI-PASSWORD"
STATION = network.WLAN(network.STA_IF)
LED = RGB_led()
#########################################