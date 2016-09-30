# Created: 23.09.2016
# Vladimir Vons, VladVons@gmail.com

from flask import redirect, request, render_template, flash
from wtforms import Form, StringField, PasswordField, SubmitField, validators
from wtforms.validators import Required, Length
from webhelpers.html.grid import Grid
from webhelpers.html import HTML

from Session import User, TUser

import sys
sys.path.insert(0, '../src/inc')
from Common import *


class TFIndex(Form):
    Title    = "Main"
    Teplate  = "TFIndex.html"

    def Render(self):
        self.UserOK  = User.OK()
        self.Version = User.Call("TAppMan.GetVersion")["Version"]
        return render_template(self.Teplate, Form = self)


class TFLogin(Form):
    Title    = "Login user"
    Teplate  = "TFLogin.html"
    UserName = StringField(description ="User", validators = [Required(), Length(min=1, max=16)])
    Password = PasswordField(description ="Password", validators = [Length(min=1, max=16)])
    Submit   = SubmitField("Log in")

    def Render(self):
        self.Error = ""
        if (User.OK()):
            return redirect("/")
        else:
            if (request.method == "POST"):
                if (self.validate()):
                    if (User.Connect(User.Host, User.Port, self.UserName.data, self.Password.data)):
                        return redirect("/conf_list")
                    else:
                        self.Error = "Username or password incorrect"
                        flash(self.Error)
            return render_template(self.Teplate, Form = self)


class TFConfList(Form):
    Title   = "Config list"
    Teplate = "TFConfList.html"

    def Render(self):
        if (not User.OK()):
            return redirect("/login")
        else:
            GridColumns = ["_numbered", "File", "Version", "Run", "Tag", "Descr"]
            GridItems   = []
            Files   = User.Call("TAppMan.GetListConf")
            for File in Files:
                User.Call("TAppMan.LoadFile", File)
                Conf  = HTML.a(File, href="pkg_info?name=" + File)
                Pairs = User.Call("TAppMan.Variable.GetPairs", "Value")
                Run   = User.Call("TAppMan.Cmd.ShowService").strip() != ""
                Ver   = User.Call("TAppMan.Cmd.PkgVersion")
                GridItems.append( {"File": Conf, "Tag": Pairs.get("Tag"), "Version": Ver, "Descr": Pairs.get("Descr"), "Run": Run } )
            self.Grid = Grid(GridItems, GridColumns)
            return render_template(self.Teplate, Form = self)

class TFPkgInfo(Form):
    Title    = "Package information"
    Template = "TFPkgInfo.html"

    def CustomSort(self, aItem1, aItem2):
        Idx1 = TList.Find(self.SortOrd, aItem1["Field"])
        Idx2 = TList.Find(self.SortOrd, aItem2["Field"])
        if ((Idx1 != -1) and (Idx2 != -1)):
            return Idx1 - Idx2
        else:
            return 0

    def GetList(self, aFile):
        Result = []

        Xlat = {}
        Xlat["Install"] = "TAppMan.Cmd.PkgVersion"
        Xlat["Service"] = "TAppMan.Cmd.ShowService"
        Xlat["Process"] = "TAppMan.Cmd.ShowProcess"
        Xlat["Port"]    = "TAppMan.Cmd.ShowPort"

        User.Call("TAppMan.LoadFile", aFile)
        PairsVar = User.Call("TAppMan.Variable.GetPairs", "Value")
        HideVar  = User.Call("TAppMan.Variable.GetFieldList", "App_HideVar/Value")
        for Item in PairsVar:
            if (not Item.startswith(tuple(HideVar))):
                if (Item in Xlat):
                    CmdRes = User.Call(Xlat[Item])
                elif (Item in ["Pid", "Script", "Config", "Log"]):
                    IsFile = User.Call("TAppMan.Util.FileExist", PairsVar.get(Item))
                    if (IsFile):
                        CmdRes = HTML.a("more...", href="/file_show?name=" + PairsVar.get(Item) + "&type=" + Item)
                    else:
                        CmdRes = "Not found"
                else:
                    CmdRes = ""
                Result.append( {"Field": Item, "Value": PairsVar.get(Item),  "Info": CmdRes} )

        Prop = User.Call("TAppMan.Editor.GetPath")
        if (Prop):
            Result.append( {"Field": "Config", "Value": Prop, "Info": ""} )

        self.SortOrd = User.Call("TAppMan.Variable.GetFieldList", "App_SortVar/Value")
        if (len(self.SortOrd) > 0):
            Result.sort(self.CustomSort)
        else:
            Result.sort()
        return Result

    def Render(self):
        if (not User.OK()):
            return redirect("/login")
        else:
            if (request.method == "GET"):
                GridColumns   = ["_numbered", "Field", "Value", "Info"]
                GridItems     = self.GetList(request.args.get("name"))
                self.Grid = Grid(GridItems, GridColumns)

            return render_template(self.Template, Form = self)

class TFFileShow(Form):
    Title    = "Show file"
    Template = "TFFileShow.html"

    def Render(self):
        if (not User.OK()):
            return redirect("/login")
        else:
            if (request.method == "GET"):
                if (request.args.get("type") == "Log"):
                    Data = User.Call("TAppMan.Cmd.ShowLog")
                else:
                    FileName = request.args.get("name")
                    Data = User.Call("TAppMan.Util.FileRead", FileName)
                    #self.FileData = Data.replace("\n", "<br>")
                self.FileData = Data

            return render_template(self.Template, Form = self)

class TFUtil(Form):
    Title   = "Utils"
    Teplate = "TFUtil.html"

    def Render(self):
        if (not User.OK()):
            return redirect("/login")
        else:
            GridColumns = ["_numbered", "Name", "Command", "Result"]
            GridItems   = []

            PairsVar = User.Call("TAppMan.Variable.GetPairs", "Value")
            Utils    = User.Call("TAppMan.Variable.GetFieldList", "App_Util/Value")
            for Util in Utils:
                #Var      = HTML.a(Util, href="util1?name=" + Util)
                Var      = Util
                ExecVar  = "Util_" + Util
                ExecStr  = PairsVar.get(ExecVar)
                ExecRes  = User.Call("TAppMan.Util.ExecVar", ExecVar)
                GridItems.append( {"Name": Var, "Command": ExecStr, "Result" : ExecRes} )
            self.Grid = Grid(GridItems, GridColumns)
            return render_template(self.Teplate, Form = self)
