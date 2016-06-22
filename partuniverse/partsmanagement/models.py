# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

# Exceptions
from .exceptions import (
    PartsNotFitException,
    PartsmanagementException,
    CircleDetectedException
)
from datetime import datetime
from hashlib import sha256
from decimal import Decimal

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
    for i in StorageItem.objects.values("part").annotate(
            Sum("on_stock")).order_by('part'):
        tmp = []
        tmp.append(i['part'])
        tmp.append(i['on_stock__sum'])
        tmp.append(Part.objects.get(pk=i['part']).min_stock)
        result_list.append(tmp)
    return result_list


@python_2_unicode_compatible
class StorageType(models.Model):
    """ Defining a general typ of storage """

    name = models.CharField(
        max_length=50,
        help_text=_("The name for a storage type. Should be unique")
    )

    def __str__(self):
        return (u'%s' % self.name)

    class Meta:
        verbose_name = _("Storage Type")
        verbose_name_plural = _("Storage Types")
        ordering = ['name']


@python_2_unicode_compatible
class StoragePlace(models.Model):
    """ Representing the general storage place. This can be either a
        general storage or a particular place inside a storage as
        e.g. a shelf."""

    # The Name could be e.g. cordinates or something else meaningfull
    name = models.CharField(
        max_length=50,
        help_text=_("A name for the storage place."
                    "E.g. coordinates inside a book shelve.")
    )
    storage_type = models.ForeignKey(
        StorageType,
        help_text=_("Of which type is the storage place.")
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        verbose_name=_("Parent storage"),
        help_text=_("The storage the current storage is part of.")
    )
    disabled = models.BooleanField(
        _("Disabled"),
        default=False,
        help_text=_("Whether a storage is active.")
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        null=True,
        help_text=_("A short description.")
    )

    def __str__(self):
        if self.parent is None:
            return (u'%s' % self.name)
        else:
            return (u'%s%s%s' % (
                self.parent,
                settings.PARENT_DELIMITER,
                self.name))

    def get_parents(self):
        """ Returns a list with parants of that StoragePare incl itself"""
        result = []
        next = self
        while True:
            if next.id in result:
                raise(
                    CircleDetectedException(
                        _('There seems to be a circle inside ancestors at %s.'
                        % (self.id)))
                    )
            else:
                result.append(next.id)
                if next.parent is not None:
                    next = next.parent
                else:
                    break
        return result

    def clean(self):
        # If there is an ID, we can check for ID and don't care about
        # the rest as it's a new object
        if self.id and self.parent:
            try:
                self.parent.get_parents()
            except CircleDetectedException:
                raise ValidationError(
                    {'parent': _('The storage cannot be one of its ancestors')}
                )

    class Meta:
        verbose_name = _("Storage Place")
        verbose_name_plural = _("Storage Places")
        ordering = ['name']


@python_2_unicode_compatible
class Manufacturer(models.Model):
    """ Manufacturer for a particular item """

    name = models.CharField(
        max_length=50,
        help_text=_("Name of the manufacturer.")
    )
    creation_time = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Timestamp the manufacturer was created at.")
    )
    created_by = models.ForeignKey(
        User,
        verbose_name=_("Added by"),
        help_text=_("The user the manufacturer was created by.")
    )

    def __str__(self):
        return ('%s' % self.name)

    class Meta:
        verbose_name = _("Manufacturer")
        verbose_name_plural = _("Manufacturers")
        ordering = ['name']


@python_2_unicode_compatible
class Distributor(models.Model):
    """ A distributor which is selling a particular part """

    name = models.CharField(
        max_length=50,
        help_text=_("Name of the distributor")
    )

    creation_time = models.DateTimeField(
        _("Creation time"),
        auto_now_add=True,
        help_text=_("Timestamp the distributor was created at.")
    )
    created_by = models.ForeignKey(
        User,
        verbose_name=_("Added by"),
        help_text=_("User who created the distributor.")
    )

    def __str__(self):
        return (u'%s' % self.name)

    class Meta:
        verbose_name = _("Distributor")
        verbose_name_plural = _("Distributors")
        ordering = ['name']


@python_2_unicode_compatible
class Category(models.Model):
    """ Representing a category a part might contains to.
    E.g. resistor """

    name = models.CharField(
        max_length=50,
        help_text=_("Name of the category.")
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        help_text=_("If having a subcateogry, the parent.")
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        null=True,
        help_text=_("A short summarize of this category.")
    )

    def __str__(self):
        if self.parent is None:
            return (u'{}'.format(self.name))
        else:
            return (u'%s%s%s' % (
                self.parent,
                settings.PARENT_DELIMITER,
                self.name)
            )

    def get_parents(self):
        """ Returns a list with parants of that StoragePare incl itself"""
        result = []
        next = self
        while True:
            if next.id in result:
                raise(CircleDetectedException(
                    _('There seems to be a circle inside ancestors of %s.' % self.id)))
            else:
                result.append(next.id)
                if next.parent is not None:
                    next = next.parent
                else:
                    break
        return result

    def clean(self):
        # If there is an ID, we can check for ID and don't care about
        # the rest as it's a new object
        if self.id and self.parent:
            try:
                self.parent.get_parents()
            except CircleDetectedException:
                raise ValidationError(
                    {'parent': _('The category cannot be one of its ancestors.')}
                )

    class Meta:
        unique_together = ("name", "parent")
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']


@python_2_unicode_compatible
class Part(models.Model):
    """ Representing a special kind of parts """

    name = models.CharField(
        _("Name of part"),
        max_length=255,
        help_text=_("Name of the part.")
    )
    sku = models.CharField(
        _("SKU"),
        max_length=60,
        unique=True,
        help_text=_("A installation unique idendifier for the part."),
        null=True,
        blank=True
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        null=True,
        help_text=_("A long text description of the part")
    )
    min_stock = models.DecimalField(
        _("Minimal stock"),
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        help_text=_("Set a minimum that should be stored.")
    )
    unit = models.CharField(
        _("Messuring unit"),
        max_length=3,
        choices=UNIT_CHOICES,
        blank=False,
        default='---',
        help_text=_("The unit quantities are in.")
    )
    pic = models.ImageField(
        null=True,
        blank=True,
        upload_to='uploads/',
        help_text=_("The actual image.")
    )
    image_url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_("The URL of the original image.")
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        verbose_name=_("Manufacturer"),
        null=True,
        blank=True,
        help_text=_("The manufacturer of the part.")
    )
    distributor = models.ForeignKey(
        Distributor,
        verbose_name=_("Distributor"),
        null=True,
        blank=True,
        help_text=_("The usual distributor of the part.")
    )
    price = models.DecimalField(
        _("Cost of the part"),
        help_text=_("The cost/price for the part"),
        null=True,
        blank=True,
        max_digits=6,
        decimal_places=2
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name=_("Category"),
        help_text=_("A list of categories the part is in.")
    )
    creation_time = models.DateTimeField(
        _("Creation time"),
        auto_now_add=True,
        help_text=_("Timestamp the part was created on.")
    )
    created_by = models.ForeignKey(
        User,
        verbose_name=_("Added by"),
        help_text=_("The user the part was created by.")
    )
    disabled = models.BooleanField(
        _("Disabled"),
        default=False,
        help_text=_("Whether the part is active or not.")
    )

    def __str__(self):
        return ('%s' % self.name)

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = '{}-{}'.format(
                sha256(self.name.encode('utf-8')).hexdigest(),
                datetime.now()
            )
        super(Part, self).save(*args, **kwargs)

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
                u'One of the storage items seems to not exists: %s, %s' % (
                    si1,
                    si2
                )
            )

        # We need to check, whether we don't merge different parts here
        if si1.part.id != si2.part.id or self.id != si1.part.id:
            raise PartsNotFitException(
                u'Cannot merge not idendical parts. Parts »%s« and »%s« are not idendical' %
                (si1.part, si2.part))

        # Check, whether si1 and si2 are different storage types at all
        # If so, we better don't do anything.
        if si1.id == si2.id:
            raise PartsmanagementException(
                u'StorageItems are idendical. Nothing to merge')

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

    def cache(self):
        """Store image locally if we have a URL"""

        if self.image_url and not self.pic:
            result = urllib.urlretrieve(self.image_url)
            self.pic.save(os.path.basename(self.image_url),
                          File(open(result[0])))
            self.save()

    class Meta:
        verbose_name = _("Part")
        verbose_name_plural = _("Parts")
        ordering = ['name']


@python_2_unicode_compatible
class StorageItem(models.Model):
    part = models.ForeignKey(
        Part,
        help_text=_("The part stored at this spot.")
    )
    storage = models.ForeignKey(
        StoragePlace,
        help_text=_("The storage the part is stored in.")
    )
    on_stock = models.DecimalField(
        _("Parts inside storage"),
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        help_text=_("The amount currently stored.")
    )
    disabled = models.BooleanField(
        _("Disabled"),
        default=False,
        help_text=_("Whether the storage item is active.")
    )

    def __str__(self):
        return (u'%s; %s' % (self.part, self.storage))

    def stock_report(self, new_on_stock, requested_user):
        if new_on_stock < 0:
            raise StorageItemBelowZeroException(
                u("Tried to set {} amount below 0" % self.name)
            )

        if new_on_stock >= 0:
            if self.on_stock is None and new_on_stock == 0:
                return
            elif self.on_stock is None:
                difference = new_on_stock
            else:
                difference = new_on_stock - self.on_stock

            trans = Transaction.objects.create(
                subject=_(u'Difference from Stocktaking'),
                created_by=requested_user,
                amount=difference,
                storage_item=self,
                date=timezone.now()
            )

    class Meta:
        unique_together = ("part", "storage")
        verbose_name = _("Storage Item")
        verbose_name_plural = _("Storage Items")
        ordering = ['storage', 'part']


@python_2_unicode_compatible
class Transaction(models.Model):
    """ The transaction really taking place for the part """

    subject = models.CharField(
        _("Subject"),
        max_length=100,
        help_text=_("A short conclusion "
                    "of the transaction.")
    )
    storage_item = models.ForeignKey(
        StorageItem,
        null=True,
        blank=True,
        help_text=_("The part-storage relation "
                    "the transaction was applied on.")
    )
    amount = models.DecimalField(
        _("Amount"),
        max_digits=10,
        decimal_places=4,
        help_text=_("The quantity transferred.")
    )
    comment = models.TextField(
        _("Comment"),
        blank=True,
        null=True,
        max_length=200,
        help_text=_("A short conclusion.")
    )
    date = models.DateTimeField(
        _("Transaction Date"),
        blank=False,
        null=False,
        default=datetime.now,
        db_index=True,
        help_text=_("The data the transaction take part.")
    )
    state = models.CharField(
        _("State"),
        max_length=6,
        choices=STATE_CHOICES,
        blank=True,
        default='---',
        help_text=_("The status a transaction is in.")
    )
    created_by = models.ForeignKey(
        User,
        verbose_name=_("Created by"),
        help_text=_("The user which created the transaction.")
    )
    created_date = models.TimeField(
        _("Creation timestamp"),
        blank=False,
        null=False,
        auto_now_add=True,
        db_index=True,
        help_text=_("The timestamp transaction has been entered.")
    )

    def __create_revert(self, old_transaction):
        revert_tran = Transaction.objects.create(
            subject=_(u'reverted {}'.format(old_transaction.subject)),
            created_by=old_transaction.created_by,
            amount=old_transaction.amount * -1,
            storage_item=old_transaction.storage_item,
            date=timezone.now()
        )

    def save(self, *args, **kwargs):
        # Trying to get origin transaction if there is one
        try:
            if self.id:
                old_transaction = Transaction.objects.get(pk=self.id)
                # Checking whether StorageItem has changed and create new
                # Transactions to represent this
                if old_transaction.storage_item.id is not self.storage_item.id:
                    self.__create_revert(old_transaction)
                    new_tran = Transaction.objects.create(
                        subject=_(u'moved {}'.format(old_transaction.subject)),
                        created_by=old_transaction.created_by,
                        amount=old_transaction.amount,
                        storage_item=self.storage_item,
                        date=timezone.now()
                    )
                if old_transaction.amount != self.amount:
                    si = StorageItem.objects.get(pk=self.storage_item.id)
                    if si.on_stock is not None:
                        si.on_stock = (
                            si.on_stock - old_transaction.amount) + self.amount
                    elif self.amount:
                        si.on_stock = self.amount
                    si.save()
            if not self.id:
                # We got a new Transaction
                si = StorageItem.objects.get(pk=self.storage_item.id)
                if si.on_stock is not None:
                    si.on_stock = si.on_stock + Decimal(self.amount)
                elif self.amount is not None:
                    si.on_stock = Decimal(self.amount)
                si.save()

        except ObjectDoesNotExist:
            pass

        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return ('%s %s %s' % (self.subject, self.storage_item, self.date))

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        ordering = ['date']
