# Created: 18.08.2016
# Vladimir Vons, VladVons@gmail.com
#
# encode adn decode serilization with JSON


import json
import logging
from AppMan import *


#---
class TSerialize():

    def __init__(self):
        # if TRUE some class variable must be cleared with Purge()
        self.CasheObj = False

        self.Clear()
        self.LastError = ""

    def Clear(self):
        self.Data = {}

    def Purge(self, aName):
        Result = 0
        Data = {}
        for Item in self.Data:
            if (Item.startswith(aName)):
                Result += 1
            else:
                Data[Item] = self.Data[Item]
        self.Data = Data
        return Result

    def AddObj(self, aName, aObj):
        self.LastError = ""
        try:
            #globals()[aName]()
            aObj
            self.Data[aName] = aObj
        except NameError as E:
            self.LastError = self.LastError
            print(self.LastError)

    def GetObj(self, aName):
        #print("GetObj", aName)

        if (aName in self.Data):
            return self.Data[aName]

        Result = None
        Delim  = "."
        Path   = ""
        self.LastError = ""
        Items  = aName.strip().split(Delim)
        for i in range(len(Items)):
            Item = Items[i]
            Char = ("" if (Path == "") else Delim)
            Path += Char + Item

            if (Path in self.Data):
                Result = self.Data[Path]
            else:
                try:
                    if (i == 0):
                        Result = globals()[Item]()
                        # Class constructor alwys in cache
                        self.Data[Path] = Result
                    else:
                        Result = getattr(Result, Item)
                        if (self.CasheObj):
                            self.Data[Path] = Result
                except Exception as E:
                    Result = None
                    self.LastError = "TSerialize->GetObj Error: " + E.message + " in " + Path
                    print(self.LastError)

        return Result

    def CallObj(self, aObj, aArgs):
        #print("CallObj", aObj, aArgs)

        self.LastError = ""
        try:
            if (aArgs):
                Result = aObj(*aArgs)
            else:
                Result = aObj()
        except Exception as E:
            self.LastError = "TSerialize->CallObj Error: " + E.message
            #Result = None
            Result = self.LastError
            print(self.LastError)

        return Result

    def SplitFunc(self, aFuncStr):
        # recognize string "ClassName.FuncName('Param')"
        Match = re.match("(?P<Name>[\w\.]+)\((?P<Arg>.*)\)", aFuncStr)
        if (Match):
            return Match.groupdict()
        else:
            return {}

    def CallFunc(self, aFuncName, aArgs = []):
        Arr = self.SplitFunc(aFuncName)
        if (Arr):
            aFuncName = Arr["Name"]
            aArgs     = Arr["Arg"].replace("'", "").split(",")

        Obj = self.GetObj(aFuncName)
        if (Obj):
          ObjType = type(Obj).__name__
          if (ObjType in ["instancemethod", "function"]):
              return self.CallObj(Obj, aArgs)
          else:
              self.LastError = "TSerialize->CallFunc Error: Object is not callable: " + aFuncName + " " + ObjType
        else:
          return self.LastError

    def GetProp(self, aPropName):
        Obj = self.GetObj(aPropName)
        if (Obj):
          return Obj
        else:
          return self.LastError

    @staticmethod
    def CEncodeData(aData):
        return json.dumps( {"Data": aData} )

    def EncodeData(self, aData):
        return TSerialize.CEncodeData(aData)

    def EncodeFuncAuth(self, aUser, aPassw):
        return self.EncodeFunc("AuthUser", aUser, aPassw)

    def EncodeFunc(self, aFuncName, *aArgs):
        if (len(aArgs) == 0):
            Data = {"Type": "Func", "Name": aFuncName}
        else:
            Data = {"Type": "Func", "Name": aFuncName, "Arg": aArgs}
        return json.dumps(Data)

    def EncodeProp(self, aPropName):
        Data = {"Type": "Prop", "Name": aPropName}
        return json.dumps(Data)

    def Decode(self, aData):
        Result = ""

        if (aData):
            try:
                Node = json.loads(aData)
            except Exception as E:
                Node   = None
                Result = "TSerialize->Decode Error: " + E

            if (Node):
                Type = Node.get("Type")
                Name = Node.get("Name")
                if (Type == "Func"):
                    if ("Arg" in Node):
                        Result = self.CallFunc(Name, Node.get("Arg"))
                    else:
                        Result = self.CallFunc(Name)
                elif (Type == "Prop"):
                    Result = self.GetObj(Name)
                else:
                    Result = "TSerialize->Decode Error: Unknown type: " + Type

        return Result

    def DecodeFuncName(self, aData):
        Result = ""

        Node = json.loads(aData)
        if (Node["Type"] == "Func"):
            Result = Node.get("Name")

        return Result

    def DecodeFuncArg(self, aData):
        Node = json.loads(aData)
        return Node.get("Arg")
