#!/usr/bin/python

# Created: 21.08.2016
# Vladimir Vons, VladVons@gmail.com, OK


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
    else:
        print("Err:", SockClient.LastError)
        sys.exit(1)
    return SockClient


def TestSocket(aJson):
    SockClient = SockConnect()

    print("SockClient.CallFunc:TAppMan.GetInfo",        SockClient.CallFunc("TAppMan.GetInfo()"))
    print("SockClient.CallFunc:TAppMan.LoadFile",       SockClient.CallFunc("TAppMan.LoadFile", aJson))
    print("SockClient.CallFunc:TAppMan.Var.GetValue",   SockClient.CallFunc("TAppMan.Var.GetValue", "Descr"))
    print("SockClient.CallFunc:TAppMan.Var.GetValue",   SockClient.CallFunc("TAppMan.Var.GetValue(Descr)"))
    print("SockClient.CallFunc:TAppMan.Cmd.ExecValue",  SockClient.CallFunc("TAppMan.Cmd.ExecValue", "PkgVersion"))
    print("SockClient.CallFunc:TAppMan.Cmd.ExecValue",  SockClient.CallFunc("TAppMan.Cmd.ExecValue", "Port"))

    #print("SockClient.CallFunc:TAppMan.Editor.SectionSet",   SockClient.CallFunc("TAppMan.Editor.SectionSet", "mysqld"))
    #print("SockClient.CallFunc:TAppMan.Editor.KeyGet",       SockClient.CallFunc("TAppMan.Editor.Section.KeyGet", "socket"))
    #print("SockClient.CallFunc:TAppMan.Editor.KeySet",       SockClient.CallFunc("TAppMan.Editor.Section.KeySet", "socket", "MySocket-mysqld"))
    #print("SockClient.CallFunc:TAppMan.Editor.KeySet",       SockClient.CallFunc("TAppMan.Editor.Section.KeySet", "port", "1234"))
    #print("SockClient.CallFunc:TAppMan.Editor.Comment",      SockClient.CallFunc("TAppMan.Editor.Comment", True))

    #print("SockClient.Purge:TAppMan.Editor.Section",         SockClient.Purge("TAppMan.Editor.Section"))
    #print("SockClient.CallFunc:TAppMan.Editor.SectionAdd",   SockClient.CallFunc("TAppMan.Editor.SectionAdd", "MySection"))
    #print("SockClient.CallFunc:TAppMan.Editor.KeySet",       SockClient.CallFunc("TAppMan.Editor.Section.KeySet", "socket1", "MySocket-MySection"))
    #print("SockClient.CallFunc:TAppMan.Editor.SaveToFile",   SockClient.CallFunc("TAppMan.Editor.SaveToFile", "my.cnf"))

    #print("SockClient.CallFunc:TAppMan.User.List",           SockClient.CallFunc("TAppMan.User.List"))
    #print("SockClient.CallFunc:TAppMan.User.Add",            SockClient.CallFunc("TAppMan.User.Add", "test2"))
    #print("SockClient.CallFunc:TAppMan.User.Del",            SockClient.CallFunc("TAppMan.User.Del", "test1"))
    #print("SockClient.CallFunc:TAppMan.User.List",           SockClient.CallFunc("TAppMan.User.List"))

    #print("SockClient.CallFunc:TAppMan.Cmd.PkgVersion",      SockClient.CallFunc("TAppMan.Cmd.PkgVersion"))
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


#----------
#FileName = "samba.json"
#FileName = "pure-ftpd.json"
#FileName = "sysuser.json"
FileName = "mysql.json"

TestSocket(FileName)


