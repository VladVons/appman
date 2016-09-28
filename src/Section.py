# Created: 30.08.2016
# Vladimir Vons, VladVons@gmail.com

import re
import time
from inc.Common import *


cFieldValue = "Value"
cFieldCmd   = "Cmd"
cFieldDescr = "Descr"
cObjDelim   = ";"
cVarPrefix  = "$<"
cVarSufix   = ">"
cVarArg     = "Arg"


#__all__ = ["TSUtil", "TSOption", "TSVariable", "TSService", "TSCheck", "TSUser", "TSAbout", "TSInstall", "TSUninstall"]

class TSection():

    def __init__(self, aParent, aName):
        self.Parent  = aParent
        self.Name    = aName
        self.Clear()

    def Clear(self):
        self.Data = {}


    def _AddItems(self, aItems, aAddComma=True):
        if (aItems):
            for Item in aItems:
                if (aAddComma and (Item in self.Data)):
                    self.Data[Item][cFieldValue] += cObjDelim + aItems[Item][cFieldValue]
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

        self._AddItems(TArray.FindNode(aNode, self.Name))
        #RemoveEmptyMethods()

    def GetItem(self, aName, aDef = ""):
        return TArray.FindNodeDef(self.Data, aName, aDef)

    def SetItem(self, aName, aValue):
        self.Data[aName] = aValue

    def GetKeys(self):
        return self.Data.keys()


#---
class TSectionVar(TSection):

    def GetField(self, aName, aDef = ""):
        Value = self.GetItem(aName, aDef)
        return self.Parent.Variable.Parse(Value)

    def GetValue(self, aName, aDef = ""):
        return self.GetField(aName + "/" + cFieldValue, aDef)

    def GetCmd(self, aName, aDef = ""):
        return self.GetField(aName + "/" + cFieldCmd, aDef)

    def GetDescr(self, aName, aDef = ""):
        return self.GetField(aName + "/" + cFieldDescr, aDef)

    def GetVar(self, aName, aDef = ""):
        return self.Parent.Variable.GetValue(aName, aDef)

    def SetVar(self, aName, aValue):
        self.Parent.Variable.Data[aName] = aValue

    def GetPairs(self, aName):
        Result = {}
        for Item in self.GetKeys():
            Result[Item] = self.GetField(Item + "/" + aName)
        return Result

#---
class TSectionVarExec(TSectionVar):
    def __init__(self, aParent, aName ):
        TSectionVar.__init__(self, aParent, aName)

        self.__DicReplace = TDicReplace(cVarPrefix, cVarSufix)
        self.__DicReplace.CallBack = self.__Replace

    def _DelMethods(self):
        for Item in self.Methods:
            print("-----123", Item)

    def __Replace(self, aName):
        Path = self.__DicReplace.CurField + "/" + aName
        return self.GetField(Path)

    def ExecStr(self, aStr, aFindRepl = {}):
        Result  = ""
        Items   = aStr.split(cObjDelim)
        if (Items):
            for Item in Items:
                Parsed  = TString.MultiRepl(Item, aFindRepl)
                Result += TShell.ExecM(Parsed) + "\n"
        return Result

    def ExecCmdDic(self, aName, aFindRepl = {}):
        self.__DicReplace.CurField = aName
        CmdOrig = self.GetCmd(aName, self.GetVar(cFieldCmd + "_" + aName))
        Cmd     = self.__DicReplace.Parse(CmdOrig)
        return self.ExecStr(Cmd, aFindRepl)

    def ExecCmd(self, aName, aArg = []):
        FindRepl = {}
        for Idx in range(0, len(aArg)):
            Key = cVarPrefix + cVarArg + str(Idx + 1) + cVarSufix
            FindRepl[Key] = aArg[Idx]
        return self.ExecCmdDic(aName, FindRepl)

    def ExecValue(self, aName, aValue = ""):
        Result  = ""

        if (aValue == ""):
            Items = self.GetValue(aName).split(cObjDelim)
        else:
            Items = aValue.split(cObjDelim)

        if (Items):
            for Item in Items:
                if (Item):
                    Idx = 0
                    FindRepl = {}
                    for Arg in Item.split("|"):
                        Idx += 1
                        Key = cVarPrefix + cVarArg + str(Idx) + cVarSufix
                        FindRepl[Key] = Arg
                    Result += self.ExecCmdDic(aName, FindRepl)
        return Result

    def ExecVar(self, aName, aArg = ""):
        Value = self.GetVar(aName)
        if (Value):
            return TShell.ExecM(Value + " " + aArg)
        else:
            return ""


#---
class TSVariable(TSectionVar):
    def __init__(self, aParent, aName):
        TSectionVar.__init__(self, aParent, aName)

        self.__DicReplace = TDicReplace(cVarPrefix, cVarSufix)
        self.__DicReplace.CallBack = self.__Replace

    def __Replace(self, aName):
        return self.GetValue(aName)

    def Parse(self, aStr):
        return self.__DicReplace.Parse(aStr)

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
