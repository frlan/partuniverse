# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import *
from .views import *


########################################################################
# Category
########################################################################


class CategoryTestCase(TestCase):
    """ Test to check whether category name is printed correctly.
        If there is a parent, it should be also printed seperated by a : """

    def setUp(self):
        self.cat1 = Category.objects.create(name=u'Category 1')
        self.cat2 = Category.objects.create(name=u'Category ü', parent=self.cat1)
        self.cat3 = Category.objects.create(name=u'Category 3', parent=self.cat2)

    def test_category_name(self):
        cat_result1 = u'Category 1'
        cat_result2 = u'Category 1' + settings.PARENT_DELIMITER + u'Category ü'
        cat_result3 = u'Category 1' + settings.PARENT_DELIMITER + u'Category ü' + settings.PARENT_DELIMITER + u'Category 3'
        self.assertEqual(self.cat1.__unicode__(), cat_result1)
        self.assertEqual(self.cat2.__unicode__(), cat_result2)
        self.assertEqual(self.cat3.__unicode__(), cat_result3)


########################################################################
# Transaction
########################################################################


class TransactionInventoryChange(TestCase):
    """ This is a test to check whether a new transaction is increasing
        on_stock or decreasing on_stock of a particular storage item """

    def setUp(self):
        self.cat = Category.objects.create(name=u'Category 1')
        self.user = User.objects.create_user(
            username='jacob',
            email='jacob@foo.baa',
            password='top_secret'
        )
        self.manu = Manufacturer.objects.create(
            name=u'Test Manufacturer 1',
            created_by=self.user
        )
        self.storagetype = StorageType.objects.create(name=u"Testtype")
        self.storageplace = StoragePlace.objects.create(
            name=u'Test Storage',
            storage_type=self.storagetype
        )
        self.part1 = Part.objects.create(
            name=u'Test Part 1 with unicode µä³½',
            unit='m',
            creation_time=timezone.now(),
            created_by=self.user
        )
        self.part2 = Part.objects.create(
            name=u'Test Part 2',
            unit='m',
            creation_time=timezone.now(),
            created_by=self.user
        )
        self.storage_item1 = StorageItem.objects.create(
            part=self.part1,
            storage=self.storageplace,
            on_stock=100
        )
        self.storage_item1 = StorageItem.objects.create(
            part=self.part2,
            storage=self.storageplace,
            on_stock=100
        )

    def test_transaction_decrease_on_stock(self):
        trans = Transaction.objects.create(
            subject=u'Testtransaction 1',
            created_by=self.user,
            amount=-10,
            storage_item=self.storage_item1,
            date=timezone.now(),
        )
        self.assertEqual(int(StorageItem.objects.get(pk=trans.storage_item.id).on_stock), 90)

    def test_transaction_increase_on_stock(self):
        trans = Transaction.objects.create(
            subject=u'Testtransaction 1 with Unicode µä³½',
            created_by=self.user,
            amount=10,
            storage_item=self.storage_item1,
            date=timezone.now(),
        )

        self.assertEqual(int(StorageItem.objects.get(pk=trans.storage_item.id).on_stock), 110)


class TransactionInventoryChangeOnUpdate(TestCase):
    """
    This test will check, whether inventory is adjusted correct, when a
    transaction is updated
    """

    def setUp(self):
        self.cat = Category.objects.create(name=u'Category 1')
        self.user = User.objects.create_user(username='jacob',
                                             email='jacob@foo.baa',
                                             password='top_secret')
        self.manu = Manufacturer.objects.create(name=u'Test Manufacturer 1',
                                                created_by=self.user)
        self.storagetype = StorageType.objects.create(name=u"Testtype")
        self.storageplace = StoragePlace.objects.create(name=u'Test Storage',
                                                        storage_type=self.storagetype)
        self.part1 = Part.objects.create(name=u'Test Part 1 with unicode µä³½',
                                         unit='m',
                                         creation_time=timezone.now(),
                                         created_by=self.user)
        self.part2 = Part.objects.create(name=u'Test Part 2',
                                         unit='m',
                                         creation_time=timezone.now(),
                                         created_by=self.user)
        self.storage_item1 = StorageItem.objects.create(part=self.part1,
                                                        storage=self.storageplace,
                                                        on_stock=100)
        self.storage_item1 = StorageItem.objects.create(part=self.part2,
                                                        storage=self.storageplace,
                                                        on_stock=100)

    def test_transaction_update(self):
        # First create a transaction which can be changed
        trans = Transaction.objects.create(
            subject=u'Testtransaction 1',
            created_by=self.user,
            amount=-10,
            storage_item=self.storage_item1,
            date=timezone.now(),
        )
        trans.save()
        # The amound of storage item1 should be 90 at this point
        # Now the transaction is updated

        trans.amount = 10
        trans.save()

        # The amount should now be 110
        self.assertEqual(int(StorageItem.objects.get(pk=trans.storage_item.id).on_stock), 110)


########################################################################
# Part related
########################################################################

class PartListWithOnStockValueFromSI(TestCase):
    def setUp(self):
        # Setting up categories
        self.cat = Category.objects.create(name=u'Category 1')

        # Setting up test user
        self.user = User.objects.create_user(username='jacob',
                                             email='jacob@foo.baa',
                                             password='top_secret')

        # Basis setting of storage
        self.storagetype = StorageType.objects.create(name=u"Testtype")
        self.storageplace1 = StoragePlace.objects.create(name=u'Test Storage1',
                                                         storage_type=self.storagetype)
        self.storageplace2 = StoragePlace.objects.create(name=u'Test Storage2',
                                                         storage_type=self.storagetype)

        # Some items
        self.part1 = Part.objects.create(name=u'Test Part 1',
                                         unit='m',
                                         creation_time=timezone.now(),
                                         created_by=self.user)

        self.part2 = Part.objects.create(name=u'Test Part 2',
                                         unit='m',
                                         creation_time=timezone.now(),
                                         created_by=self.user)

        self.storage_item1 = StorageItem.objects.create(part=self.part1,
                                                        storage=self.storageplace1,
                                                        on_stock=25)
        self.storage_item2a = StorageItem.objects.create(part=self.part2,
                                                         storage=self.storageplace1,
                                                         on_stock=7)
        self.storage_item2b = StorageItem.objects.create(part=self.part2,
                                                         storage=self.storageplace2,
                                                         on_stock=3)

    def test_part_list_with_on_stock_value(self):
        # Defining goal list
        expected_resultset = [
            [self.part1.id, 25, None],
            [self.part2.id, 10, None]
        ]
        self.assertEqual(get_all_storage_item_parts_with_on_stock_and_min_stock(), expected_resultset)


class PartExcludeDisabledTestCase(TestCase):
    """ Checking, wether get_fields() is not return the disabled field """

    def setUp(self):
        # Setting up test user
        self.cat = Category.objects.create(name=u'Category 1')
        self.user = User.objects.create_user(username='jacob',
                                             email='jacob@foo.baa',
                                             password='top_secret')

        # Settig up a part
        self.part1 = Part.objects.create(name=u'Test Part 1',
                                         unit='m',
                                         min_stock=50,
                                         creation_time=timezone.now(),
                                         created_by=self.user)

    def test_get_fields_not_showing_disabled_field(self):
        # TODO: Is there a way to do it in a cleaner way?

        # We are iterating over all fields and if field "Disabled"
        # has been found the Test 1 == 0 will fail.
        for field in self.part1.get_fields():
            if unicode(field[0]) == 'Disabled':
                self.assertTrue(False)
        self.assertTrue(True)


class PartGetOnStockAmount(TestCase):
    """ Checking for currently amount of on stock items for a special part
        Testcase include these scenario:
        - Part is having only one storage place
        - Part is having two storage places (StorageItem)
        - Part is having none storage place (StorageItem)
    """

    def setUp(self):
        # Setting up categories
        self.cat = Category.objects.create(name=u'Category 1')

        # Setting up test user
        self.user = User.objects.create_user(username='jacob',
                                             email='jacob@foo.baa',
                                             password='top_secret')

        # Basis setting of storage
        self.storagetype = StorageType.objects.create(name=u"Testtype")
        self.storageplace1 = StoragePlace.objects.create(name=u'Test Storage1',
                                                         storage_type=self.storagetype)
        self.storageplace2 = StoragePlace.objects.create(name=u'Test Storage2',
                                                         storage_type=self.storagetype)

        # Some items
        self.part1 = Part.objects.create(name=u'Test Part 1',
                                         unit='m',
                                         creation_time=timezone.now(),
                                         created_by=self.user)

        self.part2 = Part.objects.create(name=u'Test Part 2',
                                         unit='m',
                                         creation_time=timezone.now(),
                                         created_by=self.user)

        self.part3 = Part.objects.create(name=u'Test Part 3',
                                         unit='m',
                                         creation_time=timezone.now(),
                                         created_by=self.user)

        self.part4 = Part.objects.create(name=u'Test Part 4',
                                         unit='m',
                                         creation_time=timezone.now(),
                                         created_by=self.user)

        # Assigning Parts to StoragePlace aka creating StorageItem
        # Part 1: 1 StorageItem
        self.storage_item1 = StorageItem.objects.create(part=self.part1,
                                                        storage=self.storageplace1,
                                                        on_stock=25)

        # Part 2: Two items needed
        self.storage_item2a = StorageItem.objects.create(part=self.part2,
                                                         storage=self.storageplace1,
                                                         on_stock=7)
        self.storage_item2b = StorageItem.objects.create(part=self.part2,
                                                         storage=self.storageplace2,
                                                         on_stock=3)

        # Part 3: No Item needed -- just not stored somewhere
        # --

        # Part 4: One itme with amount = 0
        self.storage_item4 = StorageItem.objects.create(
            part=self.part4,
            storage=self.storageplace1,
            on_stock=0)

    def test_part_with_two_storageitems(self):
        self.assertEqual(Part.objects.get(name=u'Test Part 1').get_on_stock(), 25)

    def test_part_with_one_storageitem(self):
        self.assertEqual(Part.objects.get(name=u'Test Part 2').get_on_stock(), 10)

    def test_part_without_storageitem(self):
        self.assertEqual(Part.objects.get(name=u'Test Part 3').get_on_stock(), 0)

    def test_part_without_stock(self):
        self.assertEqual(Part.objects.get(name=u'Test Part 4').get_on_stock(), 0)


class ItemOutOfStockTestCase(TestCase):
    """ Checking whether reporting of out-of-stock-items are
        working well """

    def setUp(self):
        # Each part is having at least one storage item carring the
        # acutal on stock value

        # Setting up categories
        self.cat = Category.objects.create(name=u'Category 1')

        # Setting up test user
        self.user = User.objects.create_user(
            username='jacob', email='jacob@foo.baa', password='top_secret')

        # Basis setting of storage
        self.storagetype = StorageType.objects.create(name=u"Testtype")
        self.storageplace1 = StoragePlace.objects.create(name=u'Test Storage1',
                                                         storage_type=self.storagetype)
        self.storageplace2 = StoragePlace.objects.create(name=u'Test Storage2',
                                                         storage_type=self.storagetype)
        self.storageplace3 = StoragePlace.objects.create(name=u'Test Storage3',
                                                         storage_type=self.storagetype)
        self.storageplace4 = StoragePlace.objects.create(name=u'Test Storage4',
                                                         storage_type=self.storagetype)
        self.storageplace5 = StoragePlace.objects.create(name=u'Test Storage5',
                                                         storage_type=self.storagetype)

        # on_stock > min_stock
        self.part1 = Part.objects.create(name=u'Test Part 1',
                                         unit='m',
                                         min_stock=50,
                                         creation_time=timezone.now(),
                                         created_by=self.user)

        self.storage_item1 = StorageItem.objects.create(part=self.part1,
                                                        storage=self.storageplace1,
                                                        on_stock=100)

        # on_stock < min_stock
        self.part2 = Part.objects.create(name=u'Test Part 2',
                                         unit='m',
                                         min_stock=150,
                                         creation_time=timezone.now(),
                                         created_by=self.user)

        self.storage_item2 = StorageItem.objects.create(part=self.part2,
                                                        storage=self.storageplace2,
                                                        on_stock=100)

        # on_stock = min_stock
        self.part3 = Part.objects.create(name=u'Test Part 3',
                                         unit='m',
                                         min_stock=100,
                                         creation_time=timezone.now(),
                                         created_by=self.user)
        self.storage_item3 = StorageItem.objects.create(part=self.part3,
                                                        storage=self.storageplace3,
                                                        on_stock=100)

        # on_stock = 0
        self.part4 = Part.objects.create(name=u'Test Part 4',
                                         unit='m',
                                         min_stock=0,
                                         creation_time=timezone.now(),
                                         created_by=self.user)
        self.storage_item4 = StorageItem.objects.create(part=self.part4,
                                                        storage=self.storageplace4,
                                                        on_stock=0)

        # on_stock not defined
        # min_stock not defined
        self.part5 = Part.objects.create(name=u'Test Part 5',
                                         unit='m',
                                         creation_time=timezone.now(),
                                         created_by=self.user)
        self.storage_item5 = StorageItem.objects.create(part=self.part5,
                                                        storage=self.storageplace5)

    def test_item_out_of_stock(self):
        """ Testcase for on_stock = 0 """
        self.assertFalse(Part.objects.get(name=u'Test Part 4').is_on_stock())
        self.assertFalse(Part.objects.get(name=u'Test Part 5').is_on_stock())

    def test_item_not_out_of_stock(self):
        """ Testcase for on_stock > 0 """
        self.assertTrue(Part.objects.get(name=u'Test Part 1').is_on_stock())

    def test_item_below_min_stock(self):
        """ Testcase for checking whether
            on_stock < min_stock """
        self.assertTrue(Part.objects.get(name=u'Test Part 2').is_below_min_stock())

    def test_item_over_min_stock(self):
        """ Testcase for checking whether
            on_stock > min_stock """
        self.assertFalse(Part.objects.get(name=u'Test Part 1').is_below_min_stock())

    def test_item_equals_min_stock(self):
        """ Testcase for checking whether
            on_stock = min_stock """
        self.assertFalse(Part.objects.get(name=u'Test Part 3').is_below_min_stock())

    def test_item_min_stock_not_defined(self):
        """ Testcase for checking whether
            on_stock = min_stock """
        self.assertFalse(Part.objects.get(name=u'Test Part 5').is_below_min_stock())


########################################################################

class StorageItemsMergeTestCase(TestCase):
    """
    To check, whether the merging of two storage items is working
    """

    def setUp(self):
        # Setting up categories
        self.cat = Category.objects.create(name=u'Category 1')

        # Setting up test user
        self.user = User.objects.create_user(
            username='jacob', email='jacob@foo.baa', password='top_secret')

        # Basis setting of storage
        self.storagetype = StorageType.objects.create(name=u"Testtype")
        self.storageplace1 = StoragePlace.objects.create(
            name=u'Test Storage1',
            storage_type=self.storagetype)
        self.storageplace2 = StoragePlace.objects.create(
            name=u'Test Storage2',
            storage_type=self.storagetype)
        self.storageplace3 = StoragePlace.objects.create(
            name=u'Test Storage3',
            storage_type=self.storagetype)

        # Some items
        self.part1 = Part.objects.create(name=u'Test Part 1',
                                         unit='m',
                                         creation_time=timezone.now(),
                                         created_by=self.user)

        self.part2 = Part.objects.create(name=u'Test Part 2',
                                         unit='m',
                                         creation_time=timezone.now(),
                                         created_by=self.user)

        self.part3 = Part.objects.create(name=u'Test Part 3',
                                         unit='m',
                                         creation_time=timezone.now(),
                                         created_by=self.user)

        # Setting up storage items
        self.storage_item1 = StorageItem.objects.create(
            part=self.part1,
            storage=self.storageplace1,
            on_stock=25)

        self.storage_item2 = StorageItem.objects.create(
            part=self.part1,
            storage=self.storageplace2,
            on_stock=50)

        # and a storage items from a different part
        self.storage_item3 = StorageItem.objects.create(
            part=self.part2,
            storage=self.storageplace2,
            on_stock=100)

        # And some items for checking None-behavior of merging function
        self.storage_item_none1 = StorageItem.objects.create(
            part=self.part3,
            storage=self.storageplace1)

        self.storage_item_none2 = StorageItem.objects.create(
            part=self.part3,
            storage=self.storageplace2)

        self.storage_item4 = StorageItem.objects.create(
            part=self.part3,
            storage=self.storageplace3,
            on_stock=200)

    def test_merging_same_storage_item(self):
        """
        Checks whether merging the samse storage items fails
        """
        with self.assertRaises(PartsmanagementException):
            tmp = self.part1.merge_storage_items(self.storage_item1, self.storage_item1)

    def test_working_merge_of_two_storage_items(self):
        """
        Checks whether normal merging of two storage items is working
        """
        tmp = self.part1.merge_storage_items(self.storage_item1, self.storage_item2)
        self.assertEqual(int(StorageItem.objects.get(pk=self.storage_item1.id).on_stock), 75)
        self.assertIsNone(StorageItem.objects.filter(pk=self.storage_item2.id).first())

    def test_merging_with_different_parts(self):
        """
        Checks whether merging of storage items of two differenz parts
        are failing
        """
        with self.assertRaises(PartsNotFitException):
            self.part1.merge_storage_items(self.storage_item1, self.storage_item3)

    def test_merging_with_non_existent_storage_items(self):
        """
        Tests whether an invalid storage item causes the merge method
        to rais an exception
        """
        with self.assertRaises(PartsmanagementException):
            self.part1.merge_storage_items(self.storage_item1, None)

    def test_merging_with_two_on_stock_none(self):
        """
        Checkes whether two storage items without any on stock value
        can be successfully merged
        """
        try:
            self.part3.merge_storage_items(self.storage_item_none1, self.storage_item_none2)
            self.assertTrue(True)
            self.assertIsNone(StorageItem.objects.get(pk=self.storage_item_none1.id).on_stock)
        except:
            self.assertFalse(True)

    def test_merging_with_one_on_stock_none(self):
        """
        Checkes whether merging an storage item with items inside storage
        and one without any inforamtion is resulting into a on stock value
        """
        try:
            self.part3.merge_storage_items(self.storage_item_none1, self.storage_item4)
            self.assertTrue(True)
            self.assertEquals(int(StorageItem.objects.get(pk=self.storage_item_none1.id).on_stock), 200)
        except:
            self.assertFalse(True)

########################################################################
# Storage
########################################################################


class StrorageParentTestCase(TestCase):
    """ Test to check whether storage name is printed correctly.
        If there is a parent, it should be also printed seperated by the
        defined delimiter """

    def setUp(self):
        self.storage_type = StorageType.objects.create(name=u'Generic Typ')
        self.stor1 = StoragePlace.objects.create(name=u'Storage Lvl 1', storage_type=self.storage_type)
        self.stor2 = StoragePlace.objects.create(name=u'Storage Lvl 2', parent=self.stor1, storage_type=self.storage_type)
        self.stor3 = StoragePlace.objects.create(name=u'Storage Lvl 3 with unicode µä³½', parent=self.stor2, storage_type=self.storage_type)

    def test_storage_name(self):
        stor_result1 = u'Storage Lvl 1'
        stor_result2 = u'Storage Lvl 1' + settings.PARENT_DELIMITER + u'Storage Lvl 2'
        stor_result3 = u'Storage Lvl 1' + settings.PARENT_DELIMITER + u'Storage Lvl 2' + settings.PARENT_DELIMITER + u'Storage Lvl 3 with unicode µä³½'
        self.assertEqual(self.stor1.__unicode__(), stor_result1)
        self.assertEqual(self.stor2.__unicode__(), stor_result2)
        self.assertEqual(self.stor3.__unicode__(), stor_result3)
