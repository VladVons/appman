# Created: 13.10.2017
# Vladimir Vons, VladVons@gmail.com

import time
import multiprocessing

from inc.Common import *
from Section import *
from session import *


#---
class Gpio(TSectionVarExec):
    def __init__(self, aParent, aName):
        TSectionVarExec.__init__(self, aParent, aName)
        self.Running = False

    def Test(self):
        print('Name', self.Name, 'Startup', self.GetVar('Startup'), 'GetKeys', self.GetKeys(), 'Gpio', self.GetValue('WaterPump'), self.Data)

    def __RunThread(self, aName):
        GpioSession = TGpioSession(self, aName)
        GpioSession.Run()

    def __CreateThread(self, aTarget, aArgs):
        process = multiprocessing.Process(target = aTarget, args = aArgs)
        process.daemon = True
        process.start()
        time.sleep(0.5)

    def Run(self):
        if (not self.Running):
            self.Running = True

            Str = self.GetVar('Startup')
            for Item in Str.split(cObjDelim):
                if (Item in self.GetKeys()):
                    self.__CreateThread(self.__RunThread, [Item])
                else:
                    print('Gpio has no %s' % Item)

            while True:
                time.sleep(10) 
