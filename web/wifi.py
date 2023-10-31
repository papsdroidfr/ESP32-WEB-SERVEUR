''' this module scan for wifi networks and try to connect to WIFI_SSID
    
    args:
    - station: network.WLAN to use
    - led: RGB led to indicate status of the connection (blue: in progress, green: ok, red: ko)
    
    properties:
    - is_connected: True/False
    - ip_adress: ip adress in str format.
    
    methods:
    - scan_networks(): return a list of available SSID found
    - connect(): connection to WIFI_SSID (setup into config.py)
    - disconnect(): disconnect from network
    
'''
from .config import WIFI_SSID, WIFI_PASSWORD, STATION, LED
from .log import log_error, log_warn, log_info
import time, network, sys

class Wifi:
    ''' scan networks and connect to WIFI_SSID
    '''
    def __init__(self, station=STATION, led=LED):
        self._station = station
        self._led = led
        self.disconnect()
    
    @property
    def is_connected(self) -> bool:
        return self._station.isconnected()
    
    @property
    def ip_adress(self) -> str:
        return self._station.ifconfig()[0]
    
    def scan_networks(self) -> list[str]:
        ''' scan for active SSID
            return a list of SSID found
        '''
        log_info('Scanning for WiFi networks...')
        networks:List[str] = []
        authmodes = ['Open', 'WEP', 'WPA-PSK' 'WPA2-PSK4', 'WPA/WPA2-PSK']
        for (ssid, bssid, channel, RSSI, authmode, hidden) in self._station.scan():
            networks.append(ssid)
        if len(networks)==0:
            log_warn('No network found! ')
        else:
            log_info('networks found: ')
            log_info(networks)
        return networks

    def connect(self, max_iteration:int = 15) -> None:
        ''' try to connect to WIFI_SSID at maximum max_iteration times'''
        
        log_info('Connecting to wifi ' + WIFI_SSID)
        
        # Try to connect to WiFi access point
        iteration:int = 0
        while not self.is_connected:
            try:
                self._station.connect(WIFI_SSID, WIFI_PASSWORD)
            except:
                pass
            iteration +=1
            if (iteration == max_iteration):
                break
            time.sleep(0.5)
            self._led.blink(grb=(0,0,32)) 
        
        if self.is_connected:
            self._led.color(grb=(32,0,0)) # green led
            log_info('Connected, my IP Address: ' + self.ip_adress)
        else:
            log_warn('Fail to connect, retry ...')
            self._led.color(grb=(0,32,0)) # red led
    
    def disconnect(self) -> None:
        '''Disconnect from network'''
        self._station.disconnect()
        self._led.color(grb=(0,0,32)) # blue led
        log_info('Diconnected')
