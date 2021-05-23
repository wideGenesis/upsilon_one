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
# Start every 120 min  (в четвертую минуту, каждого 2го часа)
# 4 */2 * * * /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "120"
#
# Start every 480 min  (в шестую минуту, каждого 8го часа)
# 6 */8 * * * /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "480"
#
# Start every 720 min  (в восьмую минуту, каждого 12го часа)
# 8 */12 * * * /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "720"
#
# Start everyday  (каждый день в 2:10)
# на инстансе +5часов по отношению к New York Time ориентируемся при запуске на NYT
# что бы запустить что-то в 2:10 по NYT надо запускать в 7:10 по времени инстанса
# 10 7 * * * /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "EVERYDAY"
#
# Start on_market_open  (каждый день в 9:31)
# на инстансе +5часов по отношению к New York Time ориентируемся при запуске на NYT
# что бы запустить что-то в 9:31 по NYT надо запускать в 14:31 по времени инстанса
# 31 14 * * * /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "ON_MARKET_OPEN"
#
# Start after market close  (каждый день в 17:20)
# на инстансе +5часов по отношению к New York Time ориентируемся при запуске на NYT
# что бы запустить что-то в 17:20 по NYT надо запускать в 22:20 по времени инстанса
# 20 22 * * * /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "AFTER_MARKET_CLOSE"
#
# Start monday  (каждый понедельник в 3:13)
# на инстансе +5часов по отношению к New York Time ориентируемся при запуске на NYT
# что бы запустить что-то в 3:00 по NYT надо запускать в 8:00 по времени инстанса
# 13 8 * * MON /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "MONDAY"
#
# Start saturday  (каждую субботу в 9:22 по МСК)
# на инстансе +5часов по отношению к New York Time ориентируемся при запуске на NYT
# что бы запустить что-то в 3:00 по NYT надо запускать в 8:00 по времени инстанса
# Туту запускаем каждую субботу ориентируясь на 9 часов 22 мин по МСК
# 22 5 * * SAT /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "SATURDAY"
#
# Start wednesday  (каждую среду в 3:10)
# на инстансе +5часов по отношению к New York Time ориентируемся при запуске на NYT
# что бы запустить что-то в 3:00 по NYT надо запускать в 8:00 по времени инстанса
# 15 18 * * WED /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "WEDNESDAY"
#
# Start first date of month  (каждое первое число месяца в 4:00)
# на инстансе +5часов по отношению к New York Time ориентируемся при запуске на NYT
# что бы запустить что-то в 3:00 по NYT надо запускать в 8:00 по времени инстанса
# 20 4 1 * * /home/upsilonsfather/projects/ups_one/cron_scheduler.sh "FIRST_DAY_OF_MONTH"
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
elif [ "$1" == 'WEDNESDAY' ]
then
  echo "#Every $1 [$(date +'%Y-%m-%d %H:%M:%S')]"  >> $LOGDIR/$LOG_FILE_NAME
  python3 $BASEDIR/cron_every_wednesday.py --fname=$LOG_FILE_NAME >> $LOGDIR/$LOG_FILE_NAME  2>&1 &
elif [ "$1" == 'SATURDAY' ]
then
  echo "#Every $1 [$(date +'%Y-%m-%d %H:%M:%S')]"  >> $LOGDIR/$LOG_FILE_NAME
  python3 $BASEDIR/cron_every_saturday.py --fname=$LOG_FILE_NAME >> $LOGDIR/$LOG_FILE_NAME  2>&1 &
elif [ "$1" == 'EVERYDAY' ]
then
  echo "#Every $1 [$(date +'%Y-%m-%d %H:%M:%S')]"  >> $LOGDIR/$LOG_FILE_NAME
  python3 $BASEDIR/cron_update_closes_capital_returns.py --fname=$LOG_FILE_NAME >> $LOGDIR/"$LOG_FILE_NAME"  2>&1 &
elif [ "$1" == 'FIRST_DAY_OF_MONTH' ]
then
  echo "#Every $1 [$(date +'%Y-%m-%d %H:%M:%S')]"  >> $LOGDIR/$LOG_FILE_NAME
  python3 $BASEDIR/cron_calc_portfolios_allocation.py --fname=$LOG_FILE_NAME >> $LOGDIR/$LOG_FILE_NAME   2>&1 &
elif [ "$1" == 'ON_MARKET_OPEN' ]
then
  echo "#Every $1 [$(date +'%Y-%m-%d %H:%M:%S')]"  >> $LOGDIR/$LOG_FILE_NAME
  python3 $BASEDIR/cron_on_market_open.py --fname=$LOG_FILE_NAME >> $LOGDIR/$LOG_FILE_NAME   2>&1 &
elif [ "$1" == 'AFTER_MARKET_CLOSE' ]
then
  echo "#Every $1 [$(date +'%Y-%m-%d %H:%M:%S')]"  >> $LOGDIR/$LOG_FILE_NAME
  python3 $BASEDIR/cron_after_market_close.py --fname=$LOG_FILE_NAME >> $LOGDIR/$LOG_FILE_NAME   2>&1 &
fi
deactivate

OLD_LOG_FILE_NAME='cron_scheduler_'$(date --date="$date -10 day" +%Y_%m_%d)'.log'
echo "Old filename: $OLD_LOG_FILE_NAME"
if [[ -f $LOGDIR/$OLD_LOG_FILE_NAME ]]
then
	echo "Try delete " $OLD_LOG_FILE_NAME
	rm $LOGDIR/$OLD_LOG_FILE_NAME
fi
