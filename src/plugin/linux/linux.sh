#!/bin/bash
#--- VladVons@gmail.com

ExecM()
# Execute and show message
#-------------------------
{
  aExec="$1"; aMsg="$2";

  echo
  echo "$FUNCNAME, $aExec, $aMsg"
  eval "$aExec"
}


PkgUpgrade()
# ------------------------
{
  ExecM "dpkg --configure -a" "repair"
  #ExecM "dpkg --configure -a --force-depends"
  ExecM "apt-get install --fix-broken --yes" "fix broken"

  ExecM "apt-get update --yes" "update repositories"
  ExecM "apt-get dist-upgrade --yes" "upgrade packages and core"

  #ExecM "apt-get install update-manager-core"
  #ExecM "do-release-upgrade - d"

  ExecM "apt-get autoremove --yes"
  ExecM "apt-get clean --yes" "remove archive files"
  #ExecM "rm /var/lib/apt/lists/*" "remove cache files"
}


case $1 in
    PkgUpgrade)  $1 $2 $3 $4 $5 ;;
esac

