#!/usr/bin/env bash
die(){
    echo >&2 "$@"
    exit 1
}

BASEDIR=/home/upsilonsfather/projects/ups_one

amount=$(ps -ef | grep "python3" | grep "upsilon_bot.py" | wc -l)

if [[ $amount == 1 ]]
then
  sudo kill -9 $(pgrep -f upsilon_bot.py)
  if [[ ! -f $BASEDIR/do_not_restart.txt ]]
  then
        touch $BASEDIR/do_not_restart.txt
  fi
  die "Process successfully kiled"
  exit 0
fi
if [[ $amount == 0 ]]
then
  die "Can't find the process!"
fi
if [[ $amount > 1 ]]
then
        die "Find more than one processes!"
fi
