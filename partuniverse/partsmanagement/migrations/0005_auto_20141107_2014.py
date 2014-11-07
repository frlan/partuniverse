# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partsmanagement', '0004_delete_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='unit',
            field=models.CharField(default=b'---', max_length=3, choices=[('Length', ((b'm', 'meters'), (b'cm', 'centimeters'))), ('Volume', ((b'l', 'litres'), (b'm\xc2\xb3', 'cubicmeters'), (b'ccm', 'cubic centimeters'))), (b'---', 'Unknown')]),
            preserve_default=True,
        ),
    ]
