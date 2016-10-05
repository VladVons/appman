# Created: 11.09.2016
# Vladimir Vons, VladVons@gmail.com

from inc.Common import *
from Section import *

#---
class Cmd(TSectionVarExec):

    def __init__(self, aParent, aName):
        TSectionVarExec.__init__(self, aParent, aName)

    def ServiceRestart(self):
        if (self.HasKey("ServiceRestart")):
            Result = self.ExecField("ServiceRestart")
        else:
            Result =  self.ExecField("ServiceStop") + "\n"
            time.sleep(1)
            Result += self.ExecField("ServiceStart")
        return Result

    def PkgInstall(self):
        Result = ""

        if (self.HasKey("PkgAddPpa")):
            Result  = self.ExecField("PkgAddPpa") + "\n"

        Result += self.ExecField("PkgInstall")
        return Result

    def PkgVersion(self):
        PkgName = TStr.GetPart(self.GetVar("PkgInstall"), 0, cObjDelim)
        return self.ExecField("PkgVersion", PkgName)


#---
class User(TSectionVarExec):

    def Add(self, aName, aPassw = ""):
        return self.ExecCmd("Add", [aName, aPassw])

    def Del(self, aName):
        return self.ExecCmd("Del", [aName])

    def Enable(self, aName):
        return self.ExecCmd("Enable", [aName])

    def Disable(self, aName):
        return self.ExecCmd("Disable", [aName])

    def Password(self, aName, aPassw):
        return self.ExecCmd("Password", [aName, aPassw])

    def List(self):
        return self.ExecCmd("List")


#---
class Util(TSectionVarExec):

    def FileRead(self, aFileName):
        return TFile.LoadFromFileToStr(aFileName)

    def FileExist(self, aFileName):
        return os.path.isfile(aFileName)

    def Print(self, aValue):
        print(aValue)
        return aValue

    def IsRoot(self):
        Value = self.ExecVar("Util_IsRoot")
        return (Value != "")

    def OS(self):
        return self.ExecVar("Util_OS")

    def MemTotal(self):
        return self.ExecVar("Util_MemTotal")

    def Top(self):
        return self.ExecVar("Util_Top")

    def Reboot(self):
        return self.ExecVar("Util_Reboot")
