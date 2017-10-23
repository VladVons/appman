# Created: 15.10.2017
# Vladimir Vons, VladVons@gmail.com

#from inc.Common import *

def Debug():
    #https://docs.python.org/3/library/inspect.html
    import sys
    function_name = sys._getframe(1).f_code.co_name
    filename      = sys._getframe(1).f_code.co_filename
    class_name   = sys._getframe(1).__class__
    #print('---', class_name.__name__)
    #return filename + '->' + class_name + '->' + function_name 


class TObject():
    def __init__(self, aParent):
        self.Parent     = aParent
        self.ParentRoot = None
        self.Alias      = None

    def GetClassPath(self, aClass, aPath = '', aDepth = 99):
        Class = aClass.__bases__
        if ( (Class) and (aDepth > 0) ):
            aPath = self.GetClassPath(Class[0], aPath, aDepth - 1)
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
        #print(Debug())
        ClassPath = self.GetClassPath(self.__class__, '', 0)
        self.Logger.info('%s->DoState. State %s. Alias %s' % (ClassPath, self.State, self.Alias))

        for Key in self.Triggers:
            self.Logger.info('%s->DoState. Trigger %s' % (ClassPath, Key))
            self.Triggers[Key].Set(self.State)

        if (self.OnState):
            Result = self.OnState(self)
        else:
            Result = True
        return Result 
