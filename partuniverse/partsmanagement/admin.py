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

admin.site.register(Category)
admin.site.register(Distributor)
admin.site.register(Manufacturer)
admin.site.register(Part)
admin.site.register(StorageItem)
admin.site.register(StoragePlace)
admin.site.register(StorageType)
admin.site.register(Transaction)
admin.site.register(VerifiedStock)
