#!/usr/bin/env bash

BASEDIR=/home/upsilonsfather/projects/ups_one
LOGDIR=$BASEDIR/logs

source $BASEDIR/venv/bin/activate
echo "[$(date +'%Y-%m-%d %H:%M:%S')]************* Start bot *************" > $LOGDIR/gatekeeper.log
cd $BASEDIR
# shellcheck disable=SC2069
python3 $BASEDIR/gkeeper.py >> $LOGDIR/gatekeeper.log  2>&1 &
deactivate
