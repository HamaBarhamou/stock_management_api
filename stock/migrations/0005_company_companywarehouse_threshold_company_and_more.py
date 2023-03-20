# Generated by Django 4.1.7 on 2023-03-13 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock', '0004_remove_product_categories_delete_categories'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Company', max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_companies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyWarehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='CompanyWarehouse', max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouses', to='stock.company')),
            ],
        ),
        migrations.AddField(
            model_name='threshold',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='thresholds', to='stock.company'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stock',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.companywarehouse'),
        ),
        migrations.DeleteModel(
            name='Warehouse',
        ),
    ]