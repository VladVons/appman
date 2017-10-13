# -*- coding: cp866 -*-

# Created: 07.01.2017
# Vladimir Vons, VladVons@gmail.com

import os,sys
import tempfile
import json
# OLE
import pythoncom
import win32com.client

from Section import *

class TOle1c(TSectionVar):
    def __init__(self, aParent, aName):
        TSectionVar.__init__(self, aParent, aName)

        self.Path  = self.GetVar('_Path')
        self.User  = self.GetVar('_User')
        self.Passw = self.GetVar("_Passw")

    def Disconnect(self):
        self.Ole = None

    def Connect(self):
        self.Disconnect()

        pythoncom.CoInitialize()
        self.Ole = win32com.client.Dispatch('V77.Application')

        InitStr = '/D' + self.Path + ' /N' + self.User + ' /P' + self.Passw
        return self.Ole.Initialize(self.Ole.RMTrade , InitStr,  'NO_SPLASH_SHOW') == 1

    def TryConnect(self):
        try:
            self.GetVersion()
        except:
            self.Connect()

    def GetVersion(self):
        #return self.Ole.Константа.НомерРелиза
        return getattr(self.Ole, 'Константа.НомерРелиза')

    def GetDescr(self):
        return 'GetDescr(), _Path: ' + self.GetVar('_Path') + ', Descr: ' + self.GetVar('Descr')

    def GetDocDelivery(self, aNumber):
        Result = ''

        ResultFile = tempfile.NamedTemporaryFile().name + '.json'
        FormPath   = self.Path + '\\ExtForms\\1C7TS-CS-DocExport.ert'
        FormParam  = 'кнЕкспортДоставка|'+ ResultFile + '|' + str(aNumber)  
        if (os.path.isfile(FormPath)):
            self.Ole.OpenFormModal('Отчет', FormParam, FormPath)
            if (os.path.isfile(ResultFile)):
                File = open(ResultFile, 'r')
                Result = File.read()
                File.close()
        return Result
