from control import TControl

__all__ = ["TPio"]


class TPio(TControl):
    def __init__(self, aParent):
        TControl.__init__(self, aParent)

    def LoadParam(self, aParam):
        self.Invert = aParam.get('Invert', False)
