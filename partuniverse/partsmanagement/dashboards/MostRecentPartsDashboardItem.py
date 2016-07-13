# -*- coding: utf-8 -*-
from dashboard.DashboardItem import DashboardItem
from dashboard.DashboardItemRegistry import DashboardItemRegistry
from django.db.models import F
from django.template import RequestContext, loader
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from partsmanagement.models import Part


class MostRecentPartsDashboardItem(DashboardItem):
    id = "most_recent_parts"
    name = _("Most recent Parts")
    description = _("Displays a table with the most recent created/updated parts.")

    def render(self):
        parts = Part.objects.order_by('-creation_time')[:5].all()
        template = loader.get_template('dashboard/most_recent_parts.html')
        context = RequestContext(self.container.request, {
            'parts': parts,
        })
        return mark_safe(template.render(context))

DashboardItemRegistry.add(MostRecentPartsDashboardItem)
