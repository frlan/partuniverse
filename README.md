Partuniverse
============

Another approach to keep track of parts not only inside a hacker space
but at a more general storage.

Installation
------------

Dependencies
------------

Partuniverse depends on:

- Django and therefor Python
- A database server supported by django (PostgreSQL recommended) and
  its development libraries --
  SQLlite -- the default -- should be fine for the very beginning


For detailed list of python dependencies, have a look at
requirements.txt next to this file.


Virtualenv
----------


Install virtualenvwrapper. This can be done either via your packet
manage or by running

	$ pip install virtualenvwrapper

(This HowTo now only describes steps done on a Debian system. When
running Windows or for further detail, check documentation -- a good
idea anyway.)

Now you have to setup your environment.

	$ export WORKON_HOME=~/Envs
	$ mkdir -p $WORKON_HOME
	$ source /usr/local/bin/virtualenvwrapper.sh
	$ mkvirtualenv partuniverse

This will create a folder Envs inside your home and install the
virtualenv into it. You might want to add the export and the source
command to your local shell configuration to ensure, it's loaded on
startup.

With running the mkvirtualenv command you will be already inside the
environment. You can install as many environments you wish to and
switch between them by running workon <virutal_env_name>, for example
workon blankspot.

Once inside the virtualenv, you have to install the needed packages.
This can be done by:

	$ pip install -r requirements.txt

Running
-------

Being inside the virtual environment, go into the folder where you have
checked out the sources. Within the folder you will find a partuniverse
folder. Change into it. Run this as following:

	$ ./manage.py syncdb

This will initiate the database bhind and as you for creating a user
you will need e.g. to access admin backend.

If everything worked well, you can start the server (in debug mode):

	$ ./manage.py runserver
