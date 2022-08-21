# -*- coding: utf-8 -*-
from django.urls import re_path
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
    RestStorageTypeDetail,
)

urlpatterns = [
    re_path(r"^(?P<pk>[0-9]+)/$", RestPartDetail.as_view()),
    re_path(r"^list/$", RestPartList.as_view()),
    re_path(r"^category/list/$", RestCategoryList.as_view()),
    re_path(r"^category/(?P<pk>[0-9]+)/$", RestCategoryDetail.as_view()),
    re_path(r"^transaction/list/$", RestTransactionList.as_view()),
    re_path(r"^transaction/(?P<pk>[0-9]+)/$", RestTransactionDetail.as_view()),
    re_path(r"^manufacturer/list/$", RestManufacturerList.as_view()),
    re_path(r"^manufacturer/(?P<pk>[0-9]+)/$", RestManufacturerDetail.as_view()),
    re_path(r"^distributor/list/$", RestDistributorList.as_view()),
    re_path(r"^distributor/(?P<pk>[0-9]+)/$", RestDistributorDetail.as_view()),
    re_path(r"^storageitem/list/$", RestStorageItemList.as_view()),
    re_path(r"^storageitem/(?P<pk>[0-9]+)/$", RestStorageItemDetail.as_view()),
    re_path(r"^storage/list/$", RestStoragePlaceList.as_view()),
    re_path(r"^storage/(?P<pk>[0-9]+)/$", RestStoragePlaceDetail.as_view()),
    re_path(r"^storagetype/list/$", RestStorageTypeList.as_view()),
    re_path(r"^storagetype/(?P<pk>[0-9]+)/$", RestStorageTypeDetail.as_view()),
]
