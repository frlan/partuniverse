# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partsmanagement', '0012_transaction_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='pic',
            field=models.ImageField(null=True, upload_to=b'uploads/', blank=True),
        ),
        migrations.AddField(
            model_name='part',
            name='url',
            field=models.CharField(max_length=255, unique=True, null=True, blank=True),
        ),
    ]
