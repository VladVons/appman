#!/usr/bin/python

# Created: 21.08.2016
# Vladimir Vons, VladVons@gmail.com


from SockServer import *
from AppMan import *

#---
AppMan = TAppMan()
SockServer = TSockServer(AppMan.Option)
SockServer.Connect()

print("done")
