# Created: 15.10.2017
# Vladimir Vons, VladVons@gmail.com

import time
#
#from inc.Common import *

class TObject():
    def __init__(self, aParent):
        self.Parent     = aParent
        self.ParentRoot = None
        self.Alias      = None


class TControl(TObject):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.Clear()

    def _Check(self, aValue):
        raise NotImplementedError('Method not Implemented')

    def LoadParam(self, aParam):
        raise NotImplementedError('Method not Implemented')

    def Clear(self):
        self.Invert    = False
        self.Start     = int(time.time())
        self.State     = None
        self.StateTime = None
        self.OnState   = None
        self.Checks    = {}
        self.Controls  = {}
        self.Triggers  = {}

    def LoadParamPattern(self, aParam, aPattern):
        self.Clear()

        Diff = set(aParam.keys()) - set(aPattern.keys())
        if (Diff):
            self.Logger.warn('%s->LoadParam. Unknown key %s' % (self.__class__.__name__, str(Diff)))

        for Key in aPattern:
            Default = aPattern.get(Key)
            Param   = aParam.get(Key, Default)
            if ((Default == None) and (Param == None)):
                Msg = "%s->LoadParam. Key %s is required" % (self.__class__.__name__, Key)
                self.Logger.error(Msg)
                raise ValueError(Msg)

            setattr(self, Key, Param)
            #print('Key', Key, 'Param', Param, 'Default', Default)
  
    def CheckChild(self):
        for Key in self.Checks:
            if (not self.Checks[Key].Check()):
                return False
        return True

    def Check(self):
        Value  = self.CheckChild() ^ self.Invert
        Result = self._Check(Value)
        if (self.State != Result):
            self.State = Result
            self.DoState()

        return Result ^ self.Invert

    def DoState(self):
        ClassPath = self.__class__.__name__
        self.Logger.info('%s->DoState. Alias %s, State %s' % (ClassPath, self.Alias, self.State))

        self.StateTime = int(time.time())

        for Key in self.Triggers:
            self.Logger.info('%s->DoState. Trigger %s' % (ClassPath, Key))
            self.Triggers[Key].Check()

        if (self.OnState):
            Result = self.OnState(self)
        else:
            Result = True
        return Result 
