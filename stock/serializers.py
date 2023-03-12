from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Categories, Product, Stock

        
class CategoriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name']
        
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = [
                    'id',
                    'name',
                    'price',
                    'description',
                    'image',
                    'categories',
                    'quantity_in_stock'
                ]
        
class StockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'product', 'quantity', 'on_delivery', 'on_reorder', 'on_return', 'in_transit']