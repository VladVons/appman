#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
#from dth import DTH


def PinOut(aPin, aValue):
    print('aPin', aPin, 'aValue', aValue)
    GPIO.output(aPin, aValue)


def Test1():
    print(GPIO.RPI_INFO)
    print('mode', GPIO.getmode())

    GPIO.setmode(GPIO.BCM)

    #Pins = [2,3,4,14]
    #PinsOut = [17,22,27,18]
    PinsOut = [17]
    PinIn = 26

    GPIO.setup(PinsOut, GPIO.OUT)

    #GPIO.setup(PinIn, GPIO.IN)
    GPIO.setup(PinIn, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    i = 0
    while True:
        #for i in Pins:
        i += 1
        print('loop', i)

        PinOut(PinsOut, GPIO.HIGH)
        #GPIO.output(PinsOut, GPIO.HIGH)
        #In = GPIO.input(PinIn)
        #print('PinIn', PinIn, 'In', In)

        sleep(3)

        PinOut(PinsOut, GPIO.LOW)
        #GPIO.output(PinsOut, GPIO.LOW)

        sleep(3)
        break

    GPIO.cleanup()
    print('mode', GPIO.getmode())


Test1()
