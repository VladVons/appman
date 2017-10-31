# Created: 15.10.2017
# Vladimir Vons, VladVons@gmail.com

import time
import multiprocessing
#
#from inc.Common import *

__all__ = ['TObject', 'TControl', 'TControlThredRead', '_Required']

_Required = '_Required'
DefPattern  = {'Invert':False, 'Periodic':1, 'State':False, 'CheckAll':False}


# for reading slow devices
class TThreadRead():
    def __init__(self, aObjRead):
        self.ObjRead  = aObjRead
        self.Periodic = 3
        self.Queue    = multiprocessing.Queue()

    def Create(self):
        process = multiprocessing.Process(target = self._Run, args = [])
        process.daemon = True
        process.start()

    # Method called from outside
    def GetData(self):
        # check if Queue. is not empty
        try: 
            Result = self.Queue.get(block = False)
        except:
            Result = None
        return Result

    def _Run(self):
        while True:
            if (self.ObjRead):
                Value = self.ObjRead()
                self.Queue.put(Value)
            time.sleep(self.Periodic)


class TParam():
    def __init__(self, aParent, aPattern):
        self.Parent  = aParent
        self.Pattern = aPattern
        self.Loaded  = False
        self.Init()

    def Init(self):
        if (self.Pattern):
            for Key in self.Pattern:
                setattr(self, Key, self.Pattern.get(Key))

    def Load(self, aParam, aPattern):
        Pattern = {**self.Pattern, **aPattern}

        Diff = set(aParam.keys()) - set(Pattern.keys())
        if (Diff):
            self.Parent.Logger.warn('%s->LoadPattern. Unknown key %s' % (self.__class__.__name__, str(Diff)))

        for Key in Pattern:
            Default = Pattern.get(Key)
            Param   = aParam.get(Key, Default)
            if ( (Default == _Required) and (Param == _Required) ):
                self.Parent._Error('%s->Load. Key %s is required' % (self.__class__.__name__, Key))

            setattr(self, Key, Param)

        self.Loaded = True


class TObject():
    def __init__(self, aParent):
        self.Parent     = aParent
        self.ParentRoot = None
        self.Alias      = None
        self.Param      = TParam(self, DefPattern)
        self.Value      = None

    def _Error(self, aMsg):
        self.Logger.error(aMsg)
        raise ValueError(aMsg)


class TControl(TObject):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.OnState    = None
        self.OnValue    = None
        self.StartTime  = int(time.time())

        self.Clear()

    def _Check(self, aValue):
        raise NotImplementedError('Method not Implemented')

    def LoadParam(self, aParam):
        raise NotImplementedError('Method not Implemented')

    def Uptime(self):
        return int(time.time() - self.StartTime)

    def Clear(self):
        self.Value      = 0
        self.StateTime  = None
        self.Checks     = {}
        self.Controls   = {}
        self.Triggers   = {}

    def GetState(self): 
        return self.Param.State ^ self.Param.Invert

    def CheckChild(self):
        Result = True

        for Key in self.Checks:
            if (not self.Checks[Key].Check()):
                Result = False
                if (not self.Param.CheckAll):
                    break
        return Result

    def Check(self):
        #print('TObject->Check', 'Alias', self.Alias)
        if (self.Uptime() % self.Param.Periodic == 0):
            #print(self.Alias, self.Param.Loaded)
            if (self.Param.Loaded):
                Value = self._Get()
                if (self.Value != Value):
                    self.Value = Value
                    if (self.OnValue):
                        self.OnValue(self)

            StateChild = self.CheckChild()
            State = self._Check(StateChild) and StateChild
            if (self.Param.State != State):
                self.Param.State = State
                self.StateTime = int(time.time())
                self.DoOnState()

        return self.GetState()

    def DoOnState(self):
        ClassPath = self.__class__.__name__
        #self.Logger.info('%s->DoState. Alias %s, State %s, OnState %s, Trigger %s' % (ClassPath, self.Alias, self.GetState(), str(self.OnState), str(self.Triggers)))

        for Key in self.Triggers:
            self.Logger.info('%s->DoState. Trigger %s' % (ClassPath, Key))
            self.Triggers[Key].Check()

        if (self.OnState):
            self.OnState(self)


class TControlThredRead(TControl):
    def LoadParamPattern(self, aParam, aPattern):
        self.Param.Load(aParam, aPattern)

        self.Thread = TThreadRead(self._ReadCallBack)
        self.Thread.Create()

    # call slow method from thread
    def _ReadCallBack(self):
        raise NotImplementedError('Method not Implemented')

    def _Check(self, aValue):
        Result = (self.Value < self.Param.Min) or (self.Value > self.Param.Max)
        return Result
