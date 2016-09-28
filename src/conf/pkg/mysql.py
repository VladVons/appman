from SectionExec import *


class User(TSUser):
    def Add(self, aName, aPassw, aDbName):
        return self.ExecCmd("Add", [aName, aPassw, aDbName])

    def Del(self, aName, aDbName):
        return self.ExecCmd("Del", [aName, aDbName])

    def TestShell(self, aName):
        return TShell.ExecM(aName)


class Cmd(TSCmd):
    def CreateDB(self, aName):
        return TShell.ExecM("mysql.sh DbCreate " + aName)
