# Generated by Django 3.2.20 on 2023-12-18 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20231215_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='available',
            field=models.BooleanField(default=False),
        ),
    ]
