#!/usr/bin/python3

import json
import time
import sys
import logging
import ast

#
from LibTimer import *
from LibCommon import *
from Manager import *



class TA():
    def Test1(self, aClass):
        print('TA->Test1')

    def GetClassPath(self, aClass, aPath = ''):
        Class = aClass.__bases__
        if (Class):
            aPath = self.GetClassPath(Class[0], aPath)
        return aPath + '/' + aClass.__name__

class TB(TA):
    def Test2(self):
        print('TB->Test2')

class TC(TB):
    def Test3(self):
        print('TC->Test3')

    def GetPath(self):
        print(self.GetClassPath(self.__class__))


def GetLogger():
    Format = '[%(asctime)s], %(levelname)s:%(message)s'
    logging.basicConfig(level=logging.INFO,
                        format=Format,
                        datefmt='%Y/%m/%d %H:%M:%S'
                        )
    Logger = logging.getLogger('Log1')
    #Logger.addHandler(logging.StreamHandler())
    return Logger

def Test1():
    Data = '{"Timer_Day":{ "Range":[ { "On":"7", "Off": "10:39:30"}, { "On":"21:00:03", "Off": "22:00"}, { "On":"23:45", "Off": "23:46"} ]}}'
    root = json.loads(Data)
    TimeRangeDay = TTimeRangeDay(None)
    TimeRangeDay.Load(root.get('Timer_Day'))
    print(TimeRangeDay.Check())


def Test2a():
        print('Test2a', sys._getframe(1).f_code.co_name)

def Test2():
    File = 'greenery.json'
    with open(File) as FileData:
        Data1 = json.load(FileData)
        Data2 = Data1['Gpio']['Class'][0]['Param']

        #print('Data2', Data2)
        #I2COut  = TI2COut(None)
        #Pattern = {'Bus1':1, 'Address': 0x27, 'Pin':1, 'Invert':False}
        #Pattern = {'MailTo':None, 'Relay':'localhost', 'Port':0, 'User':'', 'Password':None}
        #I2COut.LoadParamPattern(Data2, Pattern)

        #print('Data2', Data2)
        W1DS  = TW1DS(None)
        W1DS.Logger = GetLogger()
        W1DS.LoadParam(Data2)
        W1DS.Check()
        Value = W1DS.Get()
        print('Value', Value)

def OnValue(aObj):
    #print('OnValue. Alias', aObj.Alias, 'Value', aObj.Value)
    Info = 'Alias {:25}, Value {:6}, State {:1}'.format(aObj.Alias, aObj.Value, aObj.Param.State)
    print('OnValue', Info)


def Test4():
    File = 'greenery.json'
    with open(File) as FileData:
        Data = json.load(FileData)

    Manager = TManager()
    #Manager.OnState = OnState
    Manager.OnValue  = OnValue
    Manager.Load(Data['Gpio'])
    Manager.Run()


def Test5():
    import smbus
    ONE_TIME_HIGH_RES_MODE_1 = 0x20
    ADDR = 35
    bus = smbus.SMBus(1)
    while True: 
        data = bus.read_i2c_block_data(ADDR, ONE_TIME_HIGH_RES_MODE_1)
        Var = round(((data[1] + (256 * data[0])) / 1.2))
        print('Lx', Var)
        time.sleep(1)

Test4()

