# Created: 20.10.2017
# Vladimir Vons, VladVons@gmail.com


import logging
#
from LibTimer import *
from LibPio import *


class TManager():
    def __init__(self):
        self.Obj = {}

    def _SetLoger(self, aFile):
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
        except IOError (errno, strerror):
            print ('TManager->SetLoger Error: %s: %s' % (strerror, aFile))
        return Result

    def _CreateClass(self, aData, aParent):
        Alias = aData.get('Alias')
        if (not Alias):
            Msg = 'TManager->_CreateClass. Key Alias is empty'
            self.Logger.error(Msg)
            raise ValueError(Msg)

        ClassName = aData.get('Class')
        if (not ClassName):
            Msg = 'Key Class is empty'
            self.Logger.error(Msg)
            raise ValueError(Msg)

        ModuleName = aData.get('Module')
        if (ModuleName):
            Module = __import__(ModuleName)
            TClass = getattr(Module, ClassName)
            del Module
        else:
            TClass = globals()[ClassName]

        Class  = TClass(aParent)
        Class.Alias = Alias
        Class.Logger = self.Logger

        return Class

    def _LoadClass(self, aData, aParent):
        Enable = aData.get('Enable', True)
        if (not Enable):
            return None
  
        Ref = aData.get('Ref')
        if (Ref):
            Class = self.Obj.get(Ref)
            if (not Class):
                 self.Logger.info('TManager->_LoadClass. Ref "%s" not found' % (Ref))
        else:
            Class = self._CreateClass(aData, aParent)

            Param = aData.get('Param')
            if (Param):
                Class.LoadParam(Param)

            for Section in ['Checks', 'Controls', 'Triggers']:
                Items = aData.get(Section)
                if (Items):
                    for Item in Items:
                        ClassSection = self._LoadClass(Item, Class)
                        if (ClassSection):
                            getattr(Class, Section)[ClassSection.Alias] = ClassSection

        return Class

    def Load(self, aData):
        if (not self._SetLoger('/var/log/greenery.log')):
            self._SetLoger('greenery.log')

        OptEchoConsole = True
        self.Logger = logging.getLogger('Log1')
        if (OptEchoConsole):
            self.Logger.addHandler(logging.StreamHandler())

        self.Logger.info("TManager->Load")

        for Item in aData:
            Class = self._LoadClass(Item, self)
            if (Class):
                self.Obj[Class.Alias] = Class

    def Signal(self, aList = []):
        if (len(aList) == 0):
            Keys = self.Obj
        else:
            Keys = aList

        for Key in Keys:
            print('TManager->Signal', 'Key', Key, self.Obj[Key].Check())
