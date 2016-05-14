# -*- coding: utf-8 -*-

from django.contrib import admin
from django.forms import ModelForm
from .models import *
from partsmanagement.models import Part
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

# Logging
import logging
logger = logging.getLogger(__name__)

admin.site.register(Book)
admin.site.register(Person)
admin.site.register(Publisher)


class BookAdmin(PolymorphicChildModelAdmin):
    base_model = PolymorphicChildModelAdmin
    fieldsets = (
        (None, {
            'fields': ('SKU', )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('registration_required', 'template_name'),
        }),
    )


class BookAdminForm(ModelForm):
    class Meta:
        exclude = (
            'SKU',
            'name',
            'unit'
        )
