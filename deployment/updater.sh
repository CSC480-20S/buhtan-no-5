#!/bin/bash
git checkout master
git fetch
git pull --rebase origin master
cp main.py testy.py
#to-do
#updating the documentation to reflect the changes from master
