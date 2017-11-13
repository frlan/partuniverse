# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-13 08:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('partsmanagement', '0031_storageitem_review_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='storageplace',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='The user who is responsible for the storage.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owned by'),
        ),
    ]
