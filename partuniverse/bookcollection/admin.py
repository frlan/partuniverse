from django.contrib import admin
from .models import *

# Logging
import logging
logger = logging.getLogger(__name__)

# Register your models here.
admin.site.register(Book)
admin.site.register(Person)
admin.site.register(Publisher)
