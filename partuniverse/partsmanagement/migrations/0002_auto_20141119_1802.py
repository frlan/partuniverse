# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partsmanagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='storage_place',
            field=models.ForeignKey(verbose_name='Storage', blank=True, to='partsmanagement.StoragePlace', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='part',
            name='creation_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='part',
            name='unit',
            field=models.CharField(default=b'---', max_length=3, verbose_name='Messuring unit', choices=[('Length', ((b'm', 'meters'), (b'cm', 'centimeters'))), ('Volume', ((b'l', 'litres'), (b'm\xc2\xb3', 'cubicmeters'), (b'ccm', 'cubic centimeters'))), (b'---', 'Unknown')]),
            preserve_default=True,
        ),
    ]
