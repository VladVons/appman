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
        self.Running = False

        self.Manager = TManager()
        Manager.OnSignal = OnSignal

    def __RunThread(self, aName):
        GpioSession = TGpioSession(self, aName)
        GpioSession.Run()

    def __CreateThread(self, aTarget, aArgs):
        process = multiprocessing.Process(target = aTarget, args = aArgs)
        process.daemon = True
        process.start()
        time.sleep(0.1)

    def Test(self):
        print('Name', self.Name, 'Startup', self.GetVar('Startup'), 'GetKeys', self.GetKeys(), 'Gpio', self.GetValue('WaterPump'),  self.GetField('WaterPump'))

    def OnSignal(self, aParent, aObj):
        Alias = aObj.Alias
        if (Alias == 'W1_Sensor_DS'):
            print(aObj.Alias, aObj.Get())

    def Run(self):
        if (not self.Running):
            Manager.Run(self.Data)
            self.Running = false
