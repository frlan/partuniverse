# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('partsmanagement', '0002_auto_20141119_1802'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='distributor',
            options={'verbose_name': 'Distributor', 'verbose_name_plural': 'Distributors'},
        ),
        migrations.AlterModelOptions(
            name='manufacturer',
            options={'verbose_name': 'Manufacturer', 'verbose_name_plural': 'Manufacturers'},
        ),
        migrations.AlterModelOptions(
            name='storageplace',
            options={'verbose_name': 'Storage Place', 'verbose_name_plural': 'Storage Places'},
        ),
        migrations.AlterModelOptions(
            name='storagetype',
            options={'verbose_name': 'Storage Type', 'verbose_name_plural': 'Storage Types'},
        ),
        migrations.AddField(
            model_name='storageplace',
            name='parent',
            field=models.ForeignKey(verbose_name='Parent storage', blank=True, to='partsmanagement.StoragePlace', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='distributor',
            name='creation_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(verbose_name='Amount', max_digits=10, decimal_places=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='comment',
            field=models.TextField(max_length=200, null=True, verbose_name='Comment', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='created_by',
            field=models.ForeignKey(verbose_name='Created by', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Transaction Date', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='subject',
            field=models.CharField(max_length=100, verbose_name='Subject'),
            preserve_default=True,
        ),
    ]
