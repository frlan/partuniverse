# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import F
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect

# Importing models
from partsmanagement.models import *

# Importing custom forms
from .forms import *

# Logging
import logging
logger = logging.getLogger(__name__)

########################################################################
# Category
########################################################################


class CategoryList(ListView):
    model = Category
    template_name = 'pmgmt/category/list.html'


class PartsPerCategoryList(ListView):
    pass

########################################################################
# Part
########################################################################


class PartsList(ListView):
    model = Part
    template_name = 'pmgmt/list.html'

    def get_queryset(self):
        return Part.objects.exclude(disabled='True')


class PartsReorderList(ListView):
    # model = Part
    template_name = 'pmgmt/list.html'
    context_object_name = 'reorder_items'

    # This is not using new generated functions, but should be much more
    # performant for lot of items instead
    def get_queryset(self):
        # Should be translated to something like:
        # SELECT * FROM "PARTS" WHERE NOT (on_stock > 0 AND on_stock >= min_stock)
        # TODO: Check on database level
        return Part.objects.exclude(on_stock__gt='0', on_stock__gte=F('min_stock'))


class PartsAddView(CreateView):
    model = Part
    success_url = reverse_lazy('part_list')
    template_name = 'pmgmt/add.html'
    fields = ('name',
              'sku',
              'min_stock',
              'unit',
              'manufacturer',
              'distributor',
              'categories')

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        form.instance.timestamp = now()
        return super(PartsAddView, self).form_valid(form)


class PartDeleteView(DeleteView):
    model = Part
    success_url = reverse_lazy('part_list')
    template_name = 'pmgmt/delete.html'

    def post(self, request, *args, **kwargs):
        if 'confirm' in request.POST:
            return super(PartDeleteView, self).post(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(self.success_url)


class PartDetailView(DetailView):
    template_name = "pmgmt/detail.html"
    model = Part
    fields = ('name',
              'sku',
              'min_stock',
              'unit',
              'manufacturer',
              'distributor',
              'categories',
              'created_by')


class PartUpdateView(UpdateView):
    template_name = "pmgmt/update.html"
    success_url = reverse_lazy('part_list')
    model = Part
    # We don't want to make all fields editable via
    # normal frontend.
    fields = ('name',
              'min_stock',
              'unit',
              'manufacturer',
              'distributor',
              'categories')


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
              'comment')

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        form.instance.timestamp = now()
        return super(TransactionAddView, self).form_valid(form)

########################################################################
# Manufacturer
########################################################################


class ManufacturerAddView(CreateView):
    model = Manufacturer
    success_url = reverse_lazy('manufacturer_list')
    template_name = 'pmgmt/manufacturer/add.html'
    fields = ('name',)

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
    fields = ('name',)


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
    fields = ('name',)

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
    fields = ('name',)


class DistributorListView(ListView):
    model = Distributor
    template_name = 'pmgmt/distributor/list.html'


class DistributorView(DetailView):
    template_name = "pmgmt/distributor/detail.html"
    model = Distributor


class DistributorDeleteView(DeleteView):
    model = Distributor
    success_url = reverse_lazy('distributor_list')
    template_name = 'pmgmt/distributor/delete.html'


########################################################################
# Storage
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
              'storage',
              'on_stock')
    template_name = 'pmgmt/storageitem/update.html'
    success_url = reverse_lazy('storage_item_list')


class StorageItemMergeView(FormView):
    form_class = MergeStorageItemsForm
    success_url = reverse_lazy('storage_item_list')
    template_name = 'pmgmt/storageitem/merge.html'

    def form_valid(self, form):
        si = StorageItem.objects.get(pk=self.kwargs["pk"])
        si.part.merge_storage_items(si, StorageItem.objects.get(pk=self.request.POST["storageitem1"]))
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
              'parent')
    success_url = reverse_lazy('storage_list')
