# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('partsmanagement', '0005_auto_20141107_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturer',
            name='created_by',
            field=models.ForeignKey(default='1', verbose_name='Added by', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='creation_time',
            field=models.DateTimeField(default='2014-11-07 22:07:09.035709', auto_now_add=True),
            preserve_default=False,
        ),
    ]
