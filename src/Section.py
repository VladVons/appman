# Created: 30.08.2016
# Vladimir Vons, VladVons@gmail.com

import re
import time
from inc.Common import *


cFieldValue   = "Value"
cFieldCmd     = "Cmd"
cFieldCmdExec = "CmdExec"
cFieldDescr   = "Descr"
cObjDelim     = ";"
cVarPrefix    = "$<"
cVarSufix     = ">"
cVarArg       = "Arg"


#__all__ = ["TSUtil", "TSOption", "TSVar", "TSService", "TSCheck", "TSUser", "TSAbout", "TSInstall", "TSUninstall"]

class TSection():

    def __init__(self, aParent, aName):
        self.Parent  = aParent
        self.Name    = aName
        self.Clear()

    def Clear(self):
        self.Data = {}


    def _AddItems(self, aItems, aAddComma = False):
        if (aItems):
            for Item in aItems:

                if (Item in self.Data):
                    for Key in aItems[Item].keys():
                        Data = self.Data[Item].get(Key, "")
                        if (aAddComma and Data):
                            self.Data[Item][Key] = Data + cObjDelim + aItems[Item][Key]
                        else:
                            self.Data[Item][Key] = aItems[Item][Key]
                else:
                    self.Data[Item] = aItems[Item]

    def _Load(self, aNode):
        # ToDo
        def RemoveEmptyMethods():
            if (len(self.Data) > 0 and hasattr(self, "Methods")):
                for Method in self.Methods:
                    if (self.GetItem(Method) == ""):
                        Obj = getattr(self, Method)
                        print("xxx", Method, Obj)
                        del(Obj)

        self._AddItems(TDict.FindNode(aNode, self.Name))
        #RemoveEmptyMethods()

    def GetItem(self, aName, aDef = ""):
        return TDict.FindNodeDef(self.Data, aName, aDef)

    def SetItem(self, aName, aValue):
        self.Data[aName] = aValue

    def GetKeys(self):
        return self.Data.keys()


#---
class TSectionVar(TSection):

    def GetField(self, aName, aDef = ""):
        Value = self.GetItem(aName, aDef)
        return self.Parent.Var.Parse(Value)

    def GetFieldList(self, aName):
        Str = self.GetField(aName)
        if (Str):
            return Str.split(cObjDelim)
        else:
            return []

    def GetValue(self, aName, aDef = ""):
        return self.GetField(aName + "/" + cFieldValue, aDef)

    def GetCmd(self, aName, aDef = ""):
        return self.GetField(aName + "/" + cFieldCmd, aDef)

    def GetVar(self, aName, aDef = ""):
        return self.Parent.Var.GetValue(aName, aDef)

    def SetVar(self, aName, aValue):
        self.Parent.Var.Data[aName] = aValue

    def GetPairs(self, aName):
        Result = {}
        for Item in self.GetKeys():
            Result[Item] = self.GetField(Item + "/" + aName)
        return Result

#---
class TSectionVarExec(TSectionVar):
    def __init__(self, aParent, aName ):
        TSectionVar.__init__(self, aParent, aName)

        self.__DictReplace = TDictReplace(cVarPrefix, cVarSufix)
        self.__DictReplace.CallBack = self.__Replace

    def __Replace(self, aName):
        Path   = self.__DictReplace.CurField + "/" + aName
        Result = self.GetField(Path)
        print("--- TSectionVarExec->Replace", Path, Result)
        return Result

    def ExecStr(self, aStr, aFindRepl = {}):
        Result  = ""
        Items   = aStr.split(cObjDelim)
        if (Items):
            for Item in Items:
                Parsed  = TStr.MultiRepl(Item, aFindRepl)
                Result += TShell.ExecM(Parsed) + "\n"
        return Result

    def ExecFieldDict(self, aName, aField, aFindRepl = {}):
        self.__DictReplace.CurField = aName
        CmdOrig = self.GetField(aName + "/" + aField)
        Cmd     = self.__DictReplace.Parse(CmdOrig)
        print("--- TSectionVarExec->ExecField", aName, aField, Cmd)
        Result  = self.ExecStr(Cmd, aFindRepl)
        return Result

    def ExecFieldList(self, aName, aField, aArg = []):
        FindRepl = {}
        for Idx in range(0, len(aArg)):
            Key = cVarPrefix + cVarArg + str(Idx + 1) + cVarSufix
            FindRepl[Key] = aArg[Idx]
        return self.ExecFieldDict(aName, FindRepl)

    def ExecValue(self, aName, aField = cFieldCmdExec):
        Result = ""

        Value = self.GetVar(self.GetValue(aName), self.GetVar(aName)).strip()
        if (Value):
            for Item in Value.split(cObjDelim):
                Idx = 0
                FindRepl = {}
                for Arg in Item.split("|"):
                    Idx += 1
                    Key = cVarPrefix + cVarArg + str(Idx) + cVarSufix
                    FindRepl[Key] = Arg
                Result += self.ExecFieldDict(aName, aField, FindRepl)
        return Result

    def ExecField(self, aName, aField = cFieldCmdExec):
        return self.ExecFieldDict(aName, aField)

    def ExecVar(self, aName, aArg = ""):
        Value = self.GetVar(aName)
        if (Value):
            return TShell.ExecM(Value + " " + aArg)
        else:
            return ""

#---
class TSVar(TSectionVar):
    def __init__(self, aParent, aName):
        TSectionVar.__init__(self, aParent, aName)

        self.__DictReplace = TDictReplace(cVarPrefix, cVarSufix)
        self.__DictReplace.CallBack = self.__Replace

    def __Replace(self, aName):
        return self.GetValue(aName)

    def Parse(self, aStr):
        return self.__DictReplace.Parse(aStr)

    def GetValue(self, aName, aDef = ""):
        Value = self.GetItem(aName + "/" + cFieldValue, aDef)
        return self.Parse(Value)



#---
class TSConfig(TSectionVar):
    def GetKeyField(self, aKey, aField = ""):
        return self.GetField("Main/Field/" + aKey + "/" + aField)

    def Validate(self, aKey, aValue):
        Result = (self.GetKeyField(aKey) != "")
        if (Result):
            Caller = sys._getframe(2).f_code.co_name
            #print("aaa", aKey, aValue, Caller)

        return Result

#---
class TSOption(TSectionVar):

    def UserAdd(self, aName):
        pass

    def IsAllow(self, aSect, aItem, aStr):
        OptDeny  = self.GetValue("Policy/{}/Deny/{}".format(aSect, aItem))
        if (OptDeny != ""):
            if (re.match(OptDeny, aStr)):
                return False

        OptAllow = self.GetValue("Policy/{}/Allow/{}".format(aSect, aItem))
        if (OptAllow != ""):
            if (not re.match(OptAllow, aStr)):
                return False

        return True
