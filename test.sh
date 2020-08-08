virtualenv --python=python3 .
./bin/pip install -r requirements.txt
cp partuniverse/partuniverse/local_settings.py.tpl_dev partuniverse/partuniverse/local_settings.py
cd partuniverse
../bin/python manage.py makemigrations
../bin/python manage.py migrate
../bin/python manage.py test
