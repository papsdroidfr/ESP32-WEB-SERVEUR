from web.wifi import Wifi
from web.serveur import Serveur
from web.config import LED
import time

#connection to my WIFI_SSID defined into web.config
my_wifi = Wifi()
print(my_wifi.scan_networks())
while not my_wifi.is_connected:
    my_wifi.connect()
    time.sleep(0.5)

def my_html_page() -> str:
      if LED.is_on:
        led_state="ON"
      else:
        led_state="OFF"
  
      html = """
        <html>
            <head>
                <title>ESP32-C3 Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="icon" href="data:,">
                <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
                    h1{color: #0F3376; padding: 2vh;}
                    p{font-size: 1.5rem;}
                    .button{display: inline-block; background-color: #e7bd3b; border: none; 
                        border-radius: 4px; color: white;padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
                    .button2{background-color: #4286f4;}
                </style>
            </head>
        
            <body>
                <h1>ESP32-C3 Web Server</h1> 
                <p>Led state: <strong>""" + led_state + """</strong></p>
                <p><a href="/?led=on"><button class="button">ON</button></a></p>
                <p><a href="/?led=off"><button class="button button2">OFF</button></a></p>
            </body>
        </html>
        """
      return html

def my_exec_request(request:str) ->None:
    if request.find('GET /?led=on') > -1:
        LED.color((32,0,0)) #green color
    elif request.find('GET /?led=off') > -1:
        LED.off()  

#start web serveur
my_serveur = Serveur(wifi=my_wifi, gen_html=my_html_page, exec_esp32 = my_exec_request)
    