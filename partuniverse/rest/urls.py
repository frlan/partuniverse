# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf.urls.static import static
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from partsmanagement.views import *

urlpatterns = [
    url(r'^rest/(?P<pk>[0-9]+)/$', RestPartDetail.as_view()),
    url(r'^category/rest/list/$', RestCategoryList.as_view()),
    url(r'^category/rest/(?P<pk>[0-9]+)/$', RestCategoryDetail.as_view()),
    url(r'^transaction/rest/list/$', RestTransactionList.as_view()),
    url(r'^transaction/rest/(?P<pk>[0-9]+)/$', RestTransactionDetail.as_view()),
    url(r'^manufacturer/rest/list/$', RestManufacturerList.as_view()),
    url(r'^manufacturer/rest/(?P<pk>[0-9]+)/$', RestManufacturerDetail.as_view()),
    url(r'^distributor/rest/list/$', RestDistributorList.as_view()),
    url(r'^distributor/rest/(?P<pk>[0-9]+)/$', RestDistributorDetail.as_view()),
    url(r'^storageitem/rest/list/$', RestStorageItemList.as_view()),
    url(r'^storageitem/rest/(?P<pk>[0-9]+)/$', RestStorageItemDetail.as_view()),
    url(r'^storage/rest/list/$', RestStoragePlaceList.as_view()),
    url(r'^storage/rest/(?P<pk>[0-9]+)/$', RestStoragePlaceDetail.as_view()),
    url(r'^storagetype/rest/list/$', RestStorageTypeList.as_view()),
    url(r'^storagetype/rest/(?P<pk>[0-9]+)/$',
        RestStorageTypeDetail.as_view())]
