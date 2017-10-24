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

    def Post(self, aSignal, **aParam):
        #raise NotImplementedError("Method not implemented")
        print('Post', aSignal, aParam)


class TControl(TObject):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.State     = None
        self.OnState   = None
        self.StateTime = None
        self.Start     = int(time.time())

        self.Clear()

    #def _ChaeckParam(self, aData):
    #    for Key in aData.keys()
    #        if 

    def Clear(self):
        self.Checks   = {}
        self.Controls = {}
        self.Triggers = {}

    def CheckChild(self):
        for Key in self.Checks:
            if (not self.Checks[Key].Check()):
                return False
        return True

    def Check(self):
        raise NotImplementedError('Method not Implemented')

    def DoState(self):
        ClassPath = self.__class__.__name__
        self.Logger.info('%s->DoState. Alias %s, State %s' % (ClassPath, self.Alias, self.State))

        self.StateTime = int(time.time())

        for Key in self.Triggers:
            self.Logger.info('%s->DoState. Trigger %s' % (ClassPath, Key))
            self.Triggers[Key].Set(self.State)

        if (self.OnState):
            Result = self.OnState(self)
        else:
            Result = True
        return Result 
