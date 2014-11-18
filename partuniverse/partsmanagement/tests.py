from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .models import *
from .views import *

class CategoryTestCase(TestCase):
	""" Test to check whether category name is printed correctly.
		If there is a parent, it should be also printed seperated by a : """

	def setUp(self):
		self.cat1 = Category.objects.create(name='Category 1')
		self.cat2 = Category.objects.create(name='Category 2', parent=self.cat1)
		self.cat3 = Category.objects.create(name='Category 3', parent=self.cat2)

	def test_category_name(self):
		self.assertEqual(self.cat1.__unicode__(), u'Category 1')
		self.assertEqual(self.cat2.__unicode__(), u'Category 1:Category 2')
		self.assertE+qual(self.cat3.__unicode__(), u'Category 1:Category 2:Category 3')

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



