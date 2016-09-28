#!/bin/bash

gAuth="--user=root --password=19710819"


Log()
{
  aStr="$1"

  #echo "$aStr"
}


SQL()
{
  aSQL="$1"; aHost=${2:-"localhost"};

  mysql $gAuth --host=$aHost --disable-column-names --batch --execute="$aSQL"
}


DbCreate()
{
  aDBName="$1";
  Log "$0->$FUNCNAME, $aDBName"

  SQL "CREATE DATABASE IF NOT EXISTS $aDBName;"
}


DbDelete()
{
  aDBName="$1";
  Log "$0->$FUNCNAME, $aDBName"

  SQL "DROP DATABASE $aDBName;"
}


DbGrant()
{
  aDBName="$1"; aDBUserName="$2"; aDBUserPassw="$3"
  Log "$0->$FUNCNAME, $aDBName, $aDBUserName, $aDBUserPassw"

  SQL "GRANT ALL PRIVILEGES ON ${aDBName}.* TO '${aDBUserName}'@'localhost' IDENTIFIED BY '${aDBUserPassw}' WITH GRANT OPTION;"
  SQL "flush privileges;"
}


DbList()
{
  SQL "SHOW DATABASES;" | egrep -v "(information_schema|mysql|performance_schema)"
}


UserList()
{
  SQL "SELECT host,user FROM mysql.user"
}


Help()
{
  echo "usage: $0->$FUNCNAME <Arg>"
}


clear
case $1 in
    DbCreate)  $1 $2 $3 $4 $5 ;;
    DbDelete)  $1 $2 $3 $4 $5 ;;
    DbGrant)   $1 $2 $3 $4 $5 ;;
    DbList)    $1 $2 $3 $4 $5 ;;
    SQL)       $1 $2 $3 $4 $5 ;;
    UserList)  $1 $2 $3 $4 $5 ;;
    *)      Help ;;
esac
