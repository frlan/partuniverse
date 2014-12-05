# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partsmanagement', '0005_auto_20141123_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='StorageItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('on_stock', models.DecimalField(null=True, verbose_name='Parts inside storage', max_digits=10, decimal_places=4, blank=True)),
                ('disabled', models.BooleanField(default=False, verbose_name='Disabled')),
                ('part', models.ForeignKey(to='partsmanagement.Part')),
                ('storage', models.ForeignKey(to='partsmanagement.StoragePlace')),
            ],
            options={
                'verbose_name': 'Storage Item',
                'verbose_name_plural': 'Storage Items',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='storageitem',
            unique_together=set([('part', 'storage')]),
        ),
        migrations.RemoveField(
            model_name='part',
            name='on_stock',
        ),
        migrations.RemoveField(
            model_name='part',
            name='storage_place',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='part',
        ),
        migrations.AddField(
            model_name='part',
            name='description',
            field=models.TextField(null=True, verbose_name='Description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='part',
            name='sku',
            field=models.CharField(max_length=60, unique=True, null=True, verbose_name='SKU', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transaction',
            name='storage_item',
            field=models.ForeignKey(blank=True, to='partsmanagement.StorageItem', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='part',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name of part'),
            preserve_default=True,
        ),
    ]
