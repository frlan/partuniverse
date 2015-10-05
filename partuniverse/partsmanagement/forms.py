# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Models we need
from .models import Part, StorageItem

#i18n (just in case)
from django.utils.translation import ugettext_lazy as _

# Logging
import logging
logger = logging.getLogger(__name__)

class MergeStorageItemsForm(forms.Form):
    storageitem1 = forms.ModelChoiceField(queryset=StorageItem.objects.all())


