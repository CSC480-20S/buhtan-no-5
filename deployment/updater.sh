#!/bin/bash

#this scripts get the most recent from man and relaunches the server
git checkout master
git fetch
git pull --rebase origin master
kill $(pgrep -u $USER python)

cd ../ && nohup python3 launcher.py --bind 129.3.20.26:12100 launcher:app & >/dev/null 2>1&
cd ~/csc480/deployment && nohup python3 poll_github.py &>/dev/null 2>1&
kill $(pgrep -u $USER updater.sh)
#this solution will not update at the same time, will be n seconds from time of execution.
