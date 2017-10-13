# Created: 18.08.2016
# Vladimir Vons, VladVons@gmail.com
#
# Echo server program

# https://docs.python.org/2/library/socket.html

import socket
import time
import multiprocessing
import logging
import re


from Serialize import *
from AppMan import *


class TSockSession():
    def __init__(self, aParent, aConn, aAddress):
        self.Parent     = aParent
        self.Conn       = aConn
        self.Address    = aAddress

        self.UserName   = ""
        self.UserGroup  = ""
        self.OptBufSize = self.Parent.Option.GetValue("Server/BufSize", 4096)

        self.Serialize  = TSerialize()
        # export functions
        self.Serialize.AddObj("AuthUser", self.AuthUser)
        self.Serialize.AddObj("Log",      self.Log)
        self.Serialize.AddObj("Purge",    self.Serialize.Purge)

    def __del__(self):
        self.Conn.close()
        self.Log("Connection closed")

    def Log(self, aMsg):
        self.Parent.logger.info("%s from %s %s", aMsg, self.Address, self.UserName)

    def Receive(self):
        Result = TSocket.Receive(self.Conn, self.OptBufSize)
        self.Log("Receive:" + Result)
        return Result

    def Send(self, aData):
        Data = self.Serialize.EncodeData(aData)
        self.Log("Send:" + Data)
        self.Conn.sendall(Data)

    def Login(self):
        Data = self.Receive()
        # jump to AuthUser
        Result = self.Serialize.Decode(Data)
        self.Log("Login status " + str(Result))
        self.Send(Result)
        return Result

    def Logout(self):
        self.UserName  = ""
        self.UserGroup = ""
        self.Log("Logout")

    def AuthUser(self, aUser, aPassw):
        Result = False
        if (self.UserName == ""):
            OptUser = self.Parent.Option.GetItem("Policy/User/" + aUser)
            if (OptUser != ""):
                if (OptUser.get("Value") == "Allow" and OptUser.get("Password", "xxx") == aPassw): 
                    Result = True
                    self.UserName = aUser

                    # search group by user
                    for Group in self.Parent.Option.GetItem("Policy/Group"):
                        Users = self.Parent.Option.GetValue("Policy/Group/" + Group)
                        if (Users.find(aUser) != -1):
                            self.UserGroup = Group
                            break
        else:
            Result = True
        return Result

    def AuthApi(self, aData):
        OptAuthApi  = self.Parent.Option.GetValue("Server/AuthApi", False)
        if (OptAuthApi == False):
            return True

        FuncName = self.Serialize.DecodeFuncName(aData)
        return self.Parent.Option.IsAllow("Api", self.UserGroup, FuncName)

    def AuthConf(self, aData):
        FuncName = self.Serialize.DecodeFuncName(aData)
        if (FuncName == "TAppMan.LoadFile"):
            FuncArg = self.Serialize.DecodeFuncArg(aData)
            return self.Parent.Option.IsAllow("Conf", self.UserGroup, FuncArg[0])

        return True

    def Run(self):
        self.Log("Start session")
        try:
            while True:
                #time.sleep(0.1)
                DataIn = self.Receive()
                if (DataIn == ""):
                    break
                else:
                    if (DataIn == "Stop"):
                        self.Parent.FlagRun.value = False
                        self.Send(DataOut)
                        break
                    elif (not self.AuthApi(DataIn)):
                        DataOut = "Option->Policy->Api permission failed"
                    elif (not self.AuthConf(DataIn)):
                        DataOut = "Option->Policy->Conf permission failed"
                    else:
                        DataOut = self.Serialize.Decode(DataIn)

                    self.Send(DataOut)
        except Exception as E:
            DataOut = "TSockSession->Run Error:" + E.message + ", Data:" + DataIn
            self.Log(DataOut)
            self.Send(DataOut)


class TMonit():

    def __init__(self, aParent):
        self.Parent  = aParent
        self.OptMonitTime = self.Parent.Option.GetValue("Server/MonitTime", 60)
        self.AppMan  = TAppMan()

    def Log(self, aMsg):
        self.Parent.logger.info("Monit: %s", aMsg)

    def CheckFiles(self):
        for File in self.AppMan.GetListConf():
            self.AppMan.LoadFile(File)
            if (self.AppMan.Var.GetValue("MonitProcess", False)):
                Process = self.AppMan.Cmd.ShowProcess().strip()
                if (Process == ""):
                    self.AppMan.Cmd.ServiceStart()
                    self.Log("Starting service in " + File)

    def Run(self):
        while (True):
            time.sleep(self.OptMonitTime)
            self.CheckFiles()


# https://gist.github.com/micktwomey/606178#file-server-py-L26
class TSockServer():

    def __init__(self, aOption):
        self.Option = aOption

        OptEchoConsole = self.Option.GetValue("Server/DebugConsole", True)
        OptLogFile     = self.Option.GetValue("Server/LogFile", "/var/log/appman.log")

        if (not self.__SetLoger(OptLogFile)):
            self.__SetLoger("appman.log")
            #sys.exit()

        self.logger = logging.getLogger('Log1')
        if (OptEchoConsole):
            self.logger.addHandler(logging.StreamHandler())

        self.logger.info("Start server")

    def __del__(self):
        self.__Stop()

    def __SetLoger(self, aFile):
        Result = False
        # Format = '[%(asctime)s], %(module)s->%(funcName)s->%(lineno)d,
        # %(levelname)s: %(message)s'
        Format = '[%(asctime)s], %(levelname)s:%(message)s'
        try:
            logging.basicConfig(level=logging.INFO,
                            format=Format,
                            datefmt='%Y/%m/%d %H:%M:%S',
                            filename=aFile,
                            filemode='a')
            Result = True
        except IOError as (errno, strerror):
            print ("TSockServer->SetLoger Error: {0}: {1}".format(strerror, aFile))
        return Result

    def __Stop(self):
        self.logger.info("Stop server")
        self.Sock.close()

    def __RunThreadConn(self, aConn, aAddress):
        SockSession = TSockSession(self, aConn, aAddress)

        OptAuthUser = self.Option.GetValue("Server/AuthUser", True)
        if (OptAuthUser and SockSession.Login() != True):
            return

        self.Count.value += 1
        SockSession.Run()
        self.Count.value -= 1

        self.logger.info("Session ending")

    def __RunThreadMonit(self):
        Monit = TMonit(self)
        Monit.Run()

    def __CreateThread(self, aTarget, aArgs):
        process = multiprocessing.Process(target = aTarget, args = aArgs)
        process.daemon = True
        process.start()
        time.sleep(0.3)

    def Connect(self):
        OptHost    = self.Option.GetValue("Server/Host", "")
        OptPort    = self.Option.GetValue("Server/Port", 50019)
        OptMaxConn = self.Option.GetValue("Server/MaxConn", 5)
        OptIpAllow = self.Option.GetValue("Server/IpAllow", "127.0.0.1")

        OptMonitTime = self.Option.GetValue("Server/MonitTime", 60) 
        if (OptMonitTime > 0):
            self.__CreateThread(self.__RunThreadMonit, [])

        self.logger.info("Listening host '%s', interface '%s', on port '%s'", OptHost, TSocket.GetLocalIP(), OptPort)
        self.Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Sock.bind((OptHost, OptPort))
        self.Sock.listen(OptMaxConn)

        # RW shared thread variable
        self.Count   = multiprocessing.Value('i', 0)
        self.FlagRun = multiprocessing.Value('i')
        self.FlagRun.value = True
        while (self.FlagRun.value):
            Conn, Address = self.Sock.accept()

            Error = ""
            if (not re.match(OptIpAllow, Address[0])):
                Error = "Error: Address deny {}".format(Address)
            elif (self.Count.value >= OptMaxConn):
                Error = "Error: Maximum connections reached"

            if (Error == ""):
                self.logger.info("Starting thread")
                Conn.sendall(TSerialize.CEncodeData("OK"))
                self.__CreateThread( self.__RunThreadConn, [Conn, Address])
            else:
                self.logger.info(Error)
                Conn.sendall(TSerialize.CEncodeData(Error))
                Conn.close()
