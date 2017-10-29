# Created: 20.10.2017
# Vladimir Vons, VladVons@gmail.com


import logging
import time
#
from LibTimer import *
from LibPio import *
from LibMisc import *


class TManager():
    def __init__(self):
        self.OnState  = None
        self.InRun    = False 
        self.Periodic = 1 
        self.Clear()

    def Clear(self):
        self.Obj    = {}
        self.Runs   = {}

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

    def Find(self, aAlias):
        for Item in self.Data:
            Alias = Item.get('Alias')
            if (aAlias == Alias):
                return Item
        return None

    def _AddClass(self, aClass, aAlias):
        #print("aAlias", aAlias, "aClass", aClass)
        if (aAlias in self.Obj):
            self._Error('%s->_AddClass. Alias exists %s' % (self.__class__.__name__, aAlias))
    
        self.Obj[aAlias] = aClass

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
        Result.OnState    = self.OnState
        self._AddClass(Result, aAlias)
        #print('->_CreateClass', 'Alias', Result.Alias, 'Class', aClassName, 'OnState', Result.OnState)

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
            Result = self.Obj.get(Link)
            if (not Result):
                Data = self.Find(Link)
                if (Data):
                    Result = self._LoadClass(Data, aParent)
                else:
                    self._Error('%s->_LoadClass. Link `%s` not found %s' % (self.__class__.__name__, Link, ParentInfo))
        else:
            ModuleName = aData.get('Module')

            ClassName = aData.get('Class')
            if (not ClassName):
                self._Error('%s->_LoadClass. Key `Class` is empty' % (self.__class__.__name__))

            Alias = aData.get('Alias')
            if (not Alias):
                self._Error('%s->_LoadClass. Alias is empty in Class' % (self.__class__.__name__, ClassName))

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

        #self.Logger.info('TManager->Load')

        self.Data = aData.get("Classes")
        if (not self.Data):
            self._Error('%s->_Load. Section `Classes` not found' % (self.__class__.__name__))

        Runs = aData.get("Run")
        if (not Runs):
            self._Error('%s->_Load. Section `Run` not found' % (self.__class__.__name__))

        self.Clear()
        for Key in ["Start", "Loop", "Finish"]:
            Alias = Runs.get(Key)
            if (Alias):
                Data = self.Find(Alias)
                if (Data):
                    Class = self._LoadClass(Data, None)
                    if (Class):
                        self.Runs[Key] = Class
                else:
                    self._Error('%s->_Load. Alias `%s` not found' % (self.__class__.__name__, Alias))

    def Run(self):
        Class = self.Runs.get('Start')
        if (Class):
            Class.Check()

        Class = self.Runs.get('Loop')
        if (Class):
            self.InRun = True
            while self.InRun:
                Class.Check()
                time.sleep(self.Periodic)
        else:
            self.Logger.warn('%s->Run. `Loop` is empty' % (self.__class__.__name__))

        Class = self.Runs.get('Finish')
        if (Class):
            Class.Check()

    def Stop(self):
        self.InRun = False
