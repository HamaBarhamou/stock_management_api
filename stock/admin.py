from django.contrib import admin
from .models import Categories, Product, Stock

# Register your models here.
admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Stock)