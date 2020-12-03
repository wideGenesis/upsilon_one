#!/usr/bin/env bash

BASEDIR=/home/upsilonsfather/projects/ups_one

source $BASEDIR/venv/bin/activate
#echo "[$(date +'%Y-%m-%d %H:%M:%S')]************* Start bot *************" > $BASEDIR/logs/stdout.log
python3 $BASEDIR/upsilon_bot.py &
#python3 $BASEDIR/quotes/get_screens.py >/dev/null 2>/dev/null &
deactivate
if [[ -f $BASEDIR/do_not_restart.txt ]]
then
        rm -fr $BASEDIR/do_not_restart.txt
fi
