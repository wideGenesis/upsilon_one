#!/usr/bin/env bash
# For tests run every 1 minutes
# * * * * * /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "1"
#
# For tests run every 5 minutes
# */5 * * * * /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "5"
#
# Start every 30 min
# */30 * * * * /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "30"
#
# Start every 120 min  (в первую минуту, каждого 2го часа)
# 1 */2 * * * /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "120"
#
# Start every 480 min  (в пятую минуту, каждого 8го часа)
# 5 */8 * * * /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "480"
#
# Start every 720 min  (в десятую минуту, каждого 12го часа)
# 10 */12 * * * /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "720"
#
# Start everyday  (каждый день в 3:00)
# на инстансе +5часов по отношению к New York Time ориентируемся при запуске на NYT
# что бы запустить что-то в 3:00 по NYT надо запускать в 8:00 по времени инстанса
# 0 8 * * * /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "EVERYDAY"
#
# Start monday  (каждый понедельник в 3:10)
# на инстансе +5часов по отношению к New York Time ориентируемся при запуске на NYT
# что бы запустить что-то в 3:00 по NYT надо запускать в 8:00 по времени инстанса
# 10 8 * * 0 /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "MONDAY"
#
# Start first date of month  (каждое первое число месяца в 4:00)
# на инстансе +5часов по отношению к New York Time ориентируемся при запуске на NYT
# что бы запустить что-то в 3:00 по NYT надо запускать в 8:00 по времени инстанса
# 0 9 1 * * /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "FIRST_DAY_OF_MONTH"
#
#
#
BASEDIR=/home/upsilonsfather/projects/ups_one
LOGDIR=$BASEDIR/logs

LOG_FILE_NAME='cron_scheduler_'$(date +%Y_%m_%d)'.log'

if [[ ! -f $LOGDIR/$LOG_FILE_NAME ]]
then
   echo "Create log + $(date +'%Y-%m-%d %H:%M:%S')" > $LOGDIR/$LOG_FILE_NAME
fi

cd $BASEDIR
source $BASEDIR/venv/bin/activate
echo "[$(date +'%Y-%m-%d %H:%M:%S')]************* Start  cron scheduler *************" >> $LOGDIR/$LOG_FILE_NAME
if [ "$1" == "1" ]
then
  echo "#Every  $1 [$(date +'%Y-%m-%d %H:%M:%S')]"  >> $LOGDIR/$LOG_FILE_NAME
elif [ "$1" == '5' ]
then
  echo "#Every $1 [$(date +'%Y-%m-%d %H:%M:%S')]"  >> $LOGDIR/$LOG_FILE_NAME
elif [ "$1" == '30' ]
then
  echo "#Every $1 [$(date +'%Y-%m-%d %H:%M:%S')]"  >> $LOGDIR/$LOG_FILE_NAME
  python3 $BASEDIR/cron_every_30_min.py --fname=$LOG_FILE_NAME >> $LOGDIR/$LOG_FILE_NAME 2>&1 &
elif [ "$1" == '120' ]
then
  echo "#Every $1 [$(date +'%Y-%m-%d %H:%M:%S')]"  >> $LOGDIR/$LOG_FILE_NAME
  python3 $BASEDIR/cron_every_120_min.py --fname=$LOG_FILE_NAME >> $LOGDIR/$LOG_FILE_NAME  2>&1 &
elif [ "$1" == '480' ]
then
  echo "#Every $1 [$(date +'%Y-%m-%d %H:%M:%S')]"  >> $LOGDIR/$LOG_FILE_NAME
  python3 $BASEDIR/cron_every_480_min.py  --fname=$LOG_FILE_NAME >> $LOGDIR/$LOG_FILE_NAME  2>&1 &
elif [ "$1" == '720' ]
then
  echo "#Every $1 [$(date +'%Y-%m-%d %H:%M:%S')]"  >> $LOGDIR/$LOG_FILE_NAME
  python3 $BASEDIR/cron_every_720_min.py  --fname=$LOG_FILE_NAME >> $LOGDIR/$LOG_FILE_NAME  2>&1 &
elif [ "$1" == 'MONDAY' ]
then
  echo "#Every $1 [$(date +'%Y-%m-%d %H:%M:%S')]"  >> $LOGDIR/$LOG_FILE_NAME
  python3 $BASEDIR/cron_every_monday.py --fname=$LOG_FILE_NAME >> $LOGDIR/$LOG_FILE_NAME  2>&1 &
elif [ "$1" == 'EVERYDAY' ]
then
  echo "#Every $1 [$(date +'%Y-%m-%d %H:%M:%S')]"  >> $LOGDIR/$LOG_FILE_NAME
  python3 $BASEDIR/cron_update_closes_capital_returns.py --fname=$LOG_FILE_NAME >> $LOGDIR/"$LOG_FILE_NAME"  2>&1 &
elif [ "$1" == 'FIRST_DAY_OF_MONTH' ]
then
  echo "#Every $1 [$(date +'%Y-%m-%d %H:%M:%S')]"  >> $LOGDIR/$LOG_FILE_NAME
  python3 $BASEDIR/cron_calc_portfolios_allocation.py --fname=$LOG_FILE_NAME >> $LOGDIR/$LOG_FILE_NAME   2>&1 &
fi
deactivate

OLD_LOG_FILE_NAME='cron_scheduler_'$(date --date="$date -10 day" +%Y_%m_%d)'.log'

if [[ -f $LOGDIR/$OLD_LOG_FILE_NAME ]]
then
	echo "Try delete " $OLD_LOG_FILE_NAME
	rm $LOGDIR/$OLD_LOG_FILE_NAME
fi
