#!/usr/bin/env bash

BASEDIR=/home/upsilonsfather/projects/ups_one
LOGDIR=$BASEDIR/logs

source $BASEDIR/venv/bin/activate
echo "[$(date +'%Y-%m-%d %H:%M:%S')]************* Start bot *************" > $LOGDIR/spam_sender.log
cd $BASEDIR
# shellcheck disable=SC2069
python3 $BASEDIR/spammer.py >> $LOGDIR/spam_sender.log  2>&1 &
deactivate
