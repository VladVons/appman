# Created: 18.08.2016
# Vladimir Vons, VladVons@gmail.com
#
# Echo client program

import socket
import re

from Serialize import *


class TSockClient():

    def __init__(self, aHost, aPort):
        self.BufSize   = 4096
        self.UserName  = ''
        self.Sock      = None
        self.Serialize = TSerialize()
        self.LastError = ''
        self.Connect(aHost, aPort)

    def __del__(self):
        self.Close()

    def Close(self):
        if (self.Connected()):
            self.Sock.close()
            self.Sock = None
            print("TSockClient.Close")

    def Connect(self, aHost, aPort):
        self.LastError = ''

        if (not self.Connected()):
            self.Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                #web browser GET standart has 'r\n' at the end of each line. Last line must have '\r\n'
                #Data = self.Send('TSockClient.Connect\r\n\r\n')
 
                self.Sock.connect((aHost, aPort))
                Data = self.ReceiveData()
                if (Data != "OK"):
                    self.LastError = Data
                    self.Close()
            except Exception as E:
                self.LastError = E.message
                print(self.LastError)
                self.Close()
                raise
        return (self.LastError == "")

    def Connected(self):
        return (self.Sock != None)

    def Send(self, aData):
        self.Sock.sendall(aData)
        return self.ReceiveData()

    def Receive(self):
        return TSocket.Receive(self.Sock, self.BufSize)

    def ReceiveData(self):
        Data = self.Receive()
        if (Data):
            return json.loads(Data).get('Data')
        else:
            return ''

    def SplitFunc(self, aFuncStr):
        Data = re.match("(?P<Name>[\w\.]+)\((?P<Arg>.*)\)", aFuncStr)
        if (Data):
            return Data.groupdict()
        else:
            return {}

    def CallFunc(self, aFuncName, *aArgs):
        Arr = self.SplitFunc(aFuncName)
        if (Arr):
            aFuncName = Arr["Name"]
            Args      = Arr["Arg"].replace("'", "").split(",")
            if (Args[0]):
                aArgs = Args

        Data = self.Serialize.EncodeFunc(aFuncName, *aArgs)
        return self.Send(Data)

    def GetProp(self, aProp):
        Data = self.Serialize.EncodeProp(aProp)
        return self.Send(Data)

    def Purge(self, aName):
        Data = self.Serialize.EncodeFunc("Purge", aName)
        return self.Send(Data)

    def Login(self, aUser, aPassw):
        Data = self.Serialize.EncodeFuncAuth(aUser, aPassw)
        Result = self.Send(Data)
        if (Result):
            self.UserName = aUser
        return Result
