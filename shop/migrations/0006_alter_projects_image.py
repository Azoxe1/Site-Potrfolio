# Generated by Django 3.2.20 on 2023-12-15 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_projects_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='image',
            field=models.ImageField(default='project.jpg', upload_to='projects'),
        ),
    ]