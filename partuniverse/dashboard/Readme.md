# Dashboards

Yeah! Everyone needs some dashboards.

## Introduction

I wanted something simple and as the existing dashboard solutions
where too complex or overengeneered, I decided to write something for
my own.

## Requirements

Almost none. If you want a decent layout out of the box, I recommend
you [Semantic UI](http://semantic-ui.com/).

## Install

Put the dashboard app into `INSTALLED_APPS`.

Create a view for your dashboard. Create an Instance of the
`DashbardContainer` and put an `DashboardItem` from the
`DashboardItemRegistry` into the container.

A view would look like this:

```python
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from dashboard.DashboardItemRegistry import DashboardItemRegistry
from dashboard.DashboardContainer import DashboardContainer

def dashboard(request):
    template = loader.get_template('index.html')
    dashboard = DashboardContainer(request)
    dashboard.add(DashboardItemRegistry.get('placeholder'))
    context = RequestContext(request, {
        'dashboard': dashboard,
    })
    return HttpResponse(template.render(context))
```

In the template you have to call the render method:
{{ dashboard.render }} and there comes your dashboard!

## How to implement a DashboardItem

The `DashboardItemRegistry` scans for the folder „dashboards“ in your
app. So create a file and put it into your dashboards folder of your
app. To get started you need to create a class and register it in the
`DashboardItemRegistry`. Just have a look at the
[PlaceHolderDashboardItem](dashboards/PlaceHolderDashboardItem.py) to
get started.

