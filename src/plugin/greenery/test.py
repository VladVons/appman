#!/usr/bin/python3

import json
import time
import sys
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
        I2COut= TI2COut(None)
        Pattern = {'Bus1':1, 'Address': 0x27, 'Pin':1, 'Invert':False}
        Pattern = {'MailTo':None, 'Relay':'localhost', 'Port':0, 'User':'', 'Password':None}
        I2COut.LoadParamPattern(Data2, Pattern)

def Test4():
    File = 'greenery.json'
    with open(File) as FileData:
        Data = json.load(FileData)

    Manager = TManager()
    Manager.Run(Data['Gpio'])

Test4()
#Test2()
#print(ClassPath(TC, ''))

#C = TC()
#C.GetPath()
#print(TC.__bases__[0])


#Val1 = 2
#Dig1  = 11
#print(Dig1 % Val1)