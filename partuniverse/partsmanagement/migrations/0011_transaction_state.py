# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partsmanagement', '0010_storageplace_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='state',
            field=models.CharField(default=b'---', max_length=6, verbose_name='State', blank=True, choices=[(b'paid', 'Paid'), (b'open', 'Open'), (b'res', 'Reserverd')]),
        ),
    ]
