# -*- coding: utf-8 -*-
import importlib

from django.apps import apps
from django.conf import settings
from django.template.base import TemplateDoesNotExist
from django.template.loader import BaseLoader
from django.utils._os import safe_join
from django.utils import six

from dashboard.DashboardItem import DashboardItem


class DashboardItemRegistryClass:
    items = []

    def add(self, item):
        self.items.append(item)
        return self

    def get(self, id):
        for item in self.items:
            if item.id == id:
                return item
        return None

DashboardItemRegistry = DashboardItemRegistryClass()

# scan the installed apps for dashboard items
for app_config in apps.get_app_configs():
    if not app_config.path:
        continue
    dashboard_import_path = app_config.name + '.dashboards'
    try:
        importlib.import_module(dashboard_import_path)
    except:
        pass
