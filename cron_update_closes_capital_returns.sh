#!/usr/bin/env bash

BASEDIR=/home/upsilonsfather/projects/ups_one

source $BASEDIR/venv/bin/activate
#echo "[$(date +'%Y-%m-%d %H:%M:%S')]************* Start  cron_update_closes_capital_returns *************" > $BASEDIR/logs/stdout.log
python3 $BASEDIR/cron_update_closes_capital_returns.py &
deactivate
