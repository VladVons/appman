# Created: 15.10.2017
# Vladimir Vons, VladVons@gmail.com


import RPi.GPIO as GPIO
import smbus
#
from LibCommon import TControl


__all__ = ['TPioOut', 'TPiosOut', 'TPioIn', 'TI2COut']


class TPio(TControl):
    def LoadParam(self, aParam):
        Pattern = {'Pin':None, 'Invert':False, 'Delay':0, 'Periodic':1}
        self.LoadParamPattern(aParam, Pattern)

        GPIO.setmode(GPIO.BCM)

class TPioOut(TPio):
    def LoadParam(self, aParam):
        super().LoadParam(aParam)
        GPIO.setup(self.Pin, GPIO.OUT)

    def Set(self, aValue):
        if (self.State != aValue):
            GPIO.output(self.Pin, int(aValue))

    def _Check(self, aValue):
        self.Set(aValue)
        return aValue


class TI2C(TControl):
    def LoadParam(self, aParam):
        Pattern = {'Bus':1, 'Address':None, 'Pin':None, 'Invert':False, 'Periodic':1}
        self.LoadParamPattern(aParam, Pattern)


class TI2COut(TI2C):
    def Set(self, aValue):
        if (self.State != aValue):
            print(self.Alias, self.Bus, self.Address, int(aValue))
            Bus = smbus.SMBus(self.Bus)
            Bus.write_byte(self.Address, int(aValue))

    def _Check(self, aValue):
        self.Set(aValue)
        return True


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
