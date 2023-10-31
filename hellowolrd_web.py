from web.wifi import Wifi
from web.serveur import Serveur

#connection to my WIFI_SSID defined into web.config
my_wifi = Wifi()
print(my_wifi.scan_networks())
while not my_wifi.is_connected:
    my_wifi.connect()

#start web serveur
my_serveur = Serveur(wifi=my_wifi)
    
