# Generated by Django 3.2.20 on 2023-12-18 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_product_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='quantity',
        ),
    ]
