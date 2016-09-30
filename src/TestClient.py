#!/usr/bin/python

# Created: 21.08.2016
# Vladimir Vons, VladVons@gmail.com, OK


import re
from SockClient import *
from AppMan import *


def SockConnect():
    AppMan = TAppMan()
    Host = 'localhost'
    Port = AppMan.Option.GetValue("Server/Port", 50017)
    print("Client", Host, Port)

    SockClient = TSockClient(Host, Port)
    if (SockClient.Connected()):
        Login = SockClient.Login("VladVons", "1234")
        if (Login):
            print("Login OK")
        else:
            print("Login Err")
            sys.exit(1)
    return SockClient

#---
def TestSocket(aJson):
    SockClient = SockConnect()

    print("SockClient.CallFunc:TAppMan.GetVersion",          SockClient.CallFunc("TAppMan.GetVersion"))
    print("SockClient.CallFunc:TAppMan.LoadFile",            SockClient.CallFunc("TAppMan.LoadFile", aJson))
    print("SockClient.CallFunc:TAppMan.Variable.GetValue",   SockClient.CallFunc("TAppMan.Variable.GetValue", "Descr"))

    #print("SockClient.CallFunc:TAppMan.Editor.SectionSet",   SockClient.CallFunc("TAppMan.Editor.SectionSet", "mysqld"))
    #print("SockClient.CallFunc:TAppMan.Editor.KeyGet",       SockClient.CallFunc("TAppMan.Editor.Section.KeyGet", "socket"))
    #print("SockClient.CallFunc:TAppMan.Editor.KeySet",       SockClient.CallFunc("TAppMan.Editor.Section.KeySet", "socket", "MySocket-mysqld"))
    #print("SockClient.CallFunc:TAppMan.Editor.KeySet",       SockClient.CallFunc("TAppMan.Editor.Section.KeySet", "port", "1234"))
    #print("SockClient.CallFunc:TAppMan.Editor.Comment",      SockClient.CallFunc("TAppMan.Editor.Comment", True))

    #print("SockClient.Purge:TAppMan.Editor.Section",         SockClient.Purge("TAppMan.Editor.Section"))
    #print("SockClient.CallFunc:TAppMan.Editor.SectionAdd",   SockClient.CallFunc("TAppMan.Editor.SectionAdd", "MySection"))
    #print("SockClient.CallFunc:TAppMan.Editor.KeySet",       SockClient.CallFunc("TAppMan.Editor.Section.KeySet", "socket1", "MySocket-MySection"))
    #print("SockClient.CallFunc:TAppMan.Editor.SaveToFile",   SockClient.CallFunc("TAppMan.Editor.SaveToFile", "my.cnf"))

    print("SockClient.CallFunc:TAppMan.User.List",           SockClient.CallFunc("TAppMan.User.List"))
    #print("SockClient.CallFunc:TAppMan.User.Add",            SockClient.CallFunc("TAppMan.User.Add", "test2"))
    #print("SockClient.CallFunc:TAppMan.User.Del",            SockClient.CallFunc("TAppMan.User.Del", "test1"))
    #print("SockClient.CallFunc:TAppMan.User.List",           SockClient.CallFunc("TAppMan.User.List"))

    print("SockClient.CallFunc:TAppMan.Cmd.PkgVersion",      SockClient.CallFunc("TAppMan.Cmd.PkgVersion"))
    #print("SockClient.CallFunc:TAppMan.Cmd.PkgInstall",      SockClient.CallFunc("TAppMan.Cmd.PkgInstall"))
    #print("SockClient.CallFunc:TAppMan.Cmd.PkgRemove",       SockClient.CallFunc("TAppMan.Cmd.PkgRemove"))

    #print("SockClient.CallFunc:TAppMan.Cmd.ShowPort",        SockClient.CallFunc("TAppMan.Cmd.ShowPort"))
    #print("SockClient.CallFunc:TAppMan.Cmd.ShowService",     SockClient.CallFunc("TAppMan.Cmd.ShowService"))
    #print("SockClient.CallFunc:TAppMan.Cmd.ShowProcess",     SockClient.CallFunc("TAppMan.Cmd.ShowProcess"))
    #print("SockClient.CallFunc:TAppMan.Cmd.ShowLog",         SockClient.CallFunc("TAppMan.Cmd.ShowLog"))
    #print("SockClient.CallFunc:TAppMan.Cmd.ShowMan",         SockClient.CallFunc("TAppMan.Cmd.ShowMan"))

    #print("SockClient.CallFunc:TAppMan.Cmd.ServiceStop",     SockClient.CallFunc("TAppMan.Cmd.ServiceStop"))
    #print("SockClient.CallFunc:TAppMan.Cmd.ServiceStart",    SockClient.CallFunc("TAppMan.Cmd.ServiceStart"))
    #print("SockClient.CallFunc:TAppMan.Cmd.ServiceRestart",  SockClient.CallFunc("TAppMan.Cmd.ServiceRestart"))

    #print("SockClient.CallFunc:TAppMan.Util.IsRoot",         SockClient.CallFunc("TAppMan.Util.IsRoot"))
    #print("SockClient.CallFunc:TAppMan.Util.MemTotal",       SockClient.CallFunc("TAppMan.Util.MemTotal"))
    #print("SockClient.CallFunc:TAppMan.Util.OS",             SockClient.CallFunc("TAppMan.Util.OS"))
    #print("SockClient.CallFunc:TAppMan.Util.Top",            SockClient.CallFunc("TAppMan.Util.Top"))
    #print("SockClient.CallFunc:TAppMan.Util.Reboot",         SockClient.CallFunc("TAppMan.Util.Reboot"))

    ## Plugin
    #print("SockClient.CallFunc:TAppMan.User.TestShell",      SockClient.CallFunc("TAppMan.User.TestShell", "mysql.sh"))
    #print("SockClient.CallFunc:TAppMan.TMyClass.MyFunc",     SockClient.CallFunc("TAppMan.TMyClass.MyFunc"))
    #print("SockClient.CallFunc:TAppMan.TMyClass.GetValue",   SockClient.CallFunc("TAppMan.TMyClass.GetValue", "my_value"))


#---
def TestAppMan(aJson):

    AppMan = TAppMan()
    #for Item in AppMan.GetApi():
        #print(Item)

    #print("AppMan.GetVersion",          AppMan.GetVersion())
    #print("AppMan.GetListConf",         AppMan.GetListConf())
    print("AppMan.LoadFile",            AppMan.LoadFile(aJson))
    print("AppMan.Variable.GetValue",   AppMan.Variable.GetValue("Descr"))
    #print("AppMan.Variable.GetPairs",   AppMan.Variable.GetPairs("Value"))
    print("AppMan.Editor.PathName",     AppMan.Editor.PathName)
    print("AppMan.Editor.GetPath",      AppMan.Editor.GetPath())


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

    print("Serial.CallFunc:TAppMan.LoadFile",           Serial.CallFunc("TAppMan.LoadFile", [aJson]))
    print("Serial.CallFunc:TAppMan.Variable.GetValue",  Serial.CallFunc("TAppMan.Variable.GetValue", ["Descr"]))
    #print("Serial.CallFunc:TAppMan.Editor.GetPath",     Serial.CallFunc("TAppMan.Editor.GetPath"))
    print("Serial.CallFunc:TAppMan.Util.FileRead",      Serial.CallFunc("TAppMan.Util.FileRead", ["/var/run/mysqld/mysqld.pid"]))
    print("Serial.CallFunc:TAppMan.Util.ExecVar",       Serial.CallFunc("TAppMan.Util.ExecVar", ["Util_OS"]))
    #print("Serial.GetProp:TAppMan.Editor.PathName",     Serial.GetProp("TAppMan.Editor.PathName"))
    #print("Type", type(Serial.CasheObj))

def TestDir():
    AppMan = TAppMan()

    for File in os.listdir("conf/pkg"):
        if File.endswith(".json"):
            AppMan.LoadFile(File)
            print(File, AppMan.Cmd.ShowService())

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


def TestSocketCycle(aJson):
    SockClient = SockConnect()

    for i in range(0, 1000):
        print("SockClient.CallFunc:TAppMan.GetVersion",          SockClient.CallFunc("TAppMan.GetVersion"))
        print("SockClient.CallFunc:TAppMan.LoadFile",            SockClient.CallFunc("TAppMan.LoadFile", aJson))
        print("SockClient.CallFunc:TAppMan.Variable.GetValue",   SockClient.CallFunc("TAppMan.Variable.GetValue", "Descr"))
        #print("SockClient.CallFunc:TAppMan.Cmd.PkgVersion",      SockClient.CallFunc("TAppMan.Cmd.PkgVersion"))

        time.sleep(3)



#---
#TShell.ExecM("clear")

#FileName = "samba.json"
#FileName = "pure-ftpd.json"
#FileName = "sysuser.json"
FileName = "mysql.json"

#TestSocketCycle(FileName)
#TestSocket(FileName)
#TestAppMan(FileName)
TestSerial(FileName)


#TestDir()
#TestRegEx()

#Find = "Man"
#SortOrd = ["App", "Descr", "Tag", "HomePage", "Man", "User"]
#print(TList.Find(SortOrd, Find))

