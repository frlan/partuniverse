# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partsmanagement', '0003_auto_20141107_1934'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Unit',
        ),
    ]
