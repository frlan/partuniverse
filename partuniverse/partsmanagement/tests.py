from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# For splitting of e.g. categories
from django.conf import settings

from .models import *
from .views import *

########################################################################
# Category
########################################################################
class CategoryTestCase(TestCase):
	""" Test to check whether category name is printed correctly.
		If there is a parent, it should be also printed seperated by a : """

	def setUp(self):
		self.cat1 = Category.objects.create(name='Category 1')
		self.cat2 = Category.objects.create(name='Category 2', parent=self.cat1)
		self.cat3 = Category.objects.create(name='Category 3', parent=self.cat2)

	def test_category_name(self):
		cat_result1 = u'Category 1'
		cat_result2 = u'Category 1' + settings.PARENT_DELIMITER + u'Category 2'
		cat_result3 = u'Category 1' + settings.PARENT_DELIMITER + u'Category 2' + settings.PARENT_DELIMITER + u'Category 3'
		self.assertEqual(self.cat1.__unicode__(), cat_result1)
		self.assertEqual(self.cat2.__unicode__(), cat_result2)
		self.assertEqual(self.cat3.__unicode__(), cat_result3)


########################################################################
# Transaction
########################################################################
class TransactionInventoryChange(TestCase):
	""" This is a test to check whether a new transaction is increasing
		on_stock or decreasing on_stock of a particular part """

	def setUp(self):
		self.cat = Category.objects.create(name='Category 1')
		self.user = User.objects.create_user(
            username='jacob', email='jacob@foo.baa', password='top_secret')
		self.manu = Manufacturer.objects.create(
			name='Test Manufacturer 1',
			created_by=self.user)
		self.part1 = Part.objects.create(name='Test Part 1',
			unit='m',
			on_stock = 100,
			creation_time=timezone.now(),
			created_by=self.user)
		self.part2 = Part.objects.create(name='Test Part 2',
			unit='m',
			on_stock = 100,
			creation_time=timezone.now(),
			created_by=self.user)

	def test_transaction_decrease_on_stock(self):
		trans = Transaction.objects.create(
			subject='Testtransaction 1',
			created_by=self.user,
			amount=-10,
			part=self.part1,
			date=timezone.now(),
		)

		self.assertEqual(Part.objects.get(name='Test Part 1').on_stock, 90)

	def test_transaction_increase_on_stock(self):
		trans = Transaction.objects.create(
			subject='Testtransaction 1',
			created_by=self.user,
			amount=10,
			part=self.part2,
			date=timezone.now(),
		)

		self.assertEqual(Part.objects.get(name='Test Part 2').on_stock, 110)


########################################################################
# Part related
########################################################################

class PartExcludeDisabledTestCase(TestCase):
	""" Checking, wether get_fields() is not return the disabled field """

	def setUp(self):
		# Setting up test user
		self.cat = Category.objects.create(name='Category 1')
		self.user = User.objects.create_user(
            username='jacob', email='jacob@foo.baa', password='top_secret')

		# Settig up a part
		self.part1 = Part.objects.create(name='Test Part 1',
			unit='m',
			on_stock = 100,
			min_stock = 50,
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



class ItemOutOfStockTestCase(TestCase):
	""" Checking whether reporting of out-of-stock-items are
		working well """

	def setUp(self):
		# Setting up test user
		self.cat = Category.objects.create(name='Category 1')
		self.user = User.objects.create_user(
            username='jacob', email='jacob@foo.baa', password='top_secret')

		# on_stock > min_stock
		self.part1 = Part.objects.create(name='Test Part 1',
			unit='m',
			on_stock = 100,
			min_stock = 50,
			creation_time=timezone.now(),
			created_by=self.user)

		# on_stock < min_stock
		self.part2 = Part.objects.create(name='Test Part 2',
			unit='m',
			on_stock = 100,
			min_stock = 150,
			creation_time=timezone.now(),
			created_by=self.user)

		# on_stock = min_stock
		self.part3 = Part.objects.create(name='Test Part 3',
			unit='m',
			on_stock = 100,
			min_stock = 100,
			creation_time=timezone.now(),
			created_by=self.user)

		# on_stock = 0
		self.part4 = Part.objects.create(name='Test Part 4',
			unit='m',
			on_stock = 0,
			min_stock = 0,
			creation_time=timezone.now(),
			created_by=self.user)

		# on_stock not defined
		# min_stock not defined
		self.part5 = Part.objects.create(name='Test Part 5',
			unit='m',
			creation_time=timezone.now(),
			created_by=self.user)


	def test_item_out_of_stock(self):
		""" Testcase for on_stock = 0 """
		self.assertFalse(Part.objects.get(name='Test Part 4').is_on_stock())

	def test_item_not_out_of_stock(self):
		""" Testcase for on_stock > 0 """
		self.assertTrue(Part.objects.get(name='Test Part 1').is_on_stock())
		self.assertTrue(Part.objects.get(name='Test Part 5').is_on_stock())

	def test_item_below_min_stock(self):
		""" Testcase for checking whether
			on_stock < min_stock """
		self.assertTrue(Part.objects.get(name='Test Part 2').is_below_min_stock())

	def test_item_over_min_stock(self):
		""" Testcase for checking whether
			on_stock > min_stock """
		self.assertFalse(Part.objects.get(name='Test Part 1').is_below_min_stock())

	def test_item_equals_min_stock(self):
		""" Testcase for checking whether
			on_stock = min_stock """
		self.assertFalse(Part.objects.get(name='Test Part 3').is_below_min_stock())

	def test_item_min_stock_not_defined(self):
		""" Testcase for checking whether
			on_stock = min_stock """
		self.assertFalse(Part.objects.get(name='Test Part 5').is_below_min_stock())

########################################################################
# Storage
########################################################################
class StrorageParentTestCase(TestCase):
	""" Test to check whether storage name is printed correctly.
		If there is a parent, it should be also printed seperated by the
		defined delimiter """

	def setUp(self):
		self.storage_type = StorageType.objects.create(name='Generic Typ')
		self.stor1 = StoragePlace.objects.create(name='Storage Lvl 1', storage_type=self.storage_type)
		self.stor2 = StoragePlace.objects.create(name='Storage Lvl 2', parent=self.stor1, storage_type=self.storage_type)
		self.stor3 = StoragePlace.objects.create(name='Storage Lvl 3', parent=self.stor2, storage_type=self.storage_type)

	def test_storage_name(self):
		stor_result1 = u'Storage Lvl 1'
		stor_result2 = u'Storage Lvl 1' + settings.PARENT_DELIMITER + u'Storage Lvl 2'
		stor_result3 = u'Storage Lvl 1' + settings.PARENT_DELIMITER + u'Storage Lvl 2' + settings.PARENT_DELIMITER + u'Storage Lvl 3'
		self.assertEqual(self.stor1.__unicode__(), stor_result1)
		self.assertEqual(self.stor2.__unicode__(), stor_result2)
		self.assertEqual(self.stor3.__unicode__(), stor_result3)

