# Generated by Django 3.2.20 on 2023-12-15 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_projects_git'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartorderitems',
            name='order',
        ),
        migrations.DeleteModel(
            name='CartOrder',
        ),
        migrations.DeleteModel(
            name='CartOrderItems',
        ),
    ]
