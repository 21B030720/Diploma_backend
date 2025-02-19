# Generated by Django 5.1.5 on 2025-02-19 07:46

import apps.shops.products.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commodity_groups', '0001_initial'),
        ('shops', '0002_shopcategory_shop_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductNutritionCharacteristics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время создания')),
                ('changed_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Время последнего изменения')),
                ('nutritional_value', models.FloatField(default=0.0)),
                ('fats', models.FloatField(default=0.0)),
                ('proteins', models.FloatField(default=0.0)),
                ('carbohydrates', models.FloatField(default=0.0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время создания')),
                ('changed_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Время последнего изменения')),
                ('name', models.CharField(max_length=100)),
                ('icon', models.ImageField(upload_to=apps.shops.products.models.upload_product_category_icon)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='shops.shop')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время создания')),
                ('changed_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Время последнего изменения')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to=apps.shops.products.models.upload_product_image)),
                ('description', models.TextField()),
                ('rating', models.FloatField(blank=True, null=True)),
                ('from_age', models.IntegerField()),
                ('to_age', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('measure', models.CharField(choices=[('KG', 'KG'), ('L', 'L'), ('PC', 'PC')], max_length=100)),
                ('commodity_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='commodity_groups.commoditygroup')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shops.shop')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.productcategory')),
                ('nutrition_characteristics', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='products.productnutritioncharacteristics')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
