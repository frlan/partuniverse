from django.contrib import admin
from .models import *
from partsmanagement.models import Part
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

# Logging
import logging
logger = logging.getLogger(__name__)

# Register your models here.
admin.site.register(Book)
admin.site.register(Person)
admin.site.register(Publisher)


class BookAdmin(PolymorphicChildModelAdmin):
    base_model = Part
    exclude = (
        'SKU',
        'name',
        'unit'
    )
