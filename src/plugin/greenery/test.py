#!/usr/bin/python3

import json
import time
from libtimer import *
from control import *
from manager import *



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

def Test4():
    File = 'greenery.json'
    with open(File) as FileData:
        Data = json.load(FileData)
    Manager = TManager()
    Manager.Load(Data['Gpio']['Class'])
    while True:
        Manager.Signal(['WaterPump'])
        time.sleep(1)



Test4()


