# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('partsmanagement', '0011_transaction_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='created_date',
            field=models.TimeField(default=datetime.datetime(2015, 11, 28, 12, 41, 3, 896981, tzinfo=utc), auto_now_add=True, verbose_name='Creation timestamp', db_index=True),
            preserve_default=False,
        ),
    ]
