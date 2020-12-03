#!/usr/bin/env sh

git add .
git commit -m "commit from instance [$(date +'%Y-%m-%d %H:%M:%S')]"
git push --progress github.com:wideGenesis/ups_one
exit

