# Created: 11.09.2016
# Vladimir Vons, VladVons@gmail.com

from inc.Common import *
from Section import *

#---
class TSCmd(TSectionVarExec):

    def __init__(self, aParent, aName):
        TSectionVarExec.__init__(self, aParent, aName)

        self.Methods = ["ServiceStart","ServiceStop","ServiceRestart","ServiceReload",\
                "ShowPort","ShowService","ShowProcess","ShowLog","ShowMan",\
                "PkgAddPpa","PkgInstall"]

    def ServiceStart(self):
        return self.ExecValue("ServiceStart")

    def ServiceStop(self):
        return self.ExecValue("ServiceStop")

    def ServiceRestart(self):
        if (self.GetValue("ServiceRestart")):
            Result = self.ExecValue("ServiceRestart")
        else:
            Result =  self.ServiceStop()
            time.sleep(1)
            Result += self.ServiceStart()
        return Result

    def ServiceReload(self):
        if (self.GetValue("ServiceReload")):
            return self.ExecValue("ServiceReload")
        else:
            return self.Restart()

    def ShowPort(self):
        return self.ExecValue("ShowPort")

    def ShowService(self):
        return self.ExecValue("ShowService")

    def ShowProcess(self):
        return self.ExecValue("ShowProcess")

    def ShowLog(self):
        return self.ExecValue("ShowLog")

    def ShowMan(self):
        return self.ExecValue("ShowMan")

    def PkgAddPpa(self):
        return self.ExecValue("PkgAddPpa")

    def PkgInstall(self):
        Result  = self.PkgAddPpa() + "\n"
        Result += self.ExecValue("PkgInstall")
        return Result

    def PkgRemove(self):
        Result  = self.ExecValue("PkgRemove", self.GetValue("PkgInstall"))
        Result += self.ExecValue("PkgRemove")
        return Result

    def PkgVersion(self):
        PkgName = TString.GetPart(self.GetValue("PkgInstall"), 0, cObjDelim)
        return self.ExecValue("PkgVersion", PkgName)


#---
class TSUser(TSectionVarExec):

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
class TSUtil(TSectionVarExec):

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
