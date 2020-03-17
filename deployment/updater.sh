#!/bin/bash

#this scripts get the most recent from man and relaunches the server
git checkout master
git fetch
git pull --rebase origin master
kill $(pgrep -u $USER python)

cd ../ && nohup python3 launcher.py --bind 129.3.20.26:12100 launcher:app & >/dev/null &
cd deployment && nohup python3 poll_github.py &>/dev/null &
#to-do
#updating the documentation to reflect the changes from master
