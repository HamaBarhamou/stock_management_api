from django.contrib import admin
from .models import Product, Stock, Threshold, CompanyWarehouse, Company

admin.site.site_header = "Stock Management Api administration"
admin.site.site_title = "Stock Management Api administration"

admin.site.register(Product)
admin.site.register(Stock)
#admin.site.register(Threshold)
admin.site.register(CompanyWarehouse)
admin.site.register(Company)