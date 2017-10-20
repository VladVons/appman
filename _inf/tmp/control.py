
class TControl():
    def __init__(self, aParent):
        self.Parent = aParent
        self.Obj    = {}

    def CheckChild(self):
        for Key in self.Obj:
            if (not self.Obj[Key].Check()):
                return False
        return True

    def LoadClass(self, aData):
        Name = aData.get('Name')
        if (not Name):
            raise ValueError('Key "%s" not found' % ('Name'))

        ModuleName = aData.get('Module')
        if (not ModuleName):
            raise ValueError('Key "%s" not found' % ('Module'))

        ClassName = aData.get('Class')
        if (not ClassName):
            raise ValueError('Key "%s" not found' % ('Class'))

        Module = __import__(ModuleName)
        TClass = getattr(Module, ClassName)
        del Module
        Class  = TClass(self)
        Class.Name = Name

        Param = aData.get('Param')
        if (Param):
            Class.LoadParam(Param) 

        Items = aData.get('Check')
        if (Items):
            for Item in Items:
                ClassObj = self.LoadClass(Item)
                self.Obj[ClassObj.Name] = ClassObj

        return Class
