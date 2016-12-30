from django.contrib.auth.models import User
from rest_framework import serializers
from partsmanagement.models import *


# class UserSerializer(serializers.ModelSerializer):
#   class Meta:
#       model = User
#       fields = ('url', 'username', 'email', 'is_staff')


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
