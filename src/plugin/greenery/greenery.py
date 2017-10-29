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
        print('Name', self.Name, 'Startup', self.GetVar('Startup'), 'GetKeys', self.GetKeys(), 'Gpio', self.GetValue('WaterPump'),  self.GetField('WaterPump'))

    def OnState(self, aObj):
        Alias = aObj.Alias
        print('OnState', aObj.Alias)

    def Run(self):
        Manager = TManager()
        Manager.OnState = self.OnState
        Manager.Load(self.Data)
        Manager.Run()
