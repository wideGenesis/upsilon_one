#!/usr/bin/env sh

git add .
git commit -m "commit from instance [$(date +'%Y-%m-%d %H:%M:%S')]"
ssh -i '~/.ssh/forgit' git push origin main
exit

