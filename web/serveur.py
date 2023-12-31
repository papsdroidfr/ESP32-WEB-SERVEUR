from .config import STATION, LED
from .log import log_info, log_warn, log_error
from .wifi import Wifi
import gc

try:
  import usocket as socket
except:
  import socket
  
def _gen_html_default() ->str:
    '''default html page used by the module'''
    code_html = '''
    <html>
        <head>
            <title>My ESP32-C3 Web Server</title>
            <style> html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
                    h1{color: #0F3376; padding: 2vh;}
                    p{font-size: 1.5rem;}
            </style>
        </head>
        <body>
            <h1>My ESP32-C3 Web Server</h1>
            <p><strong>Hello World !</strong></p>
        </body>
    </html>'''
    return code_html

def _exec_esp32_default(request:str) ->None:
    ''' default execution of actions on ESP32-C3 based on request received'''
    pass  #do nothing by default

class Serveur():
    ''' this class manage the web serveur.
        Makes sure first a WIFI connexion is active,
        then start listning to a socket on port 80, looping on requests
        
        params:
        - wifi: wifi connexion used
        - gen_html(): function called that generates HTML code of the web page.
        - exec_esp32(request:str): function called that manage requests in order to control ESP32-C3.
        
        properties:
        - my_html_page: return HTML page generated by gen_html()
        
        provate methods:
        - _loop_requests(): loop into GET requests received. 
    '''
    def __init__(self, wifi:Wifi = None,
                 gen_html = _gen_html_default,
                 exec_esp32 = _exec_esp32_default ) -> None:
        '''constructor'''
        gc.collect() #Sockets are automatically closed when they are garbage-collected,
        self._wifi = wifi
        self.gen_html = gen_html     #callable html generator code
        self.exec_esp32 = exec_esp32 #yecallable esp32 action execution
        if self._wifi == None:
            log_warn('Connect first to a WIFI.')
            LED.color(grb=(0,32,0)) #red color
        else:
            LED.color(grb=(32,0,0)) #green color
            self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._s.bind(('', 80))
            self._s.listen(5)
            self._loop_requests() #infinite loop into GET requests received
    
    @property
    def my_html_page(self) ->str:
        return self.gen_html()
    
    def _loop_requests(self) -> None:
        '''infinite loop into requests received'''
        log_info('Web serveur started, listing for requests from http://' + self._wifi.ip_adress)      
        while True:
            conn, addr = self._s.accept()
            log_info('Got a connection from %s' % str(addr))
            request = str(conn.recv(1024))
            #extract GET request: substring before 'HTTP' is found
            request_get = request[:request.find('HTTP')]
            log_info('Content: '+ request_get)
            
            self.exec_esp32(request_get)   #execute ESP32-C3 action with GET request received
            response = self.my_html_page   #build a dynamic new HTML page
            
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()