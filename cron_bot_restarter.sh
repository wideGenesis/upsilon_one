#!/usr/bin/env bash

BASEDIR=/home/upsilonsfather/projects/ups_one
LOGDIR=$BASEDIR/logs

amount=$(ps -ef | grep "python3" | grep "upsilon_bot.py" | wc -l)

#whoami >> $BASEDIR/cron_strter.log

if [[ $amount == 0 ]] && [[ ! -f $BASEDIR/do_not_restart.txt ]]
then
   #echo "Try start bot + $(date +'%Y-%m-%d %H:%M:%S')" >> $BASEDIR/cron_strter.log
   cd $BASEDIR
   source $BASEDIR/venv/bin/activate
   python3 $BASEDIR/upsilon_bot.py  > $LOGDIR/bot.log 2>&1 &
   deactivate
fi
#echo "END cron restarter + $(date +'%Y-%m-%d %H:%M:%S')" >> $BASEDIR/cron_strter.log

