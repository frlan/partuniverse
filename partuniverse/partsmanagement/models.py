# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


# Just defining units used on the system here.
# Might can be moved to a seperate file at some point.
UNIT_CHOICES = (
	( _('Length'), (
			('m', _('meters')),
			('cm',_('centimeters'))
		)
	),
	(_('Volume'), (
			('l', _('litres')),
			('m³', _('cubicmeters')),
			('ccm', _('cubic centimeters'))
		)
	),
	('---', _('Unknown')),
)


class StorageType(models.Model):
	""" Defining a general typ of storage """

	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _("Storage Type")
		verbose_name_plural = _("Storage Types")


class StoragePlace(models.Model):
	""" Representing the place inside the storage """
	# The Name could be e.g. cordinates
	name = models.CharField(max_length=50)
	storage_type = models.ForeignKey(StorageType)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _("Storage Place")
		verbose_name_plural = _("Storage Places")


class Manufacturer(models.Model):
	""" Manufacturer for a particular item """

	name = models.CharField(max_length=50)
	creation_time = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User,
					verbose_name=_("Added by"))

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _("Manufacturer")
		verbose_name_plural = _("Manufacturers")


class Distributor(models.Model):
	""" A distributor which is selling a particular part """

	name = models.CharField(max_length=50)

	creation_time = models.DateTimeField(_("Creation time"),
					auto_now_add=True)
	created_by = models.ForeignKey(User,
					verbose_name=_("Added by"))

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _("Distributor")
		verbose_name_plural = _("Distributors")



class Category(models.Model):
	""" Representing a category a part might contains to.
	E.g. resistor """

	name = models.CharField(max_length=50)
	parent = models.ForeignKey("self", null=True, blank=True)

	def __unicode__(self):
		if self.parent == None:
			return self.name
		else:
			tmp = unicode(str(self.parent) + ':' + str(self.name))
			return tmp

	class Meta:
		verbose_name = _("Category")
		verbose_name_plural = _("Categories")


class Part(models.Model):
	""" Representing a special kind of parts """

	name = models.CharField(_("Name of part"), max_length=50)
	min_stock = models.DecimalField(
		_("Minimal stock"),
		max_digits=10,
		decimal_places=4,
		null=True,
		blank=True)
	# Should be calculated based on transactions
	on_stock = models.DecimalField(
		_("Parts on stock"),
		max_digits=10,
		decimal_places=4,
		null=True,
		blank=True)
	unit = models.CharField(_("Messuring unit"),
		max_length=3,
		choices=UNIT_CHOICES,
		blank=False,
		default='---')
	manufacturer = models.ForeignKey(Manufacturer,
					verbose_name=_("Manufacturer"),
					null=True,
					blank=True)
	distributor = models.ForeignKey(Distributor,
					verbose_name=_("Distributor"),
					null=True,
					blank=True)
	storage_place = models.ForeignKey(StoragePlace,
					verbose_name=_("Storage"),
					blank=True,
					null=True)
	categories = models.ManyToManyField(Category,
					verbose_name=_("Category"))
	creation_time = models.DateTimeField(_("Creation time"),
					auto_now_add=True)
	created_by = models.ForeignKey(User,
					verbose_name=_("Added by"))

	def __unicode__(self):
		return self.name

	# Based upon post at http://stackoverflow.com/a/2217558/2915834
	def get_fields(self):
		return [(field.verbose_name, field.value_to_string(self)) for field in Part._meta.fields]

	def is_below_min_stock(self):
		""" Returns True, if the item is below minimum stock.
			Will returns False if on_stock >= min_stock
			If either on_stock or min_stock is not defined, it will
			return False """
		if (self.on_stock is not None and
			self.min_stock is not None and
			self.on_stock < self.min_stock):
			return True
		else:
			return False

	def is_on_stock(self):
		""" Returns True, if the item is on stock.
			Will return False if on_stock <= 0
			If either on_stock is not defined, it will
			return True """
		if (self.on_stock is None or
			self.on_stock > 0):
			return True
		else:
			return False

	class Meta:
		verbose_name = _("Part")
		verbose_name_plural = _("Parts")


class Transaction(models.Model):
	""" The transaction really taking place for the part """
	subject = models.CharField(_("Subject"),
		max_length=100)
	created_by = models.ForeignKey(User,
		verbose_name=_("Created by"))
	amount = models.DecimalField(_("Amount"),
		max_digits=10,
		decimal_places=4)
	part = models.ForeignKey(Part)
	date = models.DateField(_("Transaction Date"),
		blank=False,
		null=False,
		auto_now_add=True,
		db_index=True)
	comment = models.TextField(_("Comment"),
		blank=True,
		null=True,
		max_length=200)

	def save(self, *args, **kwargs):
		try:
			tmp_part = Part.objects.get(name = self.part.name)
			tmp_part.on_stock = tmp_part.on_stock + self.amount
			tmp_part.save()
		except:
			pass
		super(Transaction, self).save(*args, **kwargs)

	def __unicode__(self):
		tmp = self.subject + " " + str(self.part) + " " + str(self.date)
		return unicode(tmp)

	class Meta:
		verbose_name = _("Transaction")
		verbose_name_plural = _("Transactions")
