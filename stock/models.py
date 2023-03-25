from django.db import models
from user.models import User
from django.utils import timezone


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255, default='Company')
    address = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_companies')

    def __str__(self):
        return "{}".format(self.name)


class CompanyWarehouse(models.Model):
    name = models.CharField(max_length=255, default='CompanyWarehouse')
    address = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='warehouses')
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='product')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
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
    image = models.ImageField(upload_to='Product', blank=True, null=True)
    
    def __str__(self) -> str:
        return "{}".format(self.name)
    
    def update_quantity_in_stock(self, new_quantity):
        self.quantity_in_stock = new_quantity
        self.save()
    
    def is_quantity_available(self, quantity):
        return self.quantity_in_stock >= quantity


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(CompanyWarehouse, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    on_delivery = models.BooleanField(default=False)
    on_reorder = models.BooleanField(default=False)
    on_return = models.BooleanField(default=False)
    in_transit = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return "{}".format(self.product)


class Threshold(models.Model):
    name = models.CharField(max_length=50)
    value = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='thresholds')
    
    def __str__(self):
        return f"{self.name} ({self.value}) - {self.company}"