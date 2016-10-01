#!/usr/bin/python

# Created: 21.08.2016
# Vladimir Vons, VladVons@gmail.com, OK


import re
from AppMan import *


def TestAppMan(aJson):

    AppMan = TAppMan()
    #for Item in AppMan.GetApi():
        #print(Item)

    #print("AppMan.GetVersion",          AppMan.GetVersion())
    #print("AppMan.GetListConf",         AppMan.GetListConf())
    print("AppMan.LoadFile",            AppMan.LoadFile(aJson))
    print("AppMan.Variable.GetValue",   AppMan.Variable.GetValue("Descr"))
    #print("AppMan.Variable.GetPairs",   AppMan.Variable.GetPairs("Value"))
    #print("AppMan.Editor.PathName",     AppMan.Editor.PathName)
    #print("AppMan.Editor.GetPath",      AppMan.Editor.GetPath())


    #print("AppMan.Editor.KeyGet",       AppMan.Editor.Section.KeyGet("FSCharset"))
    #print("AppMan.Editor.KeyList",       AppMan.Editor.Section.KeyList())
    #print("AppMan.Editor.KeyDelete",     AppMan.Editor.Section.KeyDelete("FSCharset"))
    #print("AppMan.Editor.KeySet:PureDB",    AppMan.Editor.Section.KeySet("PureDB", "xyz1"))
    #print("AppMan.Editor.KeySet:FSCharset", AppMan.Editor.Section.KeySet("FSCharset", "UTF-9"))
    #print("AppMan.Editor.SectionSet",   AppMan.Editor.SectionSet("mysqld"))
    #print("AppMan.Editor.KeyGet",       AppMan.Editor.Section.KeyGet("socket"))
    #print("AppMan.Editor.KeySet",       AppMan.Editor.Section.KeySet("socket", "MySocket-mysqld"))
    #print("AppMan.Editor.KeySet",       AppMan.Editor.Section.KeySet("port", "1234"))
    #print("AppMan.Editor.Comment",      AppMan.Editor.Comment(True))
    #print("AppMan.Editor.SectionAdd",   AppMan.Editor.SectionAdd("MySection"))
    #print("AppMan.Editor.KeySet",       AppMan.Editor.Section.KeySet("socket", "MySocket-MySection"))
    #print("AppMan.Editor.SaveToFile",   AppMan.Editor.SaveToFile("my.cnf"))

    #print("AppMan.User.List",           AppMan.User.List())
    #print("AppMan.User.Add",            AppMan.User.Add("test1", "1234", "myDB"))
    #print("AppMan.User.List",           AppMan.User.List())
    #print("AppMan.User.Del",            AppMan.User.Del("test1", "myDB"))
    #print("AppMan.User.List",           AppMan.User.List())

    #print("AppMan.Cmd.PkgVersion",      AppMan.Cmd.PkgVersion())
    #print("AppMan.Cmd.PkgInstall",      AppMan.Cmd.PkgInstall())
    #print("AppMan.Cmd.PkgRemove",       AppMan.Cmd.PkgRemove())

    #print("AppMan.Cmd.ShowPort",        AppMan.Cmd.ShowPort())
    #print("AppMan.Cmd.ShowService",     AppMan.Cmd.ShowService())
    #print("AppMan.Cmd.ShowProcess",     AppMan.Cmd.ShowProcess())
    #print("AppMan.Cmd.ShowLog",         AppMan.Cmd.ShowLog())
    #print("AppMan.Cmd.ShowMan",         AppMan.Cmd.ShowMan())

    #print("AppMan.Cmd.ServiceStop",     AppMan.Cmd.ServiceStop())
    #print("AppMan.Cmd.ServiceStart",    AppMan.Cmd.ServiceStart())
    #print("AppMan.Cmd.ServiceRestart",  AppMan.Cmd.ServiceRestart())

    #print("AppMan.Util.IsRoot",         AppMan.Util.IsRoot())
    #print("AppMan.Util.MemTotal",       AppMan.Util.MemTotal())
    #print("AppMan.Util.OS",             AppMan.Util.OS())
    #print("AppMan.Util.Top",            AppMan.Util.Top())
    #print("AppMan.Util.Reboot",         AppMan.Util.Reboot())

    ## Plugin MySQL
    #for Item in AppMan.GetApi(): print(Item)
    #print("AppMan.User.TestShell",      AppMan.User.TestShell("mysql.sh DbCreate MyDB1"))
    #print("AppMan.Cmd.CreateDB",        AppMan.Cmd.CreateDB("MyDB2"))

#---
def TestSerial(aJson):
    Serial = TSerial()
    #print type(TestSerial).__name__
    #print type(Serial.CallFunc).__name__
    #print isinstance(Serial.CallFunc, instancemethod)
    #return

    print("Serial.CallFunc:TAppMan.GetInfo",            Serial.CallFunc("TAppMan.GetInfo"))
    print("Serial.CallFunc:TAppMan.LoadFile",           Serial.CallFunc("TAppMan.LoadFile", [aJson]))
    print("Serial.CallFunc:TAppMan.Variable.GetValue",  Serial.CallFunc("TAppMan.Variable.GetValue", ["Descr"]))
    #print("Serial.CallFunc:TAppMan.Editor.GetPath",     Serial.CallFunc("TAppMan.Editor.GetPath"))
    #print("Serial.CallFunc:TAppMan.Util.FileRead",      Serial.CallFunc("TAppMan.Util.FileRead", ["/var/run/mysqld/mysqld.pid"]))
    print("Serial.CallFunc:TAppMan.Util.ExecVar",       Serial.CallFunc("TAppMan.Util.ExecVar", ["Util_OS"]))
    #print("Serial.CallFunc:TAppMan.Util.ExecVar",       Serial.CallFunc("TAppMan.Util.ExecVar", ["Util_PkgUpdate"]))
    #print("Serial.CallFunc:TAppMan.GetInfo",             Serial.CallFunc("TAppMan.GetInfo"))
    #print("Type", type(Serial.CasheObj))


def TestRegEx():
    Str = "[section]"
    Res = re.findall("\[\s*(.*)\s*\]", Str)

    #Str = "    #label1\t \t=\t aaa      #werqwer\n"
    #Str = "basedir = usr"
    #Str = "#qqq #eeee"
    #Res = re.findall("(\w+)\s*=\s*(\w+)", Str)
    #Res = re.findall("(\w+)\s*", Str)
    #Res = re.findall("\w+=\w+", Str)
    print(Res)


#---
#FileName = "samba.json"
#FileName = "pure-ftpd.json"
#FileName = "sysuser.json"
FileName = "mysql.json"

TestAppMan(FileName)
#TestSerial(FileName)
#TestRegEx()

