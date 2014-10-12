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

	def __unicode__(self):
		return self.name

class StoragePlace(models.Model):
	'''Representing the place inside the storage'''
	# The Name could be e.g. cordinates
	name = models.CharField(max_length=50)
	storage_type = models.ForeignKey(StorageType)

	def __unicode__(self):
		return self.name


class Manufacturer(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name


class Distributor(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Category(models.Model):
	'''Representing a category a part might contains to. E.g. resistor'''
	name = models.CharField(max_length=50)
	parent = models.ForeignKey("self", null=True, blank=True)

	def __unicode__(self):
		if self.parent == None:
			return self.name
		else:
			tmp = unicode(str(self.parent) + ':' + str(self.name))
			return tmp

	class Meta:
		verbose_name_plural = "Categories"


class Part(models.Model):
	'''Representing a special kind of parts'''
	name = models.CharField(max_length=50)
	min_stock = models.DecimalField(
		max_digits=10,
		decimal_places=4,
		null=True,
		blank=True)
	# Should be calculated based on transactions
	on_stock = models.DecimalField(
		max_digits=10,
		decimal_places=4,
		null=True,
		blank=True)
	unit = models.ForeignKey(Unit)
	manufacturer = models.ForeignKey(Manufacturer)
	distributor = models.ForeignKey(Distributor)
	categories = models.ManyToManyField(Category)
	creation_time = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User)

	def __unicode__(self):
		return self.name


class Transaction(models.Model):
	'''The transaction really taking place for the part'''
	subject = models.CharField(max_length=100)
	user = models.ForeignKey(User)
	amount = models.DecimalField(max_digits=10, decimal_places=4)
	measuring_unit = models.ForeignKey(Unit)
	part = models.ForeignKey(Part)
	date = models.DateField(
		blank=False,
		null=False,
		auto_now_add=True,
		db_index=True)

	def __unicode__(self):
		tmp = self.subject + " " + str(self.part) + " " + str(self.date)
		return unicode(tmp)

