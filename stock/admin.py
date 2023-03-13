from django.contrib import admin
from .models import Product, Stock, Threshold, CompanyWarehouse, Company

# Register your models here.
admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(Threshold)
admin.site.register(CompanyWarehouse)
admin.site.register(Company)