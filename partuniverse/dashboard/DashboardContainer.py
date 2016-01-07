# -*- coding: utf-8 -*-
from django.template import RequestContext, loader
from dashboard.DashboardItem import DashboardItem
from django.utils.safestring import mark_safe


class DashboardContainer:
    columns = 3
    rows = 3
    items = []
    request = None

    def __init__(self, request):
        self.request = request
        self.items = []
        for i in range(self.rows):
            self.items.insert(i, [])
            for j in range(self.columns):
                self.items[i].insert(j, None)

    def add(self, item):
        counter_inner = 0
        counter_outer = 0
        for i in self.items:
            counter_inner = 0
            for j in self.items[counter_outer]:
                if (self.items[counter_outer][counter_inner] is None):
                    self.items[counter_outer][counter_inner] = item(self)
                    return self
                counter_inner = counter_inner + 1
            counter_outer = counter_outer + 1

    def render(self):
        template_row = loader.get_template('row.html')
        template_column = loader.get_template('column.html')
        template_container = loader.get_template('container.html')
        rows = ""
        for row in self.items:
            columns = []
            for item in row:
                context = RequestContext(self.request, {
                    'item': item,
                    'dashboard': self,
                })
                columns.append(template_column.render(context))
            context = RequestContext(self.request, {
                'columns': columns,
                'dashboard': self,
            })
            row_html = template_row.render(context)
            rows = rows + row_html
        context = RequestContext(self.request, {
                'rows': mark_safe(rows),
                'dashboard': self,
            })
        output = template_container.render(context)
        return mark_safe(output)
