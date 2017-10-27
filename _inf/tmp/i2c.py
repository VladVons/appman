#!/usr/bin/python3

# https://alselectro.wordpress.com/2016/05/12/serial-lcd-i2c-module-pcf8574/
# i2cdetect -y 1

from smbus import SMBus
from itertools import cycle
from time import sleep

LED1 = 0x01
LED2 = 0x02
LED3 = 0x04
LED4 = 0x08
LED5 = 0x10
LED6 = 0x20
LED7 = 0x40
LED8 = 0x80
LEDF = 0xFF

PATTERN = (LED1, LED2, LED3, LED4, LED5, LED6, LED7, 
            LED8,
           LED7, LED6, LED5, LED4, LED3, LED2)

PATTERN = (LED1, LED2, LED3, LED4)
PATTERN = (LED5, LED2, LED7, LED8)


addr1 = 0x26
addr2 = 0x27
bus = SMBus(1) # Port 1 used on REV2 
for LED in cycle(PATTERN):
    #print('Addr1', addr1, 'Led', )
    #bus.write_byte(addr1, LEDF)
    #sleep(1)

    print('Addr1', addr1, 'Led', LED)
    bus.write_byte(addr1, LED)

    print('Addr2', addr2, 'Led', LED)
    bus.write_byte(addr2, LED)

    sleep(2)
