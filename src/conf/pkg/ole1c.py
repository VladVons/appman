from Section import *

class TOle1c(TSectionVar):
    def Connect(self, aName, aPassw):
        return "Connect: " + aName + " " + self.GetVar("Path")

    def GetDoc(self, aNo):
        return "GetDoc: " + aNo
