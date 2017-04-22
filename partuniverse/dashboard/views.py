# -*- coding: utf-8 -*-
from dashboard.DashboardContainer import DashboardContainer
from django.http import HttpResponse
from django.template import RequestContext, loader


def index(request):
    template = loader.get_template('dashboard/container.html')
    dashboard = DashboardContainer(request)
    context = RequestContext(request, {
        'dashboard': dashboard,
    })
    return HttpResponse(template.render(context))
