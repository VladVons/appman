#!/bin/bash
# Created: 28.09.2016
# Vladimir Vons, VladVons@gmail.com


Install()
{
  Installed=$(pip list | grep Flask)
  if [ ! "$Installed" ]; then
    apt-get install python-pip
    #
    pip install Flask
    pip install Flask-WTF
    pip install webhelpers
  fi

  #pip uninstall webhelpers
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


Clean()
{
  echo "delete objects"
  find . -name '*.pyc' -exec rm -v -f -R {} \;
  find . -name '*.log' -exec rm -v -f -R {} \;

  echo
  echo "Statistics *.py"
  #find . -name '*.py' -ls | awk '{total += $7} END {print total}'
  find . -name '*.py' | xargs wc

  echo
  echo "Statistics *.json"
  find . -name '*.json' | xargs wc
}

GitCreate()
{
  # create new project on disk
  git init

  # sign with eMail
  git config --global user.email "vladvons@gmail.com"

  # no password 
  git config --global credential.helper 'cache --timeout=36000'

  # remote git server location
  git remote add origin https://github.com/VladVons/appman.git

}

GitClone()
{
  # restore clone copy fromserver to disk 
  git clone https://github.com/VladVons/appman.git

  #web admin access here
  #https://github.com/VladVons/appman
}


GitSyncToServ()
# sync only changes from disk to server 
{
  git status

  #git add install.sh
  #git rm TestClient.py
  #git mv README.md README
  #git log

  git add -u -v
  git commit -a -m "just commit"
  git push -u origin master
}

GitFromServ()
# sync changes from server to disk
{
  git pull
}

GitToServ()
# sync changes from disk to serv
{
  Clean
  # add all new files
  git add -A -v
  GitSyncToServ
}


#GitUpdate

clear
case $1 in
    Clean)          "$1"        "$2" "$3" ;;
    GitCreate)      "$1"        "$2" "$3" ;;
    GitToServ|t)    GitToServ   "$2" "$3" ;;
    GitFromServ|f)  GitFromServ "$2" "$3" ;;
    Install)        "$1"        "$2" "$3" ;;
    ServiceRun)     "$1"        "$2" "$3" ;;
esac

