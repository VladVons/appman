# Created: 23.09.2016
# Vladimir Vons, VladVons@gmail.com

from flask import redirect, request, render_template, flash
from wtforms import Form, StringField, PasswordField, SubmitField, validators
from wtforms.validators import Required, Length
from webhelpers.html.grid import Grid
from webhelpers.html import HTML
#
from Const import *
from Session import User, TUser

import sys
sys.path.insert(0, '../src/inc')
from Common import *


class TFIndex(Form):

    Title    = "Main"
    Teplate  = "TFIndex.html"

    def Render(self):
        import getpass

        self.UserOK  = User.OK()
        self.Info    = User.Call("TAppMan.GetInfo()")
        self.UserWeb = getpass.getuser()
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
                    if (User.Connect(cAppHost, cAppPort, self.UserName.data, self.Password.data)):
                        return redirect("/conf_list")
                    else:
                        self.Error = "Username or password incorrect " + User.LastError
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
            Files = User.Call("TAppMan.GetListConf")
            for File in Files:
                User.Call("TAppMan.LoadFile", File)
                Pairs = User.Call("TAppMan.Var.GetPairs('Value')")

                Run = False
                if ("Process" in Pairs):
                    Run = User.Call("TAppMan.Cmd.ExecField", "Process").strip() != ""

                Ver = ""
                if ("PkgInstall" in Pairs):
                    Ver = User.Call("TAppMan.Cmd.ExecField", "PkgVersion")

                Conf  = HTML.a(File, href="pkg_info?name=" + File)
                GridItems.append( {"File": Conf, "Tag": Pairs.get("Tag"), "Version": Ver, "Descr": Pairs.get("Descr"), "Run": Run } )
            self.Grid = Grid(GridItems, GridColumns, order_direction = "dsc")
            return render_template(self.Teplate, Form = self)

class TFPkgInfo(Form):
    Title    = "Package information"
    Template = "TFPkgInfo.html"

    def CustomSort_GridVar(self, aItem1, aItem2):
        Idx1 = TList.Find(self.SortOrd, aItem1["Field"])
        Idx2 = TList.Find(self.SortOrd, aItem2["Field"])
        if ((Idx1 != -1) and (Idx2 != -1)):
            return Idx1 - Idx2
        else:
            return 0


    def GetUserList(self):
        Result = []

        PairsVar = User.Call("TAppMan.User.GetPairs", "Cmd")
        for Item in PairsVar:
            if ("List" in Item):
                CmdRes = User.Call("TAppMan.User.List")
            else:
                CmdRes = ""

            Result.append( {"Field": Item, "Value": PairsVar.get(Item),  "Info": CmdRes} )

        return Result

    def GetVarList(self):
        Result = []

        PairsVar = User.Call("TAppMan.Var.GetPairs('Value')")
        PairsCmd = User.Call("TAppMan.Cmd.GetPairs('Value')")
        HideVar  = User.Call("TAppMan.Var.GetFieldList('App_HideVar/Value')")
        for Item in PairsVar:
            if (not Item.startswith(tuple(HideVar))):
                if (Item in PairsCmd):
                    CmdRes   = User.Call("TAppMan.Cmd.ExecField", Item, "CmdInfo")
                    LastExec = User.GetProp("TAppMan.Cmd.LastExec")
                    Result.append( {"Field": Item, "Value": PairsVar.get(Item), "Info": CmdRes,  "Command": LastExec} )
                else:
                    Result.append( {"Field": Item, "Value": PairsVar.get(Item), "Info": "",      "Command": ""} )

        Prop = User.Call("TAppMan.Editor.GetPath")
        if (Prop):
            Result.append( {"Field": "Config", "Value": Prop, "Info": "", "Command": ""} )

        self.SortOrd = User.Call("TAppMan.Var.GetFieldList('App_SortVar/Value')")
        if (len(self.SortOrd) > 0):
            Result.sort(self.CustomSort_GridVar)
        else:
            Result.sort()
        return Result

    def Render(self):
        if (not User.OK()):
            return redirect("/login")
        else:
            if (request.method == "GET"):
                aFile = request.args.get("name")
                User.Call("TAppMan.LoadFile", aFile)

                GridVarItems      = self.GetVarList()
                GridVarColumns    = ["_numbered", "Field", "Value", "Info", "Command"]
                self.GridVar      = Grid(GridVarItems, GridVarColumns)
                self.GridVarTitle = "Variables"

                GridUserItems = self.GetUserList()
                if (len(GridUserItems) > 0):
                    GridUserColumns    = ["_numbered", "Field", "Value", "Info"]
                #    self.GridUser      = Grid(GridUserItems, GridUserColumns)
                #    self.GridUserTitle = "Users"

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

            PairsVar = User.Call("TAppMan.Var.GetPairs", "Value")
            Utils    = User.Call("TAppMan.Var.GetFieldList", "App_Util/Value")
            for Util in Utils:
                #Var      = HTML.a(Util, href="util1?name=" + Util)
                Var      = Util
                ExecVar  = "Util_" + Util
                ExecStr  = PairsVar.get(ExecVar)
                ExecRes  = User.Call("TAppMan.Util.ExecVar", ExecVar)
                GridItems.append( {"Name": Var, "Command": ExecStr, "Result" : ExecRes} )
            self.Grid = Grid(GridItems, GridColumns)
            return render_template(self.Teplate, Form = self)
