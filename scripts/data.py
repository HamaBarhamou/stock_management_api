from django.utils import timezone
from user.models import User
from stock.models import CompanyWarehouse, Product, Stock, Company
from random import randint
from faker import Faker

# Supprimer les données existantes
Stock.objects.all().delete()
Product.objects.all().delete()
Company.objects.all().delete()
CompanyWarehouse.objects.all().delete()
users = User.objects.filter(is_superuser=False)
users.delete()


fake = Faker('fr_FR')

# On crée 2 utilisateurs
for i in range(2):
    user = User.objects.create_user(
        username=fake.user_name(),
        password='Mel0nie',
        email=fake.email()
    )
    # On crée 2 entreprises par utilisateur
    for j in range(2):
        company = Company.objects.create(
            name=fake.company(),
            address=fake.address(),
            created_by=user
        )
        # On crée 3 entrepôts par entreprise
        for k in range(3):
            warehouse = CompanyWarehouse.objects.create(
                name=fake.city(),
                address=fake.address(),
                company=company
            )
            # On crée 10 produits par entrepôt
            for l in range(10):
                product = Product.objects.create(
                    name=fake.word() + ' ' + fake.word(),
                    description=fake.text(),
                    company=company,
                    unit_price=fake.pydecimal(right_digits=2, min_value=1, max_value=100),
                    profit_margin=fake.pydecimal(right_digits=2, min_value=1, max_value=3),
                    quantity_in_stock=fake.random_int(min=0, max=1000),
                    minimum_quantity=fake.random_int(min=0, max=100),
                    quantity_ordered=fake.random_int(min=0, max=100),
                    reorder_quantity=fake.random_int(min=0, max=100),
                    rotation=fake.random_int(min=0, max=100),
                    on_clearance=fake.boolean(chance_of_getting_true=50),
                    on_sale=fake.boolean(chance_of_getting_true=50),
                    date_added=fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None),
                    image=fake.image_url(width=None, height=None)
                )
                # On crée un stock pour chaque produit
                stock = Stock.objects.create(
                    product=product,
                    warehouse=warehouse,
                    quantity=fake.random_int(min=0, max=1000),
                    on_delivery=fake.boolean(chance_of_getting_true=10),
                    on_reorder=fake.boolean(chance_of_getting_true=10),
                    on_return=fake.boolean(chance_of_getting_true=10),
                    in_transit=fake.boolean(chance_of_getting_true=10)
                )

#python manage.py runscript scripts.data.py -v2