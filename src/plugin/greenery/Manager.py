# Created: 20.10.2017
# Vladimir Vons, VladVons@gmail.com


import logging
import time
#
from LibTimer import *
from LibPio import *
from LibMisc import *


class TAliaser():
    def __init__(self, aData):
        self.Data = aData
        self.ClassCnt = {}

    def Find(self, aAlias):
        for Item in self.Data:
            Alias = Item.get('Alias')
            return Item
        return None

    def Get(self, aClassName):
        return aClassName + '__' + str(self.ClassCnt[aClassName])

    def Add(self, aClassName):
        if (aClassName in self.ClassCnt):
            self.ClassCnt[aClassName] += 1
        else:
            self.ClassCnt[aClassName]  = 0


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

    def _AddClass(self, aClass, aAlias):
        if (not aAlias in self.Obj):
            self.Obj[aAlias] = aClass
            return True
        return False

    def _CreateClass(self, aParent, aClassName, aAlias, aModuleName):
        if (aModuleName):
            Module = __import__(aModuleName)
            TClass = getattr(Module, aClassName)
            del Module
        else:
            TClass = globals()[aClassName]

        Result = TClass(aParent)
        Result.Alias      = aAlias
        Result.Logger     = self.Logger
        Result.ParentRoot = self
        self._AddClass(Result, aAlias)

        return Result

    def _LoadClass(self, aData, aParent):
        Result = None

        if (aParent):
            ParentInfo = aParent.Alias   
        else:
            ParentInfo = ''   

        Params = ['Enable', 'Module', 'Param', 'Class', 'Alias', 'Checks', 'Triggers', 'Controls', 'Link']
        Diff   = set(aData.keys()) - set(Params)
        if (Diff):
            self._Error('%s->_LoadClass. Unknown key %s' % (self.__class__.__name__, str(Diff)))

        Enable = aData.get('Enable', True)
        if (not Enable):
            return None 
  
        Link = aData.get('Link')
        if (Link):
            #Alias  = None
            Result = self.Obj.get(Link)
            if (not Result):
                Data = self.TmpAliaser.Find(Link)
                if (Data):
                    Result = self._LoadClass(Data, aParent)
                else:
                    self._Error('%s->_LoadClass. Link `%s` not found %s' % (self.__class__.__name__, Link, ParentInfo))
        else:
            ClassName = aData.get('Class')
            if (not ClassName):
                self._Error('%s->_LoadClass. Key `Class` is empty' % (self.__class__.__name__))

            self.TmpAliaser.Add(ClassName)
            Alias = aData.get('Alias')
            #assert(Alias), 'TManager->_CreateClass. Key `Alias` is empty'
            if (not Alias):
                Alias = self.TmpAliaser.Get(ClassName)

            if (Alias in self.Obj):
                Result = self.Obj.get(Alias)
            else:
                ModuleName = aData.get('Module')

                Result = self._CreateClass(aParent, ClassName, Alias, ModuleName)

                Param = aData.get('Param')
                if (Param):
                    Result.LoadParam(Param)

                for Section in ['Checks', 'Controls', 'Triggers']:
                    Items = aData.get(Section)
                    if (Items):
                        for Item in Items:
                            ClassSection = self._LoadClass(Item, Result)
                            if (ClassSection):
                                getattr(Result, Section)[ClassSection.Alias] = ClassSection

        #print('--- Alias', Alias, 'Link', Link, 'Result', Result)
        return Result

    def Load(self, aData):
        if (not self._SetLoger('/var/log/greenery.log')):
            self._SetLoger('greenery.log')

        OptEchoConsole = True
        self.Logger = logging.getLogger('Log1')
        if (OptEchoConsole):
            self.Logger.addHandler(logging.StreamHandler())

        self.Logger.info('TManager->Load')

        self.TmpAliaser = TAliaser(aData['Class'])
        for Item in aData['Class']:
            Class = self._LoadClass(Item, None)
            if (Class):
                self._AddClass(Class, Class.Alias)
        del self.TmpAliaser

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
