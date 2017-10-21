
class TControl():
    def __init__(self, aParent):
        self.Parent = aParent
        self.Checks   = {}
        self.Controls = {}
        self.State    = None
        self.Alias    = None
        self.OnState  = None

    #def _ChaeckParam(self, aData):
    #    for Key in aData.keys()
    #        if 

    def CheckChild(self):
        for Key in self.Checks:
            #print('TControl->CheckChild', self.Alias, Key)
            if (not self.Checks[Key].Check()):
                return False
        return True

    def Check(self):
        raise NotImplementedError("Method not Implemented")

    def DoState(self):
        self.Logger.info('TControl->DoChange. State %s. Alias %s' % (self.State, self.Alias))

        if (self.OnState):
            Result = self.OnState(self)
        else:
            Result = True
        return Result 
