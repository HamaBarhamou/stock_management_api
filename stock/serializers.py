from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Product, Stock, CompanyWarehouse, Company

        
""" class CategoriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name'] """
        
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = [
                    'id',
                    'name',
                    'description',
                    'unit_price',
                    'profit_margin',
                    'quantity_in_stock',
                    'minimum_quantity',
                    'quantity_ordered',
                    'reorder_quantity',
                    'rotation',
                    'on_clearance',
                    'on_sale',
                    'date_added',
                    'date_added',
                    'image',
                    #'categories',
                ]
        
class StockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stock
        fields = [
                    'id',
                    'product',
                    'warehouse',
                    'quantity',
                    'on_delivery',
                    'on_reorder',
                    'on_return',
                    'in_transit'
                ]

class CompanyWarehouseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CompanyWarehouse
        fields = [
                    'id',
                    'name',
                    'address',
                    'company',
                ]


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = [
                    'id',
                    'name',
                    'address',
                    #'created_by',
                ]
