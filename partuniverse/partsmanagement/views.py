# -*- coding: utf-8 -*-

from django.views.generic.base import View
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Avg
from django.contrib.auth.decorators import login_required

# Class based views to create a new dataset and Update one
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Current time
from django.utils.timezone import now

# Importing models
from partsmanagement.models import Part
from partsmanagement.models import Transaction
from partsmanagement.models import Manufacturer
from partsmanagement.models import Distributor

########################################################################
# Part
########################################################################
class PartsList(ListView):
	model = Part
	template_name = 'pmgmt/list.html'

class TransactionListView(ListView):
	model = Transaction
	template_name = 'pmgmt/trans_list.html'

class PartsAddView(CreateView):
	model = Part
	success_url='/'
	template_name='pmgmt/add.html'
	fields = (	'name',
				'min_stock',
				'on_stock',
				'unit',
				'manufacturer',
				'distributor',
				'categories' )

	def form_valid(self, form):
		user = self.request.user
		form.instance.created_by = user
		form.instance.timestamp = now()
		return super(PartsAddView, self).form_valid(form)

class PartDeleteView(DeleteView):
	model = Part
	success_url = reverse_lazy('partslist')
	template_name = 'pmgmt/delete.html'


class PartDetailView(DetailView):
	template_name = "pmgmt/detail.html"
	model = Part


class PartUpdateView(UpdateView):
	template_name = "pmgmt/update.html"
	success_url = reverse_lazy('partslist')
	model = Part
	# We don't want to amke all fields editable via
	# normal frontend.
	fields = (	'name',
				'min_stock',
				'unit',
				'manufacturer',
				'distributor',
				'categories' )

########################################################################
# Transaction
########################################################################
class TransactionAddView(CreateView):

	model = Transaction
	success_url='/'
	template_name='pmgmt/add.html'
	fields = (	'subject',
				'part',
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
	success_url='/'
	template_name='pmgmt/manufacturer/add.html'
	fields = ( 'name', )

	def form_valid(self, form):
		user = self.request.user
		form.instance.created_by = user
		form.instance.creation_time = now()
		return super(ManufacturerAddView, self).form_valid(form)


class ManufacturerUpdateView(UpdateView):
	template_name = "pmgmt/manufacturer/update.html"
	success_url = reverse_lazy('home')
	model = Manufacturer
	# We don't want to amke all fields editable via
	# normal frontend.
	fields = (	'name', )


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
	success_url='/'
	template_name='pmgmt/distributor/add.html'
	fields = ( 'name', )

	def form_valid(self, form):
		user = self.request.user
		form.instance.created_by = user
		form.instance.creation_time = now()
		return super(DistributorAddView, self).form_valid(form)


class DistributorUpdateView(UpdateView):
	template_name = "pmgmt/distributor/update.html"
	success_url = reverse_lazy('home')
	model = Distributor
	# We don't want to make all fields editable via
	# normal frontend.
	fields = (	'name', )


class DistributorListView(ListView):
	model = Distributor
	template_name = 'pmgmt/distributor/list.html'


class DistributorView(DetailView):
	template_name = "pmgmt/distributor/detail.html"
	model = Distributor


class DistributorDeleteView(DeleteView):
	model = Distributor
	success_url = reverse_lazy('distributorr_list')
	template_name = 'pmgmt/distributor/delete.html'
