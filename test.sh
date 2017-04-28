virtualenv .
./bin/pip install zc.buildout
./bin/buildout
cp partuniverse/partuniverse/local_settings.py.tpl_dev partuniverse/partuniverse/local_settings.py
./bin/django makemigrations
./bin/django migrate
./bin/test
