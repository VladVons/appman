
class TControl():
    def __init__(self, aParent):
        self.Parent = aParent
        self.State    = None
        self.Alias    = None
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
        self.Logger.info('TControl->DoState. State %s. Alias %s' % (self.State, self.Alias))

        for Key in self.Triggers:
            self.Triggers[Key].Set(self.State)

        if (self.OnState):
            Result = self.OnState(self)
        else:
            Result = True
        return Result 
