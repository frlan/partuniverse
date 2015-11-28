# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partsmanagement', '0003_auto_20141121_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='disabled',
            field=models.BooleanField(default=False, verbose_name='Disabled'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='storageplace',
            name='disabled',
            field=models.BooleanField(default=False, verbose_name='Disabled'),
            preserve_default=True,
        ),
    ]
