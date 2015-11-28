# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partsmanagement', '0009_category_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='storageplace',
            name='description',
            field=models.TextField(null=True, verbose_name='Description', blank=True),
        ),
    ]
