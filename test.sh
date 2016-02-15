cp partuniverse/partuniverse/local_settings.py.tpl_dev partuniverse/partuniverse/local_settings.py
python partuniverse/manage.py makemigrations
python partuniverse/manage.py migrate
python partuniverse/manage.py test
