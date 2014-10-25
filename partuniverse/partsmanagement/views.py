from django.views.generic.base import View
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
# Class based views to create a new dataset and Update one
from django.views.generic.edit import CreateView, UpdateView

# Current time
from django.utils.timezone import now

# Importing models
from partsmanagement.models import Part

class PartsList(View):
	model = Part
	template_name = 'pmgmt/list.html'

	def get(self, request, *args, **kwargs):
		tmp = list(Part.objects.all())
		return render(request, self.template_name, {'output': tmp})

class PartsAddView(CreateView):

	model = Part
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

