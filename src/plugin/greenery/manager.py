#!/usr/bin/python

from libtimer import *
from libpio import *


class TManager():
    def __init__(self):
        self.Obj = {}

    def _CreateClass(self, aData, aParent):
        Alias = aData.get('Alias')
        if (not Alias):
            raise ValueError('Key "%s" not found' % ('Alias'))

        ClassName = aData.get('Class')
        if (not ClassName):
            raise ValueError('Key "%s" not found %s' % ('Class', aData))

        ModuleName = aData.get('Module')
        if (ModuleName):
            Module = __import__(ModuleName)
            TClass = getattr(Module, ClassName)
            del Module
        else:
            TClass = globals()[ClassName]

        Class  = TClass(aParent)
        Class.Alias = Alias

        return Class

    def _LoadClass(self, aData, aParent):
        Enable = aData.get('Enable', True)
        if (not Enable):
            return None
  
        Ref = aData.get('Ref')
        if (Ref):
            Class = self.Obj.get(Ref)
            if (not Class):
                print('Warn: Ref "%s" not found' % (Ref))
        else:
            Class = self._CreateClass(aData, aParent)

            Param = aData.get('Param')
            if (Param):
                Class.LoadParam(Param)

            for Section in ['Checks', 'Controls']:
                Items = aData.get(Section)
                if (Items):
                    for Item in Items:
                        ClassSection = self._LoadClass(Item, Class)
                        if (ClassSection):
                            getattr(Class, Section)[ClassSection.Alias] = ClassSection

        return Class

    def Load(self, aData):
        for Item in aData:
            Class = self._LoadClass(Item, self)
            if (Class):
                self.Obj[Class.Alias] = Class

    def Signal(self, aList = []):
        if (len(aList) == 0):
            Keys = self.Obj
        else:
            Keys = aList

        for Key in Keys:
            print('TManager->Signal', 'Key', Key, self.Obj[Key].Check())
