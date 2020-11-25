#!/usr/bin/env sh

cd /projects/upsilon || exit
.venv/bin/activate
python3 telegram/upsilon_bot.py
python3 quotes/get_screens.py