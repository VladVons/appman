#!/usr/bin/python

# Created: 21.08.2016
# Vladimir Vons, VladVons@gmail.com, OK


import re
from AppMan import *
from Serialize import *
#from inc.Common import *


def TestAppMan(aJson):
    def Test1():
        for Item in AppMan.Cmd.GetKeys():
            #print("--1", Item)
            Field = AppMan.Cmd.GetField(Item)
            #print("--2", Field)
            CmdInfo = Field.get("CmdInfo")
            if (CmdInfo):
                print(Item, Field)
            #    print(AppMan.Var.Parse(CmdInfo), AppMan.Var.GetValue(Item))

    AppMan = TAppMan()
    #print("AppMan.TGpio.Test",         AppMan.TGpio.Test())

    #print("AppMan.GetInfo",          AppMan.GetInfo())
    #print("AppMan.GetListPlugin",         AppMan.GetListPlugin())
    #print("AppMan.LoadFile",            AppMan.LoadFile(aJson))
    #print("AppMan.Var.GetValue",      AppMan.Var.GetValue("Descr"))
    print("AppMan.Gpio.Run",         AppMan.Gpio.Run())
    #print("AppMan.Cmd1.Test",     AppMan.Cmd1.Test())


    #print("AppMan.Var.GetField",      AppMan.Var.GetField("App"))
    #print("AppMan.Cmd.ExecValue",       AppMan.Cmd.ExecValue("LogFile", "CmdExec"))
    #print("AppMan.Var.GetPairs",      AppMan.Var.GetPairs("Value"))
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


    #print("AppMan.Cmd.PkgVersion",        AppMan.Cmd.PkgVersion())
    #print("AppMan.Cmd.ExecValue",        AppMan.Cmd.ExecValue("PkgVersion"))
    #print("AppMan.Cmd.ExecValue",        AppMan.Cmd.ExecValue("Port"))
    #print("AppMan.Cmd.ExecField",        AppMan.Cmd.ExecField("PkgVersion",   "CmdInfo"))
    #print("AppMan.Cmd.GetValue",         AppMan.Cmd.HasKey("ServiceRestart"))
    #print("AppMan.Cmd.ExecField",         AppMan.Cmd.ExecField("ServiceStatus", "CmdExec"))


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
    Serialize = TSerialize()
    #print type(TestSerial).__name__
    #print type(Serialize.CallFunc).__name__
    #print isinstance(Serialize.CallFunc, instancemethod)
    #return

    #print("Serialize.CallFunc:TAppMan.GetInfo",            Serialize.CallFunc("TAppMan.GetInfo"))
    print("Serialize.CallFunc:TAppMan.LoadFile",           Serialize.CallFunc("TAppMan.LoadFile", [aJson]))
    print("Serialize.CallFunc:TAppMan.Var.GetValue",       Serialize.CallFunc("TAppMan.Var.GetValue", ["Descr"]))
    print("Serialize.CallFunc:TAppMan.Var.GetValue",       Serialize.CallFunc("TAppMan.Var.GetValue('Descr')"))
    #print("Serialize.CallFunc:TAppMan.Editor.GetPath",     Serialize.CallFunc("TAppMan.Editor.GetPath"))
    #print("Serialize.CallFunc:TAppMan.Util.FileRead",      Serialize.CallFunc("TAppMan.Util.FileRead", ["/var/run/mysqld/mysqld.pid"]))
    #print("Serialize.CallFunc:TAppMan.Util.ExecVar",       Serialize.CallFunc("TAppMan.Util.ExecVar", ["Util_OS"]))
    #print("Serialize.CallFunc:TAppMan.Util.ExecVar",       Serialize.CallFunc("TAppMan.Util.ExecVar", ["Util_PkgUpdate"]))
    #print("Serialize.CallFunc:TAppMan.GetInfo",             Serialize.CallFunc("TAppMan.GetInfo"))
    #print("Type", type(Serialize.CasheObj))


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
#FileName = "mysql.json"
FileName = "gpio.json"

TestAppMan(FileName)

#AppMan = TAppMan()

#List = TDir.FindFile('plugin', ['mysql.json', 'appman.json'], True)
#List = TDir.FindFile(['plugin', 'inc'], ['.json', 'Common'], True)
#print(List)

#TestSerial(FileName)
#TestRegEx()

#Str = "Func(par1,  par2)"
#Params = re.findall(r'w+', Str)
#print(Params)


#Str = "Test1.MyFunc_1()"
#Str = "Test1.MyFunc_1(arg1, arg2)"
#Str = "Test1.MyFunc_1('arg1/xxx', 'arg2')"
#m = re.match("(?P<function>\w+)\s?\((?P<args>(?P<arg>\w+(,\s?)?)+)\)", Str)
#m = re.match("(?P<function>\w+)\((?P<args>(?P<arg>\w+(,\s?)?)+)\)", Str)
#m = re.match("(?P<Name>\w+)\((?P<Arg>(\w+(,\s?)?)+)\)", Str)
#m = re.match("(?P<Name>[\w\.]+)\((?P<Arg>(\w+(,\s?)?)+)\)", Str)
#m = re.match("(?P<Name>[\w\.]+)\((?P<Arg>[\w\s,']+)\)", Str)
#m = re.match("(?P<Name>[\w\.]+)\((?P<Arg>.*)\)", Str)


#m = re.match("(\w+)", s)
#print m.groupdict()
#print(m)

#def CallFunc(aArgs, aKeys, aIdx):
#    if aIdx > 0:
#        CallFunc(aArgs, aKeys, aIdx - 1)
#        Pars = aArgs.get(aKeys[aIdx])
#        for Par in Pars.split(";"):
#            print(Par)


    #for Key in aArg.keys():
    #    for Par in aArg.get(Key).split(";"):
    #        print(Key, Par)

#Args = {"Arg1":"1;2;3", "Arg2":"a;b;c;d", "Arg3":"x;y"}
#Keys = Args.keys()
#CallFunc(Args, Keys, len(Keys))
