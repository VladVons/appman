# Created: 24.09.2016
# Vladimir Vons, VladVons@gmail.com

from flask import session
#
import sys
sys.path.insert(0, '../src')
from SockClient import *

#__all__ = ["TUser", "User"]

# map session variable on dictionaru TUser.Obj with a key = session["User"] + "_" + Var
class TUser():
    Cnt   = 0
    Debug = False
    Host  = "localhost"
    Port  = 51017

    def __init__(self):
        TUser.Cnt += 1
        if (TUser.Cnt > 1):
            raise "One instance calss allowed"
        self.Obj  = {}
        self.LKey = lambda aUser, aName: aUser + "_" + aName

    def __call__(self):
        return self.GetName()

    def OK(self):
        Result = (self.GetName() != "")
        if (not Result and self.Debug):
            self.Connect(self.Host, self.Port, "VladVons", "1234")
        return Result

    def GetName(self):
        return session.get("User", "")

    def SetObj(self, aName, aObj):
        Key = self.LKey(self.GetName(), aName)
        self.Obj[Key] = aObj

    def GetObj(self, aName):
        Key = self.LKey(self.GetName(), aName)
        return self.Obj.get(Key, None)

    def Call(self, aFunc, *aArgs):
        return self.GetObj("SockClient").CallFunc(aFunc, *aArgs)

    def GetProp(self, aProp):
        return self.GetObj("SockClient").GetProp(aProp)

    def Connect(self, aHost, aPort, aUser, aPassw):
        Result = False

        User = self.GetName()
        if (User == ""):
            SockClient = TSockClient(aHost, aPort)
            if (SockClient.Connected()):
                Result = SockClient.Login(aUser, aPassw)
                if (Result):
                    session["User"] = aUser
                    self.SetObj("SockClient", SockClient)
        return Result

    def Close(self):
        self.GetObj("SockClient").Close()
        session["User"] = ""

User = TUser()
User.Debug = True
