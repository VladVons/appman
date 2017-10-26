#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
#from dth import DTH


print(GPIO.RPI_INFO)
print('mode', GPIO.getmode())

GPIO.setmode(GPIO.BCM)

#Pins = [2,3,4,14]
PinsOut = [17,22,27,18]
PinIn = 26

GPIO.setup(PinsOut, GPIO.OUT)

#GPIO.setup(PinIn, GPIO.IN)
GPIO.setup(PinIn, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

i = 0
while True:
#for i in Pins:
    i += 1
    print('loop', i)

    GPIO.output(PinsOut, GPIO.HIGH)
    In = GPIO.input(PinIn)
    print('PinIn', PinIn, 'In', In)

    sleep(0.5)

    GPIO.output(PinsOut, GPIO.LOW)

    sleep(0.5)
    break

GPIO.cleanup()
print('mode', GPIO.getmode())
