# Generated by Django 4.1.7 on 2023-03-14 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0006_product_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threshold',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
