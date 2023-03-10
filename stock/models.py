from django.db import models


# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='Product')
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name