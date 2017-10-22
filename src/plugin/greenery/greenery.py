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

    def __RunThread(self, aName):
        GpioSession = TGpioSession(self, aName)
        GpioSession.Run()

    def __CreateThread(self, aTarget, aArgs):
        process = multiprocessing.Process(target = aTarget, args = aArgs)
        process.daemon = True
        process.start()
        time.sleep(0.5)

    def Test(self):
        print('Name', self.Name, 'Startup', self.GetVar('Startup'), 'GetKeys', self.GetKeys(), 'Gpio', self.GetValue('WaterPump'),  self.GetField('WaterPump'))

    def Run(self):
        if (not self.Running):
            self.Running = True
            self.Manager.Load(self.GetField('Class'))
            while True:
                self.Manager.Signal(['WaterPump'])
                time.sleep(1)
