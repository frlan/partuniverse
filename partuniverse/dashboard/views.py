# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext, loader
from dashboard.DashboardContainer import DashboardContainer


def index(request):
    template = loader.get_template('dashboard/container.html')
    dashboard = DashboardContainer(request)
    context = RequestContext(request, {
        'dashboard': dashboard,
    })
    return HttpResponse(template.render(context))
