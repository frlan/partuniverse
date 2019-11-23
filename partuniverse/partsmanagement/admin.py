# -*- coding: utf-8 -*-

import logging
from django.contrib import admin
from .models import (
    Category,
    Distributor,
    Manufacturer,
    Part,
    StorageItem,
    StoragePlace,
    StorageType,
    Transaction,
    VerifiedStock,
)

logger = logging.getLogger(__name__)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name", "description",)


@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    search_fields = ("name", "sku",)


@admin.register(StorageType)
class StorageTypeAdmin(admin.ModelAdmin):
    search_fields = ("name", )


admin.site.register(StorageItem)
admin.site.register(StoragePlace)

admin.site.register(Transaction)
admin.site.register(VerifiedStock)
