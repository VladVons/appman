#!/bin/bash
# Created: 28.09.2016
# Vladimir Vons, VladVons@gmail.com


Install()
{
  Installed=$(pip list | grep Flask)
  if [ ! "$Installed" ]; then
    apt-get install python-pip
    #apt-get install python3-pip
    #
    pip install Flask
    pip install Flask-WTF
    pip install webhelpers

    #pip3 install RPi.GPIO
  fi

  #pip uninstall webhelpers

  #http://www.raspberry-projects.com/pi/software_utilities/email/ssmtp-to-send-emails
  apt-get install ssmtp mailutils
}


ServiceRun()
{
  #ln -s $(pwd)/etc/init.d/appman  /etc/init.d/appman
  #ln -s $(pwd)/etc/default/appman /etc/default/appman

  cp etc/linux/init.d/appman  /etc/init.d/
  cp etc/linux/default/appman /etc/default/
  echo WORKDIR="$(pwd)/src" >> /etc/default/appman

  cp etc/linux/init.d/appman_web  /etc/init.d/appman
  cp etc/linux/default/appman /etc/default/appman
  echo WORKDIR="$(pwd)/web" >> /etc/default/appman_web

  #update-rc.d appman defaults
  #systemctl daemon-reload
  service appman start
  service appman_web start

  echo
  echo "Check appman server running"
  service appman status
  ps aux | grep -iv "grep" | egrep -i "AppMan_Server|AppMan_Web"

  #cd web
  #python AppMan_Web.py
  #nohup python AppMan_Web.py &

  #kill python process 
  #pkill -f Main.py

  #listen on http://0.0.0.0:5000
}


clear
case $1 in
    Install)        "$1"        "$2" "$3" ;;
    ServiceRun)     "$1"        "$2" "$3" ;;
esac

