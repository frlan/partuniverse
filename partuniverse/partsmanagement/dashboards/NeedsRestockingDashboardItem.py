from dashboard.DashboardItemRegistry import DashboardItemRegistry
from dashboard.DashboardItem import DashboardItem
from django.template import RequestContext, loader
from django.utils.safestring import mark_safe
from django.db.models import F

from partsmanagement.models import Part

class NeedsRestockingDashboardItem(DashboardItem):
    id = "needs_restocking"
    name = "Parts with low stock"
    description = "Display a table with parts which have low stock."

    def render(self):
        parts = Part.objects.exclude(on_stock__gt='0', on_stock__gte=F('min_stock'))
        template = loader.get_template('dashboard/needs_restocking.html')
        context = RequestContext(self.container.request, {
            'parts': parts,
        })
        return mark_safe(template.render(context))

DashboardItemRegistry.add(NeedsRestockingDashboardItem)

