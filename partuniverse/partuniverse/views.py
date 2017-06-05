from django.http import HttpResponse
from django.template import RequestContext, loader
from dashboard.DashboardItemRegistry import DashboardItemRegistry
from dashboard.DashboardContainer import DashboardContainer
from django.contrib.auth.models import User


def dashboard(request):
    template = loader.get_template('index.html')
    dashboard = DashboardContainer(request)  # pylint: disable=W0621
    dashboard.add(DashboardItemRegistry.get('needs_restocking'))
    dashboard.add(DashboardItemRegistry.get('most_recent_transactions'))
    dashboard.add(DashboardItemRegistry.get('most_recent_parts'))
    context = RequestContext(request, {
        'dashboard': dashboard,
        'user': request.user
    })
    print(context.__dict__)
    return HttpResponse(template.render(context))
