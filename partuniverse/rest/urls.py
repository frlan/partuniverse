# -*- coding: utf-8 -*-
from django.conf.urls import url
from partsmanagement.views import (
    RestPartDetail,
    RestPartList,
    RestTransactionDetail,
    RestCategoryDetail,
    RestCategoryList,
    RestTransactionList,
    RestManufacturerDetail,
    RestManufacturerList,
    RestDistributorDetail,
    RestDistributorList,
    RestStorageItemDetail,
    RestStorageItemList,
    RestStoragePlaceList,
    RestStoragePlaceDetail,
    RestStorageTypeList,
    RestStorageTypeDetail
)

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', RestPartDetail.as_view()),
    url(r'^list/$', RestPartList.as_view()),
    url(r'^category/list/$', RestCategoryList.as_view()),
    url(r'^category/(?P<pk>[0-9]+)/$', RestCategoryDetail.as_view()),
    url(r'^transaction/list/$', RestTransactionList.as_view()),
    url(r'^transaction/(?P<pk>[0-9]+)/$', RestTransactionDetail.as_view()),
    url(r'^manufacturer/list/$', RestManufacturerList.as_view()),
    url(r'^manufacturer/(?P<pk>[0-9]+)/$', RestManufacturerDetail.as_view()),
    url(r'^distributor/list/$', RestDistributorList.as_view()),
    url(r'^distributor/(?P<pk>[0-9]+)/$', RestDistributorDetail.as_view()),
    url(r'^storageitem/list/$', RestStorageItemList.as_view()),
    url(r'^storageitem/(?P<pk>[0-9]+)/$', RestStorageItemDetail.as_view()),
    url(r'^storage/list/$', RestStoragePlaceList.as_view()),
    url(r'^storage/(?P<pk>[0-9]+)/$', RestStoragePlaceDetail.as_view()),
    url(r'^storagetype/list/$', RestStorageTypeList.as_view()),
    url(r'^storagetype/(?P<pk>[0-9]+)/$',
        RestStorageTypeDetail.as_view())]
