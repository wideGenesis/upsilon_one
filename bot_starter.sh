#!/usr/bin/env bash

BASEDIR=/home/upsilonsfather/projects/ups_one
LOGDIR=$BASEDIR/logs

source $BASEDIR/venv/bin/activate
echo "[$(date +'%Y-%m-%d %H:%M:%S')]************* Start bot *************" > $LOGDIR/bot.log
cd $BASEDIR
# shellcheck disable=SC2069
python3 $BASEDIR/upsilon_bot.py 2>&1 > $LOGDIR/bot.log &
deactivate
if [[ -f $BASEDIR/do_not_restart.txt ]]
then
        rm -fr $BASEDIR/do_not_restart.txt
fi
