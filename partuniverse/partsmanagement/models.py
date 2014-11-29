# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from django.conf import settings

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
	(_('n/A'), _('Unknown')),
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
	""" Representing the general storage place. This can be either a
		general storage or a particular place inside a storage as
		e.g. a shelf."""

	# The Name could be e.g. cordinates or something else meaningfull
	name = models.CharField(max_length=50)
	storage_type = models.ForeignKey(StorageType)
	parent = models.ForeignKey("self", null=True, blank=True,
		verbose_name=_("Parent storage"))
	disabled = models.BooleanField(_("Disabled"),
		default=False)

	def __unicode__(self):
		if self.parent == None:
			return self.name
		else:
			tmp = unicode(str(self.parent) + settings.PARENT_DELIMITER + str(self.name))
			return tmp

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
			tmp = unicode(str(self.parent) + settings.PARENT_DELIMITER + str(self.name))
			return tmp

	class Meta:
		verbose_name = _("Category")
		verbose_name_plural = _("Categories")


class Part(models.Model):
	""" Representing a special kind of parts """

	name = models.CharField(_("Name of part"), max_length=255)
	sku = models.CharField(_("SKU"), max_length=60, default='n/A')
	description = models.TextField(_("Description"),
		blank=True,
		null=True,
		default="")
	min_stock = models.DecimalField(
		_("Minimal stock"),
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
	categories = models.ManyToManyField(Category,
					verbose_name=_("Category"))
	creation_time = models.DateTimeField(_("Creation time"),
					auto_now_add=True)
	created_by = models.ForeignKey(User,
					verbose_name=_("Added by"))
	disabled = models.BooleanField(_("Disabled"),
		default=False)

	def __unicode__(self):
		return self.name

	def get_on_stock(self):
		""" Returns the amount of items which are on stock over all storages """
		pass

	# Based upon a post at http://stackoverflow.com/a/2217558/2915834
	# Modified to make it better readable for n00bz and exclude disabled
	# field or maybe others in future.
	def get_fields(self):
		tmp = []
		for field in Part._meta.fields:
			if field.name is not 'disabled':
				tmp.append((field.verbose_name, field.value_to_string(self)))
		return tmp
		#return [(field.verbose_name, field.value_to_string(self)) for field in Part._meta.fields]

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


class StorageItem(models.Model):
	part = models.ForeignKey(Part)
	storage = models.ForeignKey(StoragePlace)
	on_stock = models.DecimalField(
		_("Parts inside storage"),
		max_digits=10,
		decimal_places=4,
		null=True,
		blank=True)
	disabled = models.BooleanField(_("Disabled"),
		default=False)

	def __unicode__(self):
		return str(self.part) + ": " + str(self.storage)

	class Meta:
		unique_together = ("part", "storage")
		verbose_name = _("Storage Item")
		verbose_name_plural = _("Storage Items")


class Transaction(models.Model):
	""" The transaction really taking place for the part """

	subject = models.CharField(_("Subject"),
		max_length=100)
	created_by = models.ForeignKey(User,
		verbose_name=_("Created by"))
	amount = models.DecimalField(_("Amount"),
		max_digits=10,
		decimal_places=4)
	storage_item = models.ForeignKey(StorageItem,null=True, blank=True)
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
		tmp_storage_item = StorageItem.objects.get(pk = self.storage_item.id)
		print tmp_storage_item
		tmp_storage_item.on_stock = tmp_storage_item.on_stock + self.amount
		tmp_storage_item.save()
		super(Transaction, self).save(*args, **kwargs)

	def __unicode__(self):
		tmp = self.subject + " " + str(self.storage_item) + " " + str(self.date)
		return unicode(tmp)

	class Meta:
		verbose_name = _("Transaction")
		verbose_name_plural = _("Transactions")
