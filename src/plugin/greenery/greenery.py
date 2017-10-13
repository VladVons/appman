# Created: 11.09.2016
# Vladimir Vons, VladVons@gmail.com

from inc.Common import *
from Section import *

#---
class TGpio(TSectionVarExec):
    def __init__(self, aParent, aName):
        print("TGpio-init")
        TSectionVarExec.__init__(self, aParent, aName)

    def Test(self):
        print("Gpio-Test")
