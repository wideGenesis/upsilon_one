#!/usr/bin/env bash

BASEDIR=/home/upsilonsfather/projects/ups_one
amount=$(ps -ef | grep "python3" | grep "upsilon_bot.py" | wc -l)

#whoami >> $BASEDIR/cron_strter.log

if [[ $amount == 0 ]] && [[ ! -f $BASEDIR/do_not_restart.txt ]]
then
   #echo "Try start bot + $(date +'%Y-%m-%d %H:%M:%S')" >> $BASEDIR/cron_strter.log
   cd $BASEDIR
   source $BASEDIR/venv/bin/activate
   python3 $BASEDIR/upsilon_bot.py >/dev/null 2>/dev/null &
   python3 $BASEDIR/quotes/get_screens.py >/dev/null 2>/dev/null &
   deactivate
fi
#echo "END cron restarter + $(date +'%Y-%m-%d %H:%M:%S')" >> $BASEDIR/cron_strter.log

