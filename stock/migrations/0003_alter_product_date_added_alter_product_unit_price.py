# Generated by Django 4.1.7 on 2023-03-12 15:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_alter_product_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 12, 15, 24, 36, 461363)),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit_price',
            field=models.IntegerField(),
        ),
    ]
