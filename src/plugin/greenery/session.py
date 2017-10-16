# Created: 13.10.2017
# Vladimir Vons, VladVons@gmail.com

import time
import libtimer

#---
class TGpioSession():
    def __init__(self, aParent, aName):
        self.Parent = aParent
        self.Name   = aName
 
    def Run(self):
        print("Start session")
        while True:
            #print('Item', self.Name, self.Parent.GetVar('Startup'), self.Parent.Data)
            print('Item', self.Name, self.Parent.GetItem(self.Name))
            time.sleep(3) 
