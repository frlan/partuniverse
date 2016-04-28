# -*- coding: utf-8 -*-

from bookcollection.admin import BookAdmin
from bookcollection.models import Book
from django.contrib import admin
from .models import *
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

# Logging
import logging
logger = logging.getLogger(__name__)


class PartAdmin(PolymorphicParentModelAdmin):
    base_model = Part
    child_models = (
        (Book, BookAdmin)
    )


admin.site.register(StorageType)
admin.site.register(Category)
admin.site.register(StoragePlace)
admin.site.register(Manufacturer)
admin.site.register(Distributor)
admin.site.register(Part)
admin.site.register(StorageItem)
admin.site.register(Transaction)
