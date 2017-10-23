#!/usr/bin/python3

import json
import time
#
from LibTimer import *
from LibCommon import *
from Manager import *


class TA():
    def Test1(self, aClass):
        print('TA->Test1')

    def GetClassPath(self, aClass, aPath = ''):
        Class = list(aClass.__bases__)
        for Base in Class:
            aPath = self.GetClassPath(Base, aPath)
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

def Test2():
    File = 'greenery.json'
    with open(File) as FileData:    
        Data = json.load(FileData)
        print(Data)

def GetClassPath(aClass, aPath):
    Class = list(aClass.__bases__)
    for Base in Class:
        aPath = GetClassPath(Base, aPath)
    return aPath + '/' + aClass.__name__

def Test4():
    File = 'greenery.json'
    with open(File) as FileData:
        Data = json.load(FileData)
    Manager = TManager()
    Manager.Load(Data['Gpio']['Class'])
    while True:
        Manager.Signal(['WaterPump'])
        time.sleep(1)

#Test4()
#Test3()
#print(ClassPath(TC, ''))

C = TC()
C.GetPath()


