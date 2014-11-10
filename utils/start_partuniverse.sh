#!/bin/bash

# Depending on your distro you need to place this in another place
VIRTUALENVWRAPPER="/usr/bin/virtualenvwrapper.sh"

export WORKON_HOME=~/Envs
source $VIRTUALENVWRAPPER
workon partuniverse
/home/partuniverse/partuniverse/partuniverse/manage.py runfcgi method=prefork socket=/home/partuniverse/partuniverse/var/partuniverse.sock pidfile=/home/partuniverse/partuniverse/var/django.pid

