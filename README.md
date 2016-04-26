# Partuniverse

[![Build Status](https://travis-ci.org/frlan/partuniverse.svg?branch=master)](https://travis-ci.org/frlan/partuniverse)

Another approach to keep track of parts not only inside a hacker space
but at a more general storage.

## Discussion and help

To discuss about partuniverse or get help, join our mailing list at [lstsrv.org](https://lstsrv.org/mailman/listinfo/partuniverse)

## Bugreporting

Please report bugs and feature wishes to the project page at [github](https://github.com/frlan/partuniverse/issues)

## Installation

### Dependencies

Partuniverse depends on:

- Django and therefore Python
- Virtuelenv
- A database server supported by django (PostgreSQL recommended) and
  its development libraries --
  SQLlite -- the default -- should be fine for the very beginning


For detailed list of python dependencies, have a look at
requirements.txt next to this file.

### Virtualenv

Create a virtualenv inside partuniverse subfolder inside your git checkout:

        $ pwd
        /path/to/your/sources/
        $ cd partuniverse
        $ virtuelenv .

This will create a folder inside the the partuniverse folder and
install the basic virtualenv into it -- Python, pip.


Once you have created the virtualenv, you have to install the needed packages.
This can be done by:

        $ cd partuniverse
        $ bin/pip install -r ../requirements.txt

### Running

#### Adjusting your configuration file

Inside folder `partuniverse/partuniverse` you will find some local
configuration file templates called `local_settings.py.tpl_dev` and
`local_settings.py.tpl_prod`. Copy one of these to a file called
`local_settings.py` and adjust values inside as needed. These file are
holding your local configuration which should not be part of (public)
git repository. So configure here e.g. your database connection
settings and -- this is quiet important -- your SECRET_KEY. However,
the templates are including some more configurations e.g. for debugging
purpose. So `local_settings.py.tpl_prod` is indented to be a basis
template for your production environment whereas
`local_settings.py.tpl_dev` is targeting your local developing work.
After this has been done, go ahead setting up your application.

Being inside the virtual environment, go into the folder where you have
checked out the sources. Within the folder you will find a partuniverse
folder. Change into it. Run this as following:

        $ bin/python manage.py syncdb

This will initiate the database bhind and as you for creating a user
you will need e.g. to access admin backend.

If everything worked well, you can start the server (in debug mode):

        $ bin/python manage.py runserver

### Running a production instance behind Nginx

This part assumes the following steps:

* You have already set up your partuniverse.
* You made your setup with postgresql
* It is running as user partuniverse under
  `/home/partuniverse/partuniverse`
* You are using systemd
* You have already recommpilled translations by running
  `python manage.py compilemessages`

Now do the following steps:

1.  Create the directory /run/partuniverse
2.  Set the owner of /run/partuniverse to partuniverse
3.  Collect static files by running
    `bin/python manage.py collectstatic` inside partuniversde project folder
4.  Copy `utils/service/spartuniverse.service` to `/etc/systemd/system`.
5.  Copy `utils/service/partuniverse.socket` to `/etc/systemd/system`.
6.  Copy `utils/service/nginx-host.conf` to an appropriate place and edit it to
    your liking, you should get the idea once you look at it.
7.  Reload the systemd config: `systemctl daemon-reload`
8.  Start the partuniverse service: `systemctl start partuniverse`
9.  Activate the nginx vhost and reload.
10. Your partuniverse is now running behind a high speed web server,
    you are welcome :-).


## i18n/l10n

You will find the tranlstions files inside
locales/LC_MESSAGES/django.po encoded with gettext's po file format.
To update translation file you can run

        $ bin/python manage.py makemessages --all

After this has been done, translations needs to be recompiled with

        $ bin/python manage.py compilemessages

For translation the files you can use for example poedit or just any
text editor -- like Geany which is also having some translations
plugin.


## Hacking & Contribution

If like to contribute, please send a pull reuqest via
[github](https://github.com/frlan/partuniverse/). When hacking, start
with adding a test first. So if you want to fix a bug, create a test
for that bug first. It's faster to check whether the bug is fixed and
prevents the bug from happen again.

### Code style

Please use [pep8](https://www.python.org/dev/peps/pep-0008/) for coding.
As a little support tool you might can give [autopep8](https://pypi.python.org/pypi/autopep8) a try.


### Testing

To test your changes, you can use Django's test framework

To run all available tests:

        $ bin/python manage.py test

Please add new tests for each feature you are adding to suitable
test-files.

## License

The software is distributed under terms of AGPLv3+. Please check
COPYING for details.
