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
        self.OnValue  = None
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

    def _CreateClass(self, **aParam):
        aModuleName = aParam.get('ModuleName')
        aClassName  = aParam.get('ClassName')
        aAlias      = aParam.get('Alias')
 
        if (aModuleName):
            Module = __import__(aModuleName )
            TClass = getattr(Module, aClassName)
            del Module
        else:
            TClass = globals()[aClassName]

        Result = TClass(aParam.get('aParent'))
        Result.Alias      = aAlias
        Result.Tag        = aParam.get('Tag')
        Result.Logger     = self.Logger
        Result.ParentRoot = self
        Result.OnState    = self.OnState
        Result.OnValue    = self.OnValue
        self._AddClass(Result, aAlias)
        #print('->_CreateClass', 'Alias', Result.Alias, 'Class', aClassName, 'OnState', Result.OnState)

        return Result

    def _LoadClass(self, aData, aParent):
        Result = None

        if (aParent):
            ParentInfo = aParent.Alias   
        else:
            ParentInfo = ''   

        Params = ['Enable', 'Module', 'Param', 'Class', 'Alias', 'Checks', 'Link', 'Tag', 'Triggers', 'Controls']
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
                    self._Error('%s->_LoadClass. Link `%s` not found in %s' % (self.__class__.__name__, Link, ParentInfo))
        else:
            ClassName = aData.get('Class')
            if (not ClassName):
                self._Error('%s->_LoadClass. Key `Class` is empty' % (self.__class__.__name__))

            Alias = aData.get('Alias')
            if (not Alias):
                self._Error('%s->_LoadClass. Alias is empty in Class' % (self.__class__.__name__, ClassName))

            Result = self._CreateClass(Parent=aParent, ClassName=ClassName, Alias=Alias, ModuleName=aData.get('Module'), Tag=aData.get('Tag'))

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
        for Key in ['Start', 'Loop', 'Finish']:
            KeyData = Runs.get(Key)
            if (KeyData):
                for Item in Runs.get(Key):
                    Class = self._LoadClass(Item, None)
                    if (Class):
                        if (not Key in self.Runs):
                            self.Runs[Key] = []
                        self.Runs[Key].append(Class)
                    else:
                        self.Logger.warn('%s->Load. Class not loaded in `%s`' % (self.__class__.__name__, Key))

    def _Check(self, aClass):
        if (aClass):
            for Class in aClass:
                #print('Check', 'Class', Class)
                Class.Check(True)

    def Run(self):
        Items = self.Runs.get('Start')
        self._Check(Items)

        Items = self.Runs.get('Loop')
        if (Items):
            self.InRun = True
            while self.InRun:
                self._Check(Items)
                time.sleep(self.Periodic)
        else:
            self.Logger.warn('%s->Run. `Loop` is empty' % (self.__class__.__name__))

        Items = self.Runs.get('Finish')
        self._Check(Items)

    def Stop(self):
        self.InRun = False
