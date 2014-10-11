from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class StoragePlace(models.Model):
	'''Representing the place inside the storage'''
	name = models.CharField(max_length=50)

class Part(models.Model):
	'''Representing a special kind of parts'''
	name = models.CharField(max_length=50)

class Categorie(models.Model):
	'''Representing a category a part might contains to. E.g. resistor'''
	name = models.CharField(max_length=50)
	parent = models.ForeignKey("self", null=True, blank=True)

	def __unicode__(self):
		return self.name

class Transaction(models.Model):
	'''The transaction really taking place for the part'''
	subject = models.CharField(max_length=100)
	user = models.ForeignKey(User)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	part = models.ForeignKey(Part)
	date = models.DateField(blank=False, null=False)

