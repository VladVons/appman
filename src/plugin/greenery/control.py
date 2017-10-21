
class TControl():
    def __init__(self, aParent):
        self.Parent = aParent
        self.Checks   = {}
        self.Controls = {}

    #def _ChaeckParam(self, aData):
    #    for Key in aData.keys()
    #        if 

    def CheckChild(self):
        for Key in self.Checks:
            #print('TControl->CheckChild', self.Alias, Key)
            if (not self.Checks[Key].Check()):
                return False
        return True

