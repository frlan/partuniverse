# -*- coding: utf-8 -*-

import logging
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import (StorageItem, StorageType, StoragePlace)

logger = logging.getLogger(__name__)


class MergeStorageItemsForm(forms.Form):
    storageitem1 = forms.ModelChoiceField(
        queryset=StorageItem.objects.all())


class StockTakingForm(forms.Form):
    amount = forms.DecimalField(
        label=_("Parts now inside storage"),
        max_digits=10,
        decimal_places=4,
        help_text=_("The amount of currently inside storage place."))


class BulkStorageForm(forms.Form):
    storagetype = forms.ModelChoiceField(queryset=StorageType.objects.all())
    parentstorage = forms.ModelChoiceField(queryset=StoragePlace.objects.all())
        
    cols = forms.IntegerField(
        label=_("cols"),
        help_text=_("cols"))
    rows = forms.IntegerField(
        label=_("rows"),
        help_text=_("rows"))
