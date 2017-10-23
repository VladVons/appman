# Created: 15.10.2017
# Vladimir Vons, VladVons@gmail.com


class TObject():
    def __init__(self, aParent):
        self.Parent   = aParent
        self.Alias    = None

    def GetClassPath(self, aClass, aPath = ''):
        Class = list(aClass.__bases__)
        for Base in Class:
            aPath = self.GetClassPath(Base, aPath)
        return aPath + '/' + aClass.__name__

    def Post(self, aSignal, **aParam):
        #raise NotImplementedError("Method not implemented")
        print('Post', aSignal, aParam)


class TControl(TObject):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.State    = None
        self.OnState  = None
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
        raise NotImplementedError("Method not Implemented")

    def DoState(self):
        self.Logger.info('%s->DoState. State %s. Alias %s' % (self.GetClassPath(self.__class__), self.State, self.Alias))

        for Key in self.Triggers:
            self.Triggers[Key].Set(self.State)

        if (self.OnState):
            Result = self.OnState(self)
        else:
            Result = True
        return Result 
