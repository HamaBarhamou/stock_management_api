from django.utils import timezone
from django.contrib.auth.models import User
from stock.models import Categories, Product, Stock, Threshold
from random import randint

# Supprimer les données existantes
Stock.objects.all().delete()
Product.objects.all().delete()
Categories.objects.all().delete()
Threshold.objects.all().delete()

# Créer les catégories
categories_names = ['Electronics', 'Clothing', 'Books', 'Beauty', 'Sports']
categories_instances = []
for name in categories_names:
    category = Categories.objects.create(name=name)
    categories_instances.append(category)

# Créer les produits
products = []
for i in range(100):
    product = Product.objects.create(
        name=f'Product {i}',
        description=f'Description of Product {i}',
        unit_price=randint(10, 1000),
        profit_margin=randint(5, 50),
        quantity_in_stock=randint(0, 100),
        minimum_quantity=randint(0, 10),
        quantity_ordered=0,
        reorder_quantity=randint(5, 20),
        rotation=randint(0, 100),
        on_clearance=bool(randint(0, 1)),
        on_sale=bool(randint(0, 1)),
        date_added=timezone.now(),
        image='Product/default.png',
        categories=categories_instances[randint(0, 4)]
    )
    products.append(product)

# Créer les stocks
for product in products:
    Stock.objects.create(
        product=product,
        quantity=randint(0, 10),
        on_delivery=False,
        on_reorder=False,
        on_return=False,
        in_transit=False
    )

Threshold(name='low_stock', value=10).save()
Threshold(name='low_demand', value=5).save()
Threshold(name='low_profit_margin', value=0.1).save()
Threshold(name='low_quantity', value=5).save()
Threshold(name='low_rotation', value=2).save()
Threshold(name='high_demand', value=8).save()
Threshold(name='high_profit_margin', value=0.2).save()
Threshold(name='high_rotation', value=10).save()

#python manage.py runscript scripts.data.py -v2