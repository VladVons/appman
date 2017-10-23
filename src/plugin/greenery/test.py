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

def Test2():
    File = 'greenery.json'
    with open(File) as FileData:    
        Data1 = json.load(FileData)
        Data2 = Data1['Gpio']['Class']
        Keys1 = Data2[0].keys()
        Keys2 = ['Enable', 'Param', 'Class', 'Alias', 'Ref']
        #print([i for i in Keys1 if i in Keys2])
        Diff = set(Keys1) - set(Keys2)
        if (Diff):
            print('Err ' + str(Diff))
        else:
            print('OK')

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

