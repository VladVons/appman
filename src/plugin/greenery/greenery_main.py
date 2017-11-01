#!/usr/bin/python2

# https://collectd.org/documentation/manpages/collectd-python.5.shtml#examples

import time
import json
import os
#
from Manager import *


class TParam():
    def Load(self, aItems):
        for Item in aItems:
            setattr(self, Item, aItems.get(Item))

class TCollect():
    def __init__(self):
        self.Values = {}
        self.TimeStart = int(time.time())

        self.Param = TParam()
        self.Param.Load({'FileTmp':'/tmp/greenery_collect.tmp', 'FileConfig':'greenery.json'})

    def Uptime(self):
        return int(time.time()) - self.TimeStart

    def FileWrite(self, aData):
        with open(self.Param.FileTmp, 'w') as File:
            json.dump(aData, File)

    def CallBack_OnValue(self, aObj):
        Tag = aObj.Tag
        if (Tag):
            Info = 'Tag {:15}, Alias {:25}, Value {:8}, State {:1}'.format(aObj.Tag, aObj.Alias, aObj.Value, aObj.Param.State)
            print('OnValue', Info)

            if (not Tag in self.Values):
                self.Values[Tag] = {}
            self.Values[Tag][aObj.Alias] = aObj.Value

            if (self.Uptime() % 17):
                self.FileWrite(self.Values)

    def Run(self):
        if (os.path.exists(self.Param.FileConfig)):
            with open(self.Param.FileConfig) as FileData:
                Data = json.load(FileData)

            Manager = TManager()
            Manager.OnValue  = self.CallBack_OnValue
            Manager.Load(Data['Gpio'])
            Manager.Run()
        else:
            print('---- File %s doesnt exists in %s' % (self.Param.FileConfig, os.getcwd()))


Collect = TCollect()
Collect.Run()
