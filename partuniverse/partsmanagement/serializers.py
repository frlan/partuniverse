from rest_framework import serializers
from partsmanagement.models import (
    StorageType,
    StoragePlace,
    Manufacturer,
    Distributor,
    Category,
    StorageItem,
    Transaction,
    Part
)


class StorageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageType
        fields = ('name', )


class StoragePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoragePlace
        fields = (
            'name',
            'storage_type',
            'parent',
            'disabled',
            'pic',
            'description')


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ('name', 'logo', 'url')


class DistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        fields = ('name', 'logo', 'url')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'description', 'parent')


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ('name', 'sku', 'description', 'min_stock', 'unit', 'pic',
                  'image_url', 'manufacturer', 'distributor', 'price',
                  'categories', 'disabled')


class StorageItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageItem
        fields = ('part', 'storage', 'on_stock', 'disabled')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('subject', 'storage_item', 'amount', 'comment', 'date',
                  'state', 'created_by', 'created_date', 'reverted')
