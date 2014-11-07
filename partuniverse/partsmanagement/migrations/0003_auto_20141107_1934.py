# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partsmanagement', '0002_auto_20141107_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unit',
            name='name',
        ),
        migrations.AddField(
            model_name='unit',
            name='unit',
            field=models.CharField(default='---', max_length=3, choices=[('Length', ((b'm', 'meters'), (b'cm', 'centimeters'))), (b'---', 'Unknown')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='part',
            name='unit',
            field=models.CharField(default=b'---', max_length=3, choices=[('Length', ((b'm', 'meters'), (b'cm', 'centimeters'))), (b'---', 'Unknown')]),
            preserve_default=True,
        ),
    ]
