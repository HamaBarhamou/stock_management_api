from django.db import models


# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=50)

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)