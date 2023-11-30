# Generated by Django 4.2.7 on 2023-11-30 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timezone', models.CharField(default='UTC', max_length=32)),
                ('name', models.CharField(max_length=200, verbose_name='Имя')),
                ('phone_number', models.CharField(max_length=200, verbose_name='Номер телефона')),
                ('telegram', models.CharField(default='TG не указан', max_length=100, verbose_name='Telegram')),
                ('selected_date', models.DateField(default=None, verbose_name='Выбранная дата')),
                ('request_time', models.DateTimeField(auto_now=True, verbose_name='Дата создания запроса')),
                ('course_choose', models.CharField(default='Консультация с карьерным помощником.', max_length=200, verbose_name='Тема обращения')),
            ],
            options={
                'verbose_name': 'Обращение',
                'verbose_name_plural': 'Обращения',
            },
        ),
    ]
