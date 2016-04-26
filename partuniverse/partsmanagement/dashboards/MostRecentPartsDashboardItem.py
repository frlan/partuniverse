# -*- coding: utf-8 -*-
from dashboard.DashboardItemRegistry import DashboardItemRegistry
from dashboard.DashboardItem import DashboardItem
from django.template import RequestContext, loader
from django.utils.safestring import mark_safe
from django.db.models import F
from partsmanagement.models import Part


class MostRecentPartsDashboardItem(DashboardItem):
    id = "most_recent_parts"
    name = "Most recent Parts"
    description = "Display a table with the most recent created/updated parts."

    def render(self):
        parts = Part.objects.order_by('-date')[:5].all()
        template = loader.get_template('dashboard/most_recent_parts.html')
        context = RequestContext(self.container.request, {
            'parts': parts,
        })
        return mark_safe(template.render(context))

DashboardItemRegistry.add(MostRecentPartsDashboardItem)
