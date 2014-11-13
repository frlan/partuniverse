# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('parent', models.ForeignKey(blank=True, to='partsmanagement.Category', null=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Distributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(verbose_name='Added by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Distributor',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(verbose_name='Added by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Manufacturer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name of part')),
                ('min_stock', models.DecimalField(null=True, verbose_name='Minimal stock', max_digits=10, decimal_places=4, blank=True)),
                ('on_stock', models.DecimalField(null=True, verbose_name='Parts on stock', max_digits=10, decimal_places=4, blank=True)),
                ('unit', models.CharField(default=b'---', max_length=3, choices=[('Length', ((b'm', 'meters'), (b'cm', 'centimeters'))), ('Volume', ((b'l', 'litres'), (b'm\xc2\xb3', 'cubicmeters'), (b'ccm', 'cubic centimeters'))), (b'---', 'Unknown')])),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('categories', models.ManyToManyField(to='partsmanagement.Category', verbose_name='Category')),
                ('created_by', models.ForeignKey(verbose_name='Added by', to=settings.AUTH_USER_MODEL)),
                ('distributor', models.ForeignKey(verbose_name='Distributor', blank=True, to='partsmanagement.Distributor', null=True)),
                ('manufacturer', models.ForeignKey(verbose_name='Manufacturer', blank=True, to='partsmanagement.Manufacturer', null=True)),
            ],
            options={
                'verbose_name': 'Part',
                'verbose_name_plural': 'Parts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StoragePlace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Storage Place',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StorageType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Storage Type',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=100)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=4)),
                ('date', models.DateField(auto_now_add=True, db_index=True)),
                ('comment', models.TextField(max_length=200, null=True, blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('part', models.ForeignKey(to='partsmanagement.Part')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='storageplace',
            name='storage_type',
            field=models.ForeignKey(to='partsmanagement.StorageType'),
            preserve_default=True,
        ),
    ]
