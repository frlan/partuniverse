# Partuniverse

[![Build Status](https://travis-ci.org/frlan/partuniverse.svg?branch=master)](https://travis-ci.org/frlan/partuniverse)

Another approach to keep track of parts not only inside a hacker space
but at a more general storage.

## Discussion and help

To discuss about partuniverse or get help, join our mailing list at
[lstsrv.org](https://lstsrv.org/mailman/listinfo/partuniverse). There
is also a XMPP-MUC available to chat. Join
[partuniverse@chat.kraut.space](xmpp:partuniverse@chat.kraut.space).

## Bugreporting

Please report bugs and feature wishes to the project page at [github](https://github.com/frlan/partuniverse/issues)

## Installation

### Dependencies

Partuniverse depends on:

- Django and therefore Python
- A database server supported by django (PostgreSQL recommended) and
  its development libraries --
  SQLlite -- the default -- should be fine for the very beginning
- [Install](https://pillow.readthedocs.io/en/3.0.0/installation.html#linux-installation) development headers for the pillow.


### Buildout

The [zc.buildout](http://www.buildout.org/en/latest/) and all the dependcies will be installed via its bootstrap script:

        $ pwd
        /path/to/your/sources/
        $ python bootstrap-buildout.py
        $ ./bin/buildout

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

Go into the folder where you have checked out the sources.

First you will have to create the Database:

        $ ./bin/django migrate

Create you superuser:

        $ .bin/django createsuperuser

If everything worked well, you can start the server (in debug mode):

        $ ./bin/django runserver

### Running a production instance behind Nginx

This part assumes the following steps:

* You have already set up your partuniverse.
* You made your setup with postgresql
* It is running as user partuniverse under
  `/home/partuniverse/partuniverse`
* You are using systemd
* You have already recommpilled translations by running
  `./bin/django compilemessages`

Now do the following steps:

1.  Create the directory /run/partuniverse
2.  Set the owner of /run/partuniverse to partuniverse
3.  Collect static files by running
    `./bin/django collectstatic` inside partuniversde project folder
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

        $ ./bin/django makemessages --all

After this has been done, translations needs to be recompiled with

        $ ./bin/django compilemessages

For translation the files you can use for example poedit or just any
text editor -- like Geany which is also having some translations
plugin.

## Concepts

You can drill down the basic idea into one sentence: Everything is a
storage place and everything is a part. But let's have a deeper look.

### The part

A part describes a more or less abstract item. It consists at minimum
of a name and a SKU (Stock Keeping Unit) -- something like an internal
part number. It's not a specific item but a group of items. In general
a part is storing general information, but not quantity or where to
find it inside the storage.

Differing parts by e.g. different serial numbers is currently not yet
implemented.


### The storage item

Having a part, the storage item is the combination of a particular
storage place and a quantity of items stored at that point.

### A storage place

A storage place can be everything where you can put things in. This could be a

* room
* shelve
* box
* gas tank
* country
* a person
* ....

A storage place is having a type as well as can be chained. So you
might create a storage »room«, putting a storage place »shelve« into
it. This shelve may contain several boxes ....

Also a storage place can be relocated including all storage places and
storage items connected.


## Hacking & Contribution

If like to contribute, please send a pull reuqest via
[github](https://github.com/frlan/partuniverse/). When hacking, start
with adding a test first. So if you want to fix a bug, create a test
for that bug first. It's faster to check whether the bug is fixed and
prevents the bug from happen again.

### Branching

Before start coding, make your own fork of partuniverse. This can be
done either at github or any other public git repo. Once you have done
this, please develope one feature within one branch. Try to avoid hacking
on your master branch. Having feature-branches allows easier merges/discussion/*.
When finishing your featre, please send a pull request or a patchset via mail.

### Code style

Please use [pep8](https://www.python.org/dev/peps/pep-0008/) for coding.
As a little support tool you might can give [autopep8](https://pypi.python.org/pypi/autopep8) a try.


### Testing

To test your changes, you can use Django's test framework

To run all available tests:

        $ ./bin/django test

Please add new tests for each feature you are adding to suitable
test-files.

## License

The software is distributed under terms of AGPLv3+. Please check
COPYING for details.
