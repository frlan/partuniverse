# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partsmanagement', '0007_auto_20141205_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='unit',
            field=models.CharField(default=b'---', max_length=3, verbose_name='Messuring unit', choices=[('Length', ((b'm', 'meters'), (b'cm', 'centimeters'))), ('Volume', ((b'l', 'litres'), (b'm\xc2\xb3', 'cubicmeters'), (b'ccm', 'cubic centimeters'))), ('Piece', ((b'pc', 'piece'),)), ('n/A', 'Unknown')]),
        ),
    ]
