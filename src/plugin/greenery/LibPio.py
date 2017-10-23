# Created: 15.10.2017
# Vladimir Vons, VladVons@gmail.com


import RPi.GPIO as GPIO
#
from LibCommon import TControl


__all__ = ['TPioOut', 'TPiosOut', 'TPioIn']


class TPio(TControl):
    def LoadParam(self, aParam):
        self.Clear()
        self.State  = None

        self.Pin    = aParam.get('Pin')
        self.Invert = aParam.get('Invert', False)

        GPIO.setmode(GPIO.BCM)

class TPioOut(TPio):
    def LoadParam(self, aParam):
        super().LoadParam(aParam)
        GPIO.setup(self.Pin, GPIO.OUT)

    def Set(self, aValue):
        if (self.State != aValue):
            self.State = aValue
            self.DoState()
            #self.Post(1, p1 = 2)

            if (aValue == self.Invert):
                GPIO.output(self.Pin, GPIO.LOW)
            else:
                GPIO.output(self.Pin, GPIO.HIGH)


    def Check(self):
        Result = self.CheckChild()
        self.Set(Result)
        return Result


class TPioIn(TPio):
    def LoadParam(self, aParam):
        super().LoadParam(aParam)
        GPIO.setup(self.Pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def Get(self):
        State = (GPIO.input(self.Pin) ^ int(self.Invert))
        if (self.State != State):
            self.State = State

            self.DoState()

    def Check(self):
        Result = self.CheckChild()
        self.Get()
        return Result


class TPiosOut(TPioOut):
    def LoadParam(self, aParam):
        super().LoadParam(aParam)

