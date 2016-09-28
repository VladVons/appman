# Created: 18.08.2016
# Vladimir Vons, VladVons@gmail.com
#
# Echo client program

import socket
from Serial import *

#---

class TSockClient():

    def __init__(self, aHost, aPort):
        self.BufSize  = 4096
        self.UserName = ""
        self.Sock     = None
        self.Serial   = TSerial()
        self.Connect(aHost, aPort)

    def __del__(self):
        self.Close()

    def Close(self):
        if (self.Connected()):
            self.Sock.close()
            self.Sock = None
            print("TSockClient.Close")

    def Connect(self, aHost, aPort):
        if (not self.Connected()):
            self.Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.Sock.connect((aHost, aPort))
                print("Connected")
            except Exception as E:
                self.Sock = None
                print(E)
                raise
        return self.Connected()

    def Connected(self):
        return (self.Sock != None)

    def Send(self, aData):
        self.Sock.sendall(aData)
        Data = self.Receive()
        return json.loads(Data)["Data"]

    def Receive(self):
        return TSocket.Receive(self.Sock, self.BufSize)

    def CallFunc(self, aFunc, *aArgs):
        Data = self.Serial.EncodeFunc(aFunc, *aArgs)
        return self.Send(Data)

    def GetProp(self, aProp):
        Data = self.Serial.EncodeProp(aProp)
        return self.Send(Data)

    def Purge(self, aName):
        Data = self.Serial.EncodeFunc("Purge", aName)
        return self.Send(Data)

    def Login(self, aUser, aPassw):
        Data = self.Serial.EncodeFuncAuth(aUser, aPassw)
        Result = self.Send(Data)
        if (Result):
            self.UserName = aUser
        return Result
