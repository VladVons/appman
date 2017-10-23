# Created: 15.10.2017
# Vladimir Vons, VladVons@gmail.com


class TObject():
    def __init__(self, aParent):
        self.Parent     = aParent
        self.ParentRoot = None
        self.Alias      = None

    def GetClassPath(self, aClass, aPath = ''):
        Class = aClass.__bases__
        if (Class):
            aPath = self.GetClassPath(Class[0], aPath)
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
        raise NotImplementedError('Method not Implemented')

    def DoState(self):
        ClassPath = self.GetClassPath(self.__class__)
        self.Logger.info('%s->DoState. State %s. Alias %s' % (ClassPath, self.State, self.Alias))

        for Key in self.Triggers:
            self.Logger.info('%s->DoState. Trigger %s' % (ClassPath, Key))
            self.Triggers[Key].Set(self.State)

        if (self.OnState):
            Result = self.OnState(self)
        else:
            Result = True
        return Result 
