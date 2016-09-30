# Created: 21.08.2016
# Vladimir Vons, VladVons@gmail.com

import sys
import os
import subprocess
import re


class TDicReplace:
    def __init__(self, aPrefix = "$<", aSufix = ">"):
        self.Data     = {}
        self.Err      = []
        self.CallBack = None
        self.SetDelim(aPrefix, aSufix)

    def SetDelim(self, aPrefix, aSufix):
        self.Prefix   = aPrefix
        self.Sufix    = aSufix
        self.Pattern  = "\\" + self.Prefix + "([^" + "\\" + self.Prefix + self.Sufix + "]*)" + self.Sufix

    # search macros $<xxx> in aStr and repalce it with value returned by aFunc
    def Parse(self, aStr):
        if (aStr and (type(aStr) in [str, unicode]) and (aStr.find(self.Prefix) != -1)):
            Items = re.findall(self.Pattern, aStr)
            if (Items):
                self.Err = []
                for Item in Items:
                    Item = Item.strip()
                    if (self.CallBack):
                        Repl = self.CallBack(Item)
                    else:
                        Repl = self.Data.get(Item, "")

                    if (Repl == ""):
                        self.Err.append(Item)
                    else:
                        aStr = aStr.replace(self.Prefix + Item + self.Sufix, Repl)

                if (len(self.Err) == 0):
                    aStr = self.Parse(aStr)
        return aStr


#---
class TStr():

    @staticmethod
    def MultiRepl(aStr, aFindRepl):
        for Find, Repl in aFindRepl.iteritems():
            aStr = aStr.replace(Find, Repl)

        return aStr

    @staticmethod
    def ActionDelim(self, aStr, aFunc, aDelim = ","):
        Result = ""
        Items = aStr.split(aDelim)
        for Item in Items:
            Item = Item.strip()
            if (Item != ""):
                Result += aFunc(Item)

        return Result

    @staticmethod
    def GetPart(aStr, aIdx, aDelim = ","):
        Items = aStr.split(aDelim)
        if (aIdx < len(Items)):
            return Items[aIdx]
        else:
            return ""

#---
class TShell():

    @staticmethod
    def ExecM(aCmd, aMsg = ""):
        print("Exec in:", aCmd, aMsg)

        # return os.system(aCmd)
        Pipe = subprocess.Popen(aCmd, shell=True, stdout=subprocess.PIPE)
        Result = Pipe.communicate()[0]

        #print("Exec out: " + Result)
        return Result


#---
class TFile():
    @staticmethod
    def LoadFromFileToStr(aFileName):
        Result = ""
        if (os.path.isfile(aFileName)):
            File = open(aFileName, 'r')
            Result = File.read()
            File.close()
        return Result

    @staticmethod
    def LoadFromFileToList(aName):
        Result = []
        if (os.path.isfile(aName)):
            with open(aName, "r") as File:
                Result = File.readlines()
        return Result

    @staticmethod
    def SaveToFileFromList(aName, aList):
        with open(aName, 'w') as File:
            for Line in aList:
                File.write(Line)


        if (os.path.isfile(aFileName)):
            with open(aFileName, "r") as File:
                Result = File.readlines()
 
    @staticmethod
    def Find(aName, aDirs):
        Result = []
        for Dir in aDirs:
            Path = Dir + "/" + aName
            if (os.path.isfile(Path)):
                Result.append(Path)

        return Result

    @staticmethod
    def GetCoreName(aPath):
        return os.path.splitext(os.path.basename(aPath))[0]



class TDict():

    @staticmethod
    def FindNode(aNode, aPath):
        for Item in aPath.strip("/").split("/"):
            if (Item != ""):
                Value = aNode.get(Item)
                if (Value == None):
                    return None
                else:
                    aNode = Value
        return aNode

    @staticmethod
    def FindNodeDef(aNode, aPath, aDef):
        Node = TDict.FindNode(aNode, aPath)
        if (Node == None):
            return aDef
        else:
            return Node

    @staticmethod
    def Filter(aNode, aRegEx):
        Result = []
        if (aNode):
            for Item in aNode:
                if (Item != "" and re.match(aRegEx, Item)):
                    Result.append(Item)

        return Result

class TList():

    @staticmethod
    def Find(aList, aData):
        if (aData in aList):
            return aList.index(aData)
        return -1



#---
class TSocket():
    @staticmethod
    def Receive(aConn, aBufSize):
        Result = ""
        while True:
            Data = aConn.recv(aBufSize)
            if (Data):
                Result += Data
                if (len(Data) < aBufSize):
                    break
            else:
                break

        return Result


#---
class TObject():
    @staticmethod
    def GetName(aObj):
        return aObj.__class__.__name__
