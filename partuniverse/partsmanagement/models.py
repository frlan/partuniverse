# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

# Exceptions
from .exceptions import PartsNotFitException, PartsmanagementException, CircleDetectedException

# Logging
import logging
logger = logging.getLogger(__name__)


# Just defining units used on the system here.
# Might can be moved to a seperate file at some point.
UNIT_CHOICES = (
    (_('Length'), (
                  ('m', _('meters')),
                  ('cm', _('centimeters'))
    )),
    (_('Volume'), (
                  ('l', _('litres')),
                  ('m³', _('cubicmeters')),
                  ('ccm', _('cubic centimeters'))
    )),
    (_('Piece'), (
                 ('pc', _('piece')),
    )),
    (_('n/A'), _('Unknown')),
)

STATE_CHOICES = (
    ('paid', _('Paid')),
    ('open', _('Open')),
    ('res', _('Reserverd'))
)


def get_all_storage_item_parts_with_on_stock_and_min_stock():
    """ Returns a list of list with all Parts having a StorageItem
        with its min_stock value. """
    result_list = []
    for i in StorageItem.objects.values("part").annotate(Sum("on_stock")).order_by('part'):
        tmp = []
        tmp.append(i['part'])
        tmp.append(i['on_stock__sum'])
        tmp.append(Part.objects.get(pk=i['part']).min_stock)
        result_list.append(tmp)
    return result_list


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
    parent = models.ForeignKey("self",
                               null=True,
                               blank=True,
                               verbose_name=_("Parent storage"))
    disabled = models.BooleanField(_("Disabled"),
                                   default=False)
    description = models.TextField(_("Description"),
                                   blank=True,
                                   null=True)

    def __unicode__(self):
        if self.parent is None:
            return self.name
        else:
            return (u'%s%s%s' % (self.parent.__unicode__(), settings.PARENT_DELIMITER, self.name))

    def get_parents(self):
        """ Returns a list with parants of that StoragePare incl itself"""
        result = []
        next = self
        while True:
            if next.id in result:
                raise(CircleDetectedException(
                    _('There seems to be a circle inside ansistors at %s.'% self.id)))
            else:
                result.append(next.id)
                if next.parent is not None:
                    next = next.parent
        return result

    def clean(self):
        # If there is an ID, we can check for ID and don't care about
        # the rest as it's a new object
        if self.id and self.parent:
            try:
                print self.parent.get_parents()
            except CircleDetectedException:
                raise ValidationError(
                    {'parent': _('The storage cannot be one of its ansistors')}
                )

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
    description = models.TextField(_("Description"),
                                   blank=True,
                                   null=True)

    def __unicode__(self):
        if self.parent is None:
            return self.name
        else:
            return (u'%s%s%s' % (self.parent.__unicode__(), settings.PARENT_DELIMITER, self.name))

    def get_parents(self):
        """ Returns a list with parants of that category"""
        result = []
        result.append(self)
        if self.parent is not None:
            result = result + self.parent.get_parents()
        return result

    def save(self, *args, **kwargs):
        try:
            if self.parent is not None:
                ansistor = Category.objects.get(pk=self.parent.id)
                if self in ansistor.get_parents():
                    raise CircleDetectedException("%s is causing a circle" % self.name)
        except ObjectDoesNotExist:
            pass
        super(Category, self).save(*args, **kwargs)

    class Meta:
            unique_together = ("name", "parent")
            verbose_name = _("Category")
            verbose_name_plural = _("Categories")


class Part(models.Model):
    """ Representing a special kind of parts """

    name = models.CharField(_("Name of part"), max_length=255)
    sku = models.CharField(_("SKU"),
                           max_length=60,
                           blank=True,
                           null=True,
                           unique=True)
    description = models.TextField(_("Description"),
                                   blank=True,
                                   null=True)
    min_stock = models.DecimalField(
        _("Minimal stock"),
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
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
        return (u'%s' % self.name)

    def get_on_stock(self):
        """ Returns the amount of items which are on stock over all storages """

        # Catching all StorageItems connected with this Part and
        # calculating sum of them
        # TODO: Finding a more performant way doing this
        sum_amount = 0
        for si in self.storageitem_set.all():
            if si.on_stock is not None:
                sum_amount = sum_amount + si.on_stock
        return sum_amount

    def is_below_min_stock(self):
        """ Returns True, if the item is below minimum stock.
            Will returns False if on_stock >= min_stock
            If either on_stock or min_stock is not defined, it will
            return False """
        currently_on_stock = self.get_on_stock()
        if (self.min_stock is not None and currently_on_stock < self.min_stock):
            return True
        else:
            return False

    def is_on_stock(self):
        """ Returns True, if the item is on stock.
            Will return False if on_stock <= 0
            If either on_stock is not defined, it will
            return True """
        if (self.get_on_stock() > 0):
            return True
        else:
            return False

    def merge_storage_items(self, si1, si2):
        """
        Takes two storage items of a part and merging the second
        one (si2) onto first one (si1). This is done by transfering
        on_stock value of si2 to si1. At the end, it will delete si2
        so keep care to don't use it anymore.
        """

        # We cannot work on not given StorageItems
        if si1 is None or si2 is None:
            raise PartsmanagementException(
                u'One of the storage items seems to not exists: %s, %s' % (si1, si2)
            )

        # We need to check, whether we don't merge different parts here
        if si1.part.id != si2.part.id or self.id != si1.part.id:
            raise PartsNotFitException(
                u'Cannot merge not idendical parts. Parts »%s« and »%s« are not idendical' % (si1.part, si2.part))

        # Check, whether si1 and si2 are different storage types at all
        # If so, we better don't do anything.
        if si1.id == si2.id:
            raise PartsmanagementException(
                u'StorageItems are idendical. Nothing to merge'
            )

        # Special behavior for on_stock is None storage items
        # 0x None -> New on_stock is si1.on_stock + si2.on_stock
        # 1x None -> New on_stock is based on not None value
        # 2x None -> None
        if si1.on_stock is None and si2.on_stock is None:
            # Case: Both on_stock are None
            # Just delete si2 item from database
            si2.delete()

        elif si1.on_stock is not None and si2.on_stock is not None:
            # Case: Botn on_stock are not None
            si1.on_stock = si1.on_stock + si2.on_stock
            si1.save()
            si2.delete()

        elif si1.on_stock is not None:
            # Case: si2 on_stock is None
            si2.delete()

        else:
            # Case: si1 on_stock is None
            si1.on_stock = si2.on_stock
            si1.save()
            si2.delete()

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
        blank=True
    )
    disabled = models.BooleanField(_("Disabled"),
                                   default=False)

    def __unicode__(self):
        return (u'%s; %s' % (self.part, self.storage))

    class Meta:
        unique_together = ("part", "storage")
        verbose_name = _("Storage Item")
        verbose_name_plural = _("Storage Items")


class Transaction(models.Model):
    """ The transaction really taking place for the part """

    subject = models.CharField(_("Subject"),
                               max_length=100)
    storage_item = models.ForeignKey(StorageItem, null=True, blank=True)
    amount = models.DecimalField(_("Amount"),
                                 max_digits=10,
                                 decimal_places=4)
    comment = models.TextField(_("Comment"),
                               blank=True,
                               null=True,
                               max_length=200)
    date = models.DateField(_("Transaction Date"),
                            blank=False,
                            null=False,
                            auto_now_add=True,
                            db_index=True)
    state = models.CharField(_("State"),
                             max_length=6,
                             choices=STATE_CHOICES,
                             blank=True,
                             default='---')
    created_by = models.ForeignKey(User,
                                   verbose_name=_("Created by"))
    created_date = models.TimeField(_("Creation timestamp"),
                                    blank=False,
                                    null=False,
                                    auto_now_add=True,
                                    db_index=True)

    def save(self, *args, **kwargs):
        tmp_storage_item = StorageItem.objects.get(pk=self.storage_item.id)
        try:
            old_transaction = Transaction.objects.get(pk=self.id)
            if old_transaction.amount and tmp_storage_item.on_stock is not None:
                tmp_storage_item.on_stock = tmp_storage_item.on_stock - old_transaction.amount
        except ObjectDoesNotExist:
            pass

        if tmp_storage_item.on_stock is not None:
            tmp_storage_item.on_stock = tmp_storage_item.on_stock + self.amount
        tmp_storage_item.save()
        super(Transaction, self).save(*args, **kwargs)

    def __unicode__(self):
        return (u'%s %s %s' % (self.subject, self.storage_item, self.date))

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
