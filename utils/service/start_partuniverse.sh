#!/bin/bash

/home/partuniverse/partuniverse/partuniverse/bin/python manage.py runfcgi method=prefork socket=/home/partuniverse/partuniverse/var/partuniverse.sock pidfile=/home/partuniverse/partuniverse/var/django.pid

