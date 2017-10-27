# Created: 20.10.2017
# Vladimir Vons, VladVons@gmail.com


import logging
import time
#
from LibTimer import *
from LibPio import *
from LibManager import *


class TManager():
    def __init__(self):
        self.Obj      = {}
        self.InRun    = False 
        self.Periodic = 1 
        self.OnSignal = None

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
            print ('%s->SetLoger Error: %s: %s' % (self.__class__.__name__, E, aFile))
        return Result

    def _CreateClass(self, aData, aParent):
        ClassName = aData.get('Class')
        if (not ClassName):
            self._Error('%s->_CreateClass. Key `Class` is empty' % (self.__class__.__name__))

        Alias = aData.get('Alias')
        #assert(Alias), 'TManager->_CreateClass. Key `Alias` is empty'
        if (not Alias):
            Alias = ClassName + '_' + str(len(self.Obj) + 1)
        else:
            if (Alias in self.Obj):
                self._Error('%s->_CreateClass. Alias already exists %s' % (self.__class__.__name__, Alias))

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
        self.Obj[Alias]  = Class

        return Class

    def _LoadClass(self, aData, aParent):
        if (aParent):
            ParentInfo = aParent.Alias   
        else:
            ParentInfo = ''   

        Params = ['Enable', 'Module', 'Param', 'Class', 'Alias', 'Checks', 'Triggers', 'Controls', 'Ref']
        Diff   = set(aData.keys()) - set(Params)
        if (Diff):
            self._Error('%s->_CreateClass. Unknown key %s' % (self.__class__.__name__, str(Diff)))

        Enable = aData.get('Enable', True)
        if (not Enable):
            return None
  
        Ref = aData.get('Ref')
        if (Ref):
            Class = self.Obj.get(Ref)
            if (not Class):
                self._Error('%s->_LoadClass. Ref `%s` not found or it placed below %s' % (self.__class__.__name__, Ref, ParentInfo))
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
            Class = self._LoadClass(Item, None)
            if (Class):
                self.Obj[Class.Alias] = Class

    def _Signal(self, aKeys):
        for Key in aKeys:
            Obj = self.Obj.get(Key)
            if (Obj):
                Obj.Check()
                if (self.OnSignal):
                     self.OnSignal(self, Obj)
            else:
                self._Error('%s->Signal. Key `%s` not found' % (self.__class__.__name__, Key))

    def Run(self, aData):
        self.Load(aData)

        JobStart = aData.get('JobStart')
        if (JobStart):
            self._Signal(JobStart)

        JobLoop = aData.get('JobLoop')
        if (JobLoop):
            self.InRun = True
            while self.InRun:
                self._Signal(JobLoop)
                time.sleep(self.Periodic)
        else:
            self.Logger.warn('%s->Run. `Job` is empty' % (self.__class__.__name__))

        JobFinish = aData.get('JobFinish')
        if (JobFinish):
            self._Signal(JobFinish)

    def Stop(self):
        self.InRun = False
