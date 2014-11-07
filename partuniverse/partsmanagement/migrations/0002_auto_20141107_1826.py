# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partsmanagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='distributor',
            field=models.ForeignKey(verbose_name='Distributor', blank=True, to='partsmanagement.Distributor', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='part',
            name='manufacturer',
            field=models.ForeignKey(verbose_name='Manufacturer', blank=True, to='partsmanagement.Manufacturer', null=True),
            preserve_default=True,
        ),
    ]
