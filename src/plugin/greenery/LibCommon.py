# Created: 15.10.2017
# Vladimir Vons, VladVons@gmail.com

import time
import multiprocessing
#
#from inc.Common import *

_Required = '_Required'

class TObject():
    def __init__(self, aParent):
        self.Parent     = aParent
        self.ParentRoot = None
        self.Alias      = None

    def _Error(self, aMsg):
        self.Logger.error(aMsg)
        raise ValueError(aMsg)


class TControl(TObject):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.Clear()

    def _Check(self, aValue):
        raise NotImplementedError('Method not Implemented')

    def Get(self):
        raise NotImplementedError('Method not Implemented')

    def LoadParam(self, aParam):
        raise NotImplementedError('Method not Implemented')

    def Uptime(self):
        return int(time.time() - self.Start)

    def Clear(self):
        self.Invert     = False
        self.Periodic   = 1
        self.CheckAll   = False
        self.Start      = int(time.time())
        self.State      = None
        self.StateTime  = None
        self.OnState    = None
        self.Checks     = {}
        self.Controls   = {}
        self.Triggers   = {}

    def GetState(self): 
        return self.State ^ self.Invert


    def LoadParamPattern(self, aParam, aPattern):
        self.Clear()

        Diff = set(aParam.keys()) - set(aPattern.keys())
        if (Diff):
            self.Logger.warn('%s->LoadParam. Unknown key %s' % (self.__class__.__name__, str(Diff)))

        for Key in aPattern:
            Default = aPattern.get(Key)
            Param   = aParam.get(Key, Default)
            if ( (Default == _Required) and (Param == _Required) ):
                Msg = "%s->LoadParam. Key %s is required" % (self.__class__.__name__, Key)
                self.Logger.error(Msg)
                raise ValueError(Msg)

            setattr(self, Key, Param)
  
    def CheckChild(self):
        Result = True

        for Key in self.Checks:
            if (not self.Checks[Key].Check()):
                Result = False
                if (not self.CheckAll):
                    break
        return Result

    def Check(self):
        if (self.Uptime() % self.Periodic == 0):
            StateChild = self.CheckChild()
            State      = self._Check(StateChild)
            if (self.State != State):
                self.State = State
                self.DoState()

        return self.GetState()

    def DoState(self):
        ClassPath = self.__class__.__name__
        self.Logger.info('%s->DoState. Alias %s, State %s' % (ClassPath, self.Alias, self.GetState()))

        self.StateTime = int(time.time())

        for Key in self.Triggers:
            self.Logger.info('%s->DoState. Trigger %s' % (ClassPath, Key))
            self.Triggers[Key].Check()

        if (self.OnState):
            Result = self.OnState(self)
        else:
            Result = True
        return Result 


class TThread():
    def __init__(self, aTarget, aType):
        self.Target   = aTarget
        self.Data     = multiprocessing.Value(aType, 0)
        self.Periodic = 10

    def Create(self):
        process = multiprocessing.Process(target = self._Run, args = [])
        process.daemon = True
        process.start()
        time.sleep(0.1)

    def _Run(self):
        while True:
            Value = self.Target()
            self.Data.value = Value
            time.sleep(self.Periodic)
