# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView


from .views import *

urlpatterns = patterns('',
                       # Some general url pattern
                       url(r'^list/', PartsList.as_view(), name='part_list'),
                       url(r'^add/', login_required(PartsAddView.as_view()),
                           name='part_add'),
                       url(r'^reorderlist/$', PartsReorderList.as_view(), name='part_reorderlist'),
                       # item specific ones
                       url(r'^(?P<pk>[\w]+)/$', PartDetailView.as_view(),
                           name='part_detail'),
                       url(r'^(?P<pk>[\w]+)/delete/$', login_required(PartDeleteView.as_view()),
                           name='part_delete'),
                       url(r'^(?P<pk>[\w]+)/update/$', login_required(PartUpdateView.as_view()),
                           name='part_update'),
                       # Transactions
                       url(r'^transaction/list', TransactionListView.as_view(), name='transaction_list'),
                       url(r'^transaction/add$', login_required(TransactionAddView.as_view()),
                           name='transaction_add'),
                       # Manufacturer
                       url(r'^manufacturer/list', ManufacturerListView.as_view(),
                           name='manufacturer_list'),
                       url(r'^manufacturer/add', login_required(ManufacturerAddView.as_view()),
                           name='manufacturer_add'),
                       url(r'^manufacturer/(?P<pk>[\w]+)/update/$', login_required(
                           ManufacturerUpdateView.as_view()), name='manufacturer_update'),
                       # url(r'^manufacturer/(?P<pk>[\w]+)/delete/$', ManufacturerDeleteView.as_view(),
                       #     name='manufacturer_delete'),
                       url(r'^manufacturer/(?P<pk>[\w]+)$', ManufacturerView.as_view(),
                           name='manufacturer_detail'),
                       # Distributor
                       url(r'^distributor/list', DistributorListView.as_view(),
                           name='distributor_list'),
                       url(r'^distributor/add', login_required(DistributorAddView.as_view()),
                           name='distributor_add'),
                       url(r'^distributor/(?P<pk>[\w]+)/update/$', login_required(DistributorUpdateView.as_view()),
                           name='distributor_update'),
                       # url(r'^manufacturer/(?P<pk>[\w]+)/delete/$', ManufacturerDeleteView.as_view(),
                       #     name='manufacturer_delete'),
                       url(r'^distributor/(?P<pk>[\w]+)$', DistributorView.as_view(),
                           name='distributor_detail'),
                       # Storage
                       url(r'^storageitem/add', login_required(StorageItemAddView.as_view()),
                           name='storage_item_add'),
                       url(r'^storageitem/list', StorageItemListView.as_view(),
                           name='storage_item_list'),
                       url(r'^storageitem/(?P<pk>[\w]+)$', StorageItemDetailView.as_view(),
                           name='storage_item_detail'),
                       url(r'^storageitem/(?P<pk>[\w]+)/update/$', login_required(
                           StorageItemUpdateView.as_view()), name='storage_item_update'),
                       url(r'^storageitem/(?P<pk>[\w]+)/merge/$', login_required(
                           StorageItemMergeView.as_view()), name='storage_item_merge'),
                       url(r'^storage/add', login_required(StoragePlaceAddView.as_view()),
                           name='storage_add'),
                       url(r'^storage/list', StoragePlaceListView.as_view(),
                           name='storage_list'),
                       url(r'^storage/(?P<pk>[\w]+)$', StoragePlaceDetailView.as_view(),
                           name='storage_detail'),
                       url(r'^storage/(?P<pk>[\w]+)/update/$', login_required(
                           StoragePlaceUpdateView.as_view()), name='storage_update'),
                       )
