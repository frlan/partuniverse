from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse


from .views import PartsList, PartsAddView, PartDeleteView, PartDetail

urlpatterns = patterns('',
	# Some general url pattern
	url(r'^list/', PartsList.as_view(), name='partslist'),
	url(r'^add/', login_required(
			PartsAddView.as_view()),
			name='part_add'),
	# item specific ones
	url(r'^(?P<pk>[\w]+)/$', PartDetail.as_view(), name='part_detail'),
	url(r'^(?P<pk>[\w]+)/delete/$', login_required(
			PartDeleteView.as_view()),
			name='part_delete')
)
