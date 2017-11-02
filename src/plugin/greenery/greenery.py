# Created: 13.10.2017
# Vladimir Vons, VladVons@gmail.com



import time
import multiprocessing
#
from inc.Common import *
from Section import *
from Manager import TManager


#---
class Gpio(TSectionVarExec):
    def __init__(self, aParent, aName):
        super().__init__(aParent, aName)

    def Test(self):
        print('Name:', self.Name, ', GetKeys:', self.GetKeys(), ', Field', self.GetField('Run/Loop'))
        #print('Run:', self.GetVar('Run'), self.GetValue('WaterPump'))

    def CallBack_OnValue(self, aObj):
        Tag = aObj.Tag
        if (Tag):
            Info = 'Tag {:15}, Alias {:25}, Value {:8}, State {:1}'.format(aObj.Tag, aObj.Alias, aObj.Value, aObj.Param.State)
            print('OnValue', Info)

    def Run(self):
        self.Test()

        Manager = TManager()
        Manager.OnValue = self.CallBack_OnValue
        Manager.Load(self.Data)
        Manager.Run()
