# -*- coding: utf-8 -*-
from dashboard.DashboardItem import DashboardItem
from dashboard.DashboardItemRegistry import DashboardItemRegistry
from django.db.models import F
from django.template import RequestContext, loader
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from partsmanagement.models import Part


class NeedsRestockingDashboardItem(DashboardItem):
    id = "needs_restocking"
    name = _("Parts with low stock")
    description = _("Displays a table with parts which have low stock.")

    def render(self):
        # parts = Part.objects.exclude(on_stock__gt='0', on_stock__gte=F('min_stock'))
        parts = []
        for i in Part.objects.all():
            if (i.is_below_min_stock() is True):
                parts.append(i)
        template = loader.get_template('dashboard/needs_restocking.html')
        context = RequestContext(self.container.request, {
            'parts': parts,
        })
        return mark_safe(template.render(context))

DashboardItemRegistry.add(NeedsRestockingDashboardItem)
