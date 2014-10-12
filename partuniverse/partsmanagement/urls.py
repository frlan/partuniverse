from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse


from views import PartsList

urlpatterns = patterns('',
	url(r'^list/', PartsList.as_view(), name='partslist'),
)
