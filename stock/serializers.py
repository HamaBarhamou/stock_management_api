from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Categories, Product

        
class CategoriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categories
        fields = ['name']
        
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image', 'categories']