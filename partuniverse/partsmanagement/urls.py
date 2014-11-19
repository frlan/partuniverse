# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

#i18n
from django.utils.translation import ugettext_lazy as _

from .views import *

urlpatterns = patterns('',
	# Some general url pattern
	url(r'^list/', PartsList.as_view(), name='partslist'),
	url(r'^add/', login_required(
			PartsAddView.as_view()),
			name='part_add'),
	url(r'^reorderlist/$', PartsReorderList.as_view(), name='parts_reorderlist'),
	# item specific ones
	url(r'^(?P<pk>[\w]+)/$', PartDetailView.as_view(),
			name='part_detail'),
	url(r'^(?P<pk>[\w]+)/delete/$', login_required(
			PartDeleteView.as_view()),
			name='part_delete'),
	url(r'^(?P<pk>[\w]+)/update/$', login_required(
			PartUpdateView.as_view()),
			name='part_update'),
	# Transactions
	url(r'^transaction/list', TransactionListView.as_view(), name='transaction_list'),
	url(r'^transaction/new$', login_required(TransactionAddView.as_view()),
			name='transaction_new'),
	# Manufacturer
	url(r'^manufacturer/list', ManufacturerListView.as_view(),
			name='manufacturer_list'),
	url(r'^manufacturer/add', login_required(ManufacturerAddView.as_view()),
			name='manufacturer_new'),
	url(r'^manufacturer/(?P<pk>[\w]+)/update/$', login_required(
			ManufacturerUpdateView.as_view()), name='manufacturer_update'),
#	url(r'^manufacturer/(?P<pk>[\w]+)/delete/$', ManufacturerDeleteView.as_view(),
#			name='manufacturer_delete'),
	url(r'^manufacturer/(?P<pk>[\w]+)$', ManufacturerView.as_view(),
			name='manufacturer_detail'),
	# Distributor
	url(r'^distributor/list', DistributorListView.as_view(),
			name='distributor_list'),
	url(r'^distributor/add', login_required(DistributorAddView.as_view()),
			name='distributor_new'),
	url(r'^distributor/(?P<pk>[\w]+)/update/$', login_required(
			DistributorUpdateView.as_view()), name='distributor_update'),
#	url(r'^manufacturer/(?P<pk>[\w]+)/delete/$', ManufacturerDeleteView.as_view(),
#			name='manufacturer_delete'),
	url(r'^distributor/(?P<pk>[\w]+)$', DistributorView.as_view(),
			name='distributor_detail'),
	# Storage
	url(r'^storage/add', login_required(StoragePlaceAddView.as_view()),
			name='storage_add'),
)
