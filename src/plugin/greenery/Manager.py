# Created: 20.10.2017
# Vladimir Vons, VladVons@gmail.com


import logging
import time
#
from LibTimer import *
from LibPio import *


class TManager():
    def __init__(self):
        self.Obj = {}
        self.InRun = False 

    def _Error(self, aMsg):
        self.Logger.error(aMsg)
        raise ValueError(aMsg)

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
        except IOError as E:
            print ('TManager->SetLoger Error: %s: %s' % (E, aFile))
        return Result

    def _CreateClass(self, aData, aParent):
        Alias = aData.get('Alias')
        #assert(Alias), 'TManager->_CreateClass. Key `Alias` is empty'
        if (not Alias):
            self._Error('TManager->_CreateClass. Key `Alias` is empty')

        ClassName = aData.get('Class')
        if (not ClassName):
            self._Error('TManager->_CreateClass. Key `Class` is empty')

        ModuleName = aData.get('Module')
        if (ModuleName):
            Module = __import__(ModuleName)
            TClass = getattr(Module, ClassName)
            del Module
        else:
            TClass = globals()[ClassName]

        Class = TClass(aParent)
        Class.Alias      = Alias
        Class.Logger     = self.Logger
        Class.ParentRoot = self
        return Class

    def _LoadClass(self, aData, aParent):
        Params = ['Enable', 'Module', 'Param', 'Class', 'Alias', 'Checks', 'Triggers', 'Controls', 'Ref']
        Diff   = set(aData.keys()) - set(Params)
        if (Diff):
            self._Error('TManager->_CreateClass. Unknown key %s' % (str(Diff)))

        Enable = aData.get('Enable', True)
        if (not Enable):
            return None
  
        Ref = aData.get('Ref')
        if (Ref):
            Class = self.Obj.get(Ref)
            if (not Class):
                 self.Logger.info('TManager->_LoadClass. Ref `%s` not found' % (Ref))
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

        self.Logger.info('TManager->Load')

        for Item in aData['Class']:
            Class = self._LoadClass(Item, self)
            if (Class):
                self.Obj[Class.Alias] = Class

    def _Signal(self, aKeys):
        for Key in aKeys:
            Obj = self.Obj.get(Key)
            if (Obj):
                Obj.Check()
            else:
                self._Error('TManager->Signal. Key `%s` not found' % (Key))

    def Run(self, aData):
        self.Load(aData)

        JobStart = aData.get('JobStart')
        if (JobStart):
            self._Signal(JobStart)

        Job = aData.get('Job')
        if (Job):
            self.InRun = True
            while self.InRun:
                self._Signal(Job)
                time.sleep(1)
        else:
            self.Logger.warn('TManager->Run. `Job` is empty')

        JobFinish = aData.get('JobFinish')
        if (JobFinish):
            self._Signal(JobFinish)

    def Stop(self):
        self.InRun = False
