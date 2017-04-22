# -*- coding: utf-8 -*-

import logging
from django.contrib import admin
from .models import (
    StorageItem,
    StorageType,
    Category,
    Part,
    Manufacturer,
    Distributor,
    Transaction,
    StoragePlace
)

logger = logging.getLogger(__name__)

admin.site.register(StorageType)
admin.site.register(Category)
admin.site.register(StoragePlace)
admin.site.register(Manufacturer)
admin.site.register(Distributor)
admin.site.register(Part)
admin.site.register(StorageItem)
admin.site.register(Transaction)
