''' web module starts by activating network WLAN and the RGBLed of the PYBStick ESP32-C3
'''

import network
from .config import STATION, LED
from .log import log_info, log_warn, log_error
from .RGBLed import RGB_led
from .wifi import Wifi

#activate network.WLAN
STATION.active(True)
if not STATION.active():
    log_error("network.WLAN can't be activated")
else:
    log_info("network.WLAN successfully activated")

#RGB led setup
LED = RGB_led()
LED.color((0,0,64)) #blue color

