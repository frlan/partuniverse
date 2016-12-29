# -*- coding: utf-8 -*-

from decimal import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import F
from django.forms.widgets import DateTimeInput
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView
from django.views.generic.list import ListView
from partsmanagement.forms import *
from partsmanagement.models import *

# Logging
import logging
logger = logging.getLogger(__name__)


########################################################################
# Category
########################################################################
class CategoryList(ListView):
    model = Category
    template_name = 'pmgmt/category/list.html'


class CategoryAddView(CreateView):
    model = Category
    success_url = reverse_lazy('category_list')
    template_name = 'pmgmt/category/add.html'
    fields = ('name',)

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        form.instance.creation_time = now()
        return super(CategoryAddView, self).form_valid(form)


########################################################################
# Part
########################################################################
class PartsList(ListView):
    model = Part
    template_name = 'pmgmt/part/list.html'

    def get_queryset(self):
        return Part.objects.exclude(disabled='True')


class PartsReorderList(ListView):
    # model = Part
    template_name = 'pmgmt/part/list.html'
    context_object_name = 'reorder_items'

    # This is not using new generated functions, but should be much more
    # performant for lot of items instead
    def get_queryset(self):
        # Should be translated to something like:
        # SELECT *
        # FROM "PARTS"
        # WHERE NOT (on_stock > 0
        #   AND on_stock >= min_stock)
        # TODO: Check on database level
        return Part.objects.exclude(on_stock__gt='0',
                                    on_stock__gte=F('min_stock'))


class PartsAddView(CreateView):
    model = Part
    success_url = reverse_lazy('part_list')
    template_name = 'pmgmt/part/add.html'
    fields = ('name',
              'sku',
              'min_stock',
              'unit',
              'price',
              'manufacturer',
              'distributor',
              'categories',
              'pic')

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        form.instance.timestamp = now()
        return super(PartsAddView, self).form_valid(form)


class PartDeleteView(DeleteView):
    model = Part
    success_url = reverse_lazy('part_list')
    template_name = 'pmgmt/part/delete.html'

    def post(self, request, *args, **kwargs):
        if 'confirm' in request.POST:
            return super(PartDeleteView, self).post(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(self.success_url)


class PartDetailView(DetailView):
    template_name = "pmgmt/part/detail.html"
    model = Part
    fields = ('name',
              'sku',
              'min_stock',
              'pic'
              'unit',
              'price',
              'manufacturer',
              'distributor',
              'categories',
              'created_by')


class PartUpdateView(UpdateView):
    template_name = "pmgmt/part/update.html"
    success_url = reverse_lazy('part_list')
    model = Part
    # We don't want to make all fields editable via
    # normal frontend.
    fields = ('name',
              'description',
              'min_stock',
              'unit',
              'price',
              'manufacturer',
              'distributor',
              'categories',
              'pic')


########################################################################
# Transaction
########################################################################
class TransactionListView(ListView):
    model = Transaction
    template_name = 'pmgmt/transaction/list.html'


class TransactionAddView(CreateView):
    model = Transaction
    success_url = reverse_lazy('transaction_list')
    template_name = 'pmgmt/transaction/add.html'
    fields = ('subject',
              'storage_item',
              'amount',
              'date',
              'comment')

    def get_form(self, form_class):
        form = super(TransactionAddView, self).get_form(form_class)
        form.fields['date'].widget = DateTimeInput(
            attrs={
                'type': "datetime-local",
                'icon': 'calendar'
            }
        )
        return form

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        form.instance.timestamp = now()
        return super(TransactionAddView, self).form_valid(form)


class TransactionView(DetailView):

    template_name = "pmgmt/transaction/detail.html"
    model = Transaction


########################################################################
# Manufacturer
########################################################################
class ManufacturerAddView(CreateView):
    model = Manufacturer
    success_url = reverse_lazy('manufacturer_list')
    template_name = 'pmgmt/manufacturer/add.html'
    fields = ('name', 'logo', 'url')

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        form.instance.creation_time = now()
        return super(ManufacturerAddView, self).form_valid(form)


class ManufacturerUpdateView(UpdateView):
    template_name = "pmgmt/manufacturer/update.html"
    success_url = reverse_lazy('manufacturer_list')
    model = Manufacturer
    # We don't want to make all fields editable via
    # normal frontend.
    fields = ('name', 'logo', 'url')


class ManufacturerListView(ListView):
    model = Manufacturer
    template_name = 'pmgmt/manufacturer/list.html'


class ManufacturerView(DetailView):
    template_name = "pmgmt/manufacturer/detail.html"
    model = Manufacturer


class ManufacturerDeleteView(DeleteView):
    model = Manufacturer
    success_url = reverse_lazy('manufacturer_list')
    template_name = 'pmgmt/manufacturer/delete.html'


########################################################################
# Distributor
########################################################################
class DistributorAddView(CreateView):
    model = Distributor
    success_url = reverse_lazy('distributor_list')
    template_name = 'pmgmt/distributor/add.html'
    fields = ('name', 'logo', 'url')

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        form.instance.creation_time = now()
        return super(DistributorAddView, self).form_valid(form)


class DistributorUpdateView(UpdateView):
    template_name = "pmgmt/distributor/update.html"
    success_url = reverse_lazy('distributor_list')
    model = Distributor
    # We don't want to make all fields editable via
    # normal frontend.
    fields = ('name', 'logo', 'url')


class DistributorListView(ListView):
    model = Distributor
    template_name = 'pmgmt/distributor/list.html'


class DistributorView(DetailView):
    template_name = 'pmgmt/distributor/detail.html'
    model = Distributor


class DistributorDeleteView(DeleteView):
    model = Distributor
    success_url = reverse_lazy('distributor_list')
    template_name = 'pmgmt/distributor/delete.html'


########################################################################
# StorageItem
########################################################################
class StorageItemAddView(CreateView):
    model = StorageItem
    success_url = reverse_lazy('storage_item_list')
    fields = ('part',
              'storage',
              'on_stock')
    template_name = 'pmgmt/storageitem/add.html'


class StorageItemListView(ListView):
    model = StorageItem
    template_name = 'pmgmt/storageitem/list.html'


class StorageItemDetailView(DetailView):
    model = StorageItem
    template_name = 'pmgmt/storageitem/detail.html'


class StorageItemUpdateView(UpdateView):
    model = StorageItem
    fields = ('part',
              'storage')
    template_name = 'pmgmt/storageitem/update.html'
    success_url = reverse_lazy('storage_item_list')


class StorageItemStockTakingView(FormView):
    form_class = StockTakingForm
    success_url = reverse_lazy('storage_item_list')
    template_name = 'pmgmt/storageitem/stocktaking.html'

    def form_valid(self, form):
        si = StorageItem.objects.get(pk=self.kwargs["pk"])
        si.stock_report(
            form.cleaned_data["amount"], self.request.user)
        return super(StorageItemStockTakingView, self).form_valid(form)


class StorageItemMergeView(FormView):
    form_class = MergeStorageItemsForm
    success_url = reverse_lazy('storage_item_list')
    template_name = 'pmgmt/storageitem/merge.html'

    def form_valid(self, form):
        si = StorageItem.objects.get(pk=self.kwargs["pk"])
        si.part.merge_storage_items(
            si,
            StorageItem.objects.get(pk=self.request.POST["storageitem1"]))
        return super(StorageItemMergeView, self).form_valid(form)


########################################################################
# StoragePlace
########################################################################
class StoragePlaceAddView(CreateView):
    model = StoragePlace
    success_url = reverse_lazy('storage_list')
    fields = ('name',
              'storage_type',
              'description',
              'pic',
              'parent')
    template_name = 'pmgmt/storage/add.html'


class StoragePlaceListView(ListView):
    model = StoragePlace
    template_name = 'pmgmt/storage/list.html'


class StoragePlaceDetailView(DetailView):
    model = StoragePlace
    template_name = 'pmgmt/storage/detail.html'


class StoragePlaceUpdateView(UpdateView):
    model = StoragePlace
    template_name = 'pmgmt/storage/update.html'
    fields = ('name',
              'storage_type',
              'description',
              'pic',
              'parent')
    success_url = reverse_lazy('storage_list')


########################################################################
# Storage Type
########################################################################
class StorageTypeAddView(CreateView):
    model = StorageType
    success_url = reverse_lazy('storage_type_list')
    fields = ('name',)
    template_name = 'pmgmt/storagetype/add.html'


class StorageTypeListView(ListView):
    model = StorageType
    template_name = 'pmgmt/storagetype/list.html'


class StorageTypeDetailView(DetailView):
    model = StorageType
    template_name = 'pmgmt/storagetype/detail.html'


class StorageTypeUpdateView(UpdateView):
    model = StorageType
    template_name = 'pmgmt/storagetype/update.html'
    fields = ('name',)
    success_url = reverse_lazy('storage_type_list')
