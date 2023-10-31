''' manage the RGB led of a PYBStick ESP32-C2
    
    args: none
    
    properties:
    - is_on: True/False
    
    methods
    - off(): switch off the led
    - color((g,r,b)): switch on the led with RGB color (g,r,b)
    - blink((g,r,b)): switch on/off the led to make it blinked with RGB color (g,r,b)
'''

from machine import Pin
from apa106 import APA106
import time

class RGB_led:
    def __init__(self) -> None:
        ''' constructor '''
        self._rgb_led = Pin(8, Pin.OUT)
        self._ap = APA106(self._rgb_led, 1)
        self.off() #switch off the led.
        
    @property
    def is_on(self) -> bool:
        return(self._on)

    def off(self) -> None:
        ''' switch off the led '''
        self._ap[0] = (0, 0, 0) # set the led to RGB
        self._ap.write()
        self._on = False
        
    def color(self, grb:tuple[int,int,int] = (64,64,64)) -> None:
        ''' switch on led to color (g,r,b) '''
        self._ap[0] = grb # set the led to RGB
        self._ap.write()
        self._on = True
        
    def blink(self, grb:tuple[int,int,int] = (64,64,64)) -> None:
        ''' switch on/off led to make it blinked with color (g,r,b) '''
        if self.is_on:
            self.off()
        else:
            self.color(grb)

