from django.db import models
from datetime import datetime
from django.utils import timezone


# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.name


""" class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='Product')
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name """


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit_margin = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.IntegerField(default=0)
    minimum_quantity = models.IntegerField(default=0)
    quantity_ordered = models.IntegerField(default=0)
    reorder_quantity = models.IntegerField(default=0)
    rotation = models.IntegerField(default=0)
    on_clearance = models.BooleanField(default=False)
    on_sale = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='Product')
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return "{}".format(self.name)

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    on_delivery = models.BooleanField(default=False)
    on_reorder = models.BooleanField(default=False)
    on_return = models.BooleanField(default=False)
    in_transit = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return "{}".format(self.product)
    
class Threshold(models.Model):
    name = models.CharField(max_length=50, unique=True)
    value = models.IntegerField()

    def __str__(self):
        return self.name
