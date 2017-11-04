# Created: 15.10.2017
# Vladimir Vons, VladVons@gmail.com

import logging

__all__ = ['TLog', 'Log']


class TLog():
    def __init__(self):
        self.LogLevel = 1

    def Print(self, aLevel, aType, *aParam):
        Result = 'Level %d: %s%s' % (aLevel, ' ' * aLevel, list(aParam))

        if (aLevel <= self.LogLevel):
            if (aType == 'w'):
                self.Logger.warn(Result)
            elif (aType == 'e'):
                self.Logger.error(Result)
            else:
                self.Logger.info(Result)
        return Result

    def SetConsole(self):
        self.Logger = logging.getLogger('MyConsole')
        self.Logger.addHandler(logging.StreamHandler())

    def SetFile(self, aFile):
        Result = False

        # Format = '[%(asctime)s], %(module)s->%(funcName)s->%(lineno)d,
        # %(levelname)s: %(message)s'
        Format = '[%(asctime)s], %(levelname)s:%(message)s'
        try:
            logging.basicConfig(
                            level=logging.INFO,
                            format=Format,
                            datefmt='%Y/%m/%d %H:%M:%S',
                            filename=aFile,
                            filemode='a')
            Result = True
        except IOError as E:
            print ('%s->SetLoger Error: %s: %s' % (self.__class__.__name__, E, aFile))

        return Result

Log = TLog()
