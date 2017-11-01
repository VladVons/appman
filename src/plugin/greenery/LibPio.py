# Created: 15.10.2017
# Vladimir Vons, VladVons@gmail.com


import RPi.GPIO as GPIO
import smbus
import Adafruit_DHT as dht
#
from LibCommon import *


__all__ = ['TPioOut', 'TPiosOut', 'TPioIn', 'TI2COut', 'TW1DS', 'TDHT22', 'TBH1750']

class TPio(TControl):
    def LoadParam(self, aParam):
        Pattern = {'Pin':_Required}
        self.Param.Load(aParam, Pattern)

        GPIO.setmode(GPIO.BCM)


class TPioOut(TPio):
    def LoadParam(self, aParam):
        #super().LoadParam(aParam) # __need v3.5
        TPio.LoadParam(self, aParam)

    def Set(self, aValue):
        #if (self.State != aValue):
        GPIO.setup(self.Param.Pin, GPIO.OUT)
        GPIO.output(self.Param.Pin, int(not aValue))

    def _Check(self, aValue):
        self.Set(aValue)
        return aValue

    def _Get(self):
        return self.GetState()


class TPioIn(TPio):
    def LoadParam(self, aParam):
        #super().LoadParam(aParam) # __need v3.5
        TPio.LoadParam(self, aParam)

        GPIO.setup(self.Pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def _Get(self):
        return GPIO.input(self.Pin)

    def _Check(self, aValue):
        return self._Get()


class TPiosOut(TPioOut):
    pass

#--- I2C
class TI2COut(TControl):
    def LoadParam(self, aParam):
        Pattern = {'Bus':1, 'Address':_Required, 'Value':_Required}
        self.Param.Load(aParam, Pattern)

    def Set(self, aValue):
        if (self.Param.State != aValue):
            #print(self.Alias, self.Bus, self.Address, int(aValue))
            Bus = smbus.SMBus(self.Param.Bus)
            Bus.write_byte(self.Param.Address, self.Param.Pin)

    def _Check(self, aValue):
        self.Set(aValue)
        return True

    def _Get(self):
        return self.GetState()


class TI2CIn(TControl):
    def LoadParam(self, aParam):
        Pattern = {'Bus':1, 'Address':_Required}
        self.Param.Load(aParam, Pattern)

    def _Check(self, aValue):
        return True

    def _Get(self):

        return self.GetState()


class TW1DS(TFileData):
    def _Get(self):
        # get previous value
        Result = self.Value

        Data = self.Thread.GetData()
        if (Data):
            Str1   = Data.split('\n')[1].split(' ')[9]
            Result = float(Str1[2:]) / 1000
        return round(Result, 2)


class TDHT22(TControlThredRead):
    def LoadParam(self, aParam):
        Pattern = {'Address':_Required, 'Min':-99999, 'Max':99999}
        self.LoadParamPattern(aParam, Pattern)

    def _ReadCallBack(self):
        return dht.read(dht.DHT22, self.Param.Address)

    def _Get(self):
        # get previous value
        Result = self.Value

        #print('TDHT22',  Result)
        Data = self.Thread.GetData()
        if (Data):
            Humidity, Themper = Data
            if (Humidity):
                Result = Humidity
        return round(Result, 2)


class TBH1750(TControlThredRead):
    def LoadParam(self, aParam):
        Pattern = {'Bus':1, 'Address':_Required, 'Min':-99999, 'Max':99999}
        self.LoadParamPattern(aParam, Pattern)

    def _ReadCallBack(self):
        ONE_TIME_HIGH_RES_MODE_1 = 0x20
        Bus = smbus.SMBus(self.Param.Bus)
        return Bus.read_i2c_block_data(self.Param.Address, ONE_TIME_HIGH_RES_MODE_1)

    def _Get(self):
        # get previous value
        Result = self.Value

        #print('TDHT22',  Result)
        Data = self.Thread.GetData()
        if (Data):
            Lux = 1.2
            Result = (Data[1] + (256 * Data[0])) / Lux 
        return round(Result, 2)
