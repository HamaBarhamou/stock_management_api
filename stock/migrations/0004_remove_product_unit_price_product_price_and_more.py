# Generated by Django 4.1.7 on 2023-03-12 15:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_alter_product_date_added_alter_product_unit_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='unit_price',
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 12, 15, 27, 11, 544219)),
        ),
    ]