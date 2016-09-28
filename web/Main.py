# Created: 22.09.2016
# Vladimir Vons, VladVons@gmail.com
#
# Application manager

# sudo pip install Flask
# sudo pip install Flask-WTF
# sudo pip install webhelpers

#https://sarahleejane.github.io/learning/python/2015/08/09/simple-tables-in-webapps-using-flask-and-pandas-with-python.html
#https://wtforms.readthedocs.io/en/latest/
#https://pythonspot.com/en/login-authentication-with-flask/
#http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
#https://media.readthed ocs.org/pdf/webhelpers/latest/webhelpers.pdf
#http://metanit.com/web/angular/1.1.php


import os
from flask import Flask, request, redirect
#
from Forms import *
from Session import User, TUser

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def R_index():
    form = TFIndex(request.form)
    return form.Render()

@app.route("/file_show", methods=["POST", "GET"])
def R_file_show():
    form = TFFileShow(request.form)
    return form.Render()

@app.route("/pkg_info", methods=["POST", "GET"])
def R_pkg_info():
    form = TFPkgInfo(request.form)
    return form.Render()

@app.route("/conf_list", methods=["POST", "GET"])
def R_conf_list():
    form = TFConfList(request.form)
    return form.Render()

@app.route("/login", methods=["POST", "GET"])
def R_login():
    form = TFLogin(request.form)
    return form.Render()

@app.route("/logout")
def R_logout():
    User.Close()
    return R_index()

#---
if (__name__ == "__main__"):
    print("Start main")
    app.secret_key = "Vlad_" + str(os.urandom(12))
    app.run(host = '0.0.0.0', port = 5000, debug = True)
