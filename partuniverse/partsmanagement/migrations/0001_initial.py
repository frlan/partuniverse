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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('parent', models.ForeignKey(null=True, blank=True, to='partsmanagement.Category')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Distributor',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Manufacturer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name of part', max_length=50)),
                ('min_stock', models.DecimalField(decimal_places=4, null=True, max_digits=10, verbose_name='Minimal stock', blank=True)),
                ('on_stock', models.DecimalField(decimal_places=4, null=True, max_digits=10, verbose_name='Parts on stock', blank=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('categories', models.ManyToManyField(to='partsmanagement.Category', verbose_name='Category')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Added by')),
                ('distributor', models.ForeignKey(to='partsmanagement.Distributor', verbose_name='Distributor')),
                ('manufacturer', models.ForeignKey(to='partsmanagement.Manufacturer', verbose_name='Manufacturer')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=4)),
                ('date', models.DateField(auto_now_add=True, db_index=True)),
                ('comment', models.TextField(null=True, max_length=200, blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('part', models.ForeignKey(to='partsmanagement.Part')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Unit',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='storageplace',
            name='storage_type',
            field=models.ForeignKey(to='partsmanagement.StorageType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='part',
            name='unit',
            field=models.ForeignKey(to='partsmanagement.Unit', verbose_name='Unit'),
            preserve_default=True,
        ),
    ]
