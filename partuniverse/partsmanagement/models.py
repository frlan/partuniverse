from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class StorageType(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name


class Unit(models.Model):
	name = models.CharField(max_length=50)


class StoragePlace(models.Model):
	'''Representing the place inside the storage'''
	# The Name could be e.g. cordinates
	name = models.CharField(max_length=50)
	storage_type = models.ForeignKey(StorageType)

	def __unicode__(self):
		return self.name


class Manufacturer(models.Model):
	name = models.CharField(max_length=50)


class Distributor(models.Model):
	name = models.CharField(max_length=50)


class Part(models.Model):
	'''Representing a special kind of parts'''
	name = models.CharField(max_length=50)
	min_amount = models.DecimalField(
		max_digits=10,
		decimal_places=4,
		null=True,
		blank=True)
	manufacturer = models.ForeignKey(Manufacturer)
	distributor = models.ForeignKey(Distributor)


class Category(models.Model):
	'''Representing a category a part might contains to. E.g. resistor'''
	name = models.CharField(max_length=50)
	parent = models.ForeignKey("self", null=True, blank=True)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Categories"


class Transaction(models.Model):
	'''The transaction really taking place for the part'''
	subject = models.CharField(max_length=100)
	user = models.ForeignKey(User)
	amount = models.DecimalField(max_digits=10, decimal_places=4)
	measuring_unit = models.ForeignKey(Unit)
	part = models.ForeignKey(Part)
	date = models.DateField(blank=False, null=False)

