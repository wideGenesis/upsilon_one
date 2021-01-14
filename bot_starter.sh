#!/usr/bin/env bash

BASEDIR=/home/upsilonsfather/projects/ups_one
LOGDIR=BASEDIR/logs

source $BASEDIR/venv/bin/activate
echo "[$(date +'%Y-%m-%d %H:%M:%S')]************* Start bot *************" > $LOGDIR/bot.log
python3 $BASEDIR/upsilon_bot.py > $LOGDIR/bot.log 2>&1 &
deactivate
if [[ -f $BASEDIR/do_not_restart.txt ]]
then
        rm -fr $BASEDIR/do_not_restart.txt
fi
