#!/bin/bash

clear

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

  cp etc/init.d/appman  /etc/init.d/appman
  cp etc/default/appman /etc/default/appman
  echo WORKDIR="$(pwd)/src" >> /etc/default/appman

  #update-rc.d appman defaults
  #systemctl daemon-reload
  service appman start

  echo
  echo "Check appman server running"
  service appman status
  ps aux | grep -iv "grep" | grep -i "RunServer.py"

  cd web
  python Main.py

  #listen on http://0.0.0.0:5000
}


Clean()
{
  echo "delete objects"
  find . -name '*.pyc' -exec rm -v -R {} \;
  find . -name '*.log' -exec rm -v -R {} \;

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
  git init
  git config --global user.email "vladvons@gmail.com"
  git add -A
  git commit -m "first commit"
  git remote add origin https://github.com/VladVons/appman.git
  git push -u origin master
}

GitDownload()
{
  git clone https://github.com/VladVons/appman.git
}


GitUpload()
{
  git status
  git add install.sh
  git commit
}



clear
#
Clean
#GitCreate

#Install
#ServiceRun
