# Created: 15.10.2017
# Vladimir Vons, VladVons@gmail.com


import RPi.GPIO as GPIO
import smbus
import os

import time
#
from LibCommon import TControl, _Required


__all__ = ['TPioOut', 'TPiosOut', 'TPioIn', 'TI2COut', 'TW1DS']


class TPio(TControl):
    def LoadParam(self, aParam):
        Pattern = {'Invert':False, 'Periodic':1, 'State':None, 'Pin':_Required}
        self.LoadParamPattern(aParam, Pattern)

        GPIO.setmode(GPIO.BCM)


class TPioOut(TPio):
    def LoadParam(self, aParam):
        super().LoadParam(aParam)
        GPIO.setup(self.Pin, GPIO.OUT)

    def Set(self, aValue):
        #print('Alias', self.Alias, 'Pin', self.Pin, 'State', self.State, 'aValue', aValue, 'High', GPIO.HIGH)

        #print(0)
        #GPIO.output(self.Pin, 0)
        #time.sleep(5)
        #print(1)
        #GPIO.output(self.Pin, 1)
        #time.sleep(5)


        #if (self.State != aValue):
        GPIO.output(self.Pin, int(not aValue))
        #time.sleep(1)
        #GPIO.output(self.Pin, int(not aValue))
        #GPIO.output(self.Pin, GPIO.HIGH)
        #assert (False)

    def _Check(self, aValue):
        self.Set(aValue)
        return aValue


class TPioIn(TPio):
    def LoadParam(self, aParam):
        super().LoadParam(aParam)
        GPIO.setup(self.Pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def Get(self):
        return GPIO.input(self.Pin)

    def _Check(self, aValue):
        return self.Get()


class TPiosOut(TPioOut):
    def LoadParam(self, aParam):
        super().LoadParam(aParam)



#--- I2C
class TI2C(TControl):
    def LoadParam(self, aParam):
        Pattern = {'Invert':False, 'Periodic':1, 'State':None, 'Bus':1, 'Address':_Required, 'Pin':_Required}
        self.LoadParamPattern(aParam, Pattern)


class TI2COut(TI2C):
    def Set(self, aValue):
        if (self.State != aValue):
            #print(self.Alias, self.Bus, self.Address, int(aValue))
            Bus = smbus.SMBus(self.Bus)
            Bus.write_byte(self.Address, self.Pin)

    def _Check(self, aValue):
        self.Set(aValue)
        return True


#--- One wire file
class TW1File(TControl):
    def LoadParam(self, aParam):
        Pattern = {'Invert':False, 'Periodic':1, 'State':None, 'Dir':'/sys/bus/w1/devices/', 'File':_Required, 'Min':-99999, 'Max':99999}
        self.LoadParamPattern(aParam, Pattern)

        self.File = self.Dir + self.File
        if (not os.path.exists(self.File)):
            self._Error('File not found %s' % self.File)

    def _ReadFile(self):
        HFile  = open(self.File)
        Result = HFile.read()
        HFile.close()
        return Result

    def _Check(self, aValue):
        Value  = self.Get()
        Result = (Value < self.Min) or (Value > self.Max)
        return Result


class TW1DS(TW1File):
    def Get(self):
        Data   = self._ReadFile()
        Str1   = Data.split('\n')[1].split(' ')[9]
        Result = float(Str1[2:]) / 1000
        return Result
