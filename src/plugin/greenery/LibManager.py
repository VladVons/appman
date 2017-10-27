# Created: 26.10.2017
# Vladimir Vons, VladVons@gmail.com

from LibCommon import TControl, _Required


class TGroup(TControl):
    def LoadParam(self, aParam):
        Pattern = {'Diff':10}
        self.LoadParamPattern(aParam, Pattern)

    def _Check(self, aValue):
        self.Get()
        return True

    def Get(self):
        pass
