from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from dashboard.DashboardItemRegistry import DashboardItemRegistry
from dashboard.DashboardContainer import DashboardContainer
from dashboard.DashboardItemRegistry import DashboardItemRegistry


def dashboard(request):
    template = loader.get_template('index.html')
    dashboard = DashboardContainer(request)
    dashboard.add(DashboardItemRegistry.get('needs_restocking'))
    context = RequestContext(request, {
        'dashboard': dashboard,
    })
    return HttpResponse(template.render(context))
