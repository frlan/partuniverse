# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView
from django.urls import include, re_path


from .views import (
    CategoryAddView,
    CategoryDetailView,
    CategoryList,
    CategoryUpdateView,
    DistributorAddView,
    DistributorListView,
    DistributorUpdateView,
    DistributorView,
    ManufacturerAddView,
    ManufacturerListView,
    ManufacturerUpdateView,
    ManufacturerView,
    PartDeleteView,
    PartDetailView,
    PartsAddView,
    PartsList,
    PartsReorderList,
    PartUpdateView,
    StorageItemAddView,
    StorageItemAddPartView,
    StorageItemDetailView,
    StorageItemListView,
    StorageItemMergeView,
    StorageItemStockTakingView,
    StorageItemToReviewListView,
    StorageItemTransactionAddView,
    StorageItemUpdateView,
    StoragePlaceAddView,
    StoragePlaceBulkAddView,
    StoragePlaceDetailView,
    StoragePlaceListView,
    StoragePlaceListEmptyView,
    StoragePlaceUpdateView,
    StorageTypeAddView,
    StorageTypeDetailView,
    StorageTypeListView,
    StorageTypeUpdateView,
    TransactionAddView,
    TransactionListView,
    TransactionView,
)

urlpatterns = [
    # Some general url pattern
    re_path(r"^$", RedirectView.as_view(url="list", permanent=True), name="index"),
    re_path(r"^list/", PartsList.as_view(), name="part_list"),
    re_path(r"^add/", login_required(PartsAddView.as_view()), name="part_add"),
    re_path(
        r"^reorderlist/$", PartsReorderList.as_view(), name="part_reorderlist"
    ),
    # item specific ones
    re_path(r"^(?P<pk>[\w]+)/$", PartDetailView.as_view(), name="part_detail"),
    re_path(
        r"^(?P<pk>[\w]+)/addstorage$",
        login_required(StorageItemAddPartView.as_view()),
        name="part_add_storage_item",
    ),
    re_path(
        r"^(?P<pk>[\w]+)/delete/$",
        login_required(PartDeleteView.as_view()),
        name="part_delete",
    ),
    re_path(
        r"^(?P<pk>[\w]+)/update/$",
        login_required(PartUpdateView.as_view()),
        name="part_update",
    ),
    # Category
    re_path(r"^category/list", CategoryList.as_view(), name="category_list"),
    re_path(r"^category/add", CategoryAddView.as_view(), name="category_add"),
    re_path(
        r"^category/(?P<pk>[\w]+)/$",
        CategoryDetailView.as_view(),
        name="category_detail",
    ),
    re_path(
        r"^category/(?P<pk>[\w]+)/update/$",
        login_required(CategoryUpdateView.as_view()),
        name="category_update",
    ),
    # Transactions
    re_path(
        r"^transaction/list",
        TransactionListView.as_view(),
        name="transaction_list",
    ),
    re_path(
        r"^transaction/add$",
        login_required(TransactionAddView.as_view()),
        name="transaction_add",
    ),
    re_path(
        r"^transaction/(?P<pk>[\w]+)$",
        TransactionView.as_view(),
        name="transaction_detail",
    ),
    # Manufacturer
    re_path(
        r"^manufacturer/list",
        ManufacturerListView.as_view(),
        name="manufacturer_list",
    ),
    re_path(
        r"^manufacturer/add",
        login_required(ManufacturerAddView.as_view()),
        name="manufacturer_add",
    ),
    re_path(
        r"^manufacturer/(?P<pk>[\w]+)/update/$",
        login_required(ManufacturerUpdateView.as_view()),
        name="manufacturer_update",
    ),
    re_path(
        r"^manufacturer/(?P<pk>[\w]+)$",
        ManufacturerView.as_view(),
        name="manufacturer_detail",
    ),
    # Distributor
    re_path(
        r"^distributor/list",
        DistributorListView.as_view(),
        name="distributor_list",
    ),
    re_path(
        r"^distributor/add",
        login_required(DistributorAddView.as_view()),
        name="distributor_add",
    ),
    re_path(
        r"^distributor/(?P<pk>[\w]+)/update/$",
        login_required(DistributorUpdateView.as_view()),
        name="distributor_update",
    ),
    re_path(
        r"^distributor/(?P<pk>[\w]+)$",
        DistributorView.as_view(),
        name="distributor_detail",
    ),
    # Storageitems
    re_path(
        r"^storageitem/add",
        login_required(StorageItemAddView.as_view()),
        name="storage_item_add",
    ),
    re_path(
        r"^storageitem/list",
        StorageItemListView.as_view(),
        name="storage_item_list",
    ),
    re_path(
        r"^storageitem/reviewlist",
        StorageItemToReviewListView.as_view(),
        name="storage_item_review_list",
    ),
    re_path(
        r"^storageitem/(?P<pk>[\w]+)$",
        StorageItemDetailView.as_view(),
        name="storage_item_detail",
    ),
    re_path(
        r"^storageitem/(?P<pk>[\w]+)/update/$",
        login_required(StorageItemUpdateView.as_view()),
        name="storage_item_update",
    ),
    re_path(
        r"^storageitem/(?P<pk>[\w]+)/merge/$",
        login_required(StorageItemMergeView.as_view()),
        name="storage_item_merge",
    ),
    re_path(
        r"^storageitem/(?P<pk>[\w]+)/stocktaking/$",
        login_required(StorageItemStockTakingView.as_view()),
        name="storage_item_stocktaking",
    ),
    re_path(
        r"^storageitem/(?P<pk>[\w]+)/addtransaction/$",
        login_required(StorageItemTransactionAddView.as_view()),
        name="storage_item_transaction",
    ),
    # Storage Place
    re_path(
        r"^storage/add",
        login_required(StoragePlaceAddView.as_view()),
        name="storage_add",
    ),
    re_path(
        r"^storage/bulkadd",
        login_required(StoragePlaceBulkAddView.as_view()),
        name="storage_bulkadd",
    ),
    re_path(r"^storage/list", StoragePlaceListView.as_view(), name="storage_list"),
    re_path(
        r"^storage/empty_list",
        StoragePlaceListEmptyView.as_view(),
        name="storage_empty_list",
    ),
    re_path(
        r"^storage/(?P<pk>[\w]+)$",
        StoragePlaceDetailView.as_view(),
        name="storage_detail",
    ),
    re_path(
        r"^storage/(?P<pk>[\w]+)/update/$",
        login_required(StoragePlaceUpdateView.as_view()),
        name="storage_update",
    ),
    # Storage Types
    re_path(
        r"^storagetype/list",
        StorageTypeListView.as_view(),
        name="storage_type_list",
    ),
    re_path(
        r"^storagetype/add",
        login_required(StorageTypeAddView.as_view()),
        name="storage_type_add",
    ),
    re_path(
        r"^storagetype/(?P<pk>[\w]+)$",
        StorageTypeDetailView.as_view(),
        name="storage_type_detail",
    ),
    re_path(
        r"^storagetype/(?P<pk>[\w]+)/update/$",
        login_required(StorageTypeUpdateView.as_view()),
        name="storage_type_update",
    ),
]
