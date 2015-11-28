from dashboard.DashboardItemRegistry import DashboardItemRegistry
from dashboard.DashboardItem import DashboardItem
from django.utils.safestring import mark_safe


class PlaceHolderDashboardItem(DashboardItem):
    id = "placeholder"
    name = "Placeholder Item"
    description = "An empty dashboard item."

    def render(self):
        return mark_safe('<div class="ui segment">&nbsp;</div>')

DashboardItemRegistry.add(PlaceHolderDashboardItem)
