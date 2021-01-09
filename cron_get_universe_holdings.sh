#!/usr/bin/env bash

BASEDIR=/home/upsilonsfather/projects/ups_one

source $BASEDIR/venv/bin/activate
#echo "[$(date +'%Y-%m-%d %H:%M:%S')]************* Start  cron_get_universe_holdings *************" > $BASEDIR/logs/stdout.log
python3 $BASEDIR/cron_get_universe_holdings.py &
deactivate
