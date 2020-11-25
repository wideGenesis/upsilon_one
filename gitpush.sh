#!/usr/bin/env sh

#git config credential.helper store

git add .
git commit -m "autoupdate $(date +%F-%T)"
git push origin main
exit

