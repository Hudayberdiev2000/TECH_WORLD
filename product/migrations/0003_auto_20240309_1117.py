# Generated by Django 3.2a1 on 2024-03-09 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='old_price',
        ),
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.IntegerField(default=0),
        ),
    ]
