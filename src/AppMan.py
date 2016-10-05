# Created: 17.08.2016
# Vladimir Vons, VladVons@gmail.com
#
# Application manager
# autopep8 AppMan.py > AppMan.py8

import os
import sys
import json
import importlib
import inspect
import ast
import re
import datetime

from inc.Common import *
from Section import *
from Editor import *


sys.path.insert(0, './conf')
sys.path.insert(0, './conf/pkg')


__version__ = {"Sys_AppVer": "1.031", "Sys_Mail": "VladVons@gmail.com"}
cPathConf   = "conf/pkg"

#---
class TAppMan():

    def __init__(self):
        self.Path = ["/etc/appman", "conf", cPathConf]
        os.environ["PATH"] += os.pathsep + os.pathsep.join(self.Path)
        self.TimeStart = datetime.datetime.now()

        self.Clear()

    def Clear(self):
        self.Editor   = None

        self.Option = TSOption(self, "Option")
        self.Var    = TSVar(self, "Var")
        self.Config = TSConfig(self, "Config")

        Items = self.GetInfo()
        for Item in Items:
            self.Var.SetItem(Item, {"Value":Items[Item]})

        self.__LoadFileSearch("appman.json")

    def LoadEditor(self, aName):
        Node = self.Config.GetItem(aName)
        if (Node):
            self.Editor = None
            Type = Node.get("Type")
            if (Type in ["Ini", "Conf", "Dir"]):
                if (Type == "Ini"):
                    self.Editor = TEditorIni()
                elif (Type == "Conf"):
                    self.Editor = TEditorConf()
                elif (Type == "Dir"):
                    self.Editor = TEditorDir()

                self.Editor.CharComment = Node.get("Comment", "#")

                if (Node.get("Validate", True)):
                    self.Editor.OnKeyValid  = self.Config.Validate

                self.Editor.LoadFromFile(Node.get("Path"))
            else:
                print("Unknown editor type")

    # Dynamicly add classes from a aFile
    # Add class Items from json file by ClassName
    def __AddModule(self, aFileName, aCoreName, aNode):
        print("AddModule", aFileName, aCoreName)
        Lib = importlib.import_module(aCoreName)
        Objects = ast.parse(TFile.LoadFromFileToStr(aFileName))
        for Item in ast.walk(Objects):
            if (isinstance(Item, ast.ClassDef)):
                TCl = getattr(Lib, Item.name)
                Cl  = TCl(self, Item.name)
                setattr(self, Item.name, Cl)
                Cl._AddItems(TDict.FindNode(aNode, Item.name))

    def __LoadFileSearch(self, aFileName):
        Result = False
        Files = TFile.Find(aFileName, self.Path)
        for File in Files:
            Result |= self.__LoadFile(File)

        return Result

    def __LoadFile(self, aFileName):
        #print("LoadFile", aFileName)

        Result = os.path.isfile(aFileName)
        if (Result):
            with open(aFileName) as File:
                root = json.load(File)

            IncludeFile = TDict.FindNode(root, "Include/File/" + cFieldValue)
            if (IncludeFile):
                for Item in IncludeFile.split(cObjDelim):
                    Value = self.Var.Parse(Item)
                    self.__LoadFileSearch(Value)

            self.Option._Load(root)
            self.Var._Load(root)
            self.Config._Load(root)

            CoreName = TFile.GetCoreName(aFileName)
            Files = TFile.Find(CoreName + ".py", self.Path)
            for File in Files:
                self.__AddModule(File, CoreName, root)

        return Result

    def LoadFile(self, aFileName):
        self.Clear()
        Result = self.__LoadFileSearch(aFileName)
        self.LoadEditor("Main")
        return Result

    def GetInfo(self):
        import platform, getpass

        Result = __version__
        Result["Sys_Platform"]  = platform.system().lower()
        Result["Sys_Release"]   = platform.release()
        Result["Sys_User"]      = getpass.getuser()
        Result["Sys_TimeStart"] = str(self.TimeStart)
        Result["Sys_TimeNow"]   = str(datetime.datetime.now())
        return Result

    def __GetApi(self, aClass, aPath):
        Result = []

        Items = dir(aClass)
        for Item in Items:
            # skip hidden methods and recursion in instance of Parent
            if (not re.findall("(_|Parent)", Item)):
                Obj = getattr(aClass, Item)
                if (inspect.ismethod(Obj)):
                    Result.append(aPath + Item)
                elif (hasattr(Obj, '__class__')):
                    Result += self.__GetApi(Obj, aPath + Item + ".")
        return Result

    def GetListApi(self):
        return self.__GetApi(self,  TObject.GetName(self) + ".")

    def GetListConf(self):
        Result = []
        for File in os.listdir(cPathConf):
            if File.endswith('.json'):
                Result.append(File)
        Result.sort()
        return Result
