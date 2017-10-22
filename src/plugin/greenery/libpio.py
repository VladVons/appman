import RPi.GPIO as GPIO

from control import TControl

__all__ = ["TPio"]


class TPio(TControl):
    def __init__(self, aParent):
        TControl.__init__(self, aParent)

    def LoadParam(self, aParam):
        self.Clear()

        self.Pin    = int(aParam.get('Pin'))
        self.Access = aParam.get('Access')
        self.Invert = aParam.get('Invert', False)
        self.State  = None

        GPIO.setmode(GPIO.BCM)

        if (self.Access == 'Write'):
            GPIO.setup(self.Pin, GPIO.OUT)
        else:
            GPIO.setup(self.Pin, GPIO.IN)

    def Set(self, aValue):
        if (self.State != aValue):
            self.State = aValue
            self.DoState()

            if (aValue == self.Invert):
                GPIO.output(self.Pin, GPIO.LOW)
            else:
                GPIO.output(self.Pin, GPIO.HIGH)


    def Check(self):
        Result = self.CheckChild()
        self.Set(Result)
        return Result
