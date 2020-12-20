#!/usr/bin/env bash

BASEDIR=/home/upsilonsfather/projects/ups_one

source $BASEDIR/venv/bin/activate
#echo "[$(date +'%Y-%m-%d %H:%M:%S')]************* Start invest services *************"
python3 $BASEDIR/invest_services.py &
deactivate

